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
import sys
import argparse
import pandas as pd
from datetime import datetime
import psycopg2 
import numpy as np 
import psycopg2.extras as extras 
from config import *



###################################################################################
###################################################################################
###################################################################################

parser = argparse.ArgumentParser(description="Process input variables for the script.")

# example python rmn_excel_template_reader.py -r MS01 -g 502418 -v 1-year "C:\javi\repos\rmn\data\MS01 - post\DONE-PA - Monitoring - RMN survey - 202324 - Post-restoration - MS01 Ben Lawyers - 1-year excel - 08 Oct 2024 (A4770282).xlsx"

parser.add_argument('-r', '--rmn_id', type=str, required=True, help="The RMN ID")
parser.add_argument('-g', '--grant_id', type=str, required=True, help="The The Grant ID")
parser.add_argument('-v', '--visit', type=str, required=True, help="The Visit")
parser.add_argument('path', type=str, help="The file path, just paste it")


args = parser.parse_args()

rmn_id = args.rmn_id
grant_id = args.grant_id
visit = args.visit
file_path = args.path

if not os.path.exists(file_path):
    print(f" Error: The file at '{file_path}' does not exist")
    sys.exit(1)

###################################################################################
###################################################################################
###################################################################################

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
                    print(f"\n....The table {table} already has a survey in it with the same {grant_id}, {rmn_id} and {visit}. Skipping....\n")

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
    print(query) 
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
  
def modify_sampling_point(value):
            parts = value.rsplit("_", 1) # get the last part of the string, split from right
            if len(parts) == 2 and parts[-1].isdigit(): # makes sure valid split and numeric last part
                if len(parts[-1]) == 1: # check if the last bit is 1,2,3,4,5,6,7,8,9
                    parts[-1] = f"0{parts[-1]}" # add the 0
            return "_".join(parts) # join back the modified value
      

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



## function to remap sheets and export csv:

def remap_and_export(s,df,rmn_id,grant_id,visit,conn, tables_to_push):

    print("\n\n 3 WITHIN THE REMAP AND EXPORT FUNCTION. S: ", s)
    
    try:

        # filter rempa_df based on the layer name
        remap_df = map_df[map_df['Tab or geopackage layer'] == s]

        # convert column names to a dictionary
        rename_mapping = dict(zip(remap_df['Field name'], remap_df['Field name for DB']))
    
        print("Rename_mapping: ", rename_mapping)
    
    except Exception as e:
        print("Issue when preparing dictionary for mapping: ", e)
    
    ## Add missing fields to the dataframe (updates over the versions)
    if s == 'Photos':
        #print("INSERTING DAMS LINK: ", s)
        df['dams_link'] = df.get('dams_link', pd.NA)
    
    if s == 'Area-level assessment':
        df['other_damage_notes'] = df.get('other_damage_notes', pd.NA)
        

    # renema colums in the daframe using remap dataframe
    try:
        df.rename(columns=rename_mapping,inplace=True)
    except Exception as e:
        print("Issue when renaming columns: ", e)

    # fix data times types in any dataframe

    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])

    # keep only the columns from the remap dataframe
    try:
        print("Just about to remap: ", df)
        df = df[list(rename_mapping.values())]
        print("df that keeps ranamed lists columns only: ", df)
    except Exception as e:
        print("Issue when keeping the columns after remaping: ", e)

     ## add code project ID to every single table
    df['rmn_id'] = rmn_id
    df['grant_id'] = grant_id
    df['visit'] = visit

    # Replace all Nan or Nat on any table
    df = df.replace('^\s*$', np.nan, regex=True)  ## replaces any white spaces with NaN
    df = df.replace({np.nan: None}) ## replaces any NaN or NaT with Null (for PostgreSQL)

    print("\n\n 4 CLEAN : ",s)

    ## keeps only the two columns with layer names and removes all duplicates 
    column_remap_df = remap_df[['Tab or geopackage layer','Database layer']].drop_duplicates() 

    ## remove empty rows
    exclude_columns = ['rmn_id','visit','grant_id']
    columns_to_check = [col for col in df.columns if col not in exclude_columns]
    df = df[~df[columns_to_check].isnull().all(axis=1)]

    ## rename the sampling points ids and also the drain points ids

    if "sampling_point" in df.columns:
        # Apply the transformation
        df["sampling_point"] = df["sampling_point"].apply(modify_sampling_point)

    if "drain_point" in df.columns:
        # update the drain columns by adding underscore
        df["drain_point"] = df["sampling_point"] + "_drain"

         




    #print(df.info())  ## just for testing
    df.to_csv(f'{s}_after_test.csv')  ## just for testing
    #print(column_remap_df)   ## just for testing
    #print("\n\n\n\n\n\n","df to the database: ", df, "\n\n\n\n\n\n")   ## just for testing

    if column_remap_df['Database layer'].iloc[0] in tables_to_push:

        print(f"\n....Pushing table {column_remap_df['Database layer'].iloc[0]}....\n") 

    ## Push to DB the iloc method takes the shortest name of the table
        execute_values(conn, df, "pa_restoration_monitoring_network."+column_remap_df['Database layer'].iloc[0])
    

## loop over each sheet from each excel survey

for s in sheets_of_interest:
    print("\n\n\ 1 INDIVIDUAL SHEEETS FROM EXCEL ", s)
    try:
        print("\n 2 ....Preparing table: ",s,"\n")
        if s == 'Desk study':
            df = pd.read_excel(file_path, sheet_name=s, index_col=1, keep_default_na=False, na_values=[""])
            # Assuming 'NA' is a string in the Excel file, check for empty cells and Nans. Replace empty cells with None for database NULL while keeping 'NA' intact
            df = df.applymap(lambda x: "Not Applicable" if isinstance(x,str) and x.strip() == "NA" else x)
            df = df.applymap(lambda x: None if x in [np.nan, None, ""] else x)
            #print(df)
            df = df.T
            df = df.dropna(axis=0, how='all') # delete all rows with nulls
            df = df.dropna(axis=1, how='all') # delete all columns with nulls
            #print(df)
            # get columns names from map file
            remap_and_export(s,df,rmn_id,grant_id,visit,conn, tables_to_push)
            
        if s == 'Feature status - drains' or s == 'Feature status - gullies' or s == 'Feature status - hags or banks' or s == 'Feature status - bare peat' or s == 'Feature status - F2B':
            df = pd.read_excel(file_path, sheet_name=s, index_col=0, header=1, keep_default_na=False, na_values=[""])
            df.to_csv(f'{s}_CHECK_NA0.csv')  ## just for testing
            # Assuming 'NA' is a string in the Excel file, check for empty cells and Nans. Replace empty cells with None for database NULL while keeping 'NA' intact
            df = df.applymap(lambda x: "Not Applicable" if isinstance(x,str) and x.strip() == "NA" else x)
            df = df.applymap(lambda x: None if x in [np.nan, None, ""] else x)
            df = df.dropna(axis=0, how='all') # delete all rows with nulls
            df = df.dropna(axis=1, how='all') # delete all columns with nulls
            #print(df)
            df = df.reset_index()
            df = df.drop([0])  # delete first row from dataframe as it contains the datatypes
            df.to_csv(f'{s}_CHECK_NA1.csv')  ## just for testing
            # get columns names from map file
            remap_and_export(s,df,rmn_id,grant_id,visit,conn, tables_to_push)
        
        if s == 'Quadrat information' or s == 'Vegetation' or s == 'Photos':
            #print("\n\n\nHEEEEREEEE ", s)
            df = pd.read_excel(file_path, sheet_name=s, index_col=0, keep_default_na=False, na_values=[""])
            # Assuming 'NA' is a string in the Excel file, check for empty cells and Nans. Replace empty cells with None for database NULL while keeping 'NA' intact
            df = df.applymap(lambda x: "Not Applicable" if isinstance(x,str) and x.strip() == "NA" else x)
            df = df.applymap(lambda x: None if x in [np.nan, None, ""] else x)
            df = df.dropna(axis=0, how='all') # delete all rows with nulls
            df = df.dropna(axis=1, how='all') # delete all columns with nulls
            #print(df)
            df = df.reset_index()
            df = df.drop([0])  # delete second row from dataframe as it contains the datatypes
            
            df.to_csv(f'{s}_before_remap_test.csv')  ## just for testing

            # get columns names from map file
            remap_and_export(s,df,rmn_id,grant_id,visit,conn, tables_to_push)

        if s == 'Area-level assessment':
            print("\n\n\nHEEEEREEEE ", s)
            df = pd.read_excel(file_path, sheet_name=s, header=None, keep_default_na=False, na_values=[""])
            # Assuming 'NA' is a string in the Excel file, check for empty cells and Nans. Replace empty cells with None for database NULL while keeping 'NA' intact
            df = df.applymap(lambda x: "Not Applicable" if isinstance(x,str) and x.strip() == "NA" else x)
            df = df.applymap(lambda x: None if x in [np.nan, None, ""] else x)
            df = df.dropna(axis=0, how='all') # delete all rows with nulls
            df = df.dropna(axis=1, how='all') # delete all columns with nulls

            # Extract headers (rows B2:B6 as headers)
            headers_main = df.loc[1:5, 1].astype(str).tolist()  # B2:B6

            # Extract first row of data (C2:C6)
            first_row_main = df.loc[1:5, 2].tolist()  # C2:C6

            # Create the initial DataFrame
            df_main = pd.DataFrame([first_row_main], columns=headers_main)

            df_main.to_csv(f'{s}_initial_df_main_test.csv')  ## just for testing

            # Extract additional headers (B10:B31)
            headers_extra = df.loc[9:30, 1].astype(str).tolist()  # B10:B31

            # Extract first row of data for extra headers (C10:C31)
            first_row_extra = df.loc[9:30, 2].tolist()  # C10:C31

            # Extract additional headers with _notes suffix (B10:B31 again)
            headers_extra_notes = [h + "_notes" for h in headers_extra]

            # Extract first row for _notes headers (D10:D31)
            first_row_notes = df.loc[9:30, 3].tolist()  # D10:D31

            # Combine into a single DataFrame
            df_extra = pd.DataFrame([first_row_extra + first_row_notes], 
                                    columns=headers_extra + headers_extra_notes)
            
            df_extra.to_csv(f'{s}_initial_df_extra_test.csv')  ## just for testing

            # Concatenate both parts horizontally
            df = pd.concat([df_main, df_extra], axis=1)

            df.to_csv(f'{s}_before_remap_test.csv')  ## just for testing

            # get columns names from map file
            remap_and_export(s,df,rmn_id,grant_id,visit,conn, tables_to_push)

            check_values_not_exist(conn, tables, columns, values)


    except ValueError:
        print(f'{s}: Layer not found')
    except KeyError as k:
        print(f'{s}: Key Error {k}')
    except TypeError:
        print(f'{s}: Data Type Error')
    except FileNotFoundError:
        print(f'{file_path}: File not found')
    except Exception as e:
        print(f'Unexpected error occurred. Could be related with the sheets names in excel being different or not present: {e}')
    
   
## check for invalid and null records

