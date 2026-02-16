'''
FileHandlingUtilities
Utilities used by various reports for file handling
'''

import logging
import os
import pandas as pd
import reports.ExcelFileOutput
import reports.division_detail_report
import reports.kata_score_sheet
import reports.sparring_tree
from pathlib import Path
import re

def pathDelimiter():
    path = os.getcwd()
    if "\\" in path:
        delimiter = "\\"  # Windows
    else:
        delimiter = "/"  # Unix
    return delimiter

def next_versioned_filename(path: str, width: int = 2) -> Path:
    """
    Given 'file.txt', returns:
        file-01.txt (if none exist)
        file-02.txt (if file-01.txt exists)
        etc.
    """
    p = Path(path)
    parent = p.parent
    stem = p.stem
    suffix = p.suffix

    # Check to see if the stem already contains a version number
    pattern = re.compile(r"^(.+)-\d{2}$")
    match = pattern.match(stem)
    if match:
        stem = match.group(1)

    # Regex to match existing versions
    pattern = re.compile(rf"^{re.escape(stem)}-(\d+){re.escape(suffix)}$")


    max_version = 0
    search_string = f"{stem}-*{suffix}"

    for f in parent.glob(search_string):
        match = pattern.match(f.name)
        if match:
            max_version = max(max_version, int(match.group(1)))

    next_version = max_version + 1
    next_filename = f"{stem}-{next_version:0{width}d}{suffix}"
    return next_filename



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
