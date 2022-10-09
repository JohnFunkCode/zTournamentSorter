#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  5 20:36:56 2016

@author: john funk
"""
import pandas
import datetime
import time

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from reportlab.platypus import PageBreak
from reportlab.platypus import SimpleDocTemplate, Spacer, Table, TableStyle
import domain_model.constants as constants


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

        if df.shape[0] > constants.TOO_MANY_COMPETITORS:
            print("\u001b[31m*** Warning: {} {} Ring {} has too many competitors. It has {}\u001b[0m".format(event_time,division_name,ring_number,df.shape[0]))

        if split_warning_text is None:
            headerdata2 = [['RING', ring_number + '   ' + event_time],
                           ['DIVISION', division_name],
                           ['AGE', age],
                           ['RANKS', belts],
                           ['COMPETITORS',df.shape[0]]]
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
                           ['RANKS', belts, split_warning_text],
                           ['COMPETITORS',df.shape[0]]]
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

        #insert number into the dataframe
        number_list=[*range(1,df.shape[0]+1)]
        df.insert(1,'#',number_list)

        #remove the Registrant_ID Column if it exists
        column_list = df.columns.values.tolist()
        if ('Registrant_ID' in column_list):
            df_for_printing=df.drop(columns="Registrant_ID")

        #remove the Events Column if it exists
        column_list = df_for_printing.columns.values.tolist()
        if ('Events' in column_list):
            df_for_printing=df_for_printing.drop(columns="Events")

        # remove the Weapons Column if it exists
        column_list = df_for_printing.columns.values.tolist()
        if ('Weapons' in column_list):
            df_for_printing = df_for_printing.drop(columns="Weapons")

        # remove the Height Column if it exists
        column_list = df_for_printing.columns.values.tolist()
        if ('Height' in column_list):
            df_for_printing = df_for_printing.drop(columns="Height")

        data_list = [df_for_printing.columns[:, ].values.astype(str).tolist()] + df_for_printing.values.tolist()

        t = Table(data_list)
        if len(data_list) > constants.TOO_MANY_COMPETITORS +1 :
            t.setStyle(TableStyle([('FONTNAME', (0, 0), (-1, -1), "Helvetica"),
                                   ('FONTSIZE', (0, 0), (-1, -1), 8),
                                   ('TEXTCOLOR', (0, 0), (-1, -1), colors.red),
                                   ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                                   ('BOX', (0, 0), (-1, -1), 0.25, colors.black)]))
        else:
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


    ###############################################################################
    # writeSingleDivisionDetailReport
    #  This method provides a re-usable method to write output to the Divsion Detail Report PDF

    def writeSingleDivisionDetailReport(self,event_time: str, division_name: str, division_type: str, gender: str, rank_label:str, minimum_age: int, maximum_age: int, rings: list, ranks:list, clean_df: pandas.DataFrame):
        if(maximum_age==100):
            age_label= '{0}+'.format(minimum_age)
        else:
            age_label= '{0}-{1}'.format(minimum_age,maximum_age)

        # Hack for 3 year olds
        if minimum_age==4:
            minimum_age=2

        print(time.strftime("%X") + " Generating Detail Report PDF for " + event_time + " " + division_name + " " + age_label)

        self.set_title(division_name)

        age_query= 'Age >={0} and Age <={1}'.format(minimum_age,maximum_age)

        rank_query=''
        for r in range(0, len(ranks)):
            rank_query=rank_query + 'Rank =="' + ranks[r] + '"'
            if r<len(ranks)-1:  #Add ' and ' to everything but the last one
                rank_query=rank_query + ' or '

        assert division_type == 'Weapons' or division_type=='Sparring' or division_type=='Forms', "Error: Invalid division_type"
        if division_type == 'Weapons':
            division_type_query='Weapons.str.contains("Weapons")'
        else:
            division_type_query='Events.str.contains("'+division_type+'")'

        if gender != '*':
            gender_query= 'Gender == "'+ gender +'"'
            combined_query='({0}) and ({1}) and ({2}) and ({3})'.format(division_type_query,age_query,rank_query,gender_query)
        else:
            combined_query='({0}) and ({1}) and ({2})'.format(division_type_query, age_query,rank_query)

        #wmk = clean_df.query(combined_query).sort_values("Age").sort_values("BMI")
        wmk=clean_df[["Registrant_ID", "First_Name", "Last_Name", "Gender", "Dojo", "Age", "Rank", "Feet", "Inches", "Height",
             "Weight", "BMI",
             "Events", "Weapons"]].query(combined_query).sort_values("Age").sort_values("BMI")

        if len(rings)>1:

            # filter to only keep contestants who's last name fall into the first alphabetic split
            first_alphabetic_split = wmk[wmk['Last_Name'].str.contains(constants.FIRST_ALPHABETIC_SPLIT_REGEX)]

            # filter to only keep contestants who's last name fall into the second alphabetic split
            second_alphabetic_split = wmk[wmk['Last_Name'].str.contains(constants.SECOND_ALPHABETIC_SPLIT_REGEX)]

            self.put_dataframe_on_pdfpage(first_alphabetic_split, str(rings[0]), event_time,
                                                               division_name, age_label,
                                                               rank_label +"(" + constants.FIRST_ALPHABETIC_SPLIT_LABEL + ")",
                                                               "*** PLEASE NOTE - These are contestants " + constants.FIRST_ALPHABETIC_SPLIT_LABEL)

            self.put_dataframe_on_pdfpage(second_alphabetic_split, str(rings[1]), event_time,
                                                               division_name, age_label,
                                                               rank_label +"(" + constants.SECOND_ALPHABETIC_SPLIT_LABEL + ")",
                                                               "*** PLEASE NOTE - These are contestants " + constants.SECOND_ALPHABETIC_SPLIT_LABEL)
        else:
            self.put_dataframe_on_pdfpage(wmk, str(rings[0]), event_time, division_name, age_label, rank_label)


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
