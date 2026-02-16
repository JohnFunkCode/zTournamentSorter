import sys
import os
from pathlib import Path
import logging

import pandas as pd
# from pandas.core.interchange.dataframe_protocol import DataFrame

from LoadTournamentTable import LoadTournamentTable
from ringevelopeparser.ring_envelope_parser import RingCollection

from cleaninput import cleaninput as CI
from cleaninput import rename_colums as RN
from cleaninput import input_errors


from reports.division_detail_report import DivisionDetailReport
from reports.working_guide_report import WorkingGuideReport
from reports.kata_score_sheet import KataScoreSheet
from reports.technique_score_sheet import TechniqueScoreSheet
import reports.sparring_tree.sparring_tree_report
import reports.ExcelFileOutput
import reports.FileHandlingUtilities
from reports import working_guide_google_sheet


def classify_division( division_name: str):
    if "Weapons" in division_name:
        return "Weapons"
    elif "Sparring" in division_name:
        return "Sparring"
    elif "Kata" in division_name:
        return "Kata"
    elif "Techniques" in division_name:
        return "Techniques"
    else:
        assert False, "Error: Invalid division_name"

def process_registrations_with_ring_envelope_data(ring_definition_file_name: str, registration_file_name:str, clean_df: pd.DataFrame, output_folder_path: str):
    clean_df['hitcount'] = 0  # setup a new column for hit rate.

    # load ring definition data from the ring_envelope file
    ring_defition_collection = RingCollection.from_csv(ring_definition_file_name)

    # get all events
    events = ring_defition_collection.get_all_events()

    #instanciate a LoadTournamentTable class
    ltt = LoadTournamentTable()

    ###############################################################################
    # Setup a few things for the Division Detail PDF report
    ltt.tournament_summary_report_pdf = WorkingGuideReport("Tournament Summary", registration_file_name, output_folder_path)

    ###############################################################################
    # Setup a few things for the Division Detail PDF report
    ltt.division_detail_report_pdf = DivisionDetailReport("Division Detail", registration_file_name, output_folder_path)

    ###############################################################################
    # Setup a few things for the Kata Score Sheet PDF report
    ltt.kata_score_sheet_pdf = KataScoreSheet("Forms", registration_file_name, output_folder_path, isCustomDivision=False)

    ###############################################################################
    # Setup a few things for the Techniques Score Sheet PDF report
    ltt.technique_score_sheet_pdf = TechniqueScoreSheet("Techniques", registration_file_name, output_folder_path)

    ###############################################################################
    # Setup a few things for the Sparring Tree PDF report
    ltt.sparing_tree_pdf = reports.sparring_tree.sparring_tree_report.SparringTreeReportPDF(registration_file_name, output_folder_path,
                                                                                            isCustomDivision=False)

    # print them out
    for evt in events:
        header = (
            f"event_time: {evt.event_time} \t| "
            f"division_name: {evt.division_name} | "
            f"gender: {evt.gender} |  "
            f"minimum_age: {evt.min_age} | "
            f" maximum_age: {evt.max_age} | "
            f"ranks_label: {evt.rank_label} | "
            f"ranks: {evt.ranks} 7| "
            f"ring_info: {evt.ring_info}"
        )
        print(header)


        division_type = classify_division(evt.division_name)
        if division_type == "Kata":
            ltt.writeSingleKataScoreSheetandDivisionReport(evt.event_time, evt.division_name, evt.gender, evt.rank_label, evt.min_age, evt.max_age, evt.ring_info, evt.ranks, clean_df)
        elif division_type == "Techniques":
            ltt.writeSingleTechniqueScoreSheetandDivisionReport(evt.event_time, evt.division_name, evt.gender, evt.rank_label, evt.min_age, evt.max_age, evt.ring_info, evt.ranks, clean_df)
        elif division_type == "Weapons":
            ltt.writeWeaponsDivisionToSingleKataScoreSheetandDivisionReport(evt.event_time, evt.division_name, evt.gender, evt.rank_label, evt.min_age, evt.max_age, evt.ring_info, evt.ranks, clean_df)
        elif division_type == "Sparring":
            ltt.writeSingleSparringTreeandDivisionReport(evt.event_time, evt.division_name, evt.gender, evt.rank_label, evt.min_age, evt.max_age, evt.ring_info, evt.ranks, clean_df)
        else:
            assert False, "Error: Invalid division_name"


    logging.info("Saving PDFs to disk")

    logging.info("..Saving Working Guide Report")
    test=ltt.division_detail_report_pdf.summary_info
    working_guide_list, working_guide_dataframe = ltt.tournament_summary_report_pdf.build_working_guide_data(ltt.division_detail_report_pdf.summary_info)
    ltt.tournament_summary_report_pdf.add_summary_info_to_page(working_guide_list)

    # call new code that will send the working_guide_dataframe to the judge assignment google sheet
    # try:
    #     spreadsheet_id = working_guide_google_sheet.upload_working_guide_dataframe(working_guide_dataframe)
    #     if spreadsheet_id:
    #         logging.info("Working guide Google Sheet updated. Spreadsheet ID: %s", spreadsheet_id)
    # except working_guide_google_sheet.WorkingGuideGoogleSheetError as exc:
    #     logging.error("Unable to update working guide Google Sheet: %s", exc)
    spreadsheet_id = working_guide_google_sheet.upload_working_guide_dataframe(working_guide_dataframe)
    if spreadsheet_id:
        logging.info("Working guide Google Sheet updated. Spreadsheet ID: %s", spreadsheet_id)

    

    ltt.tournament_summary_report_pdf.write_pdfpage()

    logging.info("..Saving Division Report")
    ltt.division_detail_report_pdf.write_pdfpage()

    logging.info("..Saving Kata Score Sheets")
    ltt.kata_score_sheet_pdf.write_pdfpage()
    logging.info("..Saving Technique Score Sheets")
    ltt.technique_score_sheet_pdf.write_pdfpage()
    logging.info("..Saving Sparring Trees")
    ltt.sparing_tree_pdf.close()

    logging.info("Division Summary Report")
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    logging.info(ltt.division_detail_report_pdf.summary_info)

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

    # except Exception as e:            #<--- un-comment for final distribution
    #     logging.error(f'Fatal error processing the data:\n {e}')
    #     exc = sys.exception()
    #     logging.error(repr(traceback.format_tb(exc.__traceback__)))

    logging.info("Done!")


if __name__ == "__main__":
    # Set cwd to the directory containing this script
    # os.chdir(Path(__file__).parent)
    ring_definition_file_path = Path(__file__).parent
    os.chdir(Path(__file__).parent.parent.parent)



    # hard code registration file name, ring definition file name, and output folder path for now
    registration_file_name = "/Users/johnfunk/documents/Tournaments/2025-May-03/RegExp_LizTrialFile_20250425-FixedHeaders_Processed.csv"
    # ring_definition_file_name = ring_definition_file_path / "Tourn Ring Envelope Data Base_2025_05_03-fixed_rank+fixed_ring_numbers.csv"
    ring_definition_file_name = ring_definition_file_path / "Tourn Ring Envelope Data Base_2025_05_03-proposed.csv"

    output_folder_path = "test_output"
    os.makedirs(output_folder_path, exist_ok=True)

    #setup logging
    errorLogFileName = registration_file_name[0:len(registration_file_name) - 4] + "-Error.txt"

    logger = logging.getLogger('')
    logger.setLevel(logging.INFO)
    fh = logging.FileHandler(errorLogFileName)
    sh = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s %(message)s', datefmt='%H:%M:%S')
    fh.setFormatter(formatter)
    sh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(sh)

    logging.info("Reading the data from:" + registration_file_name + "....")


    #### read and clean the registration data
    CI.set_utf_encoding()
    CI.clean_unicode_from_file(registration_file_name)

    # rename all the columns in the dataframe to usable names
    r = RN.RenameColumns(registration_file_name)
    r.rename_all_columns()
    renamed_df = r.get_dataframe_copy()

    input_error_list = input_errors.InputErrors()
    clean_df, error_count = CI.clean_all_input_errors(renamed_df, input_error_list)
    del renamed_df  # make sure we don't use the renamed_df again
    # logging.info(f'Input Errors:{input_error_list.error_list}')
    if error_count > 0:
        sys.exit("Exiting - The input must be fixed manually")

    # clean_df['hitcount'] = 0  # setup a new column for hit rate.

    process_registrations_with_ring_envelope_data(ring_definition_file_name, registration_file_name, clean_df, output_folder_path)
