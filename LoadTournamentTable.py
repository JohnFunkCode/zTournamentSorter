# V 04/18/2023

import os
import sys
import time
import logging
import re
import pathlib

from tkinter import Tk
from tkinter.filedialog import askopenfilename

import pandas as pd

from cleaninput import cleaninput
from cleaninput import rename_colums as RN
from cleaninput import input_errors

from reports.division_detail_report import DivisionDetailReport
from reports.kata_score_sheet import KataScoreSheet
from reports.technique_score_sheet import TechniqueScoreSheet
import reports.sparring_tree.sparring_tree_report
import reports.ExcelFileOutput
import reports.FileHandlingUtilities
import domain_model.constants as constants


class LoadTournamentTable:
    def __int__(self):
        ###############################################################################
        # Setup a few variables to hold all the reports
        self.divison_detail_report_pdf =None #= DivisionDetailReport.DivisionDetailReport()
        #self.kata_score_sheet = None #kata_score_sheet_pdf.KataScoreSheet()
        self.kata_score_sheet_pdf = None
        self.technique_score_sheet_pdf = None
        self.sparing_tree_pdf = None #reports.sparring_tree.sparring_tree_report.SparringTreeReportPDF()

    ###############################################################################
    # writeSingleKataScoreSheetandDivisionReport
    #  Provides a convenience wrapper that writes to both the division detail report and the kata score sheet in one line
    #  This prevents a lot of duplication
    def writeSingleKataScoreSheetandDivisionReport(self,event_time: str, division_name: str, gender: str, rank_label: str, minimum_age: int,maximum_age: int, rings: list, ranks: list,clean_df: pd.DataFrame):
        self.divison_detail_report_pdf.writeSingleDivisionDetailReport(event_time=event_time, division_name=division_name, division_type="Forms", gender=gender, rank_label=rank_label, minimum_age=minimum_age, maximum_age=maximum_age, rings=rings, ranks=ranks, clean_df=clean_df)
        self.kata_score_sheet_pdf.writeSingleKataScoreSheet(event_time=event_time, division_name=division_name,division_type="Forms", gender=gender,rank_label=rank_label, minimum_age=minimum_age, maximum_age=maximum_age, rings=rings,ranks=ranks, clean_df=clean_df)
    #
    # def self.writeSingleKataScoreSheetandDivisionReport(event_time: str, division_name: str, gender: str, rank_label: str, minimum_age: int,maximum_age: int, rings: list, ranks: list,clean_df: pd.DataFrame):
    #     self.divison_detail_report_pdf.writeSingleDivisionDetailReport(event_time=event_time, division_name=division_name,division_type="Forms", gender=gender,rank_label=rank_label, minimum_age=minimum_age,maximum_age=maximum_age, rings=rings,ranks=ranks,clean_df=clean_df)
    #     self.kata_score_sheet.writeSingleKataScoreSheet(event_time=event_time, division_name=division_name,division_type="Forms", gender=gender,rank_label=rank_label, minimum_age=minimum_age, maximum_age=maximum_age, rings=rings,ranks=ranks, clean_df=clean_df)
    
    ###############################################################################
    # write_single_sparring_treeShim
    #  Provides a convenience wrapper that writes to both the division detail report and the sparring tree in one line
    #  This prevents a lot of duplication
    def writeSingleSparringTreeandDivisionReport(self, event_time: str, division_name, gender: str, rank_label: str, minimum_age: int, maximum_age: int, rings: list, ranks: list, clean_df : pd.DataFrame ):
        self.divison_detail_report_pdf.writeSingleDivisionDetailReport(event_time=event_time, division_name=division_name,division_type="Sparring", gender=gender,rank_label=rank_label, minimum_age=minimum_age,maximum_age=maximum_age, rings=rings,ranks=ranks,clean_df=clean_df)
        self.sparing_tree_pdf.write_single_sparring_tree(event_time=event_time, division_name=division_name, gender=gender,rank_label=rank_label, minimum_age=minimum_age, maximum_age=maximum_age, rings=rings,ranks=ranks, clean_df=clean_df)

    ###############################################################################
    # self.writeSingleKataScoreSheetandDivisionReport
    #  Provides a convenience wrapper that writes to both the division detail report and the kata score sheet in one line
    #  This prevents a lot of duplication
    def writeWeaponsDivisionToSingleKataScoreSheetandDivisionReport(self,event_time: str, division_name: str, gender: str, rank_label: str, minimum_age: int,maximum_age: int, rings: list, ranks: list,clean_df: pd.DataFrame):
        self.divison_detail_report_pdf.writeSingleDivisionDetailReport(event_time=event_time, division_name=division_name,division_type="Weapons", gender=gender,rank_label=rank_label, minimum_age=minimum_age, maximum_age=maximum_age, rings=rings,ranks=ranks, clean_df=clean_df)
        self.kata_score_sheet_pdf.writeSingleKataScoreSheet(               event_time=event_time, division_name=division_name,division_type="Weapons", gender=gender,rank_label=rank_label, minimum_age=minimum_age, maximum_age=maximum_age, rings=rings,ranks=ranks, clean_df=clean_df)

    ###############################################################################
    # writeSingleKataScoreSheetandDivisionReport
    #  Provides a convenience wrapper that writes to both the division detail report and the kata score sheet in one line
    #  This prevents a lot of duplication
    def writeSingleTechniqueScoreSheetandDivisionReport(self,event_time: str, division_name: str, gender: str, rank_label: str, minimum_age: int,maximum_age: int, rings: list, ranks: list,clean_df: pd.DataFrame):
        self.divison_detail_report_pdf.writeSingleDivisionDetailReport(event_time=event_time, division_name=division_name, division_type="Techniques", gender=gender, rank_label=rank_label, minimum_age=minimum_age, maximum_age=maximum_age, rings=rings, ranks=ranks, clean_df=clean_df)
        self.technique_score_sheet_pdf.writeSingleTechniqueScoreSheet(event_time=event_time, division_name=division_name,division_type="Techniques", gender=gender,rank_label=rank_label, minimum_age=minimum_age, maximum_age=maximum_age, rings=rings,ranks=ranks, clean_df=clean_df)



    ###############################################################################
    #
    # process_tournament_table Function
    #
    # logging.basicConfig(format='%(asctime)s %(levelname)s - %(message)s', level=logging.INFO, datefmt='%H:%M:%S')
    def process_tournament_table(self, filename, clean_df, output_folder_path):
        # # get the filename from the environment var named  tourname_filename
        # filename = os.getenv("tournament_filename")
        #
        # if filename is None:
        #     # Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
        #     root = Tk()
        #     root.withdraw()  # we don't want a full GUI, so keep the root window from appearing
        #     root.update()  # Prevent the askfilename() window doesn't stay open
        #     filename = askopenfilename()
        #     root.update()  # Prevent the askfilename() window doesn't stay open
        # else:
        #     print("Using the file " + filename + "from the environment")
        #
        # # filename = "C:\\Users\\Maria\\Downloads\\tournamentprojectmaterial\\RegistrantExport.csv"
        # # filename = "/users/johnfunk/CloudStation/TournamentProject/Clean_RegistrantExport_EM0393_20160411140713.csv"  # For Testing on John's machine
        #
        # errorLogFileName = filename[0:len(filename) - 4] + "-Error.txt"
        #
        # logger = logging.getLogger('')
        # logger.setLevel(logging.INFO)
        # fh = logging.FileHandler(errorLogFileName)
        # sh = logging.StreamHandler(sys.stdout)
        # formatter = logging.Formatter('[%(asctime)s] %(levelname)s %(message)s', datefmt='%H:%M:%S')
        # fh.setFormatter(formatter)
        # sh.setFormatter(formatter)
        # logger.addHandler(fh)
        # logger.addHandler(sh)
        #
        # logging.info("Reading the data from:" + filename + "....")
        #
        # #### SET Encoding to UTF-8 added 3/27/2022
        # cleaninput.set_utf_encoding()
        #
        #
        #
        # cleaninput.clean_unicode_from_file(filename)
        #
        # # rename all the columns in the dataframe to usable names
        # r = RN.RenameColumns(filename)
        # r.rename_all_columns()
        # renamed_df = r.get_dataframe_copy()
        #
        # input_error_list = input_errors.InputErrors()
        # clean_df,error_count = cleaninput.clean_all_input_errors(renamed_df, input_error_list)
        # del renamed_df  # make sure we don't use the renamed_df again
        # # logging.info(f'Input Errors:{input_error_list.error_list}')
        # if error_count > 0:
        #     sys.exit("Exiting - The input must be fixed manually")
    
    # everything previous needs to go into main
    
        # create test data
        clean_df.to_pickle(output_folder_path + reports.FileHandlingUtilities.pathDelimiter() + "pickled_clean_dataframe.pkl")

        #make sure the sorted directory exists
        new_folder_path = pathlib.Path( output_folder_path + reports.FileHandlingUtilities.pathDelimiter() + 'sorted')
        expanded_folder_path = new_folder_path.expanduser()
        pathlib.Path(expanded_folder_path).mkdir(exist_ok=True, parents=True)

        # #make sure the sorted directory exists
        # try:
        #     os.mkdir("sorted")
        # except:
        #     assert(1==1)
        #     #logging.info("expected error")
        #
    
        clean_df['hitcount'] = 0  # setup a new column for hit rate.
    
        logging.info("Generating the output results...")
    
        ###############################################################################
        # Setup a few things for the Division Detail PDF report
        self.divison_detail_report_pdf = DivisionDetailReport("Division Detail",filename,output_folder_path)
        # DivisionDetailReport.DivisionDetailReport.set_title("Division Detail")
        # DivisionDetailReport.DivisionDetailReport.set_sourcefile(filename)

        ###############################################################################
        # Setup a few things for the Kata Score Sheet PDF report
        self.kata_score_sheet_pdf = KataScoreSheet("Forms", filename, output_folder_path)
        # self.kata_score_sheet_pdf.set_title("Forms")
        # self.kata_score_sheet_pdf.set_sourcefile(filename)

        ###############################################################################
        # Setup a few things for the Techniques Score Sheet PDF report
        self.technique_score_sheet_pdf = TechniqueScoreSheet("Techniques", filename, output_folder_path)
    
        ###############################################################################
        # Setup a few things for the Sparring Tree PDF report
        self.sparing_tree_pdf = reports.sparring_tree.sparring_tree_report.SparringTreeReportPDF(filename, output_folder_path)
        # self.sparing_tree_pdf.set_source_file( filename )
    
        ### Special Handling for files with less than 30 competitors- Added for Fall 2022 Tournament
        if clean_df.shape[0] < 30:
            logging.warning("\u001b[31m*** Special Handling!  Printing Just One Kata Sheet and One Sparring Tree with the small data file provided!\u001b[0m")
            #self.divison_detail_report_pdf.writeSingleDivisionDetailReport(event_time="", division_name="",division_type="Forms", gender="*", rank_label="",minimum_age=1, maximum_age=constants.AGELESS, rings=[1],ranks=[constants.WHITE_BELT,constants.YELLOW_BELT,constants.ORANGE_BELT,constants.PURPLE_BELT,constants.BLUE_BELT,constants.BLUE_STRIPE_BELT,constants.GREEN_BELT,constants.GREEN_STRIPE_BELT,constants.THIRD_DEGREE_BROWN_BELT,constants.SECOND_DEGREE_BROWN_BELT,constants.FIRST_DEGREE_BROWN_BELT,constants.FIRST_DEGREE_BLACK_BELT,constants.SECOND_DEGREE_BLACK_BELT, constants.THIRD_DEGREE_BLACK_BELT,constants.FOURTH_DEGREE_BLACK_BELT,constants.FIFTH_DEGREE_BLACK_BELT,constants.JUNIOR_BLACK_BELT], clean_df=clean_df)
            self.writeSingleKataScoreSheetandDivisionReport(               event_time="", division_name="",                       gender="*", rank_label="",minimum_age=1, maximum_age=constants.AGELESS, rings=[''],ranks=[constants.WHITE_BELT,constants.YELLOW_BELT,constants.ORANGE_BELT,constants.PURPLE_BELT,constants.BLUE_BELT,constants.BLUE_STRIPE_BELT,constants.GREEN_BELT,constants.GREEN_STRIPE_BELT,constants.THIRD_DEGREE_BROWN_BELT,constants.SECOND_DEGREE_BROWN_BELT,constants.FIRST_DEGREE_BROWN_BELT,constants.FIRST_DEGREE_BLACK_BELT,constants.SECOND_DEGREE_BLACK_BELT, constants.THIRD_DEGREE_BLACK_BELT,constants.FOURTH_DEGREE_BLACK_BELT,constants.FIFTH_DEGREE_BLACK_BELT,constants.JUNIOR_BLACK_BELT], clean_df=clean_df)
            self.writeSingleSparringTreeandDivisionReport(              event_time="", division_name="",                       gender="*", rank_label="",minimum_age=1, maximum_age=constants.AGELESS, rings=[''],ranks=[constants.WHITE_BELT,constants.YELLOW_BELT,constants.ORANGE_BELT,constants.PURPLE_BELT,constants.BLUE_BELT,constants.BLUE_STRIPE_BELT,constants.GREEN_BELT,constants.GREEN_STRIPE_BELT,constants.THIRD_DEGREE_BROWN_BELT,constants.SECOND_DEGREE_BROWN_BELT,constants.FIRST_DEGREE_BROWN_BELT,constants.FIRST_DEGREE_BLACK_BELT,constants.SECOND_DEGREE_BLACK_BELT, constants.THIRD_DEGREE_BLACK_BELT,constants.FOURTH_DEGREE_BLACK_BELT,constants.FIFTH_DEGREE_BLACK_BELT,constants.JUNIOR_BLACK_BELT], clean_df=clean_df)
        else:
    
    
            ### 9:00AM Events
    
            ###############################################################################
            # Kids Kata  - 4-6 year olds
            #
            reports.ExcelFileOutput.writePattern4ToExcelViaQuery(output_folder_path=output_folder_path, filename="KidsKata.xlsx", division_type='Forms', gender="*",minimum_age=4, maximum_age=6, clean_df=clean_df)
    
            self.writeSingleKataScoreSheetandDivisionReport(event_time="9:00am",division_name="Kids Kata",gender="*",rank_label="White",                     minimum_age=4, maximum_age=6, rings=[1],  ranks=[constants.WHITE_BELT], clean_df=clean_df)
            self.writeSingleKataScoreSheetandDivisionReport(event_time="9:00am",division_name="Kids Kata",gender="*",rank_label="Yellow",                    minimum_age=4, maximum_age=6, rings=[2,3],ranks=[constants.YELLOW_BELT], clean_df=clean_df)
            self.writeSingleKataScoreSheetandDivisionReport(event_time="9:00am",division_name="Kids Kata",gender="*",rank_label="Orange",                    minimum_age=4, maximum_age=6, rings=[4,5],ranks=[constants.ORANGE_BELT], clean_df=clean_df)
            self.writeSingleKataScoreSheetandDivisionReport(event_time="9:00am",division_name="Kids Kata",gender="*",rank_label="Purple, Blue, Blue/Stripe", minimum_age=4, maximum_age=6, rings=[6],  ranks=[constants.PURPLE_BELT,constants.BLUE_BELT,constants.BLUE_STRIPE_BELT], clean_df=clean_df)
            self.writeSingleKataScoreSheetandDivisionReport(event_time="9:00am",division_name="Kids Kata",gender="*",rank_label="Green, Green/Stripe, Brown",minimum_age=4, maximum_age=6, rings=[7],  ranks=[constants.GREEN_BELT,constants.GREEN_STRIPE_BELT,constants.THIRD_DEGREE_BROWN_BELT,constants.SECOND_DEGREE_BROWN_BELT,constants.FIRST_DEGREE_BROWN_BELT], clean_df=clean_df)
    
    
            ###############################################################################
            # Youth Kata  - 7-8 year olds
            #
            reports.ExcelFileOutput.writePattern5ToExcelViaQuery(output_folder_path=output_folder_path, filename="YouthKata.xlsx", division_type='Forms', gender="*",minimum_age=7, maximum_age=8,clean_df=clean_df)
    
            self.writeSingleKataScoreSheetandDivisionReport(event_time="9:00am",division_name="Youth Kata",gender="*",rank_label="White",                     minimum_age=7, maximum_age=8, rings=[8],    ranks=[constants.WHITE_BELT], clean_df=clean_df)
            self.writeSingleKataScoreSheetandDivisionReport(event_time="9:00am",division_name="Youth Kata",gender="*",rank_label="Yellow",                    minimum_age=7, maximum_age=8, rings=[9],    ranks=[constants.YELLOW_BELT], clean_df=clean_df)
            self.writeSingleKataScoreSheetandDivisionReport(event_time="9:00am",division_name="Youth Kata",gender="*",rank_label="Orange",                    minimum_age=7, maximum_age=8, rings=[10,11],ranks=[constants.ORANGE_BELT], clean_df=clean_df)
            self.writeSingleKataScoreSheetandDivisionReport(event_time="9:00am",division_name="Youth Kata",gender="*",rank_label="Purple",                    minimum_age=7, maximum_age=8, rings=[12,13],ranks=[constants.PURPLE_BELT], clean_df=clean_df)
            self.writeSingleKataScoreSheetandDivisionReport(event_time="9:00am",division_name="Youth Kata",gender="*",rank_label="Blue, Blue/Stripe",         minimum_age=7, maximum_age=8, rings=[14,15],ranks=[constants.BLUE_BELT,constants.BLUE_STRIPE_BELT], clean_df=clean_df)
            self.writeSingleKataScoreSheetandDivisionReport(event_time="9:00am",division_name="Youth Kata",gender="*",rank_label="Green, Green/Stripe, Brown",minimum_age=7, maximum_age=8, rings=[16],   ranks=[constants.GREEN_BELT,constants.GREEN_STRIPE_BELT,constants.THIRD_DEGREE_BROWN_BELT,constants.SECOND_DEGREE_BROWN_BELT,constants.FIRST_DEGREE_BROWN_BELT], clean_df=clean_df)
    
            ### 9:45 Events
    
            ###############################################################################
            # Kids Sparring Spreadsheet - 4-6 year olds
            #
            reports.ExcelFileOutput.writePattern4ToExcelViaQuery(output_folder_path=output_folder_path, filename="KidsSparring.xlsx", division_type='Sparring', gender="*",minimum_age=4, maximum_age=6,clean_df=clean_df)
    
            self.writeSingleSparringTreeandDivisionReport(event_time="9:45am",division_name="Kids Sparring",gender="*", rank_label="White",                     minimum_age=4, maximum_age=6, rings=[1],     ranks=[constants.WHITE_BELT],clean_df=clean_df)
            self.writeSingleSparringTreeandDivisionReport(event_time="9:45am",division_name="Kids Sparring",gender="*", rank_label="Yellow",                    minimum_age=4, maximum_age=6, rings=[2,3],  ranks=[constants.YELLOW_BELT],clean_df=clean_df)
            self.writeSingleSparringTreeandDivisionReport(event_time="9:45am",division_name="Kids Sparring",gender="*", rank_label="Orange",                    minimum_age=4, maximum_age=6, rings=[4],  ranks=[constants.ORANGE_BELT],clean_df=clean_df)
            self.writeSingleSparringTreeandDivisionReport(event_time="9:45am",division_name="Kids Sparring",gender="*", rank_label="Purple, Blue, Blue/Stripe", minimum_age=4, maximum_age=6, rings=[6],  ranks=[constants.PURPLE_BELT,constants.BLUE_BELT,constants.BLUE_STRIPE_BELT],clean_df=clean_df)
            self.writeSingleSparringTreeandDivisionReport(event_time="9:45am",division_name="Kids Sparring",gender="*", rank_label="Green, Green/Stripe, Brown", minimum_age=4, maximum_age=6, rings=[7],  ranks=[constants.GREEN_BELT,constants.GREEN_STRIPE_BELT,constants.THIRD_DEGREE_BROWN_BELT,constants.SECOND_DEGREE_BROWN_BELT,constants.FIRST_DEGREE_BROWN_BELT],clean_df=clean_df)
    
    
            ###############################################################################
            # Boy's & Girl's Kata  - 9-11 year olds
            #
            reports.ExcelFileOutput.writePattern6ToExcelViaQuery(output_folder_path=output_folder_path, filename="BoysGirlsKata.xlsx", division_type='Forms', gender="*",minimum_age=9, maximum_age=11,clean_df=clean_df)
    
            self.writeSingleKataScoreSheetandDivisionReport(event_time="9:45am",division_name="Boy's & Girl's Kata",gender="*", rank_label="White, Yellow",         minimum_age=9, maximum_age=11, rings=[8],     ranks=[constants.WHITE_BELT,constants.YELLOW_BELT], clean_df=clean_df)
            self.writeSingleKataScoreSheetandDivisionReport(event_time="9:45am",division_name="Boy's & Girl's Kata",gender="*", rank_label="Orange",                minimum_age=9, maximum_age=11, rings=[9],     ranks=[constants.ORANGE_BELT], clean_df=clean_df)
            self.writeSingleKataScoreSheetandDivisionReport(event_time="9:45am",division_name="Boy's & Girl's Kata",gender="*", rank_label="Purple",                minimum_age=9, maximum_age=11, rings=[10], ranks=[constants.PURPLE_BELT], clean_df=clean_df)
            self.writeSingleKataScoreSheetandDivisionReport(event_time="9:45am",division_name="Boy's & Girl's Kata",gender="*", rank_label="Blue, Blue w/Stripe",   minimum_age=9, maximum_age=11, rings=[13], ranks=[constants.BLUE_BELT,constants.BLUE_STRIPE_BELT], clean_df=clean_df)
            self.writeSingleKataScoreSheetandDivisionReport(event_time="9:45am",division_name="Boy's & Girl's Kata",gender="*", rank_label="Green, Green w/Stripe", minimum_age=9, maximum_age=11, rings=[15],    ranks=[constants.GREEN_BELT,constants.GREEN_STRIPE_BELT], clean_df=clean_df)
            self.writeSingleKataScoreSheetandDivisionReport(event_time="9:45am",division_name="Boy's & Girl's Kata",gender="*", rank_label="Brown",                 minimum_age=9, maximum_age=11, rings=[16],    ranks=[constants.THIRD_DEGREE_BROWN_BELT,constants.SECOND_DEGREE_BROWN_BELT,constants.FIRST_DEGREE_BROWN_BELT], clean_df=clean_df)
            self.writeSingleKataScoreSheetandDivisionReport(event_time="9:45am",division_name="Boy's & Girl's Kata",gender="*", rank_label="Jr. Black",             minimum_age=9, maximum_age=11, rings=[17],    ranks=[constants.FIRST_DEGREE_BLACK_BELT,constants.SECOND_DEGREE_BLACK_BELT, constants.THIRD_DEGREE_BLACK_BELT,constants.FOURTH_DEGREE_BLACK_BELT,constants.FIFTH_DEGREE_BLACK_BELT,constants.JUNIOR_BLACK_BELT], clean_df=clean_df)
    
            ### 10:30 Events
    
            ###############################################################################
            # Youth Girl's Sparring  - 7-8 year olds
            #
            reports.ExcelFileOutput.writePattern3ToExcelViaQuery(output_folder_path=output_folder_path, filename="YouthGirlSparring.xlsx", division_type='Forms', gender="Female",minimum_age=7, maximum_age=8,clean_df=clean_df)
    
            self.writeSingleSparringTreeandDivisionReport(event_time="10:30am",division_name="Youth Girl's Sparring",gender="Female", rank_label="White, Yellow",             minimum_age=7, maximum_age=8, rings=[1], ranks=[constants.WHITE_BELT,constants.YELLOW_BELT],clean_df=clean_df)
            self.writeSingleSparringTreeandDivisionReport(event_time="10:30am",division_name="Youth Girl's Sparring",gender="Female", rank_label="Orange",                    minimum_age=7, maximum_age=8, rings=[2], ranks=[constants.ORANGE_BELT],clean_df=clean_df)
            self.writeSingleSparringTreeandDivisionReport(event_time="10:30am",division_name="Youth Girl's Sparring",gender="Female", rank_label="Purple",                    minimum_age=7, maximum_age=8, rings=[3], ranks=[constants.PURPLE_BELT],clean_df=clean_df)
            self.writeSingleSparringTreeandDivisionReport(event_time="10:30am",division_name="Youth Girl's Sparring",gender="Female", rank_label="Blue, Blue/Stripe",         minimum_age=7, maximum_age=8, rings=[4], ranks=[constants.BLUE_BELT,constants.BLUE_STRIPE_BELT],clean_df=clean_df)
            self.writeSingleSparringTreeandDivisionReport(event_time="10:30am",division_name="Youth Girl's Sparring",gender="Female", rank_label="Green, Green/Stripe, Brown",minimum_age=7, maximum_age=8, rings=[5], ranks=[constants.GREEN_BELT,constants.GREEN_STRIPE_BELT,constants.THIRD_DEGREE_BROWN_BELT,constants.SECOND_DEGREE_BROWN_BELT,constants.FIRST_DEGREE_BROWN_BELT],clean_df=clean_df)
    
            ###############################################################################
            # Youth Boy's Sparring - 7-8 year olds
            #
            reports.ExcelFileOutput.writePattern3ToExcelViaQuery(output_folder_path=output_folder_path, filename="YouthBoysSparring.xlsx", division_type='Forms', gender="Male",minimum_age=7, maximum_age=8,clean_df=clean_df)
    
            self.writeSingleSparringTreeandDivisionReport(event_time="10:30am",division_name="Youth Boy's Sparring",gender="Male", rank_label="White, Yellow",             minimum_age=7, maximum_age=8, rings=[6], ranks=[constants.WHITE_BELT,constants.YELLOW_BELT],clean_df=clean_df)
            self.writeSingleSparringTreeandDivisionReport(event_time="10:30am",division_name="Youth Boy's Sparring",gender="Male", rank_label="Orange",                    minimum_age=7, maximum_age=8, rings=[7], ranks=[constants.ORANGE_BELT],clean_df=clean_df)
            self.writeSingleSparringTreeandDivisionReport(event_time="10:30am",division_name="Youth Boy's Sparring",gender="Male", rank_label="Purple",                    minimum_age=7, maximum_age=8, rings=[8], ranks=[constants.PURPLE_BELT],clean_df=clean_df)
            self.writeSingleSparringTreeandDivisionReport(event_time="10:30am",division_name="Youth Boy's Sparring",gender="Male", rank_label="Blue, Blue/Stripe",         minimum_age=7, maximum_age=8, rings=[9], ranks=[constants.BLUE_BELT,constants.BLUE_STRIPE_BELT],clean_df=clean_df)
            self.writeSingleSparringTreeandDivisionReport(event_time="10:30am",division_name="Youth Boy's Sparring",gender="Male", rank_label="Green, Green/Stripe, Brown",minimum_age=7, maximum_age=8, rings=[10], ranks=[constants.GREEN_BELT,constants.GREEN_STRIPE_BELT,constants.THIRD_DEGREE_BROWN_BELT,constants.SECOND_DEGREE_BROWN_BELT,constants.FIRST_DEGREE_BROWN_BELT],clean_df=clean_df)

            ###############################################################################
            # Girl's Sparring - 9-11 year olds
            #
            reports.ExcelFileOutput.writePattern1ToExcelViaQuery(output_folder_path=output_folder_path, filename="GirlsSparring.xlsx", division_type='Sparring', gender="Female",minimum_age=9, maximum_age=11,clean_df=clean_df)
    
            self.writeSingleSparringTreeandDivisionReport(event_time="10:30am",division_name="Girl's Sparring",gender="Female", rank_label="White, Yellow, Orange",     minimum_age=9, maximum_age=11, rings=[11], ranks=[constants.WHITE_BELT,constants.YELLOW_BELT,constants.ORANGE_BELT],clean_df=clean_df)
            self.writeSingleSparringTreeandDivisionReport(event_time="10:30am",division_name="Girl's Sparring",gender="Female", rank_label="Purple",                    minimum_age=9, maximum_age=11, rings=[14], ranks=[constants.PURPLE_BELT],clean_df=clean_df)
            self.writeSingleSparringTreeandDivisionReport(event_time="10:30am",division_name="Girl's Sparring",gender="Female", rank_label="Blue, Blue/Stripe",         minimum_age=9, maximum_age=11, rings=[12], ranks=[constants.BLUE_BELT,constants.BLUE_STRIPE_BELT],clean_df=clean_df)
            self.writeSingleSparringTreeandDivisionReport(event_time="10:30am",division_name="Girl's Sparring",gender="Female", rank_label="Green, Green/Stripe, Brown",minimum_age=9, maximum_age=11, rings=[13], ranks=[constants.GREEN_BELT,constants.GREEN_STRIPE_BELT,constants.THIRD_DEGREE_BROWN_BELT,constants.SECOND_DEGREE_BROWN_BELT,constants.FIRST_DEGREE_BROWN_BELT],clean_df=clean_df)
            self.writeSingleSparringTreeandDivisionReport(event_time="10:30am",division_name="Girl's Sparring",gender="Female", rank_label="Jr. Black",                 minimum_age=9, maximum_age=11, rings=[14], ranks=[constants.JUNIOR_BLACK_BELT,constants.FIRST_DEGREE_BLACK_BELT,constants.SECOND_DEGREE_BLACK_BELT,constants.THIRD_DEGREE_BLACK_BELT,constants.FOURTH_DEGREE_BLACK_BELT,constants.FIFTH_DEGREE_BLACK_BELT],clean_df=clean_df)
    
            ### 11:15 Events
    
            ###############################################################################
            # Boy's Sparring - 9-11 year olds
            #
            reports.ExcelFileOutput.writePattern6ToExcelViaQuery(output_folder_path=output_folder_path, filename="BoysSparring.xlsx", division_type='Sparring', gender="Male",minimum_age=9, maximum_age=11,clean_df=clean_df)
    
            self.writeSingleSparringTreeandDivisionReport(event_time="11:15am",division_name="Boy's Sparring",gender="Male", rank_label="White, Yellow",             minimum_age=9, maximum_age=11, rings=[1], ranks=[constants.WHITE_BELT,constants.YELLOW_BELT],clean_df=clean_df)
            self.writeSingleSparringTreeandDivisionReport(event_time="11:15am",division_name="Boy's Sparring",gender="Male", rank_label="Orange",                    minimum_age=9, maximum_age=11, rings=[2], ranks=[constants.ORANGE_BELT],clean_df=clean_df)
            self.writeSingleSparringTreeandDivisionReport(event_time="11:15am",division_name="Boy's Sparring",gender="Male", rank_label="Purple",                    minimum_age=9, maximum_age=11, rings=[3], ranks=[constants.PURPLE_BELT],clean_df=clean_df)
            self.writeSingleSparringTreeandDivisionReport(event_time="11:15am",division_name="Boy's Sparring",gender="Male", rank_label="Blue, Blue/Stripe",         minimum_age=9, maximum_age=11, rings=[4,5], ranks=[constants.BLUE_BELT,constants.BLUE_STRIPE_BELT],clean_df=clean_df)
            self.writeSingleSparringTreeandDivisionReport(event_time="11:15am",division_name="Boy's Sparring",gender="Male", rank_label="Green, Green/Stripe",       minimum_age=9, maximum_age=11, rings=[6], ranks=[constants.GREEN_BELT,constants.GREEN_STRIPE_BELT],clean_df=clean_df)
            self.writeSingleSparringTreeandDivisionReport(event_time="11:15am",division_name="Boy's Sparring",gender="Male", rank_label="Brown",                     minimum_age=9, maximum_age=11, rings=[7], ranks=[constants.THIRD_DEGREE_BROWN_BELT,constants.SECOND_DEGREE_BROWN_BELT,constants.FIRST_DEGREE_BROWN_BELT],clean_df=clean_df)
            self.writeSingleSparringTreeandDivisionReport(event_time="11:15am",division_name="Boy's Sparring",gender="Male", rank_label="Jr. Black",                 minimum_age=9, maximum_age=11, rings=[8], ranks=[constants.JUNIOR_BLACK_BELT,constants.FIRST_DEGREE_BLACK_BELT,constants.SECOND_DEGREE_BLACK_BELT,constants.THIRD_DEGREE_BLACK_BELT,constants.FOURTH_DEGREE_BLACK_BELT,constants.FIFTH_DEGREE_BLACK_BELT],clean_df=clean_df)

            ###############################################################################
            # Defense Techniques
            # TBD - Figure out how to write Def Techs to excel
            # reports.ExcelFileOutput.writePattern6ToExcelViaQuery(output_folder_path=output_folder_path, filename="BoysSparring.xlsx", division_type='Sparring', gender="Male",minimum_age=9, maximum_age=11,clean_df=clean_df)

            self.writeSingleTechniqueScoreSheetandDivisionReport(event_time="11:15am",division_name="Defense Technique",gender="*", rank_label="Green, Green/Stripe, Brown", minimum_age=4,  maximum_age=11,                rings=[9], ranks=[constants.GREEN_BELT,constants.GREEN_STRIPE_BELT,constants.THIRD_DEGREE_BROWN_BELT,constants.SECOND_DEGREE_BROWN_BELT,constants.FIRST_DEGREE_BROWN_BELT],clean_df=clean_df)
            self.writeSingleTechniqueScoreSheetandDivisionReport(event_time="11:15am",division_name="Defense Technique",gender="*", rank_label="Green, Green/Stripe, Brown", minimum_age=12, maximum_age=17,                rings=[10], ranks=[constants.GREEN_BELT,constants.GREEN_STRIPE_BELT,constants.THIRD_DEGREE_BROWN_BELT,constants.SECOND_DEGREE_BROWN_BELT,constants.FIRST_DEGREE_BROWN_BELT],clean_df=clean_df)
            self.writeSingleTechniqueScoreSheetandDivisionReport(event_time="11:15am",division_name="Defense Technique",gender="*", rank_label="Green, Green/Stripe, Brown", minimum_age=18, maximum_age=39,                rings=[11], ranks=[constants.GREEN_BELT,constants.GREEN_STRIPE_BELT,constants.THIRD_DEGREE_BROWN_BELT,constants.SECOND_DEGREE_BROWN_BELT,constants.FIRST_DEGREE_BROWN_BELT],clean_df=clean_df)
            self.writeSingleTechniqueScoreSheetandDivisionReport(event_time="11:15am",division_name="Defense Technique",gender="*", rank_label="Green, Green/Stripe, Brown", minimum_age=40, maximum_age=constants.AGELESS, rings=[11], ranks=[constants.GREEN_BELT,constants.GREEN_STRIPE_BELT,constants.THIRD_DEGREE_BROWN_BELT,constants.SECOND_DEGREE_BROWN_BELT,constants.FIRST_DEGREE_BROWN_BELT],clean_df=clean_df)
            self.writeSingleTechniqueScoreSheetandDivisionReport(event_time="11:15am",division_name="Defense Technique",gender="*", rank_label="Jr. Black",                  minimum_age=4,  maximum_age=11,                rings=[13], ranks=[constants.JUNIOR_BLACK_BELT,constants.FIRST_DEGREE_BLACK_BELT,constants.SECOND_DEGREE_BLACK_BELT,constants.THIRD_DEGREE_BLACK_BELT,constants.FOURTH_DEGREE_BLACK_BELT,constants.FIFTH_DEGREE_BLACK_BELT],clean_df=clean_df)
            self.writeSingleTechniqueScoreSheetandDivisionReport(event_time="11:15am",division_name="Defense Technique",gender="*", rank_label="Jr. Black & Black",          minimum_age=12, maximum_age=17,                rings=[14], ranks=[constants.JUNIOR_BLACK_BELT,constants.FIRST_DEGREE_BLACK_BELT,constants.SECOND_DEGREE_BLACK_BELT,constants.THIRD_DEGREE_BLACK_BELT,constants.FOURTH_DEGREE_BLACK_BELT,constants.FIFTH_DEGREE_BLACK_BELT],clean_df=clean_df)
            self.writeSingleTechniqueScoreSheetandDivisionReport(event_time="11:15am",division_name="Defense Technique",gender="*", rank_label="Black",                      minimum_age=18, maximum_age=39,                rings=[15], ranks=[constants.JUNIOR_BLACK_BELT,constants.FIRST_DEGREE_BLACK_BELT,constants.SECOND_DEGREE_BLACK_BELT,constants.THIRD_DEGREE_BLACK_BELT,constants.FOURTH_DEGREE_BLACK_BELT,constants.FIFTH_DEGREE_BLACK_BELT],clean_df=clean_df)
            self.writeSingleTechniqueScoreSheetandDivisionReport(event_time="11:15am",division_name="Defense Technique",gender="*", rank_label="Black",                      minimum_age=40, maximum_age=constants.AGELESS, rings=[16], ranks=[constants.JUNIOR_BLACK_BELT,constants.FIRST_DEGREE_BLACK_BELT,constants.SECOND_DEGREE_BLACK_BELT,constants.THIRD_DEGREE_BLACK_BELT,constants.FOURTH_DEGREE_BLACK_BELT,constants.FIFTH_DEGREE_BLACK_BELT],clean_df=clean_df)

            ###############################################################################
            # Weapons Division 1 - 4-8 year olds
            #
            reports.ExcelFileOutput.writeWeaponsDivision1ToExcelViaQuery(output_folder_path=output_folder_path, filename="WeaponsDivision1.xlsx", division_type='Weapons', gender="*", minimum_age=4, maximum_age=8, clean_df=clean_df)
            self.writeWeaponsDivisionToSingleKataScoreSheetandDivisionReport(event_time="11:15am",division_name="Weapons Division 1",gender="*", rank_label="White to Jr. Back", minimum_age=4, maximum_age=8, rings=['*TBA'],
                                                       ranks=[constants.WHITE_BELT,constants.YELLOW_BELT,constants.ORANGE_BELT,constants.PURPLE_BELT,
                                                              constants.BLUE_BELT,constants.BLUE_STRIPE_BELT,
                                                              constants.GREEN_BELT,constants.GREEN_STRIPE_BELT,
                                                              constants.THIRD_DEGREE_BROWN_BELT,constants.SECOND_DEGREE_BROWN_BELT,constants.FIRST_DEGREE_BROWN_BELT,
                                                              constants.JUNIOR_BLACK_BELT],
                                                       clean_df= clean_df)
    
    
            ###############################################################################
            # Weapons Division 2 - 9-11 year olds White - Blue W/Green Stripe
            #
            reports.ExcelFileOutput.writeWeaponsDivision2ToExcelViaQuery(output_folder_path=output_folder_path, filename="WeaponsDivision2.xlsx", division_type='Weapons', gender="*", minimum_age=9, maximum_age=11, clean_df=clean_df)
            self.writeWeaponsDivisionToSingleKataScoreSheetandDivisionReport(event_time="11:15am",division_name="Weapons Division 2-new",gender="*", rank_label="White to Blue w/Green Stripe", minimum_age=9, maximum_age=11, rings=['*TBA'],
                                                                        ranks=[constants.WHITE_BELT,constants.YELLOW_BELT,
                                                                               constants.ORANGE_BELT,constants.PURPLE_BELT,
                                                                               constants.BLUE_BELT,constants.BLUE_STRIPE_BELT],
                                                                        clean_df= clean_df)
    
    
            ###############################################################################
            #  WeaponsDivision3  - 9-11 year olds Green - Jr. Black
            #
            reports.ExcelFileOutput.writeWeaponsDivision3ToExcelViaQuery(output_folder_path=output_folder_path, filename="WeaponsDivision3.xlsx", division_type='Weapons', gender="*", minimum_age=9, maximum_age=11, clean_df=clean_df)
            self.writeWeaponsDivisionToSingleKataScoreSheetandDivisionReport(event_time="11:15am",division_name="Weapons Division 3-new",gender="*", rank_label="Green - Jr. Black", minimum_age=9, maximum_age=11, rings=['*TBA'],
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
            reports.ExcelFileOutput.writePattern6ToExcelViaQuery(output_folder_path=output_folder_path, filename="MenAndWomensKata.xlsx", division_type='Forms', gender="*",minimum_age=18, maximum_age=39,clean_df=clean_df)
    
            self.writeSingleKataScoreSheetandDivisionReport(event_time="1:30pm",division_name="Men's & Women's Kata",gender="*", rank_label="White, Yellow",         minimum_age=18, maximum_age=39, rings=[1], ranks=[constants.WHITE_BELT,constants.YELLOW_BELT], clean_df=clean_df)
            self.writeSingleKataScoreSheetandDivisionReport(event_time="1:30pm",division_name="Men's & Women's Kata",gender="*", rank_label="Orange",                minimum_age=18, maximum_age=39, rings=[2], ranks=[constants.ORANGE_BELT], clean_df=clean_df)
            self.writeSingleKataScoreSheetandDivisionReport(event_time="1:30pm",division_name="Men's & Women's Kata",gender="*", rank_label="Purple",                minimum_age=18, maximum_age=39, rings=[3], ranks=[constants.PURPLE_BELT], clean_df=clean_df)
            self.writeSingleKataScoreSheetandDivisionReport(event_time="1:30pm",division_name="Men's & Women's Kata",gender="*", rank_label="Blue, Blue w/Stripe",   minimum_age=18, maximum_age=39, rings=[4], ranks=[constants.BLUE_BELT,constants.BLUE_STRIPE_BELT], clean_df=clean_df)
            self.writeSingleKataScoreSheetandDivisionReport(event_time="1:30pm",division_name="Men's & Women's Kata",gender="*", rank_label="Green, Green w/Stripe", minimum_age=18, maximum_age=39, rings=[5], ranks=[constants.GREEN_BELT,constants.GREEN_STRIPE_BELT], clean_df=clean_df)
            self.writeSingleKataScoreSheetandDivisionReport(event_time="1:30pm",division_name="Men's & Women's Kata",gender="*", rank_label="Brown",                 minimum_age=18, maximum_age=39, rings=[6], ranks=[constants.THIRD_DEGREE_BROWN_BELT,constants.SECOND_DEGREE_BROWN_BELT,constants.FIRST_DEGREE_BROWN_BELT], clean_df=clean_df)
            self.writeSingleKataScoreSheetandDivisionReport(event_time="1:30pm",division_name="Men's & Women's Kata",gender="*", rank_label="Black",                 minimum_age=18, maximum_age=39, rings=[7], ranks=[constants.FIRST_DEGREE_BLACK_BELT,constants.SECOND_DEGREE_BLACK_BELT, constants.THIRD_DEGREE_BLACK_BELT,constants.FOURTH_DEGREE_BLACK_BELT,constants.FIFTH_DEGREE_BLACK_BELT,constants.JUNIOR_BLACK_BELT], clean_df=clean_df)
    
    
            ###############################################################################
            # Teen Kata - 12-14 year olds
            #
            reports.ExcelFileOutput.writePattern6ToExcelViaQuery(output_folder_path=output_folder_path, filename="TeenKata.xlsx", division_type='Forms', gender="*",minimum_age=12, maximum_age=14,clean_df=clean_df)
    
            self.writeSingleKataScoreSheetandDivisionReport(event_time="1:30pm",division_name="Teen Kata",gender="*", rank_label="White, Yellow",         minimum_age=12, maximum_age=14, rings=[8],     ranks=[constants.WHITE_BELT,constants.YELLOW_BELT], clean_df=clean_df)
            self.writeSingleKataScoreSheetandDivisionReport(event_time="1:30pm",division_name="Teen Kata",gender="*", rank_label="Orange",                minimum_age=12, maximum_age=14, rings=[9],     ranks=[constants.ORANGE_BELT], clean_df=clean_df)
            self.writeSingleKataScoreSheetandDivisionReport(event_time="1:30pm",division_name="Teen Kata",gender="*", rank_label="Purple",                minimum_age=12, maximum_age=14, rings=[10],    ranks=[constants.PURPLE_BELT], clean_df=clean_df)
            self.writeSingleKataScoreSheetandDivisionReport(event_time="1:30pm",division_name="Teen Kata",gender="*", rank_label="Blue, Blue w/Stripe",   minimum_age=12, maximum_age=14, rings=[11,12], ranks=[constants.BLUE_BELT,constants.BLUE_STRIPE_BELT], clean_df=clean_df)
            self.writeSingleKataScoreSheetandDivisionReport(event_time="1:30pm",division_name="Teen Kata",gender="*", rank_label="Green, Green w/Stripe", minimum_age=12, maximum_age=14, rings=[13,14], ranks=[constants.GREEN_BELT,constants.GREEN_STRIPE_BELT], clean_df=clean_df)
            self.writeSingleKataScoreSheetandDivisionReport(event_time="1:30pm",division_name="Teen Kata",gender="*", rank_label="Brown",                 minimum_age=12, maximum_age=14, rings=[15],    ranks=[constants.THIRD_DEGREE_BROWN_BELT,constants.SECOND_DEGREE_BROWN_BELT,constants.FIRST_DEGREE_BROWN_BELT], clean_df=clean_df)
            self.writeSingleKataScoreSheetandDivisionReport(event_time="1:30pm",division_name="Teen Kata",gender="*", rank_label="Jr. Black",             minimum_age=12, maximum_age=14, rings=[16],    ranks=[constants.FIRST_DEGREE_BLACK_BELT,constants.SECOND_DEGREE_BLACK_BELT, constants.THIRD_DEGREE_BLACK_BELT,constants.FOURTH_DEGREE_BLACK_BELT,constants.FIFTH_DEGREE_BLACK_BELT,constants.JUNIOR_BLACK_BELT], clean_df=clean_df)
    
            ### 2:15 Events
    
            ###############################################################################
            # Senior Men's Sparring - 40+ year olds
            #
            reports.ExcelFileOutput.writePattern1ToExcelViaQuery(output_folder_path=output_folder_path, filename="SeniorMensSparring.xlsx", division_type='Sparring', gender="Male",minimum_age=40, maximum_age=constants.AGELESS,clean_df=clean_df)
    
            self.writeSingleSparringTreeandDivisionReport(event_time="2:15pm",division_name="Sr. Men's Sparring",gender="Male", rank_label="White, Yellow, Orange",     minimum_age=40, maximum_age=constants.AGELESS, rings=[1], ranks=[constants.WHITE_BELT,constants.YELLOW_BELT,constants.ORANGE_BELT],clean_df=clean_df)
            self.writeSingleSparringTreeandDivisionReport(event_time="2:15pm",division_name="Sr. Men's Sparring",gender="Male", rank_label="Purple, Blue, Blue/Stripe", minimum_age=40, maximum_age=constants.AGELESS, rings=[2], ranks=[constants.PURPLE_BELT,constants.BLUE_BELT,constants.BLUE_STRIPE_BELT],clean_df=clean_df)
            self.writeSingleSparringTreeandDivisionReport(event_time="2:15pm",division_name="Sr. Men's Sparring",gender="Male", rank_label="Green, Green/Stripe, Brown",minimum_age=40, maximum_age=constants.AGELESS, rings=[3], ranks=[constants.GREEN_BELT,constants.GREEN_STRIPE_BELT,constants.THIRD_DEGREE_BROWN_BELT,constants.SECOND_DEGREE_BROWN_BELT,constants.FIRST_DEGREE_BROWN_BELT],clean_df=clean_df)
            self.writeSingleSparringTreeandDivisionReport(event_time="2:15pm",division_name="Sr. Men's Sparring",gender="Male", rank_label="Black",                     minimum_age=40, maximum_age=constants.AGELESS, rings=[4], ranks=[constants.JUNIOR_BLACK_BELT,constants.FIRST_DEGREE_BLACK_BELT,constants.SECOND_DEGREE_BLACK_BELT,constants.THIRD_DEGREE_BLACK_BELT,constants.FOURTH_DEGREE_BLACK_BELT,constants.FIFTH_DEGREE_BLACK_BELT],clean_df=clean_df)
    
            ###############################################################################
            # Senior Women's Sparring - 40+ year olds
            #
            reports.ExcelFileOutput.writePattern1ToExcelViaQuery(output_folder_path=output_folder_path, filename="SeniorWomensSparring.xlsx", division_type='Sparring', gender="Female",minimum_age=40, maximum_age=constants.AGELESS,clean_df=clean_df)
    
            self.writeSingleSparringTreeandDivisionReport(event_time="2:15pm",division_name="Sr. Women's Sparring",gender="Female", rank_label="White, Yellow, Orange",     minimum_age=40, maximum_age=constants.AGELESS, rings=[5], ranks=[constants.WHITE_BELT,constants.YELLOW_BELT,constants.ORANGE_BELT],clean_df=clean_df)
            self.writeSingleSparringTreeandDivisionReport(event_time="2:15pm",division_name="Sr. Women's Sparring",gender="Female", rank_label="Purple, Blue, Blue/Stripe", minimum_age=40, maximum_age=constants.AGELESS, rings=[6], ranks=[constants.PURPLE_BELT,constants.BLUE_BELT,constants.BLUE_STRIPE_BELT],clean_df=clean_df)
            self.writeSingleSparringTreeandDivisionReport(event_time="2:15pm",division_name="Sr. Women's Sparring",gender="Female", rank_label="Green, Green/Stripe, Brown",minimum_age=40, maximum_age=constants.AGELESS, rings=[7], ranks=[constants.GREEN_BELT,constants.GREEN_STRIPE_BELT,constants.THIRD_DEGREE_BROWN_BELT,constants.SECOND_DEGREE_BROWN_BELT,constants.FIRST_DEGREE_BROWN_BELT],clean_df=clean_df)
            self.writeSingleSparringTreeandDivisionReport(event_time="2:15pm",division_name="Sr. Women's Sparring",gender="Female", rank_label="Black",                     minimum_age=40, maximum_age=constants.AGELESS, rings=[8], ranks=[constants.JUNIOR_BLACK_BELT,constants.FIRST_DEGREE_BLACK_BELT,constants.SECOND_DEGREE_BLACK_BELT,constants.THIRD_DEGREE_BLACK_BELT,constants.FOURTH_DEGREE_BLACK_BELT,constants.FIFTH_DEGREE_BLACK_BELT],clean_df=clean_df)
    
            ###############################################################################
            # Young Adult Kata - 15-17 year olds
            #
            reports.ExcelFileOutput.writePattern1ToExcelViaQuery(output_folder_path=output_folder_path, filename="YoungAdultKata.xlsx", division_type='Forms', gender="*",minimum_age=15, maximum_age=17,clean_df=clean_df)
    
            self.writeSingleKataScoreSheetandDivisionReport(event_time="2:15pm",division_name="Young Adult Kata",gender="*",rank_label="White,Yellow,Orange",       minimum_age=15, maximum_age=17, rings=[9],  ranks=[constants.WHITE_BELT,constants.YELLOW_BELT,constants.ORANGE_BELT], clean_df=clean_df)
            self.writeSingleKataScoreSheetandDivisionReport(event_time="2:15pm",division_name="Young Adult Kata",gender="*",rank_label="Purple, Blue, Blue/Stripe", minimum_age=15, maximum_age=17, rings=[10], ranks=[constants.PURPLE_BELT,constants.BLUE_BELT,constants.BLUE_STRIPE_BELT], clean_df=clean_df)
            self.writeSingleKataScoreSheetandDivisionReport(event_time="2:15pm",division_name="Young Adult Kata",gender="*",rank_label="Green, Green/Stripe, Brown",minimum_age=15, maximum_age=17, rings=[11], ranks=[constants.GREEN_BELT,constants.GREEN_STRIPE_BELT,constants.THIRD_DEGREE_BROWN_BELT,constants.SECOND_DEGREE_BROWN_BELT,constants.FIRST_DEGREE_BROWN_BELT], clean_df=clean_df)
            self.writeSingleKataScoreSheetandDivisionReport(event_time="2:15pm",division_name="Young Adult Kata",gender="*",rank_label="Jr. Black & Black",         minimum_age=15, maximum_age=17, rings=[12], ranks=[constants.FIRST_DEGREE_BLACK_BELT,constants.SECOND_DEGREE_BLACK_BELT, constants.THIRD_DEGREE_BLACK_BELT,constants.FOURTH_DEGREE_BLACK_BELT,constants.FIFTH_DEGREE_BLACK_BELT,constants.JUNIOR_BLACK_BELT], clean_df=clean_df)
    
    
            ###############################################################################
            # Teen Girl's Sparring - 12-14 year olds
            #
            reports.ExcelFileOutput.writePattern1ToExcelViaQuery(output_folder_path=output_folder_path, filename="TeenGirlSparring.xlsx", division_type='Sparring', gender="Female",minimum_age=12, maximum_age=14,clean_df=clean_df)
    
            self.writeSingleSparringTreeandDivisionReport(event_time="2:15pm",division_name="Teen Girl's Sparring",gender="Female", rank_label="White, Yellow, Orange",     minimum_age=12, maximum_age=14, rings=[13], ranks=[constants.WHITE_BELT,constants.YELLOW_BELT,constants.ORANGE_BELT],clean_df=clean_df)
            self.writeSingleSparringTreeandDivisionReport(event_time="2:15pm",division_name="Teen Girl's Sparring",gender="Female", rank_label="Purple, Blue, Blue/Stripe", minimum_age=12, maximum_age=14, rings=[14], ranks=[constants.PURPLE_BELT,constants.BLUE_BELT,constants.BLUE_STRIPE_BELT],clean_df=clean_df)
            self.writeSingleSparringTreeandDivisionReport(event_time="2:15pm",division_name="Teen Girl's Sparring",gender="Female", rank_label="Green, Green/Stripe, Brown",minimum_age=12, maximum_age=14, rings=[15], ranks=[constants.GREEN_BELT,constants.GREEN_STRIPE_BELT,constants.THIRD_DEGREE_BROWN_BELT,constants.SECOND_DEGREE_BROWN_BELT,constants.FIRST_DEGREE_BROWN_BELT],clean_df=clean_df)
            self.writeSingleSparringTreeandDivisionReport(event_time="2:15pm",division_name="Teen Girl's Sparring",gender="Female", rank_label="Jr. Black",                 minimum_age=12, maximum_age=14, rings=[16], ranks=[constants.JUNIOR_BLACK_BELT,constants.FIRST_DEGREE_BLACK_BELT,constants.SECOND_DEGREE_BLACK_BELT,constants.THIRD_DEGREE_BLACK_BELT,constants.FOURTH_DEGREE_BLACK_BELT,constants.FIFTH_DEGREE_BLACK_BELT],clean_df=clean_df)
    
    
            ### 3:00 Events
    
            ###############################################################################
            #  Men's Sparring - 18-39 year olds
            #
            reports.ExcelFileOutput.writePattern1ToExcelViaQuery(output_folder_path=output_folder_path, filename="MensSparring.xlsx", division_type='Sparring', gender="Male",minimum_age=18, maximum_age=39,clean_df=clean_df)
    
            self.writeSingleSparringTreeandDivisionReport(event_time="3:00pm",division_name="Men's Sparring",gender="Male", rank_label="White, Yellow, Orange",     minimum_age=18, maximum_age=39, rings=[1], ranks=[constants.WHITE_BELT,constants.YELLOW_BELT,constants.ORANGE_BELT],clean_df=clean_df)
            self.writeSingleSparringTreeandDivisionReport(event_time="3:00pm",division_name="Men's Sparring",gender="Male", rank_label="Purple, Blue, Blue/Stripe", minimum_age=18, maximum_age=39, rings=[2], ranks=[constants.PURPLE_BELT,constants.BLUE_BELT,constants.BLUE_STRIPE_BELT],clean_df=clean_df)
            self.writeSingleSparringTreeandDivisionReport(event_time="3:00pm",division_name="Men's Sparring",gender="Male", rank_label="Green, Green/Stripe, Brown",minimum_age=18, maximum_age=39, rings=[3], ranks=[constants.GREEN_BELT,constants.GREEN_STRIPE_BELT,constants.THIRD_DEGREE_BROWN_BELT,constants.SECOND_DEGREE_BROWN_BELT,constants.FIRST_DEGREE_BROWN_BELT],clean_df=clean_df)
            self.writeSingleSparringTreeandDivisionReport(event_time="3:00pm",division_name="Men's Sparring",gender="Male", rank_label="Black",                     minimum_age=18, maximum_age=39, rings=[4], ranks=[constants.JUNIOR_BLACK_BELT,constants.FIRST_DEGREE_BLACK_BELT,constants.SECOND_DEGREE_BLACK_BELT,constants.THIRD_DEGREE_BLACK_BELT,constants.FOURTH_DEGREE_BLACK_BELT,constants.FIFTH_DEGREE_BLACK_BELT],clean_df=clean_df)
    
            ###############################################################################
            #  Teen Boy's Sparring - 12-14 year olds
            #
            reports.ExcelFileOutput.writePattern2ToExcelViaQuery(output_folder_path=output_folder_path, filename="TeenBoysSparring.xlsx", division_type='Sparring', gender="Male",minimum_age=12, maximum_age=14,clean_df=clean_df)
    
            self.writeSingleSparringTreeandDivisionReport(event_time="3:00pm",division_name="Teen Boy's Sparring",gender="Male", rank_label="White, Yellow, Orange", minimum_age=12, maximum_age=14, rings=[5], ranks=[constants.WHITE_BELT,constants.YELLOW_BELT,constants.ORANGE_BELT],clean_df=clean_df)
            self.writeSingleSparringTreeandDivisionReport(event_time="3:00pm",division_name="Teen Boy's Sparring",gender="Male", rank_label="Purple",                minimum_age=12, maximum_age=14, rings=[10], ranks=[constants.PURPLE_BELT],clean_df=clean_df)
            self.writeSingleSparringTreeandDivisionReport(event_time="3:00pm",division_name="Teen Boy's Sparring",gender="Male", rank_label="Blue, Blue/Stripe",     minimum_age=12, maximum_age=14, rings=[6], ranks=[constants.BLUE_BELT,constants.BLUE_STRIPE_BELT],clean_df=clean_df)
            self.writeSingleSparringTreeandDivisionReport(event_time="3:00pm",division_name="Teen Boy's Sparring",gender="Male", rank_label="Green, Green/Stripe",   minimum_age=12, maximum_age=14, rings=[7], ranks=[constants.GREEN_BELT,constants.GREEN_STRIPE_BELT],clean_df=clean_df)
            self.writeSingleSparringTreeandDivisionReport(event_time="3:00pm",division_name="Teen Boy's Sparring",gender="Male", rank_label="Brown",                 minimum_age=12, maximum_age=14, rings=[8], ranks=[constants.THIRD_DEGREE_BROWN_BELT,constants.SECOND_DEGREE_BROWN_BELT,constants.FIRST_DEGREE_BROWN_BELT],clean_df=clean_df)
            self.writeSingleSparringTreeandDivisionReport(event_time="3:00pm",division_name="Teen Boy's Sparring",gender="Male", rank_label="Jr. Black",             minimum_age=12, maximum_age=14, rings=[9], ranks=[constants.JUNIOR_BLACK_BELT,constants.FIRST_DEGREE_BLACK_BELT,constants.SECOND_DEGREE_BLACK_BELT,constants.THIRD_DEGREE_BLACK_BELT,constants.FOURTH_DEGREE_BLACK_BELT,constants.FIFTH_DEGREE_BLACK_BELT],clean_df=clean_df)
    
            ###############################################################################
            #  Young Adult Men's Sparring - 15-17 year olds
            #
            reports.ExcelFileOutput.writePattern2ToExcelViaQuery(output_folder_path=output_folder_path, filename="YoungAdultMensSparring.xlsx", division_type='Sparring', gender="Male",minimum_age=15, maximum_age=17,clean_df=clean_df)
    
            self.writeSingleSparringTreeandDivisionReport(event_time="3:00pm",division_name="Young Adult Men's Sparring",gender="Male", rank_label="White, Yellow, Orange",     minimum_age=15, maximum_age=17, rings=[10], ranks=[constants.WHITE_BELT,constants.YELLOW_BELT,constants.ORANGE_BELT],clean_df=clean_df)
            self.writeSingleSparringTreeandDivisionReport(event_time="3:00pm",division_name="Young Adult Men's Sparring",gender="Male", rank_label="Purple, Blue, Blue/Stripe", minimum_age=15, maximum_age=17, rings=[11], ranks=[constants.PURPLE_BELT,constants.BLUE_BELT,constants.BLUE_STRIPE_BELT],clean_df=clean_df)
            self.writeSingleSparringTreeandDivisionReport(event_time="3:00pm",division_name="Young Adult Men's Sparring",gender="Male", rank_label="Green, Green/Stripe",       minimum_age=15, maximum_age=17, rings=[12], ranks=[constants.GREEN_BELT,constants.GREEN_STRIPE_BELT],clean_df=clean_df)
            self.writeSingleSparringTreeandDivisionReport(event_time="3:00pm",division_name="Young Adult Men's Sparring",gender="Male", rank_label="Brown",                     minimum_age=15, maximum_age=17, rings=[13], ranks=[constants.THIRD_DEGREE_BROWN_BELT,constants.SECOND_DEGREE_BROWN_BELT,constants.FIRST_DEGREE_BROWN_BELT],clean_df=clean_df)
            self.writeSingleSparringTreeandDivisionReport(event_time="3:00pm",division_name="Young Adult Men's Sparring",gender="Male", rank_label="Jr. Black & Black",         minimum_age=15, maximum_age=17, rings=[14], ranks=[constants.JUNIOR_BLACK_BELT,constants.FIRST_DEGREE_BLACK_BELT,constants.SECOND_DEGREE_BLACK_BELT,constants.THIRD_DEGREE_BLACK_BELT,constants.FOURTH_DEGREE_BLACK_BELT,constants.FIFTH_DEGREE_BLACK_BELT],clean_df=clean_df)
    
    
            ###############################################################################
            #  Women's Sparring - 18-39 year olds
            #
            reports.ExcelFileOutput.writePattern1ToExcelViaQuery(output_folder_path=output_folder_path, filename="WomensSparring.xlsx", division_type='Sparring', gender="Female",minimum_age=18, maximum_age=39,clean_df=clean_df)
    
            self.writeSingleSparringTreeandDivisionReport(event_time="3:00pm",division_name="Women's Sparring",gender="Female", rank_label="White, Yellow, Orange",     minimum_age=18, maximum_age=39, rings=[15], ranks=[constants.WHITE_BELT,constants.YELLOW_BELT,constants.ORANGE_BELT],clean_df=clean_df)
            self.writeSingleSparringTreeandDivisionReport(event_time="3:00pm",division_name="Women's Sparring",gender="Female", rank_label="Purple, Blue, Blue/Stripe", minimum_age=18, maximum_age=39, rings=[16], ranks=[constants.PURPLE_BELT,constants.BLUE_BELT,constants.BLUE_STRIPE_BELT],clean_df=clean_df)
            self.writeSingleSparringTreeandDivisionReport(event_time="3:00pm",division_name="Women's Sparring",gender="Female", rank_label="Green, Green/Stripe, Brown",minimum_age=18, maximum_age=39, rings=[17], ranks=[constants.GREEN_BELT,constants.GREEN_STRIPE_BELT,constants.THIRD_DEGREE_BROWN_BELT,constants.SECOND_DEGREE_BROWN_BELT,constants.FIRST_DEGREE_BROWN_BELT],clean_df=clean_df)
            self.writeSingleSparringTreeandDivisionReport(event_time="3:00pm",division_name="Women's Sparring",gender="Female", rank_label="Black",                     minimum_age=18, maximum_age=39, rings=[18], ranks=[constants.JUNIOR_BLACK_BELT,constants.FIRST_DEGREE_BLACK_BELT,constants.SECOND_DEGREE_BLACK_BELT,constants.THIRD_DEGREE_BLACK_BELT,constants.FOURTH_DEGREE_BLACK_BELT,constants.FIFTH_DEGREE_BLACK_BELT],clean_df=clean_df)
    
    
            ### 3:45 Events
    
            ###############################################################################
            # Senior Kata - 40+ year olds
            #
            reports.ExcelFileOutput.writePattern6ToExcelViaQuery(output_folder_path=output_folder_path, filename="SeniorKata.xlsx", division_type='Forms', gender="*",minimum_age=40, maximum_age=constants.AGELESS,clean_df=clean_df)
    
            self.writeSingleKataScoreSheetandDivisionReport(event_time="3:45pm",division_name="Senior Kata",gender="*", rank_label="White, Yellow",         minimum_age=40, maximum_age=constants.AGELESS, rings=[1], ranks=[constants.WHITE_BELT,constants.YELLOW_BELT], clean_df=clean_df)
            self.writeSingleKataScoreSheetandDivisionReport(event_time="3:45pm",division_name="Senior Kata",gender="*", rank_label="Orange",                minimum_age=40, maximum_age=constants.AGELESS, rings=[2], ranks=[constants.ORANGE_BELT], clean_df=clean_df)
            self.writeSingleKataScoreSheetandDivisionReport(event_time="3:45pm",division_name="Senior Kata",gender="*", rank_label="Purple",                minimum_age=40, maximum_age=constants.AGELESS, rings=[3], ranks=[constants.PURPLE_BELT], clean_df=clean_df)
            self.writeSingleKataScoreSheetandDivisionReport(event_time="3:45pm",division_name="Senior Kata",gender="*", rank_label="Blue, Blue w/Stripe",   minimum_age=40, maximum_age=constants.AGELESS, rings=[4], ranks=[constants.BLUE_BELT,constants.BLUE_STRIPE_BELT], clean_df=clean_df)
            self.writeSingleKataScoreSheetandDivisionReport(event_time="3:45pm",division_name="Senior Kata",gender="*", rank_label="Green, Green w/Stripe", minimum_age=40, maximum_age=constants.AGELESS, rings=[5], ranks=[constants.GREEN_BELT,constants.GREEN_STRIPE_BELT], clean_df=clean_df)
            self.writeSingleKataScoreSheetandDivisionReport(event_time="3:45pm",division_name="Senior Kata",gender="*", rank_label="Brown",                 minimum_age=40, maximum_age=constants.AGELESS, rings=[6], ranks=[constants.THIRD_DEGREE_BROWN_BELT,constants.SECOND_DEGREE_BROWN_BELT,constants.FIRST_DEGREE_BROWN_BELT], clean_df=clean_df)
            self.writeSingleKataScoreSheetandDivisionReport(event_time="3:45pm",division_name="Senior Kata",gender="*", rank_label="Black",                 minimum_age=40, maximum_age=constants.AGELESS, rings=[7], ranks=[constants.FIRST_DEGREE_BLACK_BELT,constants.SECOND_DEGREE_BLACK_BELT, constants.THIRD_DEGREE_BLACK_BELT,constants.FOURTH_DEGREE_BLACK_BELT,constants.FIFTH_DEGREE_BLACK_BELT,constants.JUNIOR_BLACK_BELT], clean_df=clean_df)
    
    
    
            ###############################################################################
            #  Young Adult Women's Sparring - 15-17 year olds
            #
            reports.ExcelFileOutput.writePattern1ToExcelViaQuery(output_folder_path=output_folder_path, filename="YoungAdultWomensSparring.xlsx", division_type='Sparring', gender="Female",minimum_age=15, maximum_age=17,clean_df=clean_df)
    
            self.writeSingleSparringTreeandDivisionReport(event_time="3:45pm",division_name="Young Adult Women's Sparring",gender="Female", rank_label="White, Yellow, Orange",     minimum_age=15, maximum_age=17, rings=[8], ranks=[constants.WHITE_BELT,constants.YELLOW_BELT,constants.ORANGE_BELT],clean_df=clean_df)
            self.writeSingleSparringTreeandDivisionReport(event_time="3:45pm",division_name="Young Adult Women's Sparring",gender="Female", rank_label="Purple, Blue, Blue/Stripe", minimum_age=15, maximum_age=17, rings=[9], ranks=[constants.PURPLE_BELT,constants.BLUE_BELT,constants.BLUE_STRIPE_BELT],clean_df=clean_df)
            self.writeSingleSparringTreeandDivisionReport(event_time="3:45pm",division_name="Young Adult Women's Sparring",gender="Female", rank_label="Green, Green/Stripe, Brown",minimum_age=15, maximum_age=17, rings=[10], ranks=[constants.GREEN_BELT,constants.GREEN_STRIPE_BELT,constants.THIRD_DEGREE_BROWN_BELT,constants.SECOND_DEGREE_BROWN_BELT,constants.FIRST_DEGREE_BROWN_BELT],clean_df=clean_df)
            self.writeSingleSparringTreeandDivisionReport(event_time="3:45pm",division_name="Young Adult Women's Sparring",gender="Female", rank_label="Jr. Black & Black",         minimum_age=15, maximum_age=17, rings=[11], ranks=[constants.JUNIOR_BLACK_BELT,constants.FIRST_DEGREE_BLACK_BELT,constants.SECOND_DEGREE_BLACK_BELT,constants.THIRD_DEGREE_BLACK_BELT,constants.FOURTH_DEGREE_BLACK_BELT,constants.FIFTH_DEGREE_BLACK_BELT],clean_df=clean_df)
    
    
            ### 4:15 Events
    
            ###############################################################################
            #  WeaponsDivision4 12-17 White-Blue Stripe year olds
            #
            reports.ExcelFileOutput.writeWeaponsDivision4ToExcelViaQuery(output_folder_path=output_folder_path, filename="WeaponsDivision4.xlsx", division_type='Weapons', gender="*", minimum_age=12, maximum_age=17, clean_df=clean_df)
            self.writeWeaponsDivisionToSingleKataScoreSheetandDivisionReport(event_time="4:15pm",
                                                                        division_name="Weapons Division 4",
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
            reports.ExcelFileOutput.writeWeaponsDivision5ToExcelViaQuery(output_folder_path=output_folder_path, filename="WeaponsDivision5.xlsx", division_type='Weapons', gender="*", minimum_age=18, maximum_age=constants.AGELESS, clean_df=clean_df)
            self.writeWeaponsDivisionToSingleKataScoreSheetandDivisionReport(event_time="4:15pm",
                                                                        division_name="Weapons Division 5",
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
            reports.ExcelFileOutput.writeWeaponsDivision6ToExcelViaQuery(output_folder_path=output_folder_path, filename="WeaponsDivision6.xlsx", division_type='Weapons', gender="*", minimum_age=12, maximum_age=constants.AGELESS, clean_df=clean_df)
            self.writeWeaponsDivisionToSingleKataScoreSheetandDivisionReport(event_time="4:15pm",
                                                                        division_name="Weapons Division 6",
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
            reports.ExcelFileOutput.writeWeaponsDivision7ToExcelViaQuery(output_folder_path=output_folder_path, filename="WeaponsDivision7.xlsx", division_type='Weapons', gender="*", minimum_age=12, maximum_age=constants.AGELESS, clean_df=clean_df)
            self.writeWeaponsDivisionToSingleKataScoreSheetandDivisionReport(event_time="4:15pm",
                                                                        division_name="Weapons Division 7",
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
            reports.ExcelFileOutput.writeWeaponsDivision8ToExcelViaQuery(output_folder_path=output_folder_path, filename="WeaponsDivision8.xlsx", division_type='Weapons', gender="*", minimum_age=12, maximum_age=17, clean_df=clean_df)
            self.writeWeaponsDivisionToSingleKataScoreSheetandDivisionReport(event_time="4:15pm",
                                                                        division_name="Weapons Division 8",
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
            reports.ExcelFileOutput.writeWeaponsDivision9ToExcelViaQuery(output_folder_path=output_folder_path, filename="WeaponsDivision9.xlsx", division_type='Weapons', gender="*", minimum_age=18, maximum_age=constants.AGELESS, clean_df=clean_df)
            self.writeWeaponsDivisionToSingleKataScoreSheetandDivisionReport(event_time="4:15pm",
                                                                        division_name="Weapons Division 9",
                                                                        gender="*",
                                                                        rank_label="Black",
                                                                        minimum_age=18,maximum_age=constants.AGELESS,
                                                                        rings=['*TBA'],
                                                                        ranks=[constants.JUNIOR_BLACK_BELT,constants.FIRST_DEGREE_BLACK_BELT,constants.SECOND_DEGREE_BLACK_BELT,constants.THIRD_DEGREE_BLACK_BELT,constants.FOURTH_DEGREE_BLACK_BELT,constants.FIFTH_DEGREE_BLACK_BELT],
                                                                        clean_df=clean_df)
    
        logging.info("Saving PDFs to disk")
        self.divison_detail_report_pdf.write_pdfpage()
        self.kata_score_sheet_pdf.write_pdfpage()
        self.technique_score_sheet_pdf.write_pdfpage()
        self.sparing_tree_pdf.close()
    
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

###############################################################################
#
# Main Function
#
if __name__ == '__main__':
    # get the filename from the environment var named  tourname_filename
    filename = os.getenv("tournament_filename")


    if filename is None:
        # Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
        root = Tk()
        root.withdraw()  # we don't want a full GUI, so keep the root window from appearing
        root.update()  # Prevent the askfilename() window doesn't stay open
        # filename = askopenfilename()
        filename = askopenfilename(title="Select the file with the tournament data",filetypes=[("csv","*.csv"),("excel","*.xls")])
        root.update()  # Prevent the askfilename() window doesn't stay open
    else:
        print("Using the file " + filename + "from the environment")

    p=pathlib.Path(filename)
    output_folder_path=str(p.parent)

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
    clean_df, error_count = cleaninput.clean_all_input_errors(renamed_df, input_error_list)
    del renamed_df  # make sure we don't use the renamed_df again
    # logging.info(f'Input Errors:{input_error_list.error_list}')
    if error_count > 0:
        sys.exit("Exiting - The input must be fixed manually")

    ltt = LoadTournamentTable()
    ltt.process_tournament_table( filename, clean_df, output_folder_path )