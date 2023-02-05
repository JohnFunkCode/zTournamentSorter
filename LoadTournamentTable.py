# V 11/20/2022
# There are 6 patterns in the Denver Tournament Guide
#
# Pattern1 - ranking based on size of the division it would be use for: 
#  White, Yellow, Orange
#  Purple, Blue, Blue Stripe
#  Green, Green Stripe, Brown
#  Black
#
# Pattern2 - ranking based on size of the division it would be use for:
#    White, Yellow & Orange
#    Purple, Blue & Blue Stripe
#    Green, Green Stripe,
#    Brown
#    Black
#
# Pattern3 - ranking based on size of the division it would be use for:
#  White, Yellow
#  Orange
#  Purple
#  Blue, Blue Stripe
#  Green, Green Stripe, Brown
#
# Pattern4 - ranking based on size of the division it would be use for:
#    White
#    Yellow
#    Orange
#    Purple, Blue, Blue Stripe
#    Green, Green Stripe
#
# Pattern5 - ranking based on size of the division it would be use for:
#  White
#  Yellow
#  Orange
#  Purple
#  Blue, Blue Stripe
#  Green, Green Stripe, Brown
#
#
# Pattern6 - ranking based on size of the division it would be use for:
#  White, Yellow
#  Orange
#  Purple
#  Blue, Blue Stripe
#  Green, Green Stripe
#  Brown
#  Black

import os
import sys
import time
import logging
import re

from tkinter import Tk
from tkinter.filedialog import askopenfilename

import pandas as pd

from cleaninput import cleaninput
from cleaninput import rename_colums as RN
from cleaninput import input_errors

from reports import DivisionDetailReportPDF
from reports import KataScoreSheetPDF as kata_score_sheet_pdf
import reports.sparring_tree.sparring_tree_report
import reports.ExcelFileOutput
import reports.FileHandlingUtilities
import domain_model.constants as constants


###############################################################################
# writeSingleKataScoreSheetandDivisionReport
#  Provides a convenience wrapper that writes to both the division detail report and the kata score sheet in one line
#  This prevents a lot of duplication
def writeSingleKataScoreSheetandDivisionReport(event_time: str, division_name: str, gender: str, rank_label: str, minimum_age: int,maximum_age: int, rings: list, ranks: list,clean_df: pd.DataFrame):
    divison_detail_report_pdf.writeSingleDivisionDetailReport(event_time=event_time, division_name=division_name, division_type="Forms", gender=gender, rank_label=rank_label, minimum_age=minimum_age, maximum_age=maximum_age, rings=rings, ranks=ranks, clean_df=clean_df)
    kata_score_sheet.writeSingleKataScoreSheet(event_time=event_time, division_name=division_name,division_type="Forms", gender=gender,rank_label=rank_label, minimum_age=minimum_age, maximum_age=maximum_age, rings=rings,ranks=ranks, clean_df=clean_df)
#
# def writeSingleKataScoreSheetandDivisionReport(event_time: str, division_name: str, gender: str, rank_label: str, minimum_age: int,maximum_age: int, rings: list, ranks: list,clean_df: pd.DataFrame):
#     divison_detail_report_pdf.writeSingleDivisionDetailReport(event_time=event_time, division_name=division_name,division_type="Forms", gender=gender,rank_label=rank_label, minimum_age=minimum_age,maximum_age=maximum_age, rings=rings,ranks=ranks,clean_df=clean_df)
#     kata_score_sheet.writeSingleKataScoreSheet(event_time=event_time, division_name=division_name,division_type="Forms", gender=gender,rank_label=rank_label, minimum_age=minimum_age, maximum_age=maximum_age, rings=rings,ranks=ranks, clean_df=clean_df)

###############################################################################
# write_single_sparring_treeShim
#  Provides a convenience wrapper that writes to both the division detail report and the sparring tree in one line
#  This prevents a lot of duplication
def writeSingleSparringTreeandDivisionReport(event_time: str, division_name, gender: str, rank_label: str, minimum_age: int, maximum_age: int, rings: list, ranks: list, clean_df : pd.DataFrame ):
    divison_detail_report_pdf.writeSingleDivisionDetailReport(event_time=event_time, division_name=division_name,division_type="Sparring", gender=gender,rank_label=rank_label, minimum_age=minimum_age,maximum_age=maximum_age, rings=rings,ranks=ranks,clean_df=clean_df)
    sparing_tree_pdf.write_single_sparring_tree(event_time=event_time, division_name=division_name, gender=gender,rank_label=rank_label, minimum_age=minimum_age, maximum_age=maximum_age, rings=rings,ranks=ranks, clean_df=clean_df)

###############################################################################
# writeSingleKataScoreSheetandDivisionReport
#  Provides a convenience wrapper that writes to both the division detail report and the kata score sheet in one line
#  This prevents a lot of duplication
def writeWeaponsDivisionToSingleKataScoreSheetandDivisionReport(event_time: str, division_name: str, gender: str, rank_label: str, minimum_age: int,maximum_age: int, rings: list, ranks: list,clean_df: pd.DataFrame):
    divison_detail_report_pdf.writeSingleDivisionDetailReport(event_time=event_time, division_name=division_name,division_type="Weapons", gender=gender,rank_label=rank_label, minimum_age=minimum_age, maximum_age=maximum_age, rings=rings,ranks=ranks, clean_df=clean_df)
    kata_score_sheet.writeSingleKataScoreSheet(               event_time=event_time, division_name=division_name,division_type="Weapons", gender=gender,rank_label=rank_label, minimum_age=minimum_age, maximum_age=maximum_age, rings=rings,ranks=ranks, clean_df=clean_df)



###############################################################################
#
# Main Function
#
# logging.basicConfig(format='%(asctime)s %(levelname)s - %(message)s', level=logging.INFO, datefmt='%H:%M:%S')

# get the filename from the environment var named  tourname_filename
filename = os.getenv("tournament_filename")

if filename is None:
    # Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    root = Tk()
    root.withdraw()  # we don't want a full GUI, so keep the root window from appearing
    root.update()  # Prevent the askfilename() window doesn't stay open
    filename = askopenfilename()
    root.update()  # Prevent the askfilename() window doesn't stay open
else:
    print("Using the file " + filename + "from the environment")

# filename = "C:\\Users\\Maria\\Downloads\\tournamentprojectmaterial\\RegistrantExport.csv"
# filename = "/users/johnfunk/CloudStation/TournamentProject/Clean_RegistrantExport_EM0393_20160411140713.csv"  # For Testing on John's machine

errorLogFileName = filename[0:len(filename) - 4] + "-Error.txt"

logger = logging.getLogger('')
logger.setLevel(logging.INFO)
fh = logging.FileHandler(errorLogFileName)
sh = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('[%(asctime)s] %(levelname)s %(message)s', datefmt='%H:%M:%S')
fh.setFormatter(formatter)
sh.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(sh)

logging.info("Reading the data from:" + filename + "....")

#### SET Encoding to UTF-8 added 3/27/2022
cleaninput.set_utf_encoding()



cleaninput.clean_unicode_from_file(filename)

# rename all the columns in the dataframe to usable names
r = RN.RenameColumns(filename)
r.rename_all_columns()
renamed_df = r.get_dataframe_copy()

input_error_list = input_errors.InputErrors()
clean_df,error_count = cleaninput.clean_all_input_errors(renamed_df, input_error_list)
del renamed_df  # make sure we don't use the renamed_df again
# logging.info(f'Input Errors:{input_error_list.error_list}')
if error_count > 0:
    sys.exit("Exiting - The input must be fixed manually")

# create test data
clean_df.to_pickle("pickled_clean_dataframe.pkl")

#make sure the sorted directory exists
try:
    os.mkdir("sorted")
except:
    assert(1==1)
    #logging.info("expected error")


clean_df['hitcount'] = 0  # setup a new column for hit rate.

logging.info("Generating the output results...")

###############################################################################
# Setup a few things for the Division Detail PDF report
divison_detail_report_pdf = DivisionDetailReportPDF.DivisionDetailReportPDF()
DivisionDetailReportPDF.DivisionDetailReportPDF.set_title("Division Detail")
DivisionDetailReportPDF.DivisionDetailReportPDF.set_sourcefile(filename)

###############################################################################
# Setup a few things for the Kata Score Sheet PDF report
kata_score_sheet = kata_score_sheet_pdf.KataScoreSheetPDF()
kata_score_sheet_pdf.KataScoreSheetPDF.set_title("Forms")
kata_score_sheet_pdf.KataScoreSheetPDF.set_sourcefile(filename)

###############################################################################
# Setup a few things for the Sparring Tree PDF report
sparing_tree_pdf = reports.sparring_tree.sparring_tree_report.SparringTreeReportPDF()
sparing_tree_pdf.set_source_file( filename )

### Special Handling for files with less than 30 competitors- Added for Fall 2022 Tournament
if clean_df.shape[0] < 30:
    logging.warning("\u001b[31m*** Special Handling!  Printing Just One Kata Sheet and One Sparring Tree with the small data file provided!\u001b[0m")
    #divison_detail_report_pdf.writeSingleDivisionDetailReport(event_time="", division_name="",division_type="Forms", gender="*", rank_label="",minimum_age=1, maximum_age=constants.AGELESS, rings=[1],ranks=[constants.WHITE_BELT,constants.YELLOW_BELT,constants.ORANGE_BELT,constants.PURPLE_BELT,constants.BLUE_BELT,constants.BLUE_STRIPE_BELT,constants.GREEN_BELT,constants.GREEN_STRIPE_BELT,constants.THIRD_DEGREE_BROWN_BELT,constants.SECOND_DEGREE_BROWN_BELT,constants.FIRST_DEGREE_BROWN_BELT,constants.FIRST_DEGREE_BLACK_BELT,constants.SECOND_DEGREE_BLACK_BELT, constants.THIRD_DEGREE_BLACK_BELT,constants.FOURTH_DEGREE_BLACK_BELT,constants.FIFTH_DEGREE_BLACK_BELT,constants.JUNIOR_BLACK_BELT], clean_df=clean_df)
    writeSingleKataScoreSheetandDivisionReport(               event_time="", division_name="",                       gender="*", rank_label="",minimum_age=1, maximum_age=constants.AGELESS, rings=[''],ranks=[constants.WHITE_BELT,constants.YELLOW_BELT,constants.ORANGE_BELT,constants.PURPLE_BELT,constants.BLUE_BELT,constants.BLUE_STRIPE_BELT,constants.GREEN_BELT,constants.GREEN_STRIPE_BELT,constants.THIRD_DEGREE_BROWN_BELT,constants.SECOND_DEGREE_BROWN_BELT,constants.FIRST_DEGREE_BROWN_BELT,constants.FIRST_DEGREE_BLACK_BELT,constants.SECOND_DEGREE_BLACK_BELT, constants.THIRD_DEGREE_BLACK_BELT,constants.FOURTH_DEGREE_BLACK_BELT,constants.FIFTH_DEGREE_BLACK_BELT,constants.JUNIOR_BLACK_BELT], clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(              event_time="", division_name="",                       gender="*", rank_label="",minimum_age=1, maximum_age=constants.AGELESS, rings=[''],ranks=[constants.WHITE_BELT,constants.YELLOW_BELT,constants.ORANGE_BELT,constants.PURPLE_BELT,constants.BLUE_BELT,constants.BLUE_STRIPE_BELT,constants.GREEN_BELT,constants.GREEN_STRIPE_BELT,constants.THIRD_DEGREE_BROWN_BELT,constants.SECOND_DEGREE_BROWN_BELT,constants.FIRST_DEGREE_BROWN_BELT,constants.FIRST_DEGREE_BLACK_BELT,constants.SECOND_DEGREE_BLACK_BELT, constants.THIRD_DEGREE_BLACK_BELT,constants.FOURTH_DEGREE_BLACK_BELT,constants.FIFTH_DEGREE_BLACK_BELT,constants.JUNIOR_BLACK_BELT], clean_df=clean_df)
else:


    ### 9:00AM Events

    ###############################################################################
    # Kids Kata  - 4-6 year olds
    #
    reports.ExcelFileOutput.writePattern4ToExcelViaQuery(filename="KidsKata.xlsx", division_type='Forms', gender="*",minimum_age=4, maximum_age=6, clean_df=clean_df)

    writeSingleKataScoreSheetandDivisionReport(event_time="9:00am",division_name="Kids Kata",gender="*",rank_label="White",                     minimum_age=4, maximum_age=6, rings=[1],  ranks=[constants.WHITE_BELT], clean_df=clean_df)
    writeSingleKataScoreSheetandDivisionReport(event_time="9:00am",division_name="Kids Kata",gender="*",rank_label="Yellow",                    minimum_age=4, maximum_age=6, rings=[2,3],ranks=[constants.YELLOW_BELT], clean_df=clean_df)
    writeSingleKataScoreSheetandDivisionReport(event_time="9:00am",division_name="Kids Kata",gender="*",rank_label="Orange",                    minimum_age=4, maximum_age=6, rings=[4,5],ranks=[constants.ORANGE_BELT], clean_df=clean_df)
    writeSingleKataScoreSheetandDivisionReport(event_time="9:00am",division_name="Kids Kata",gender="*",rank_label="Purple, Blue, Blue/Stripe", minimum_age=4, maximum_age=6, rings=[6],  ranks=[constants.PURPLE_BELT,constants.BLUE_BELT,constants.BLUE_STRIPE_BELT], clean_df=clean_df)
    writeSingleKataScoreSheetandDivisionReport(event_time="9:00am",division_name="Kids Kata",gender="*",rank_label="Green, Green/Stripe, Brown",minimum_age=4, maximum_age=6, rings=[7],  ranks=[constants.GREEN_BELT,constants.GREEN_STRIPE_BELT,constants.THIRD_DEGREE_BROWN_BELT,constants.SECOND_DEGREE_BROWN_BELT,constants.FIRST_DEGREE_BROWN_BELT], clean_df=clean_df)


    ###############################################################################
    # Youth Kata  - 7-8 year olds
    #
    reports.ExcelFileOutput.writePattern5ToExcelViaQuery(filename="YouthKata.xlsx", division_type='Forms', gender="*",minimum_age=7, maximum_age=8,clean_df=clean_df)

    writeSingleKataScoreSheetandDivisionReport(event_time="9:00am",division_name="Youth Kata",gender="*",rank_label="White",                     minimum_age=7, maximum_age=8, rings=[8],    ranks=[constants.WHITE_BELT], clean_df=clean_df)
    writeSingleKataScoreSheetandDivisionReport(event_time="9:00am",division_name="Youth Kata",gender="*",rank_label="Yellow",                    minimum_age=7, maximum_age=8, rings=[9],    ranks=[constants.YELLOW_BELT], clean_df=clean_df)
    writeSingleKataScoreSheetandDivisionReport(event_time="9:00am",division_name="Youth Kata",gender="*",rank_label="Orange",                    minimum_age=7, maximum_age=8, rings=[10,11],ranks=[constants.ORANGE_BELT], clean_df=clean_df)
    writeSingleKataScoreSheetandDivisionReport(event_time="9:00am",division_name="Youth Kata",gender="*",rank_label="Purple",                    minimum_age=7, maximum_age=8, rings=[12,13],ranks=[constants.PURPLE_BELT], clean_df=clean_df)
    writeSingleKataScoreSheetandDivisionReport(event_time="9:00am",division_name="Youth Kata",gender="*",rank_label="Blue, Blue/Stripe",         minimum_age=7, maximum_age=8, rings=[14,15],ranks=[constants.BLUE_BELT,constants.BLUE_STRIPE_BELT], clean_df=clean_df)
    writeSingleKataScoreSheetandDivisionReport(event_time="9:00am",division_name="Youth Kata",gender="*",rank_label="Green, Green/Stripe, Brown",minimum_age=7, maximum_age=8, rings=[16],   ranks=[constants.GREEN_BELT,constants.GREEN_STRIPE_BELT,constants.THIRD_DEGREE_BROWN_BELT,constants.SECOND_DEGREE_BROWN_BELT,constants.FIRST_DEGREE_BROWN_BELT], clean_df=clean_df)

    ### 9:45 Events

    ###############################################################################
    # Kids Sparring Spreadsheet - 4-6 year olds
    #
    reports.ExcelFileOutput.writePattern4ToExcelViaQuery(filename="KidsSparring.xlsx", division_type='Sparring', gender="*",minimum_age=4, maximum_age=6,clean_df=clean_df)

    writeSingleSparringTreeandDivisionReport(event_time="9:45am",division_name="Kids Sparring",gender="*", rank_label="White",                     minimum_age=4, maximum_age=6, rings=[1],     ranks=[constants.WHITE_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="9:45am",division_name="Kids Sparring",gender="*", rank_label="Yellow",                    minimum_age=4, maximum_age=6, rings=[2,3],  ranks=[constants.YELLOW_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="9:45am",division_name="Kids Sparring",gender="*", rank_label="Orange",                    minimum_age=4, maximum_age=6, rings=[4,5],  ranks=[constants.ORANGE_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="9:45am",division_name="Kids Sparring",gender="*", rank_label="Purple, Blue, Blue/Stripe", minimum_age=4, maximum_age=6, rings=[6],  ranks=[constants.PURPLE_BELT,constants.BLUE_BELT,constants.BLUE_STRIPE_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="9:45am",division_name="Kids Sparring",gender="*", rank_label="Green, Green/Stripe, Brown", minimum_age=4, maximum_age=6, rings=[7],  ranks=[constants.GREEN_BELT,constants.GREEN_STRIPE_BELT,constants.THIRD_DEGREE_BROWN_BELT,constants.SECOND_DEGREE_BROWN_BELT,constants.FIRST_DEGREE_BROWN_BELT],clean_df=clean_df)


    ###############################################################################
    # Boy's & Girl's Kata  - 9-11 year olds
    #
    reports.ExcelFileOutput.writePattern6ToExcelViaQuery(filename="BoysGirlsKata.xlsx", division_type='Forms', gender="*",minimum_age=9, maximum_age=11,clean_df=clean_df)

    writeSingleKataScoreSheetandDivisionReport(event_time="9:45am",division_name="Boy's & Girl's Kata",gender="*", rank_label="White, Yellow",         minimum_age=9, maximum_age=11, rings=[8],     ranks=[constants.WHITE_BELT,constants.YELLOW_BELT], clean_df=clean_df)
    writeSingleKataScoreSheetandDivisionReport(event_time="9:45am",division_name="Boy's & Girl's Kata",gender="*", rank_label="Orange",                minimum_age=9, maximum_age=11, rings=[9],     ranks=[constants.ORANGE_BELT], clean_df=clean_df)
    writeSingleKataScoreSheetandDivisionReport(event_time="9:45am",division_name="Boy's & Girl's Kata",gender="*", rank_label="Purple",                minimum_age=9, maximum_age=11, rings=[10,11], ranks=[constants.PURPLE_BELT], clean_df=clean_df)
    writeSingleKataScoreSheetandDivisionReport(event_time="9:45am",division_name="Boy's & Girl's Kata",gender="*", rank_label="Blue, Blue w/Stripe",   minimum_age=9, maximum_age=11, rings=[12,13], ranks=[constants.BLUE_BELT,constants.BLUE_STRIPE_BELT], clean_df=clean_df)
    writeSingleKataScoreSheetandDivisionReport(event_time="9:45am",division_name="Boy's & Girl's Kata",gender="*", rank_label="Green, Green w/Stripe", minimum_age=9, maximum_age=11, rings=[15],    ranks=[constants.GREEN_BELT,constants.GREEN_STRIPE_BELT], clean_df=clean_df)
    writeSingleKataScoreSheetandDivisionReport(event_time="9:45am",division_name="Boy's & Girl's Kata",gender="*", rank_label="Brown",                 minimum_age=9, maximum_age=11, rings=[16],    ranks=[constants.THIRD_DEGREE_BROWN_BELT,constants.SECOND_DEGREE_BROWN_BELT,constants.FIRST_DEGREE_BROWN_BELT], clean_df=clean_df)
    writeSingleKataScoreSheetandDivisionReport(event_time="9:45am",division_name="Boy's & Girl's Kata",gender="*", rank_label="Jr. Black",             minimum_age=9, maximum_age=11, rings=[17],    ranks=[constants.FIRST_DEGREE_BLACK_BELT,constants.SECOND_DEGREE_BLACK_BELT, constants.THIRD_DEGREE_BLACK_BELT,constants.FOURTH_DEGREE_BLACK_BELT,constants.FIFTH_DEGREE_BLACK_BELT,constants.JUNIOR_BLACK_BELT], clean_df=clean_df)

    ### 10:30 Events

    ###############################################################################
    # Youth Girl's Sparring  - 7-8 year olds
    #
    reports.ExcelFileOutput.writePattern3ToExcelViaQuery(filename="YouthGirlSparring.xlsx", division_type='Forms', gender="Female",minimum_age=7, maximum_age=8,clean_df=clean_df)

    writeSingleSparringTreeandDivisionReport(event_time="10:30am",division_name="Youth Girl's Sparring",gender="Female", rank_label="White, Yellow",             minimum_age=7, maximum_age=8, rings=[1], ranks=[constants.WHITE_BELT,constants.YELLOW_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="10:30am",division_name="Youth Girl's Sparring",gender="Female", rank_label="Orange",                    minimum_age=7, maximum_age=8, rings=[2], ranks=[constants.ORANGE_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="10:30am",division_name="Youth Girl's Sparring",gender="Female", rank_label="Purple",                    minimum_age=7, maximum_age=8, rings=[3], ranks=[constants.PURPLE_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="10:30am",division_name="Youth Girl's Sparring",gender="Female", rank_label="Blue, Blue/Stripe",         minimum_age=7, maximum_age=8, rings=[4], ranks=[constants.BLUE_BELT,constants.BLUE_STRIPE_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="10:30am",division_name="Youth Girl's Sparring",gender="Female", rank_label="Green, Green/Stripe, Brown",minimum_age=7, maximum_age=8, rings=[5], ranks=[constants.GREEN_BELT,constants.GREEN_STRIPE_BELT,constants.THIRD_DEGREE_BROWN_BELT,constants.SECOND_DEGREE_BROWN_BELT,constants.FIRST_DEGREE_BROWN_BELT],clean_df=clean_df)

    ###############################################################################
    # Youth Boy's Sparring - 7-8 year olds
    #
    reports.ExcelFileOutput.writePattern3ToExcelViaQuery(filename="YouthBoysSparring.xlsx", division_type='Forms', gender="Male",minimum_age=7, maximum_age=8,clean_df=clean_df)

    writeSingleSparringTreeandDivisionReport(event_time="10:30am",division_name="Youth Boy's Sparring",gender="Male", rank_label="White, Yellow",             minimum_age=7, maximum_age=8, rings=[6], ranks=[constants.WHITE_BELT,constants.YELLOW_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="10:30am",division_name="Youth Boy's Sparring",gender="Male", rank_label="Orange",                    minimum_age=7, maximum_age=8, rings=[7], ranks=[constants.ORANGE_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="10:30am",division_name="Youth Boy's Sparring",gender="Male", rank_label="Purple",                    minimum_age=7, maximum_age=8, rings=[8], ranks=[constants.PURPLE_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="10:30am",division_name="Youth Boy's Sparring",gender="Male", rank_label="Blue, Blue/Stripe",         minimum_age=7, maximum_age=8, rings=[9], ranks=[constants.BLUE_BELT,constants.BLUE_STRIPE_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="10:30am",division_name="Youth Boy's Sparring",gender="Male", rank_label="Green, Green/Stripe, Brown",minimum_age=7, maximum_age=8, rings=[10], ranks=[constants.GREEN_BELT,constants.GREEN_STRIPE_BELT,constants.THIRD_DEGREE_BROWN_BELT,constants.SECOND_DEGREE_BROWN_BELT,constants.FIRST_DEGREE_BROWN_BELT],clean_df=clean_df)

    ###############################################################################
    # Girl's Sparring - 9-11 year olds
    #
    reports.ExcelFileOutput.writePattern1ToExcelViaQuery(filename="GirlsSparring.xlsx", division_type='Sparring', gender="Female",minimum_age=9, maximum_age=11,clean_df=clean_df)

    writeSingleSparringTreeandDivisionReport(event_time="10:30am",division_name="Girl's Sparring",gender="Female", rank_label="White, Yellow, Orange",     minimum_age=9, maximum_age=11, rings=[11], ranks=[constants.WHITE_BELT,constants.YELLOW_BELT,constants.ORANGE_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="10:30am",division_name="Girl's Sparring",gender="Female", rank_label="Purple, Blue, Blue/Stripe", minimum_age=9, maximum_age=11, rings=[12], ranks=[constants.PURPLE_BELT,constants.BLUE_BELT,constants.BLUE_STRIPE_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="10:30am",division_name="Girl's Sparring",gender="Female", rank_label="Green, Green/Stripe, Brown",minimum_age=9, maximum_age=11, rings=[13], ranks=[constants.GREEN_BELT,constants.GREEN_STRIPE_BELT,constants.THIRD_DEGREE_BROWN_BELT,constants.SECOND_DEGREE_BROWN_BELT,constants.FIRST_DEGREE_BROWN_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="10:30am",division_name="Girl's Sparring",gender="Female", rank_label="Jr. Black",                 minimum_age=9, maximum_age=11, rings=[14], ranks=[constants.JUNIOR_BLACK_BELT,constants.FIRST_DEGREE_BLACK_BELT,constants.SECOND_DEGREE_BLACK_BELT,constants.THIRD_DEGREE_BLACK_BELT,constants.FOURTH_DEGREE_BLACK_BELT,constants.FIFTH_DEGREE_BLACK_BELT],clean_df=clean_df)

    ### 11:15 Events

    ###############################################################################
    # Boy's Sparring - 9-11 year olds
    #
    reports.ExcelFileOutput.writePattern6ToExcelViaQuery(filename="BoysSparring.xlsx", division_type='Sparring', gender="Male",minimum_age=9, maximum_age=11,clean_df=clean_df)

    writeSingleSparringTreeandDivisionReport(event_time="11:15am",division_name="Boy's Sparring",gender="Male", rank_label="White, Yellow",             minimum_age=9, maximum_age=11, rings=[1], ranks=[constants.WHITE_BELT,constants.YELLOW_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="11:15am",division_name="Boy's Sparring",gender="Male", rank_label="Orange",                    minimum_age=9, maximum_age=11, rings=[2], ranks=[constants.ORANGE_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="11:15am",division_name="Boy's Sparring",gender="Male", rank_label="Purple",                    minimum_age=9, maximum_age=11, rings=[3], ranks=[constants.PURPLE_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="11:15am",division_name="Boy's Sparring",gender="Male", rank_label="Blue, Blue/Stripe",         minimum_age=9, maximum_age=11, rings=[4,5], ranks=[constants.BLUE_BELT,constants.BLUE_STRIPE_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="11:15am",division_name="Boy's Sparring",gender="Male", rank_label="Green, Green/Stripe",       minimum_age=9, maximum_age=11, rings=[21], ranks=[constants.GREEN_BELT,constants.GREEN_STRIPE_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="11:15am",division_name="Boy's Sparring",gender="Male", rank_label="Brown",                     minimum_age=9, maximum_age=11, rings=[22], ranks=[constants.THIRD_DEGREE_BROWN_BELT,constants.SECOND_DEGREE_BROWN_BELT,constants.FIRST_DEGREE_BROWN_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="11:15am",division_name="Boy's Sparring",gender="Male", rank_label="Jr. Black",                 minimum_age=9, maximum_age=11, rings=[23], ranks=[constants.JUNIOR_BLACK_BELT,constants.FIRST_DEGREE_BLACK_BELT,constants.SECOND_DEGREE_BLACK_BELT,constants.THIRD_DEGREE_BLACK_BELT,constants.FOURTH_DEGREE_BLACK_BELT,constants.FIFTH_DEGREE_BLACK_BELT],clean_df=clean_df)

    ###############################################################################
    # Weapons Division 1 - 4-8 year olds
    #
    reports.ExcelFileOutput.writeWeaponsDivision1ToExcelViaQuery(filename="WeaponsDivision1.xlsx", division_type='Weapons', gender="*", minimum_age=4, maximum_age=8, clean_df=clean_df)
    writeWeaponsDivisionToSingleKataScoreSheetandDivisionReport(event_time="11:15am",division_name="Weapons Division 1",gender="*", rank_label="White to Jr. Back", minimum_age=4, maximum_age=8, rings=['*TBA'],
                                               ranks=[constants.WHITE_BELT,constants.YELLOW_BELT,constants.ORANGE_BELT,constants.PURPLE_BELT,
                                                      constants.BLUE_BELT,constants.BLUE_STRIPE_BELT,
                                                      constants.GREEN_BELT,constants.GREEN_STRIPE_BELT,
                                                      constants.THIRD_DEGREE_BROWN_BELT,constants.SECOND_DEGREE_BROWN_BELT,constants.FIRST_DEGREE_BROWN_BELT,
                                                      constants.JUNIOR_BLACK_BELT],
                                               clean_df= clean_df)


    ###############################################################################
    # Weapons Division 2 - 9-11 year olds White - Blue W/Green Stripe
    #
    reports.ExcelFileOutput.writeWeaponsDivision2ToExcelViaQuery(filename="WeaponsDivision2.xlsx", division_type='Weapons', gender="*", minimum_age=9, maximum_age=11, clean_df=clean_df)
    writeWeaponsDivisionToSingleKataScoreSheetandDivisionReport(event_time="11:15am",division_name="Weapons Division 2-new",gender="*", rank_label="White to Blue w/Green Stripe", minimum_age=9, maximum_age=11, rings=['*TBA'],
                                                                ranks=[constants.WHITE_BELT,constants.YELLOW_BELT,
                                                                       constants.ORANGE_BELT,constants.PURPLE_BELT,
                                                                       constants.BLUE_BELT,constants.BLUE_STRIPE_BELT],
                                                                clean_df= clean_df)


    ###############################################################################
    #  WeaponsDivision3  - 9-11 year olds Green - Jr. Black
    #
    reports.ExcelFileOutput.writeWeaponsDivision3ToExcelViaQuery(filename="WeaponsDivision3.xlsx", division_type='Weapons', gender="*", minimum_age=9, maximum_age=11, clean_df=clean_df)
    writeWeaponsDivisionToSingleKataScoreSheetandDivisionReport(event_time="11:15am",division_name="Weapons Division 3-new",gender="*", rank_label="Green - Jr. Black", minimum_age=9, maximum_age=11, rings=['*TBA'],
                                                                ranks=[constants.GREEN_BELT,
                                                                       constants.GREEN_STRIPE_BELT,
                                                                       constants.THIRD_DEGREE_BROWN_BELT,
                                                                       constants.SECOND_DEGREE_BROWN_BELT,
                                                                       constants.FIRST_DEGREE_BROWN_BELT,
                                                                       constants.JUNIOR_BLACK_BELT],
                                               clean_df= clean_df)




    ### 1:30 Events

    ###############################################################################
    # Men And Women's Kata - 18-39 year olds
    #
    reports.ExcelFileOutput.writePattern6ToExcelViaQuery(filename="MenAndWomensKata.xlsx", division_type='Forms', gender="*",minimum_age=18, maximum_age=39,clean_df=clean_df)

    writeSingleKataScoreSheetandDivisionReport(event_time="1:30pm",division_name="Men's & Women's Kata",gender="*", rank_label="White, Yellow",         minimum_age=18, maximum_age=39, rings=[1], ranks=[constants.WHITE_BELT,constants.YELLOW_BELT], clean_df=clean_df)
    writeSingleKataScoreSheetandDivisionReport(event_time="1:30pm",division_name="Men's & Women's Kata",gender="*", rank_label="Orange",                minimum_age=18, maximum_age=39, rings=[2], ranks=[constants.ORANGE_BELT], clean_df=clean_df)
    writeSingleKataScoreSheetandDivisionReport(event_time="1:30pm",division_name="Men's & Women's Kata",gender="*", rank_label="Purple",                minimum_age=18, maximum_age=39, rings=[3], ranks=[constants.PURPLE_BELT], clean_df=clean_df)
    writeSingleKataScoreSheetandDivisionReport(event_time="1:30pm",division_name="Men's & Women's Kata",gender="*", rank_label="Blue, Blue w/Stripe",   minimum_age=18, maximum_age=39, rings=[4], ranks=[constants.BLUE_BELT,constants.BLUE_STRIPE_BELT], clean_df=clean_df)
    writeSingleKataScoreSheetandDivisionReport(event_time="1:30pm",division_name="Men's & Women's Kata",gender="*", rank_label="Green, Green w/Stripe", minimum_age=18, maximum_age=39, rings=[5], ranks=[constants.GREEN_BELT,constants.GREEN_STRIPE_BELT], clean_df=clean_df)
    writeSingleKataScoreSheetandDivisionReport(event_time="1:30pm",division_name="Men's & Women's Kata",gender="*", rank_label="Brown",                 minimum_age=18, maximum_age=39, rings=[6], ranks=[constants.THIRD_DEGREE_BROWN_BELT,constants.SECOND_DEGREE_BROWN_BELT,constants.FIRST_DEGREE_BROWN_BELT], clean_df=clean_df)
    writeSingleKataScoreSheetandDivisionReport(event_time="1:30pm",division_name="Men's & Women's Kata",gender="*", rank_label="Black",                 minimum_age=18, maximum_age=39, rings=[7], ranks=[constants.FIRST_DEGREE_BLACK_BELT,constants.SECOND_DEGREE_BLACK_BELT, constants.THIRD_DEGREE_BLACK_BELT,constants.FOURTH_DEGREE_BLACK_BELT,constants.FIFTH_DEGREE_BLACK_BELT,constants.JUNIOR_BLACK_BELT], clean_df=clean_df)


    ###############################################################################
    # Teen Kata - 12-14 year olds
    #
    reports.ExcelFileOutput.writePattern6ToExcelViaQuery(filename="TeenKata.xlsx", division_type='Forms', gender="*",minimum_age=12, maximum_age=14,clean_df=clean_df)

    writeSingleKataScoreSheetandDivisionReport(event_time="1:30pm",division_name="Teen Kata",gender="*", rank_label="White, Yellow",         minimum_age=12, maximum_age=14, rings=[8],     ranks=[constants.WHITE_BELT,constants.YELLOW_BELT], clean_df=clean_df)
    writeSingleKataScoreSheetandDivisionReport(event_time="1:30pm",division_name="Teen Kata",gender="*", rank_label="Orange",                minimum_age=12, maximum_age=14, rings=[9],     ranks=[constants.ORANGE_BELT], clean_df=clean_df)
    writeSingleKataScoreSheetandDivisionReport(event_time="1:30pm",division_name="Teen Kata",gender="*", rank_label="Purple",                minimum_age=12, maximum_age=14, rings=[10],    ranks=[constants.PURPLE_BELT], clean_df=clean_df)
    writeSingleKataScoreSheetandDivisionReport(event_time="1:30pm",division_name="Teen Kata",gender="*", rank_label="Blue, Blue w/Stripe",   minimum_age=12, maximum_age=14, rings=[11,12], ranks=[constants.BLUE_BELT,constants.BLUE_STRIPE_BELT], clean_df=clean_df)
    writeSingleKataScoreSheetandDivisionReport(event_time="1:30pm",division_name="Teen Kata",gender="*", rank_label="Green, Green w/Stripe", minimum_age=12, maximum_age=14, rings=[13,14], ranks=[constants.GREEN_BELT,constants.GREEN_STRIPE_BELT], clean_df=clean_df)
    writeSingleKataScoreSheetandDivisionReport(event_time="1:30pm",division_name="Teen Kata",gender="*", rank_label="Brown",                 minimum_age=12, maximum_age=14, rings=[15],    ranks=[constants.THIRD_DEGREE_BROWN_BELT,constants.SECOND_DEGREE_BROWN_BELT,constants.FIRST_DEGREE_BROWN_BELT], clean_df=clean_df)
    writeSingleKataScoreSheetandDivisionReport(event_time="1:30pm",division_name="Teen Kata",gender="*", rank_label="Jr. Black",             minimum_age=12, maximum_age=14, rings=[16],    ranks=[constants.FIRST_DEGREE_BLACK_BELT,constants.SECOND_DEGREE_BLACK_BELT, constants.THIRD_DEGREE_BLACK_BELT,constants.FOURTH_DEGREE_BLACK_BELT,constants.FIFTH_DEGREE_BLACK_BELT,constants.JUNIOR_BLACK_BELT], clean_df=clean_df)

    ### 2:15 Events

    ###############################################################################
    # Senior Men's Sparring - 40+ year olds
    #
    reports.ExcelFileOutput.writePattern1ToExcelViaQuery(filename="SeniorMensSparring.xlsx", division_type='Sparring', gender="Male",minimum_age=40, maximum_age=constants.AGELESS,clean_df=clean_df)

    writeSingleSparringTreeandDivisionReport(event_time="2:15pm",division_name="Sr. Men's Sparring",gender="Male", rank_label="White, Yellow, Orange",     minimum_age=40, maximum_age=constants.AGELESS, rings=[1], ranks=[constants.WHITE_BELT,constants.YELLOW_BELT,constants.ORANGE_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="2:15pm",division_name="Sr. Men's Sparring",gender="Male", rank_label="Purple, Blue, Blue/Stripe", minimum_age=40, maximum_age=constants.AGELESS, rings=[2], ranks=[constants.PURPLE_BELT,constants.BLUE_BELT,constants.BLUE_STRIPE_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="2:15pm",division_name="Sr. Men's Sparring",gender="Male", rank_label="Green, Green/Stripe, Brown",minimum_age=40, maximum_age=constants.AGELESS, rings=[3], ranks=[constants.GREEN_BELT,constants.GREEN_STRIPE_BELT,constants.THIRD_DEGREE_BROWN_BELT,constants.SECOND_DEGREE_BROWN_BELT,constants.FIRST_DEGREE_BROWN_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="2:15pm",division_name="Sr. Men's Sparring",gender="Male", rank_label="Black",                     minimum_age=40, maximum_age=constants.AGELESS, rings=[4], ranks=[constants.JUNIOR_BLACK_BELT,constants.FIRST_DEGREE_BLACK_BELT,constants.SECOND_DEGREE_BLACK_BELT,constants.THIRD_DEGREE_BLACK_BELT,constants.FOURTH_DEGREE_BLACK_BELT,constants.FIFTH_DEGREE_BLACK_BELT],clean_df=clean_df)

    ###############################################################################
    # Senior Women's Sparring - 40+ year olds
    #
    reports.ExcelFileOutput.writePattern1ToExcelViaQuery(filename="SeniorWomensSparring.xlsx", division_type='Sparring', gender="Female",minimum_age=40, maximum_age=constants.AGELESS,clean_df=clean_df)

    writeSingleSparringTreeandDivisionReport(event_time="2:15pm",division_name="Sr. Women's Sparring",gender="Female", rank_label="White, Yellow, Orange",     minimum_age=40, maximum_age=constants.AGELESS, rings=[5], ranks=[constants.WHITE_BELT,constants.YELLOW_BELT,constants.ORANGE_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="2:15pm",division_name="Sr. Women's Sparring",gender="Female", rank_label="Purple, Blue, Blue/Stripe", minimum_age=40, maximum_age=constants.AGELESS, rings=[6], ranks=[constants.PURPLE_BELT,constants.BLUE_BELT,constants.BLUE_STRIPE_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="2:15pm",division_name="Sr. Women's Sparring",gender="Female", rank_label="Green, Green/Stripe, Brown",minimum_age=40, maximum_age=constants.AGELESS, rings=[7], ranks=[constants.GREEN_BELT,constants.GREEN_STRIPE_BELT,constants.THIRD_DEGREE_BROWN_BELT,constants.SECOND_DEGREE_BROWN_BELT,constants.FIRST_DEGREE_BROWN_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="2:15pm",division_name="Sr. Women's Sparring",gender="Female", rank_label="Black",                     minimum_age=40, maximum_age=constants.AGELESS, rings=[8], ranks=[constants.JUNIOR_BLACK_BELT,constants.FIRST_DEGREE_BLACK_BELT,constants.SECOND_DEGREE_BLACK_BELT,constants.THIRD_DEGREE_BLACK_BELT,constants.FOURTH_DEGREE_BLACK_BELT,constants.FIFTH_DEGREE_BLACK_BELT],clean_df=clean_df)

    ###############################################################################
    # Young Adult Kata - 15-17 year olds
    #
    reports.ExcelFileOutput.writePattern1ToExcelViaQuery(filename="YoungAdultKata.xlsx", division_type='Forms', gender="*",minimum_age=15, maximum_age=17,clean_df=clean_df)

    writeSingleKataScoreSheetandDivisionReport(event_time="2:15pm",division_name="Young Adult Kata",gender="*",rank_label="White,Yellow,Orange",       minimum_age=15, maximum_age=17, rings=[9],  ranks=[constants.WHITE_BELT,constants.YELLOW_BELT,constants.ORANGE_BELT], clean_df=clean_df)
    writeSingleKataScoreSheetandDivisionReport(event_time="2:15pm",division_name="Young Adult Kata",gender="*",rank_label="Purple, Blue, Blue/Stripe", minimum_age=15, maximum_age=17, rings=[10], ranks=[constants.PURPLE_BELT,constants.BLUE_BELT,constants.BLUE_STRIPE_BELT], clean_df=clean_df)
    writeSingleKataScoreSheetandDivisionReport(event_time="2:15pm",division_name="Young Adult Kata",gender="*",rank_label="Green, Green/Stripe, Brown",minimum_age=15, maximum_age=17, rings=[11], ranks=[constants.GREEN_BELT,constants.GREEN_STRIPE_BELT,constants.THIRD_DEGREE_BROWN_BELT,constants.SECOND_DEGREE_BROWN_BELT,constants.FIRST_DEGREE_BROWN_BELT], clean_df=clean_df)
    writeSingleKataScoreSheetandDivisionReport(event_time="2:15pm",division_name="Young Adult Kata",gender="*",rank_label="Jr. Black & Black",         minimum_age=15, maximum_age=17, rings=[12], ranks=[constants.FIRST_DEGREE_BLACK_BELT,constants.SECOND_DEGREE_BLACK_BELT, constants.THIRD_DEGREE_BLACK_BELT,constants.FOURTH_DEGREE_BLACK_BELT,constants.FIFTH_DEGREE_BLACK_BELT,constants.JUNIOR_BLACK_BELT], clean_df=clean_df)


    ###############################################################################
    # Teen Girl's Sparring - 12-14 year olds
    #
    reports.ExcelFileOutput.writePattern1ToExcelViaQuery(filename="TeenGirlSparring.xlsx", division_type='Sparring', gender="Female",minimum_age=12, maximum_age=14,clean_df=clean_df)

    writeSingleSparringTreeandDivisionReport(event_time="2:15pm",division_name="Teen Girl's Sparring",gender="Female", rank_label="White, Yellow, Orange",     minimum_age=12, maximum_age=14, rings=[13], ranks=[constants.WHITE_BELT,constants.YELLOW_BELT,constants.ORANGE_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="2:15pm",division_name="Teen Girl's Sparring",gender="Female", rank_label="Purple, Blue, Blue/Stripe", minimum_age=12, maximum_age=14, rings=[14], ranks=[constants.PURPLE_BELT,constants.BLUE_BELT,constants.BLUE_STRIPE_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="2:15pm",division_name="Teen Girl's Sparring",gender="Female", rank_label="Green, Green/Stripe, Brown",minimum_age=12, maximum_age=14, rings=[15], ranks=[constants.GREEN_BELT,constants.GREEN_STRIPE_BELT,constants.THIRD_DEGREE_BROWN_BELT,constants.SECOND_DEGREE_BROWN_BELT,constants.FIRST_DEGREE_BROWN_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="2:15pm",division_name="Teen Girl's Sparring",gender="Female", rank_label="Jr. Black",                 minimum_age=12, maximum_age=14, rings=[16], ranks=[constants.JUNIOR_BLACK_BELT,constants.FIRST_DEGREE_BLACK_BELT,constants.SECOND_DEGREE_BLACK_BELT,constants.THIRD_DEGREE_BLACK_BELT,constants.FOURTH_DEGREE_BLACK_BELT,constants.FIFTH_DEGREE_BLACK_BELT],clean_df=clean_df)


    ### 3:00 Events

    ###############################################################################
    #  Men's Sparring - 18-39 year olds
    #
    reports.ExcelFileOutput.writePattern1ToExcelViaQuery(filename="MensSparring.xlsx", division_type='Sparring', gender="Male",minimum_age=18, maximum_age=39,clean_df=clean_df)

    writeSingleSparringTreeandDivisionReport(event_time="3:00pm",division_name="Men's Sparring",gender="Male", rank_label="White, Yellow, Orange",     minimum_age=18, maximum_age=39, rings=[1], ranks=[constants.WHITE_BELT,constants.YELLOW_BELT,constants.ORANGE_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="3:00pm",division_name="Men's Sparring",gender="Male", rank_label="Purple, Blue, Blue/Stripe", minimum_age=18, maximum_age=39, rings=[2], ranks=[constants.PURPLE_BELT,constants.BLUE_BELT,constants.BLUE_STRIPE_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="3:00pm",division_name="Men's Sparring",gender="Male", rank_label="Green, Green/Stripe, Brown",minimum_age=18, maximum_age=39, rings=[3], ranks=[constants.GREEN_BELT,constants.GREEN_STRIPE_BELT,constants.THIRD_DEGREE_BROWN_BELT,constants.SECOND_DEGREE_BROWN_BELT,constants.FIRST_DEGREE_BROWN_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="3:00pm",division_name="Men's Sparring",gender="Male", rank_label="Black",                     minimum_age=18, maximum_age=39, rings=[4], ranks=[constants.JUNIOR_BLACK_BELT,constants.FIRST_DEGREE_BLACK_BELT,constants.SECOND_DEGREE_BLACK_BELT,constants.THIRD_DEGREE_BLACK_BELT,constants.FOURTH_DEGREE_BLACK_BELT,constants.FIFTH_DEGREE_BLACK_BELT],clean_df=clean_df)

    ###############################################################################
    #  Teen Boy's Sparring - 12-14 year olds
    #
    reports.ExcelFileOutput.writePattern2ToExcelViaQuery(filename="TeenBoysSparring.xlsx", division_type='Sparring', gender="Male",minimum_age=12, maximum_age=14,clean_df=clean_df)

    writeSingleSparringTreeandDivisionReport(event_time="3:00pm",division_name="Teen Boy's Sparring",gender="Male", rank_label="White, Yellow, Orange",      minimum_age=12, maximum_age=14, rings=[5], ranks=[constants.WHITE_BELT,constants.YELLOW_BELT,constants.ORANGE_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="3:00pm",division_name="Teen Boy's Sparring",gender="Male", rank_label="Purple, Blue, Blue/Stripe",  minimum_age=12, maximum_age=14, rings=[6], ranks=[constants.PURPLE_BELT,constants.BLUE_BELT,constants.BLUE_STRIPE_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="3:00pm",division_name="Teen Boy's Sparring",gender="Male", rank_label="Green, Green/Stripe",        minimum_age=12, maximum_age=14, rings=[7], ranks=[constants.GREEN_BELT,constants.GREEN_STRIPE_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="3:00pm",division_name="Teen Boy's Sparring",gender="Male", rank_label="Brown",                      minimum_age=12, maximum_age=14, rings=[8], ranks=[constants.THIRD_DEGREE_BROWN_BELT,constants.SECOND_DEGREE_BROWN_BELT,constants.FIRST_DEGREE_BROWN_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="3:00pm",division_name="Teen Boy's Sparring",gender="Male", rank_label="Jr. Black",                  minimum_age=12, maximum_age=14, rings=[9], ranks=[constants.JUNIOR_BLACK_BELT,constants.FIRST_DEGREE_BLACK_BELT,constants.SECOND_DEGREE_BLACK_BELT,constants.THIRD_DEGREE_BLACK_BELT,constants.FOURTH_DEGREE_BLACK_BELT,constants.FIFTH_DEGREE_BLACK_BELT],clean_df=clean_df)

    ###############################################################################
    #  Young Adult Men's Sparring - 15-17 year olds
    #
    reports.ExcelFileOutput.writePattern2ToExcelViaQuery(filename="YoungAdultMensSparring.xlsx", division_type='Sparring', gender="Male",minimum_age=15, maximum_age=17,clean_df=clean_df)

    writeSingleSparringTreeandDivisionReport(event_time="3:00pm",division_name="Young Adult Men's Sparring",gender="Male", rank_label="White, Yellow, Orange",     minimum_age=15, maximum_age=17, rings=[10], ranks=[constants.WHITE_BELT,constants.YELLOW_BELT,constants.ORANGE_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="3:00pm",division_name="Young Adult Men's Sparring",gender="Male", rank_label="Purple, Blue, Blue/Stripe", minimum_age=15, maximum_age=17, rings=[11], ranks=[constants.PURPLE_BELT,constants.BLUE_BELT,constants.BLUE_STRIPE_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="3:00pm",division_name="Young Adult Men's Sparring",gender="Male", rank_label="Green, Green/Stripe",       minimum_age=15, maximum_age=17, rings=[12], ranks=[constants.GREEN_BELT,constants.GREEN_STRIPE_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="3:00pm",division_name="Young Adult Men's Sparring",gender="Male", rank_label="Brown",                     minimum_age=15, maximum_age=17, rings=[13], ranks=[constants.THIRD_DEGREE_BROWN_BELT,constants.SECOND_DEGREE_BROWN_BELT,constants.FIRST_DEGREE_BROWN_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="3:00pm",division_name="Young Adult Men's Sparring",gender="Male", rank_label="Jr. Black & Black",         minimum_age=15, maximum_age=17, rings=[14], ranks=[constants.JUNIOR_BLACK_BELT,constants.FIRST_DEGREE_BLACK_BELT,constants.SECOND_DEGREE_BLACK_BELT,constants.THIRD_DEGREE_BLACK_BELT,constants.FOURTH_DEGREE_BLACK_BELT,constants.FIFTH_DEGREE_BLACK_BELT],clean_df=clean_df)


    ###############################################################################
    #  Women's Sparring - 18-39 year olds
    #
    reports.ExcelFileOutput.writePattern1ToExcelViaQuery(filename="WomensSparring.xlsx", division_type='Sparring', gender="Female",minimum_age=18, maximum_age=39,clean_df=clean_df)

    writeSingleSparringTreeandDivisionReport(event_time="3:00pm",division_name="Women's Sparring",gender="Female", rank_label="White, Yellow, Orange",     minimum_age=18, maximum_age=39, rings=[15], ranks=[constants.WHITE_BELT,constants.YELLOW_BELT,constants.ORANGE_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="3:00pm",division_name="Women's Sparring",gender="Female", rank_label="Purple, Blue, Blue/Stripe", minimum_age=18, maximum_age=39, rings=[16], ranks=[constants.PURPLE_BELT,constants.BLUE_BELT,constants.BLUE_STRIPE_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="3:00pm",division_name="Women's Sparring",gender="Female", rank_label="Green, Green/Stripe, Brown",minimum_age=18, maximum_age=39, rings=[17], ranks=[constants.GREEN_BELT,constants.GREEN_STRIPE_BELT,constants.THIRD_DEGREE_BROWN_BELT,constants.SECOND_DEGREE_BROWN_BELT,constants.FIRST_DEGREE_BROWN_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="3:00pm",division_name="Women's Sparring",gender="Female", rank_label="Black",                     minimum_age=18, maximum_age=39, rings=[18], ranks=[constants.JUNIOR_BLACK_BELT,constants.FIRST_DEGREE_BLACK_BELT,constants.SECOND_DEGREE_BLACK_BELT,constants.THIRD_DEGREE_BLACK_BELT,constants.FOURTH_DEGREE_BLACK_BELT,constants.FIFTH_DEGREE_BLACK_BELT],clean_df=clean_df)


    ### 3:45 Events

    ###############################################################################
    # Senior Kata - 40+ year olds
    #
    reports.ExcelFileOutput.writePattern6ToExcelViaQuery(filename="SeniorKata.xlsx", division_type='Forms', gender="*",minimum_age=40, maximum_age=constants.AGELESS,clean_df=clean_df)

    writeSingleKataScoreSheetandDivisionReport(event_time="3:45pm",division_name="Senior Kata",gender="*", rank_label="White, Yellow",         minimum_age=40, maximum_age=constants.AGELESS, rings=[1], ranks=[constants.WHITE_BELT,constants.YELLOW_BELT], clean_df=clean_df)
    writeSingleKataScoreSheetandDivisionReport(event_time="3:45pm",division_name="Senior Kata",gender="*", rank_label="Orange",                minimum_age=40, maximum_age=constants.AGELESS, rings=[2], ranks=[constants.ORANGE_BELT], clean_df=clean_df)
    writeSingleKataScoreSheetandDivisionReport(event_time="3:45pm",division_name="Senior Kata",gender="*", rank_label="Purple",                minimum_age=40, maximum_age=constants.AGELESS, rings=[3], ranks=[constants.PURPLE_BELT], clean_df=clean_df)
    writeSingleKataScoreSheetandDivisionReport(event_time="3:45pm",division_name="Senior Kata",gender="*", rank_label="Blue, Blue w/Stripe",   minimum_age=40, maximum_age=constants.AGELESS, rings=[4], ranks=[constants.BLUE_BELT,constants.BLUE_STRIPE_BELT], clean_df=clean_df)
    writeSingleKataScoreSheetandDivisionReport(event_time="3:45pm",division_name="Senior Kata",gender="*", rank_label="Green, Green w/Stripe", minimum_age=40, maximum_age=constants.AGELESS, rings=[5], ranks=[constants.GREEN_BELT,constants.GREEN_STRIPE_BELT], clean_df=clean_df)
    writeSingleKataScoreSheetandDivisionReport(event_time="3:45pm",division_name="Senior Kata",gender="*", rank_label="Brown",                 minimum_age=40, maximum_age=constants.AGELESS, rings=[6], ranks=[constants.THIRD_DEGREE_BROWN_BELT,constants.SECOND_DEGREE_BROWN_BELT,constants.FIRST_DEGREE_BROWN_BELT], clean_df=clean_df)
    writeSingleKataScoreSheetandDivisionReport(event_time="3:45pm",division_name="Senior Kata",gender="*", rank_label="Black",                 minimum_age=40, maximum_age=constants.AGELESS, rings=[7], ranks=[constants.FIRST_DEGREE_BLACK_BELT,constants.SECOND_DEGREE_BLACK_BELT, constants.THIRD_DEGREE_BLACK_BELT,constants.FOURTH_DEGREE_BLACK_BELT,constants.FIFTH_DEGREE_BLACK_BELT,constants.JUNIOR_BLACK_BELT], clean_df=clean_df)



    ###############################################################################
    #  Young Adult Women's Sparring - 15-17 year olds
    #
    reports.ExcelFileOutput.writePattern1ToExcelViaQuery(filename="YoungAdultWomensSparring.xlsx", division_type='Sparring', gender="Female",minimum_age=15, maximum_age=17,clean_df=clean_df)

    writeSingleSparringTreeandDivisionReport(event_time="3:45pm",division_name="Young Adult Women's Sparring",gender="Female", rank_label="White, Yellow, Orange",     minimum_age=15, maximum_age=17, rings=[8], ranks=[constants.WHITE_BELT,constants.YELLOW_BELT,constants.ORANGE_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="3:45pm",division_name="Young Adult Women's Sparring",gender="Female", rank_label="Purple, Blue, Blue/Stripe", minimum_age=15, maximum_age=17, rings=[9], ranks=[constants.PURPLE_BELT,constants.BLUE_BELT,constants.BLUE_STRIPE_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="3:45pm",division_name="Young Adult Women's Sparring",gender="Female", rank_label="Green, Green/Stripe, Brown",minimum_age=15, maximum_age=17, rings=[10], ranks=[constants.GREEN_BELT,constants.GREEN_STRIPE_BELT,constants.THIRD_DEGREE_BROWN_BELT,constants.SECOND_DEGREE_BROWN_BELT,constants.FIRST_DEGREE_BROWN_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="3:45pm",division_name="Young Adult Women's Sparring",gender="Female", rank_label="Jr. Black & Black",         minimum_age=15, maximum_age=17, rings=[11], ranks=[constants.JUNIOR_BLACK_BELT,constants.FIRST_DEGREE_BLACK_BELT,constants.SECOND_DEGREE_BLACK_BELT,constants.THIRD_DEGREE_BLACK_BELT,constants.FOURTH_DEGREE_BLACK_BELT,constants.FIFTH_DEGREE_BLACK_BELT],clean_df=clean_df)


    ### 4:15 Events

    ###############################################################################
    #  WeaponsDivision4 12-17 White-Blue Stripe year olds
    #
    reports.ExcelFileOutput.writeWeaponsDivision4ToExcelViaQuery(filename="WeaponsDivision4.xlsx", division_type='Weapons', gender="*", minimum_age=12, maximum_age=17, clean_df=clean_df)
    writeWeaponsDivisionToSingleKataScoreSheetandDivisionReport(event_time="4:15pm",
                                                                division_name="Weapons Division 4-new",
                                                                gender="*",
                                                                rank_label="White - Blue w/Green Stripe",
                                                                minimum_age=12, maximum_age=17,
                                                                rings=['*TBA'],
                                                                ranks=[constants.WHITE_BELT,constants.YELLOW_BELT,
                                                                       constants.ORANGE_BELT,constants.PURPLE_BELT,
                                                                       constants.BLUE_BELT,constants.BLUE_STRIPE_BELT],
                                                                clean_df= clean_df)


    ###############################################################################
    #  WeaponsDivision5 18+ year olds
    #
    reports.ExcelFileOutput.writeWeaponsDivision5ToExcelViaQuery(filename="WeaponsDivision5.xlsx", division_type='Weapons', gender="*", minimum_age=18, maximum_age=constants.AGELESS, clean_df=clean_df)
    writeWeaponsDivisionToSingleKataScoreSheetandDivisionReport(event_time="4:15pm",
                                                                division_name="Weapons Division 5-new",
                                                                gender="*",
                                                                rank_label="White - Blue w/Green Stripe",
                                                                minimum_age=18, maximum_age=constants.AGELESS,
                                                                rings=['*TBA'],
                                                                ranks=[constants.WHITE_BELT,constants.YELLOW_BELT,
                                                                       constants.ORANGE_BELT,constants.PURPLE_BELT,
                                                                       constants.BLUE_BELT,constants.BLUE_STRIPE_BELT],
                                                                clean_df= clean_df)

    ###############################################################################
    #  WeaponsDivision6 12+ year olds green belts
    #
    reports.ExcelFileOutput.writeWeaponsDivision6ToExcelViaQuery(filename="WeaponsDivision6.xlsx", division_type='Weapons', gender="*", minimum_age=12, maximum_age=constants.AGELESS, clean_df=clean_df)
    writeWeaponsDivisionToSingleKataScoreSheetandDivisionReport(event_time="4:15pm",
                                                                division_name="Weapons Division 6-new",
                                                                gender="*",
                                                                rank_label="Green, Green w/Brown Stripe",
                                                                minimum_age=12,maximum_age=constants.AGELESS,
                                                                rings=['*TBA'],
                                                                ranks=[constants.GREEN_BELT,
                                                                       constants.GREEN_STRIPE_BELT],
                                                                clean_df=clean_df)

    ###############################################################################
    #  WeaponsDivision7 12+ year olds brown belts
    #
    reports.ExcelFileOutput.writeWeaponsDivision7ToExcelViaQuery(filename="WeaponsDivision7.xlsx", division_type='Weapons', gender="*", minimum_age=12, maximum_age=constants.AGELESS, clean_df=clean_df)
    writeWeaponsDivisionToSingleKataScoreSheetandDivisionReport(event_time="4:15pm",
                                                                division_name="Weapons Division 7-new",
                                                                gender="*",
                                                                rank_label="Brown",
                                                                minimum_age=12,maximum_age=constants.AGELESS,
                                                                rings=['*TBA'],
                                                                ranks=[constants.THIRD_DEGREE_BROWN_BELT,
                                                                       constants.SECOND_DEGREE_BROWN_BELT,
                                                                       constants.FIRST_DEGREE_BROWN_BELT],
                                                                clean_df=clean_df)

    ###############################################################################
    #  WeaponsDivision8 12+ Black
    #
    reports.ExcelFileOutput.writeWeaponsDivision8ToExcelViaQuery(filename="WeaponsDivision8.xlsx", division_type='Weapons', gender="*", minimum_age=12, maximum_age=17, clean_df=clean_df)
    writeWeaponsDivisionToSingleKataScoreSheetandDivisionReport(event_time="4:15pm",
                                                                division_name="Weapons Division 8-new",
                                                                gender="*",
                                                                rank_label="Jr. Back & Black",
                                                                minimum_age=12,maximum_age=17,
                                                                rings=['*TBA'],
                                                                ranks=[constants.JUNIOR_BLACK_BELT,
                                                                       constants.FIRST_DEGREE_BLACK_BELT,constants.SECOND_DEGREE_BLACK_BELT,constants.THIRD_DEGREE_BLACK_BELT,constants.FOURTH_DEGREE_BLACK_BELT,constants.FIFTH_DEGREE_BLACK_BELT],
                                                                clean_df=clean_df)

    ###############################################################################
    #  WeaponsDivision9 18+ year olds
    #
    reports.ExcelFileOutput.writeWeaponsDivision9ToExcelViaQuery(filename="WeaponsDivision9.xlsx", division_type='Weapons', gender="*", minimum_age=18, maximum_age=constants.AGELESS, clean_df=clean_df)
    writeWeaponsDivisionToSingleKataScoreSheetandDivisionReport(event_time="4:15pm",
                                                                division_name="Weapons Division 9-new",
                                                                gender="*",
                                                                rank_label="Black",
                                                                minimum_age=18,maximum_age=constants.AGELESS,
                                                                rings=['*TBA'],
                                                                ranks=[constants.JUNIOR_BLACK_BELT,constants.FIRST_DEGREE_BLACK_BELT,constants.SECOND_DEGREE_BLACK_BELT,constants.THIRD_DEGREE_BLACK_BELT,constants.FOURTH_DEGREE_BLACK_BELT,constants.FIFTH_DEGREE_BLACK_BELT],
                                                                clean_df=clean_df)

logging.info("Saving PDFs to disk")
divison_detail_report_pdf.write_pdfpage()
kata_score_sheet.write_pdfpage()
sparing_tree_pdf.close()

#print hitcount warnings
if clean_df.shape[0] > 30:
    logging.warning("\u001b[31mInvestigate these entries in the spreadsheet!  They didn't get put into any events:\u001b[0m")
    for index, row in clean_df.iterrows():
        name = row['First_Name'] + " " + row['Last_Name']
        events = row['Events']
        hc = row['hitcount']
        if hc < 1 :
            # logging.info("  " + name + ": " + str(hc))
            logging.warning(f'\u001b[31m   Name:{name} Events:{events} <---was put in {hc} events\u001b[0m')

logging.info("Done!")
