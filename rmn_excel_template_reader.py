"""
This script reads the excel spreadsheet from RMS
and covert each sheet into a dataframe.
Then remap the columns names and check for invalid records.
Finally, prepares the df to be pushed to the database.
Author: Javier Soto
Date: 06/01/2024
Version: V1.0
"""

## IMPORT LIBRARIES

import os
import pandas as pd
from datetime import datetime
import psycopg2 
import numpy as np 
import psycopg2.extras as extras 
from config import *

pd.options.mode.chained_assignment = None  # default='warn'
## DB connection credentials:

conn = psycopg2.connect( 
        database=dbname, user=username, password=password, host=host, port=port
    )

def check_values_not_exist(conn, tables, columns, values):
    """
    Check if the combination of values does not exist in the specified tables and columns.

    Parameters:
        conn: psycopg2 connection object
        tables (list): List of table names to query.
        columns (list): List of column names in the order [rmn_id, grant_id, visit].
        values (list): List of values to check in the order [rmn_id, grant_id, visit].

    Returns:
        bool: True if the values do not exist in any table, False otherwise.
    """
    if len(columns) != 3 or len(values) != 3:
        raise ValueError("Columns and values must each contain exactly 3 items: [rmn_id, grant_id, visit].")

    rmn_id, grant_id, visit = columns
    value_rmn_id, value_grant_id, value_visit = values

    # List to store tables where values do not exists
    tables_where_values_not_exist = []

    try:
        with conn.cursor() as cur:
            for table in tables:
                # Build the query dynamically
                query = (
                    f"SELECT EXISTS ("
                    f"  SELECT 1 FROM pa_restoration_monitoring_network.{table}"
                    f"  WHERE {rmn_id} = %s AND {grant_id} = %s AND {visit} = %s"
                    f")")
                # Execute the query
                cur.execute(query, (value_rmn_id, value_grant_id, value_visit))

                # Fetch the result (True if exists, False otherwise)
                result = cur.fetchone()[0]

                # Add table to the list if the values do not exist
                if not result:
                    #print(f"\n....The table {table} will be added to the list....\n")
                    tables_where_values_not_exist.append(table)
                
                if result:
                    print(f"\n....The table {table} already has a survey in it. Skipping....\n")

            # If no matches were found in any table, return list of tables
            return tables_where_values_not_exist

    except Exception as e:
        print(f"Error occurred: {e}")
        return None


def execute_values(conn, df, table): 

    """
    https://www.geeksforgeeks.org/how-to-insert-a-pandas-dataframe-to-an-existing-postgresql-table/
    """
  
    tuples = [tuple(x) for x in df.to_numpy()] 
  
    cols = ','.join(list(df.columns))

    #print("table", table)
    #print("cols", cols)

    # SQL query to execute 
    query = f"INSERT INTO %s(%s) VALUES %%s" % (table, cols)
    #print(query) 
    cursor = conn.cursor() 
    try: 
        extras.execute_values(cursor, query, tuples) 
        conn.commit() 
    except (Exception, psycopg2.DatabaseError) as error: 
        print("Error: %s" % error) 
        conn.rollback() 
        cursor.close() 
        return 1
    print("\n....The dataframe is inserted....\n") 
    cursor.close() 
  
  

## User to input the area code ID

#rmn_id = input('Please type the Restoration monitoring id, for exmaple MSO5: ')
#grant_id = input('Please type the grant id, for exmaple 502600: ')
rmn_id = 'MS05'
grant_id = '502600'
visit = "1-year"

## SCRIPT SETTINGS
pd.set_option('display.max_columns', None)  # print all column names
 
## READ EXCEL MAP
map_df = pd.read_excel(r'map\RMN data for database.xlsx')
#print(map_df)

##FILTER MAP BY COLUMS UPLOAD TO DB

map_df = map_df[map_df['Upload to DB'] == 'Yes'] # keep only columns where Upload to DB is YES
#print(map_df)

## CREATE LIST OF SHEETS OF INTEREST
sheets_of_interest = map_df['Tab or geopackage layer'].unique() ## get the list from mapdataframe
tables = map_df['Database layer'].unique() ## get the list for checker

## Parameters for cheker function
columns = ['rmn_id','grant_id','visit']
values = [rmn_id,grant_id,visit]

## Tables to push data to the database

tables_to_push = check_values_not_exist(conn, tables, columns, values)

## READ EXCEL SURVEY FILES

## loop over the list of xlsx files in the root folder
rootdir = r'data'
xlsx_files = []  # create empty list of xlsx files

for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        filepath = subdir + os.sep + file
        if filepath.endswith(".xlsx"):
            #print(filepath)
            xlsx_files.append(filepath) # append xlsx files to a list
        

## function to remap sheets and export csv:

def remap_and_export(s,df,rmn_id,grant_id,visit,conn, tables_to_push):

    # filter rempa_df based on the layer name
    remap_df = map_df[map_df['Tab or geopackage layer'] == s]

    # convert column names to a dictionary
    rename_mapping = dict(zip(remap_df['Field name'], remap_df['Field name for DB']))

    # renema colums in the daframe using remap dataframe
    df.rename(columns=rename_mapping,inplace=True)

    # fix data times types in any dataframe

    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])

    # keep only the columns from the remap dataframe
    df = df[list(rename_mapping.values())]

     ## add code project ID to every single table
    df['rmn_id'] = rmn_id
    df['grant_id'] = grant_id
    df['visit'] = visit

    # Replace all Nan or Nat on any table
    df = df.replace('^\s*$', np.nan, regex=True)  ## replaces any white spaces with NaN
    df = df.replace({np.nan: None}) ## replaces any NaN or NaT with Null (for PostgreSQL)

    ## keeps only the two columns with layer names and removes all duplicates 
    column_remap_df = remap_df[['Tab or geopackage layer','Database layer']].drop_duplicates() 

    #print(df.info())  ## just for testing
    #df.to_csv(f'{s}_test.csv')  ## just for testing
    #print(column_remap_df)   ## just for testing
    #print("\n\n\n\n\n\n","df to the database: ", df, "\n\n\n\n\n\n")   ## just for testing

    if column_remap_df['Database layer'].iloc[0] in tables_to_push:

        print(f"\n....Pushing table {column_remap_df['Database layer'].iloc[0]}....\n") 

    ## Push to DB the iloc method takes the shortest name of the table
        execute_values(conn, df, "pa_restoration_monitoring_network."+column_remap_df['Database layer'].iloc[0])
    

## loop over each sheet from each excel survey

for s in sheets_of_interest:
    try:
        print("\n....Preparing table: ",s,"\n")
        if s == 'Desk study':
            df = pd.read_excel(xlsx_files[0], sheet_name=s, index_col=1)
            #print(df)
            df = df.T
            df = df.dropna(axis=0, how='all') # delete all rows with nulls
            df = df.dropna(axis=1, how='all') # delete all columns with nulls
            #print(df)
            # get columns names from map file
            remap_and_export(s,df,rmn_id,grant_id,visit,conn, tables_to_push)
            
        if s == 'Feature status - drains' or s == 'Feature status - gullies' or s == 'Feature status - bare peat' or s == 'Feature status - F2B':
            df = pd.read_excel(xlsx_files[0], sheet_name=s, index_col=0, header=1)
            df = df.dropna(axis=0, how='all') # delete all rows with nulls
            df = df.dropna(axis=1, how='all') # delete all columns with nulls
            #print(df)
            df = df.reset_index()
            df = df.drop([0])  # delete first row from dataframe as it contains the datatypes
            
            # get columns names from map file
            remap_and_export(s,df,rmn_id,grant_id,visit,conn, tables_to_push)
        
        if s == 'Quadrat information' or s == 'Vegetation':
            df = pd.read_excel(xlsx_files[0], sheet_name=s, index_col=0)
            df = df.dropna(axis=0, how='all') # delete all rows with nulls
            df = df.dropna(axis=1, how='all') # delete all columns with nulls
            #print(df)
            df = df.reset_index()
            df = df.drop([0])  # delete second row from dataframe as it contains the datatypes
            
            # get columns names from map file
            remap_and_export(s,df,rmn_id,grant_id,visit,conn, tables_to_push)

    except ValueError:
        print(f'{s}: Layer not found')
    except KeyError:
        print(f'{s}: Key Error')
    except TypeError:
        print(f'{s}: Data Type Error')
    except FileNotFoundError:
        print(f'{xlsx_files[0]}: File not found')
    except Exception as e:
        print(f'Unexpected error occurred. Could be related with the sheets names in excel being different or not present: {e}')
    
   
## check for invalid and null records

