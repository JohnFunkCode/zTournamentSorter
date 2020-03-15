#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  5 20:36:56 2016

@author: john funk
"""

import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from reportlab.platypus import PageBreak
from reportlab.platypus import SimpleDocTemplate, Spacer, Table, TableStyle

class DivisionDetailReportPDF(object):
    def __init__(self):
        self.doc = SimpleDocTemplate("DivisionDetailReport.pdf", pagesize=landscape(letter),topMargin=0)
        self.docElements = []
        #setup the package scoped global variables we need
        now = datetime.datetime.now()
        DivisionDetailReportPDF.timestamp = now.strftime("%Y-%m-%d %H:%M")
        DivisionDetailReportPDF.sourcefile = "not initialized"
        DivisionDetailReportPDF.pageinfo = "not initialized"
        DivisionDetailReportPDF.Title = "not initialized"
        DivisionDetailReportPDF.PAGE_HEIGHT =  11 * inch
        DivisionDetailReportPDF.PAGE_WIDTH = 8.5 * inch
        DivisionDetailReportPDF.styles = getSampleStyleSheet()   #sample style sheet doesn't seem to be used

    @staticmethod
    def set_title(title):
        DivisionDetailReportPDF.Title = title

    @staticmethod
    def set_pageInfo(pageinfo):
        DivisionDetailReportPDF.pageinfo = pageinfo

    @staticmethod
    def set_sourcefile(sourcefile):
        DivisionDetailReportPDF.sourcefile = sourcefile

    def put_dataframe_on_pdfpage(self, df, ring_number, event_time, division_name, age, belts, split_warning_text=None):
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

        headerdata1 = [['Division Detail Report','']]

        t = Table(headerdata1)

        t.setStyle(TableStyle([('FONTNAME', (0, 0), (1, -1), "Times-Bold"),
                               ('TEXTCOLOR', (0, 0), (1, -1), colors.black),
                               ('FONTSIZE', (0, 0), (1, -1), 20),
                               ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                               ('LEADING', (0, 0), (1, -1), 9)]))

        elements.append(t)
        elements.append(Spacer(1, 0.1 * inch))

        if split_warning_text is None:
            headerdata2 = [['RING', ring_number + '   ' + event_time],
                           ['DIVISION', division_name],
                           ['AGE', age],
                           ['RANKS', belts]]
            t = Table(headerdata2)

            # remember table styles attributes specified as From (Column,Row), To (Column,Row)
            # - see reportlab users guide chapter 7, page 78 for details
            t.setStyle(TableStyle([('FONTNAME', (0, 0), (1, -1), "Times-Bold"),
                                   ('TEXTCOLOR', (0, 0), (1, -1), colors.black),
                                   ('FONTSIZE', (0, 0), (1, -1), 10),
                                   ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
                                   ('ALIGN', (1, 0), (1, -1), 'LEFT'),
                                   ('LEADING', (0, 0), (1, -1), 7)]))
        else:
            headerdata2 = [['RING', ring_number + '   ' + event_time, ''],
                           ['DIVISION', division_name, ''],
                           ['AGE', age, ''],
                           ['RANKS', belts, split_warning_text]]
            t = Table(headerdata2)

            # remember table styles attributes specified as From (Column,Row), To (Column,Row)
            # - see reportlab users guide chapter 7, page 78 for details
            t.setStyle(TableStyle([('FONTNAME', (0, 0), (-1, -1), "Times-Bold"),
                                   ('TEXTCOLOR', (2, 0), (-1, -1), colors.red),
                                   ('FONTSIZE', (0, 0), (2, -1), 10),
                                   ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
                                   ('ALIGN', (1, 0), (1, -1), 'LEFT'),
                                   ('ALIGN', (2, 0), (2, -1), 'LEFT'),
                                   ('LEADING', (0, 0), (-1, -1), 7)]))

        # headerdata2 = [['RING', ring_number + '   ' + event_time],
        #                ['DIVISION', division_name],
        #                ['AGE', age],
        #                ['RANKS', belts]]
        #
        # t = Table(headerdata2)
        #
        # t.setStyle(TableStyle([('FONTNAME', (0, 0), (1, -1), "Times-Bold"),
        #                        ('TEXTCOLOR', (0, 0), (1, -1), colors.black),
        #                        ('FONTSIZE', (0, 0), (1, -1), 10),
        #                        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        #                        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        #                        ('LEADING', (0, 0), (1, -1), 7)]))


        elements.append(t)
        elements.append(Spacer(1, 0.1 * inch))

        # headerdata = [["Ring: " + ring_number + " " + event_time, division_name],
        #               ["Age: " + age, belts]]
        # t = Table(headerdata)
        # t.setStyle(TableStyle([('FONTNAME', (0, 0), (1, -1), "Helvetica"),
        #                        ('TEXTCOLOR', (0, 0), (1, -1), colors.black),
        #                        ('FONTSIZE', (0, 0), (1, -1), 28),
        #                        ('RIGHTPADDING', (0, 0), (1, 1), 50),
        #                        ('LEADING', (0, 0), (1, -1), 40)]))
        # elements.append(t)
        # elements.append(Spacer(1, 0.2 * inch))

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
 #       self.doc.build(self.docElements)

        return elements;

    def write_pdfpage(self):
        self.doc.build(self.docElements, onFirstPage=page_layout, onLaterPages=page_layout)


# define layout for first page
def first_page_layout(canvas, doc):
    canvas.saveState()
    canvas.setFont('Times-Bold', 16)
    #    canvas.drawCentredString(PAGE_WIDTH/2.0, PDFReport.PAGE_HEIGHT-108, PDFReport.Title)
    canvas.drawCentredString(DivisionDetailReportPDF.PAGE_WIDTH / 2.0, 8 * inch, DivisionDetailReportPDF.Title)
    canvas.setFont('Times-Roman', 9)
    canvas.canvas.drawCentredString(DivisionDetailReportPDF.PAGE_WIDTH / 2.0, 0.25 * inch, "First Page / %s" % DivisionDetailReportPDF.pageinfo)
    canvas.restoreState()

# define layout for subsequent pages
def later_page_layout(canvas, doc):
    canvas.saveState()
    #logo = ImageReader('Z_LOGO_HalfInch.jpg')
    #canvas.drawImage(logo, .25 * inch, 7.5 * inch, mask='auto')
    canvas.setFont('Times-Roman', 9)
    canvas.drawCentredString(DivisionDetailReportPDF.PAGE_WIDTH / 2.0, 0.25 * inch,
                      "Page: %d   Generated: %s   From file: %s" % (
                          doc.page, DivisionDetailReportPDF.timestamp, DivisionDetailReportPDF.sourcefile))
    canvas.restoreState()

# define layout for subsequent pages
def page_layout(canvas, doc):
    canvas.saveState()
    logo = ImageReader('Z_LOGO_HalfInch.jpg')
    canvas.drawImage(logo, .25 * inch, 7.5 * inch, mask='auto')
    canvas.setFont('Times-Roman', 9)
    canvas.drawCentredString(DivisionDetailReportPDF.PAGE_WIDTH / 2.0, 0.25 * inch,
                      "Page: %d   Generated: %s   From file: %s" % (
                          doc.page, DivisionDetailReportPDF.timestamp, DivisionDetailReportPDF.sourcefile))
    canvas.restoreState()

########
# main
#
# doc = SimpleDocTemplate("simple_table.pdf", pagesize=landscape(letter))
# docElements = []
#
# Title = "Hello World"
# pageinfo = "PlatypusTable2 example"
# now = datetime.datetime.now()
# timestamp = now.strftime("%Y-%m-%d %H:%M")
# sourcefile = "RegistrantExport_EM0393 Liz 10-19-2016 Clean.csv"
#
# PAGE_HEIGHT = defaultPageSize[1];
# PAGE_WIDTH = defaultPageSize[0]
# styles = getSampleStyleSheet()
#
# # my data frame
# index = ['a', 'b', 'c', 'd']
# columns = ['one', 'two', 'three', 'four']
# df = pd.DataFrame(np.random.randn(4, 4), index=index, columns=columns)
# data = [df.columns[:, ].values.astype(str).tolist()] + df.values.tolist()
#
# pdfg=Reporting()
# stuff=pdfg.put_dataframe_on_pdfpage(data, doc, "2", "1:00pm", "Senion Mens Kata", "35+", "Green, Green Stripe")
# docElements.extend(stuff)
# #docElements.extend(Reporting.put_dataframe_on_pdfpage(data, doc, "1", "9:00am", "Boys & Girls Kata", "10-13", "Blue/Blue Green"))
#
# index = ['a', 'b', 'c', 'd', 'e']
# columns = ['one', 'two', 'three', 'four', 'five']
# df2 = pd.DataFrame(np.random.randn(5, 5), index=index, columns=columns)
# data = [df2.columns[:, ].values.astype(str).tolist()] + df2.values.tolist()
#
# #docElements.extend(pdfg.put_dataframe_on_pdfpage(data, doc, "2", "1:00pm", "Senion Mens Kata", "35+", "Green, Green Stripe"))
#
# # write the document to disk
# doc.build(docElements, onFirstPage=pdfg.page_layout, onLaterPages=pdfg.page_layout)
#
