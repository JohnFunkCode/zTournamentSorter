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


class TournamentSummaryReport():

    def __init__(self, title:str, data_file_name: str, output_folder_path:str):
        self.filename_with_path = f'{pathlib.Path(output_folder_path)}{reports.FileHandlingUtilities.pathDelimiter()}{"TournamentSummaryReport.pdf"}'
        # self.filename_with_path=str(pathlib.Path(output_folder_path + FileHandlingUtilities.reports.FileHandlingUtilities.pathDelimiter() +'TournamentSummaryReport.pdf')) #<--un-comment for stand alone test files

        # self.doc = SimpleDocTemplate("TournamentSummaryReport.pdf", pagesize=portrait(letter),topMargin=0, bottomMargin=0)
        self.doc = SimpleDocTemplate(self.filename_with_path, pagesize=portrait(letter),topMargin=0, bottomMargin=0, leftMargin=0, rightMargin=0)
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

    # def add_summary_info_to_page(self, summary_info: pd.DataFrame):
    #     # logging.info( f'summary_info:{summary_info}')
    #     elements = []
    #     # data_list = [summary_info.columns[:, ].values.astype(str).tolist()] + summary_info.values.tolist()
    #     data_list = [summary_info.columns.astype(str).tolist()] + summary_info.astype(str).values.tolist()
    #
    #     # # format a datalist with a header for the event time followed by columnar data with all the date for each event
    #     # data_list = []
    #     # print_columns = [c for c in summary_info.columns if c != "Event_Time"]
    #     # for _, row in summary_info.iterrows():
    #     #     data_list.append(f"=== Event Time: {row['Event_Time']} ===")
    #     #     # print the column headers in one line
    #     #     data_list.append("  ".join(print_columns))
    #     #     # print the row values in one line
    #     #     data_list.append("  ".join(str(row[c]) for c in print_columns))
    #     #     data_list.append("")  # blank line between events
    #
    #     t=Table(data_list)
    #
    #     t.setStyle(TableStyle([('FONTNAME', (0, 0), (-1, -1), "Helvetica"),
    #                            ('FONTSIZE', (0, 0), (-1, -1), 8),
    #                            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
    #                            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
    #                            ('BOX', (0, 0), (-1, -1), 0.25, colors.black)]))
    #
    #     elements.append(t)
    #
    #     self.docElements.extend(elements)
    #     return elements;

    # from reportlab.platypus import SimpleDocTemplate, Spacer, Table, TableStyle, KeepTogether

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
            rows.append([f"=== Event Time: {event_time} ==="] + [""] * (len(detail_cols) - 1))
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
                # Emphasis + span for the event header row
                ("SPAN", (0, 0), (-1, 0)),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                # Emphasis for the detail column header row
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
    # return
    canvas.saveState()
    # logo = ImageReader('Z_LOGO_HalfInch.jpg')
    # canvas.drawImage(logo, .25 * inch, 8.0 * inch, mask='auto')
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
