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
from reportlab.platypus import PageBreak, KeepTogether
from reportlab.platypus import SimpleDocTemplate, Spacer, Table, TableStyle

import domain_model.constants as constants
import reports
import reports.FileHandlingUtilities


class WorkingGuideReport():

    def __init__(self, title:str, data_file_name: str, output_folder_path:str):
        self.filename_with_path = f'{pathlib.Path(output_folder_path)}{reports.FileHandlingUtilities.pathDelimiter()}{"WorkingGuideReport.pdf"}'
        # self.filename_with_path=str(pathlib.Path(output_folder_path + FileHandlingUtilities.reports.FileHandlingUtilities.pathDelimiter() +'WorkingGuideReport.pdf')) #<--un-comment for stand alone test files

        # self.doc = SimpleDocTemplate("WorkingGuideReport.pdf", pagesize=portrait(letter),topMargin=0, bottomMargin=0)
        self.doc = SimpleDocTemplate(self.filename_with_path, pagesize=portrait(letter),topMargin=0, bottomMargin=0, leftMargin=0, rightMargin=0)
        self.docElements = []
        
        #setup the package scoped global variables we need
        now = datetime.datetime.now()
        WorkingGuideReport.timestamp = now.strftime("%Y-%m-%d %H:%M")
        # WorkingGuideReport.sourcefile = "not initialized"
        WorkingGuideReport.sourcefile = data_file_name
        WorkingGuideReport.pageinfo = "not initialized"
        # WorkingGuideReport.Title = "not initialized"
        WorkingGuideReport.Title = title
        WorkingGuideReport.PAGE_HEIGHT = 11 * inch
        WorkingGuideReport.PAGE_WIDTH = 8.5 * inch
        WorkingGuideReport.ring_number= "not initialized"
        WorkingGuideReport.event_time= "not initialized"
        WorkingGuideReport.division_name= "not initialized"
        WorkingGuideReport.age= "not initialized"
        WorkingGuideReport.belts= "not initialized"
        # WorkingGuideReport.split_warning_text="not initialized"

    @staticmethod
    def set_title(title):
        WorkingGuideReport.Title = title

    @staticmethod
    def set_pageInfo(pageinfo):
        WorkingGuideReport.pageinfo = pageinfo

    @staticmethod
    def set_sourcefile(sourcefile):
        WorkingGuideReport.sourcefile = sourcefile

    def add_division_details(self,event_time: str, division_name: str, division_type: str, gender: str, rank_label:str, minimum_age: int, maximum_age: int, rings: list, ranks:list, division_competitors: pandas.DataFrame):
        logging.info( f'division summary:{event_time} {division_name}  {division_type} {gender} {rank_label} {minimum_age} {maximum_age} {rings} {ranks}')
        logging.info( f'{division_competitors}')


    def add_summary_info_to_page(self, summary_info: pd.DataFrame):
        # Keep each Event_Time group together and sort chronologically.
        elements = []
        if summary_info is None or summary_info.empty:
            return elements

        detail_cols = [c for c in summary_info.columns if c != "Event_Time"]
        if not detail_cols:
            return elements

        df = summary_info.copy()

        # Build a sortable time key from 'Event_Time' like '9:05 a.m.'/'9:05 am'/'9:05am'
        import re
        def _normalize_event_time(s):
            if pd.isna(s):
                return None
            s = str(s).strip().lower().replace(".", "")
            # remove whitespace before am/pm (e.g., '9:00 am' -> '9:00am')
            s = re.sub(r"\s*(am|pm)$", r"\1", s)
            return s

        df["_EventTimeKey"] = pd.to_datetime(
            df["Event_Time"].map(_normalize_event_time),
            format="%I:%M%p",
            errors="coerce",
        )

        # Ensure string rendering for ReportLab cells (leave the key as datetime)
        for c in df.columns:
            if c != "_EventTimeKey":
                df[c] = df[c].astype(str)

        # Iterate groups in true chronological order
        for event_time, group in df.sort_values("_EventTimeKey", kind="mergesort").groupby("Event_Time", sort=False):
            rows = []
            # Group header spanning all columns
            # rows.append([f"Event Time: {event_time}"] + [""] * (len(detail_cols) - 1))
            rows.append([f"{event_time}"] )
            # Detail column headers
            rows.append([str(c) for c in detail_cols])
            # Group detail rows
            for _, r in group.iterrows():
                rows.append([r[c] for c in detail_cols])

            t = Table(rows, hAlign="LEFT")
            style = TableStyle([
                ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("TEXTCOLOR", (0, 0), (-1, -1), colors.black),
                ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.black),
                ("BOX", (0, 0), (-1, -1), 0.25, colors.black),
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),

                # Event header row (row 0)
                ("SPAN", (0, 0), (-1, 0)),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 16),
                ("ALIGN", (0, 0), (-1, 0), "CENTER"),
                ("VALIGN", (0, 0), (-1, 0), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, 0), 8),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),

                # Detail column header row (row 1)
                ("FONTNAME", (0, 1), (-1, 1), "Helvetica-Bold"),
            ])
            t.setStyle(style)

            elements.append(KeepTogether([t, Spacer(0, 6)]))

        self.docElements.extend(elements)
        return elements

    def write_pdfpage(self):
        self.doc.build(self.docElements, onFirstPage=page_layout, onLaterPages=page_layout)


#
# # define layout for first page
# def first_page_layout(canvas, doc):
#     canvas.saveState()
#     canvas.setFont('Times-Bold', 16)
#     #    canvas.drawCentredString(PAGE_WIDTH/2.0, PDFReport.PAGE_HEIGHT-108, PDFReport.Title)
#     canvas.drawCentredString(WorkingGuideReport.PAGE_WIDTH / 2.0, 8 * inch, WorkingGuideReport.Title)
#     canvas.setFont('Times-Roman', 9)
#     canvas.canvas.drawCentredString(WorkingGuideReport.PAGE_WIDTH / 2.0, 0.25 * inch, "First Page / %s" % WorkingGuideReport.pageinfo)
#     canvas.restoreState()
#
# # define layout for subsequent pages
# def later_page_layout(canvas, doc):
#     canvas.saveState()
#     #logo = ImageReader('Z_LOGO_HalfInch.jpg')
#     #canvas.drawImage(logo, .25 * inch, 7.5 * inch, mask='auto')
#     canvas.setFont('Times-Roman', 9)
#     canvas.drawCentredString(WorkingGuideReport.PAGE_WIDTH / 2.0, 0.25 * inch,
#                       "Page: %d   Generated: %s   From file: %s" % (
#                                  doc.page, WorkingGuideReport.timestamp, WorkingGuideReport.sourcefile))
#     canvas.restoreState()

# define layout for subsequent pages
def page_layout(canvas, doc):
    # return
    canvas.saveState()
    # logo = ImageReader('Z_LOGO_HalfInch.jpg')
    # canvas.drawImage(logo, .25 * inch, 8.0 * inch, mask='auto')
    canvas.setFont('Times-Roman', 9)
    canvas.drawCentredString(WorkingGuideReport.PAGE_WIDTH / 2.0, 0.25 * inch,
                      "Page: %d   Generated: %s   From file: %s" % (
                                 doc.page, WorkingGuideReport.timestamp, WorkingGuideReport.sourcefile))
    canvas.restoreState()
   
    
def main():
    logger = logging.getLogger('')
    logger.setLevel(logging.INFO)
    fh = logging.FileHandler("WorkingGuideReport.log")
    sh = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s %(message)s', datefmt='%H:%M:%S')
    fh.setFormatter(formatter)
    sh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(sh)

    TSR_pdf = WorkingGuideReport("Working Guide Report", "DataFileName", "")
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
