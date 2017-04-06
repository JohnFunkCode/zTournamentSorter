#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed April 5 2017

@author: john funk
"""

#
import pandas as pd
import numpy as np

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter, landscape, portrait
from reportlab.platypus import PageBreak
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
import datetime
from reportlab.lib.utils import ImageReader

class KataScoreSheetPDF(object):
    def __init__(self):
        self.doc = SimpleDocTemplate("KataScoreSheet.pdf", pagesize=portrait(letter))
        self.docElements = []
        #setup the package scoped global variables we need
        now = datetime.datetime.now()
        KataScoreSheetPDF.timestamp = now.strftime("%Y-%m-%d %H:%M")
        KataScoreSheetPDF.sourcefile = "not initialized"
        KataScoreSheetPDF.pageinfo = "not initialized"
        KataScoreSheetPDF.Title = "not initialized"
        KataScoreSheetPDF.PAGE_HEIGHT = defaultPageSize[1];
        KataScoreSheetPDF.PAGE_WIDTH = defaultPageSize[0]
        KataScoreSheetPDF.styles = getSampleStyleSheet()   #sample style sheet doesn't seem to be used

    @staticmethod
    def set_title(title):
        KataScoreSheetPDF.Title = title

    @staticmethod
    def set_pageInfo(pageinfo):
        KataScoreSheetPDF.pageinfo = pageinfo

    @staticmethod
    def set_sourcefile(sourcefile):
        KataScoreSheetPDF.sourcefile = sourcefile

    def put_dataframe_on_pdfpage(self, df, ring_number, event_time, division_name, age, belts):
        elements = []
        #   elements = [Spacer(1,2*inch)]

        # Title
        #    style = styles["Title"]
        #    normal.alignmnet = TA_RIGHT
        #    normal.fontName = "Helvetica"
        #    normal.fontSize = 28
        #    normal.leading = 15
        #    p = Paragraph("Ring Number: "+ring_number, style)
        #    elements.append(p)
        #    p = Paragraph(division_name, style)
        #    elements.append(p)
        #    p = Paragraph("Age: "+age+".............."+belts, style)
        #    elements.append(p)
        #    elements.append(Spacer(1,0.2*inch))

        headerdata = [["Ring: " + ring_number + " " + event_time, division_name],
                      ["Age: " + age, belts]]
        t = Table(headerdata)
        t.setStyle(TableStyle([('FONTNAME', (0, 0), (1, -1), "Helvetica"),
                               ('TEXTCOLOR', (0, 0), (1, -1), colors.black),
                               ('FONTSIZE', (0, 0), (1, -1), 28),
                               ('RIGHTPADDING', (0, 0), (1, 1), 50),
                               ('LEADING', (0, 0), (1, -1), 40)]))
        elements.append(t)
        elements.append(Spacer(1, 0.2 * inch))

        # Data Frame
        #  Convert data fram to a list format
        data_list = [df.columns[:, ].values.astype(str).tolist()] + df.values.tolist()

        t = Table(data_list)
        t.setStyle(TableStyle([('FONTNAME', (0, 0), (-1, -1), "Helvetica"),
                               ('FONTSIZE', (0, 0), (-1, -1), 8),
                               ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                               ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                               ('BOX', (0, 0), (-1, -1), 0.25, colors.black)]))
        elements.append(t)
        elements.append(Spacer(1, 0.2 * inch))
        elements.append(PageBreak())

        #    # write the document to disk
        #    doc.build(elements)

        ####tbd - fiture out how to add a page break, and also add headers and footers
        self.docElements.extend(elements)
        return elements;

    def write_pdfpage(self):
        self.doc.build(self.docElements, onFirstPage=first_page_layout, onLaterPages=page_layout)


# define layout for first page
def first_page_layout(canvas, doc):
    canvas.saveState()
    logo = ImageReader('../Z_LOGO_HalfInch.jpg')
    canvas.drawImage(logo, .25 * inch, 7.5 * inch, mask='auto')
    canvas.setFont('Times-Bold', 16)
    #    canvas.drawCentredString(PAGE_WIDTH/2.0, PDFReport.PAGE_HEIGHT-108, PDFReport.Title)
    canvas.drawCentredString(KataScoreSheetPDF.PAGE_WIDTH / 2.0, 8 * inch, "Forms")
    canvas.setFont('Times-Bold', 9)
    canvas.drawCentredString(KataScoreSheetPDF.PAGE_WIDTH / 2.0, 8 * inch, "Score Sheet")


    canvas.setFont('Times-Roman', 9)
    canvas.drawString(inch, 0.75 * inch, "First Page / %s" % KataScoreSheetPDF.pageinfo)
    canvas.restoreState()

# define layout for subsequent pages
def later_page_layout(canvas, doc):
    canvas.saveState()
    canvas.setFont('Times-Roman', 9)
    canvas.drawString(inch, 0.75 * inch, "Page %d %s" % (doc.page, KataScoreSheetPDF.pageinfo))
    canvas.restoreState()

# define layout for subsequent pages
def page_layout(canvas, doc):
    canvas.saveState()
    logo = ImageReader('Z_LOGO_HalfInch.jpg')
    canvas.drawImage(logo, .25 * inch, 7.5 * inch, mask='auto')
    canvas.setFont('Times-Roman', 9)
    canvas.drawString(inch * 3, 0.75 * inch,
                      "Page: %d     Generated: %s     From file: %s" % (
                          doc.page, KataScoreSheetPDF.timestamp, KataScoreSheetPDF.sourcefile))
    canvas.restoreState()


if __name__ == "__main__":
  #setup the Kata Score Sheet PDF
  kata_score_sheet=KataScoreSheetPDF()
  KataScoreSheetPDF.set_title("Kata Score Sheet")
  KataScoreSheetPDF.set_sourcefile("testing//no//file//name")

  # create a test data frame
  index = ['a', 'b', 'c', 'd']
  columns = ['one', 'two', 'three', 'four']
  df = pd.DataFrame(np.random.randn(4, 4), index=index, columns=columns)
  data = [df.columns[:, ].values.astype(str).tolist()] + df.values.tolist()

  kata_score_sheet.put_dataframe_on_pdfpage(df,"Ring1","22:22","KataDivision","12-22","Black")
  # divison_detail_report_pdf.put_dataframe_on_pdfpage(wmk, "tba", event_time, division_name, age, "Weapons Division 6")

  kata_score_sheet.write_pdfpage()
