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
from reportlab.lib.pagesizes import letter, portrait, landscape
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
        self.filename_with_path = f'{pathlib.Path(output_folder_path)}{reports.FileHandlingUtilities.pathDelimiter()}{"TournamentSummaryReport.pdf"}'
        # self.filename_with_path=str(pathlib.Path(output_folder_path + FileHandlingUtilities.reports.FileHandlingUtilities.pathDelimiter() +'TournamentSummaryReport.pdf')) #<--un-comment for stand alone test files

        # self.doc = SimpleDocTemplate("TournamentSummaryReport.pdf", pagesize=portrait(letter),topMargin=0, bottomMargin=0)
        self.doc = SimpleDocTemplate(self.filename_with_path, pagesize=landscape(letter),topMargin=0, bottomMargin=0, leftMargin=0, rightMargin=0)
        self.docElements = []
        
        #setup the package scoped global variables we need
        now = datetime.datetime.now()
        TournamentSummaryReport.timestamp = now.strftime("%Y-%m-%d %H:%M")
        # TournamentSummaryReport.sourcefile = "not initialized"
        TournamentSummaryReport.sourcefile = data_file_name
        TournamentSummaryReport.pageinfo = "not initialized"
        # TournamentSummaryReport.Title = "not initialized"
        TournamentSummaryReport.Title = title
        TournamentSummaryReport.PAGE_HEIGHT = 11 * inch
        TournamentSummaryReport.PAGE_WIDTH = 8.5 * inch
        TournamentSummaryReport.ring_number= "not initialized"
        TournamentSummaryReport.event_time= "not initialized"
        TournamentSummaryReport.division_name= "not initialized"
        TournamentSummaryReport.age= "not initialized"
        TournamentSummaryReport.belts= "not initialized"
        # TournamentSummaryReport.split_warning_text="not initialized"

    @staticmethod
    def set_title(title):
        TournamentSummaryReport.Title = title

    @staticmethod
    def set_pageInfo(pageinfo):
        TournamentSummaryReport.pageinfo = pageinfo

    @staticmethod
    def set_sourcefile(sourcefile):
        TournamentSummaryReport.sourcefile = sourcefile

    def add_division_details(self,event_time: str, division_name: str, division_type: str, gender: str, rank_label:str, minimum_age: int, maximum_age: int, rings: list, ranks:list, division_competitors: pandas.DataFrame):
        logging.info( f'division summary:{event_time} {division_name}  {division_type} {gender} {rank_label} {minimum_age} {maximum_age} {rings} {ranks}')
        logging.info( f'{division_competitors}')

    def add_summary_info_to_page(self, summary_info: pd.DataFrame):
        # logging.info( f'summary_info:{summary_info}')
        elements = []
        # data_list = [summary_info.columns[:, ].values.astype(str).tolist()] + summary_info.values.tolist()
        data_list = [summary_info.columns.astype(str).tolist()] + summary_info.astype(str).values.tolist()

        t=Table(data_list)

        t.setStyle(TableStyle([('FONTNAME', (0, 0), (-1, -1), "Helvetica"),
                               ('FONTSIZE', (0, 0), (-1, -1), 8),
                               ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                               ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                               ('BOX', (0, 0), (-1, -1), 0.25, colors.black)]))

        elements.append(t)
        
        self.docElements.extend(elements)
        return elements;

    def write_pdfpage(self):
        self.doc.build(self.docElements, onFirstPage=page_layout, onLaterPages=page_layout)


#
# # define layout for first page
# def first_page_layout(canvas, doc):
#     canvas.saveState()
#     canvas.setFont('Times-Bold', 16)
#     #    canvas.drawCentredString(PAGE_WIDTH/2.0, PDFReport.PAGE_HEIGHT-108, PDFReport.Title)
#     canvas.drawCentredString(TournamentSummaryReport.PAGE_WIDTH / 2.0, 8 * inch, TournamentSummaryReport.Title)
#     canvas.setFont('Times-Roman', 9)
#     canvas.canvas.drawCentredString(TournamentSummaryReport.PAGE_WIDTH / 2.0, 0.25 * inch, "First Page / %s" % TournamentSummaryReport.pageinfo)
#     canvas.restoreState()
#
# # define layout for subsequent pages
# def later_page_layout(canvas, doc):
#     canvas.saveState()
#     #logo = ImageReader('Z_LOGO_HalfInch.jpg')
#     #canvas.drawImage(logo, .25 * inch, 7.5 * inch, mask='auto')
#     canvas.setFont('Times-Roman', 9)
#     canvas.drawCentredString(TournamentSummaryReport.PAGE_WIDTH / 2.0, 0.25 * inch,
#                       "Page: %d   Generated: %s   From file: %s" % (
#                                  doc.page, TournamentSummaryReport.timestamp, TournamentSummaryReport.sourcefile))
#     canvas.restoreState()

# define layout for subsequent pages
def page_layout(canvas, doc):
    return
    canvas.saveState()
    logo = ImageReader('Z_LOGO_HalfInch.jpg')
    canvas.drawImage(logo, .25 * inch, 8.0 * inch, mask='auto')
    canvas.setFont('Times-Roman', 9)
    canvas.drawCentredString(TournamentSummaryReport.PAGE_WIDTH / 2.0, 0.25 * inch,
                      "Page: %d   Generated: %s   From file: %s" % (
                                 doc.page, TournamentSummaryReport.timestamp, TournamentSummaryReport.sourcefile))
    canvas.restoreState()
   
    
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
    # TSR_pdf.add_division_details(event_time="9:00am",division_name="Kids Kata",division_type="Forms",gender="*",rank_label="White",                     minimum_age=4, maximum_age=6, rings=[[1,'A','Z']],  ranks=[constants.WHITE_BELT], division_competitors=competitors)

    summary_info = pd.DataFrame(
        columns=['Event_Time', 'Division_Name', 'Division_Type', 'Gender', 'Rank_Label', 'Minimum_Age', 'Maximum_Age',
                 'Rings', 'Competitors'])

    event_time="9:00am"
    division_name="Kids Kata"
    division_type="Forms"
    gender="*"
    rank_label="White"
    minimum_age=4
    maximum_age=6
    rings=[[1,'A','Z']]
    ranks=[constants.WHITE_BELT],
    division_competitors=competitors

    new_row = {'Event_Time': event_time, 'Division_Name': division_name, 'Division_Type': division_type,
               'Gender': gender, 'Rank_Label': rank_label, 'Minimum_Age': minimum_age, 'Maximum_Age': maximum_age,
               'Rings': rings, 'Competitors': "test"}

    summary_info.loc[len(summary_info)] = new_row

    TSR_pdf.add_summary_info_to_page(summary_info)
    TSR_pdf.write_pdfpage()

if __name__ == "__main__":
    main()
