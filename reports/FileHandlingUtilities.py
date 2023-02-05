'''
FileHandlingUtilities
Utilities used by various reports for file handling
'''

import logging
import os
import pandas as pd
import reports.ExcelFileOutput
import reports.DivisionDetailReportPDF
import reports.KataScoreSheetPDF
import reports.sparring_tree

def pathDelimiter():
    path = os.getcwd()
    if "\\" in path:
        delimiter = "\\"  # Windows
    else:
        delimiter = "/"  # Unix
    return delimiter


#Experimental
def newDataFrameFromQuery(clean_df:pd.DataFrame, query_string: str):
    #query_string='Rank == "White" and Rank == "Yellow" and Age >= 4 and Age =< 6'
    newdf = clean_df[["Registrant_ID","First_Name", "Last_Name", "Gender", "Dojo", "Age", "Rank", "Feet", "Inches", "Height", "Weight", "BMI",
    "Events", "Weapons"]].query(query_string).sort_values("Age").sort_values("BMI")

    ## update the hitcount every time we touch someone
    for index, row in newdf.iterrows():
        name = row['First_Name'] + " " + row['Last_Name']
        id= row['Registrant_ID']
        hc=clean_df.at[index,'hitcount']
        newhc = hc + 1
        #logging.info(f'{id}:{name} has a row count of {newhc}')
        clean_df.at[index,'hitcount']=newhc
    return newdf
