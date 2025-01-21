"""
This script reads the spatial data template from RMS
and covert each table into a dataframe.
Then remap the columns names and check for invalid records.
Finally, prepares the df to be pushed to the database.
Author: Javier Soto
Date: 20/01/2024
Version: V1.0
"""

## IMPORT LIBRARIES

import os
import glob

import pandas as pd
import geopandas as gpd


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

## READ GPKG SURVEY DATA

## loop over the list of GPKG files in the root folder
rootdir = r'data'
gpkg_files = []  # create empty list of gpkg files

for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        filepath = subdir + os.sep + file
        if filepath.endswith(".gpkg"):
            #print(filepath)
            gpkg_files.append(filepath) # append gpkg files to a list
        

## function to remap sheets and export csv:

def remap_and_export(s):

    remap_df = map_df[map_df['Tab or layer'] == s]  
    # convert column names to a dictionary
    rename_mapping = dict(zip(remap_df['Field name'], remap_df['Field name for DB']))
    df.rename(columns=rename_mapping,inplace=True)
    df.to_csv(f'{s}_test.csv')


## loop over each sheet from each excel survey

for s in sheets_of_interest:

    try:
        df = gpd.read_file(gpkg_files[0], layer=s)
        df = df.dropna(axis=0, how='all') # delete all rows with nulls
        df = df.dropna(axis=1, how='all') # delete all columns with nulls
        # get columns names from map file
        remap_and_export(s)
    except ValueError:
        print(f'{s}: layer not found')

        


