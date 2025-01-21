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
import glob

import pandas as pd


## SCRIPT SETTINGS
pd.set_option('display.max_columns', None)  # print all column names
 
## READ EXCEL MAP
map_df = pd.read_excel(r'map\RMN data for database.xlsx')
#print(map_df)

##FILTER MAP BY COLUMS UPLOAD TO DB

map_df = map_df[map_df['Upload to DB'] == 'Yes'] # keep only columns where Upload to DB is YES
#print(map_df)



## CREATE LIST OF SHEETS OF INTEREST
sheets_of_interest = map_df['Tab or layer'].unique() ## get the list from mapdataframe
#print(sheets_of_interest)

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

def remap_and_export(s):

    remap_df = map_df[map_df['Tab or layer'] == s]  
    # convert column names to a dictionary
    rename_mapping = dict(zip(remap_df['Field name'], remap_df['Field name for DB']))
    df.rename(columns=rename_mapping,inplace=True)
    df.to_csv(f'{s}_test.csv')


## loop over each sheet from each excel survey

for s in sheets_of_interest:
    #print(s)
    if s == 'Desk study':
        df = pd.read_excel(xlsx_files[0], sheet_name=s, index_col=1)
        #print(df)
        df = df.T
        df = df.dropna(axis=0, how='all') # delete all rows with nulls
        df = df.dropna(axis=1, how='all') # delete all columns with nulls
        #print(df)
        # get columns names from map file
        remap_and_export(s)
        
    if s == 'Feature status - drains' or s == 'Feature status - gullies' or s == 'Feature status - bare peat' or s == 'Feature status - F2B':
        df = pd.read_excel(xlsx_files[0], sheet_name=s, index_col=0, header=1)
        df = df.dropna(axis=0, how='all') # delete all rows with nulls
        df = df.dropna(axis=1, how='all') # delete all columns with nulls
        #print(df)
        df = df.reset_index()
        df = df.drop([0])  # delete first row from dataframe as it contains the datatypes
        
        # get columns names from map file
        remap_and_export(s)
    
    if s == 'Quadrat information' or s == 'Vegetation':
        df = pd.read_excel(xlsx_files[0], sheet_name=s, index_col=0)
        df = df.dropna(axis=0, how='all') # delete all rows with nulls
        df = df.dropna(axis=1, how='all') # delete all columns with nulls
        #print(df)
        df = df.reset_index()
        df = df.drop([0])  # delete second row from dataframe as it contains the datatypes
        
        # get columns names from map file
        remap_and_export(s)



## check for invalid and null records

