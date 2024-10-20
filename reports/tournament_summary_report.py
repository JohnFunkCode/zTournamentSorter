"""
@author: john funk
"""
import logging
import pandas
import sys
import datetime
import time
import pathlib

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from reportlab.platypus import PageBreak
from reportlab.platypus import SimpleDocTemplate, Spacer, Table, TableStyle
import domain_model.constants as constants
import reports
import reports.FileHandlingUtilities


class TournamentSummaryReport():

    def __init__(self, title:str, data_file_name: str, output_folder_path:str):
        filename_with_path = f'{pathlib.Path(output_folder_path)}{reports.FileHandlingUtilities.pathDelimiter()}{"TournamentSummaryReport.pdf"}'


    def add_division_details(self,event_time: str, division_name: str, division_type: str, gender: str, rank_label:str, minimum_age: int, maximum_age: int, rings: list, ranks:list, division_competitors: pandas.DataFrame):
        logging.info( f'division summary:{event_time} {division_name}  {division_type} {gender} {rank_label} {minimum_age} {maximum_age} {rings} {ranks}')
        logging.info( f'{division_competitors}')


def main():
    logger = logging.getLogger('')
    logger.setLevel(logging.INFO)
    fh = logging.FileHandler("TournamentSummaryReport.log")
    sh = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s %(message)s', datefmt='%H:%M:%S')
    fh.setFormatter(formatter)
    sh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(sh)

    TSR_pdf = TournamentSummaryReport( "Tournament Summary Report", "DataFileName", "")
    competitors_list = { 'First_Name': ['John','Jason'],
                         'Last_Name':  ['Funk','Stele'] }
    competitors = pd.DataFrame(competitors_list)
    TSR_pdf.add_division_details(event_time="9:00am",division_name="Kids Kata",division_type="Forms",gender="*",rank_label="White",                     minimum_age=4, maximum_age=6, rings=[[1,'A','Z']],  ranks=[constants.WHITE_BELT], division_competitors=competitors)

if __name__ == "__main__":
    main()
