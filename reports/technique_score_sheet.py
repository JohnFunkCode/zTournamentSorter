import logging
import pandas
import datetime
import time
import pathlib


#
import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, portrait
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from reportlab.platypus import PageBreak
from reportlab.platypus import SimpleDocTemplate, Spacer, Table, TableStyle
import domain_model.constants as constants
import reports


from reports.kata_score_sheet import KataScoreSheet


class TechniqueScoreSheet(KataScoreSheet):
    def __init__(self,title:str, sourcefile:str,output_folder_path:str):
        self.filename_with_path=str(pathlib.Path(output_folder_path + reports.FileHandlingUtilities.pathDelimiter() +'TechniquesScoreSheet.pdf'))

        # self.doc = SimpleDocTemplate("KataScoreSheet.pdf", pagesize=portrait(letter),topMargin=0, bottomMargin=0)
        self.doc = SimpleDocTemplate(self.filename_with_path, pagesize=portrait(letter),topMargin=0, bottomMargin=0)
        self.docElements = []
        #setup the package scoped global variables we need
        now = datetime.datetime.now()
        KataScoreSheet.timestamp = now.strftime("%Y-%m-%d %H:%M")
        # KataScoreSheet.sourcefile = "not initialized"
        KataScoreSheet.sourcefile = sourcefile
        KataScoreSheet.pageinfo = "not initialized"
        # KataScoreSheet.Title = "not initialized"
        KataScoreSheet.Title = title
        KataScoreSheet.PAGE_HEIGHT = 11 * inch
        KataScoreSheet.PAGE_WIDTH = 8.5 * inch
        KataScoreSheet.styles = getSampleStyleSheet()   #sample style sheet doesn't seem to be used
        KataScoreSheet.ring_number= "not initialized"
        KataScoreSheet.event_time= "not initialized"
        KataScoreSheet.division_name= "not initialized"
        KataScoreSheet.age= "not initialized"
        KataScoreSheet.belts= "not initialized"

    ###############################################################################
    # writeSingleKataScoreSheet
    #  Spring 2023
    #  This method writes a single kata score sheet based on parameters provided
    #
    def writeSingleTechniqueScoreSheet(self,event_time: str, division_name: str, division_type: str, gender: str, rank_label: str, minimum_age: int,
                                  maximum_age: int, rings: list, ranks: list,clean_df: pandas.DataFrame):
        if (maximum_age == constants.AGELESS):
            age_label = '{0}+'.format(minimum_age)
        else:
            age_label = '{0} - {1}'.format(minimum_age, maximum_age)

        # Hack for 3 year olds
        if minimum_age == 4:
            minimum_age = 2

        #logging.info("Generating Kata Score PDF for " + event_time + " " + division_name + " " + age_label)
        logging.info(f'Generating {division_type} Score PDF for {event_time} {division_name} {age_label}')
        self.set_title(f'{division_type}')

        age_query = 'Age >={0} and Age <={1}'.format(minimum_age, maximum_age)

        rank_query = ''
        for r in range(0, len(ranks)):
            rank_query = rank_query + 'Rank =="' + ranks[r] + '"'
            if r < len(ranks) - 1:  # Add ' and ' to everything but the last one
                rank_query = rank_query + ' or '

        assert  division_type == 'Techniques', "Error: Invalid division_type"
        division_type_query = 'Techniques.str.contains("Technique")'

        if gender != '*':
            gender_query = 'Gender == "' + gender + '"'
            combined_query = f'({division_type_query}) and ({age_query}) and ({rank_query}) and ({gender_query})'
        else:
            combined_query = f'({division_type_query}) and ({age_query}) and ({rank_query})'

        # wmk=newDataFrameFromQuery(combined_query)
        wmk = clean_df[
            ["Registrant_ID", "First_Name", "Last_Name", "Gender", "Dojo", "Age", "Rank", "Feet", "Inches", "Height",
             "Weight", "BMI", "Events", "Techniques", "Weapons"]].query(combined_query).sort_values("Age").sort_values("BMI")

        if len(rings) > 1:  # more than 1 ring means we split
            # filter to only keep contestants who's last name fall into the first alphabetic split
            first_alphabetic_split = wmk[wmk['Last_Name'].str.contains(constants.FIRST_ALPHABETIC_SPLIT_REGEX)]

            # filter to only keep contestants who's last name fall into the second alphabetic split
            second_alphabetic_split = wmk[wmk['Last_Name'].str.contains(constants.SECOND_ALPHABETIC_SPLIT_REGEX)]

            self.put_dataframe_on_pdfpage(first_alphabetic_split, str(rings[0]), event_time, division_name,
                                                      age_label,
                                                      rank_label + " (" + constants.FIRST_ALPHABETIC_SPLIT_LABEL + ")",
                                                      "*** PLEASE NOTE - These are contestants " + constants.FIRST_ALPHABETIC_SPLIT_LABEL)

            self.put_dataframe_on_pdfpage(second_alphabetic_split, str(rings[1]), event_time,
                                                      division_name, age_label,
                                                      rank_label + "  (" + constants.SECOND_ALPHABETIC_SPLIT_LABEL + ")",
                                                      "*** PLEASE NOTE - These are contestants " + constants.SECOND_ALPHABETIC_SPLIT_LABEL)
        else:
            self.put_dataframe_on_pdfpage(wmk, str(rings[0]), event_time, division_name, age_label,
                                                      rank_label)

