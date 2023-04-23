#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed April 5 2017

@author: john funk
"""

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


class KataScoreSheet(object):
    def __init__(self,title:str, sourcefile:str,output_folder_path:str, isCustomDivision: bool):
        if isCustomDivision:
            p=pathlib.Path(sourcefile)
            name_only = str(p.name)
            output_folder_path_no_extension = name_only[0:len(name_only)-4]
            self.filename_with_path = str(pathlib.Path(output_folder_path + reports.FileHandlingUtilities.pathDelimiter() + output_folder_path_no_extension + '-' + 'KataScoreSheet.pdf'))
        else:
            self.filename_with_path=str(pathlib.Path(output_folder_path + reports.FileHandlingUtilities.pathDelimiter() +'KataScoreSheet.pdf'))

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

    @staticmethod
    def set_title(title):
        KataScoreSheet.Title = title

    @staticmethod
    def set_pageInfo(pageinfo):
        KataScoreSheet.pageinfo = pageinfo

    @staticmethod
    def set_sourcefile(sourcefile):
        KataScoreSheet.sourcefile = sourcefile

    def convert_inputdf_to_outputdf(self,inputdf):
        columns = ['Compettitors Name', 'Form', 'Scores', '', 'Total', 'Place']
        data=[]
        outputdf = pd.DataFrame(data, columns=columns)

        counter=1
        for index, row in inputdf.iterrows():
            outputdf.at[index, 'Compettitors Name'] = str(counter) +") " + inputdf.at[index, 'First_Name'] + " " + inputdf.at[index, 'Last_Name'] + " " + inputdf.at[index, 'Dojo'] + "\n"
            outputdf.at[index, 'Form'] = ''
            outputdf.at[index,'Scores'] = ''
            outputdf.at[index,''] = ''
            outputdf.at[index,'Total'] = ''
            outputdf.at[index, 'Place'] = ''
            counter = counter+1

        return outputdf

    def put_dataframe_on_pdfpage(self, inputdf, ring_number, event_time, division_name, age, belts, split_warning_text=None):
        # put args in class variables so the static page header functions can use them
        KataScoreSheet.ring_number = ring_number
        KataScoreSheet.event_time = event_time
        KataScoreSheet.division_name = division_name
        KataScoreSheet.age = age
        KataScoreSheet.belts = belts

        elements = []

        headerdata1 = [[KataScoreSheet.Title, 'Score Sheet']]

        t = Table(headerdata1)

        # remember table styles attributes specified as From (Column,Row), To (Column,Row)
        # - see reportlab users guide chapter 7, page 78 for details
        t.setStyle(TableStyle([('FONTNAME', (0, 0), (1, -1), "Times-Bold"),
                               ('TEXTCOLOR', (0, 0), (1, -1), colors.black),
                               ('FONTSIZE', (0, 0), (1, -1), 20),
                               ('ALIGN', (0, 0), (1, 0), 'CENTER'),
                               ('LEADING', (0, 0), (1, -1), 9)]))

        elements.append(t)
        elements.append(Spacer(1, 0.1 * inch))

        if inputdf.shape[0] > constants.TOO_MANY_COMPETITORS:
            logging.warning("\u001b[31m*** {} {} Ring:{} has too many competitors. It has {}\u001b[0m".format(event_time,division_name,ring_number,inputdf.shape[0]))

        if split_warning_text is None:
            headerdata2 = [['RING', ring_number + '   ' + event_time],
                           ['DIVISION', division_name],
                           ['AGE', age],
                           ['RANKS', belts],
                           ['COMPETITORS',inputdf.shape[0]]]
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
                           ['DIVISION', division_name, '' ],
                           ['AGE', age,''],
                           ['RANKS', belts,split_warning_text],
                           ['COMPETITORS',inputdf.shape[0]]]
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


        t.setStyle(TableStyle([('FONTNAME', (0, 0), (1, -1), "Times-Bold"),
                               ('TEXTCOLOR', (0, 0), (1, -1), colors.black),
                               ('FONTSIZE', (0, 0), (1, -1), 10),
                               ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
                               ('ALIGN', (1, 0), (1, -1), 'LEFT'),
                               ('LEADING', (0, 0), (1, -1), 7)]))

        elements.append(t)
        elements.append(Spacer(1, 0.1 * inch))

        # Data Frame
        outputdf=self.convert_inputdf_to_outputdf(inputdf)

        #  Convert data frame to a list format
        data_list = [outputdf.columns[:, ].values.astype(str).tolist()] + outputdf.values.tolist()

        t = Table(data_list)
        if len(data_list) > constants.TOO_MANY_COMPETITORS +1:
            t.setStyle(TableStyle([('FONTNAME', (0, 0), (-1, -1), "Helvetica"),
                                   ('FONTSIZE', (0, 0), (-1, -1), 8),
                                   ('TEXTCOLOR', (0, 0), (-1, -1), colors.red),
                                   ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                                   ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                                   ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                                   ('SPAN', (2, 0), (3, 0)),
                                   ('BOX', (0, 0), (-1, -1), 0.25, colors.black)]))
        else:
            t.setStyle(TableStyle([('FONTNAME', (0, 0), (-1, -1), "Helvetica"),
                                   ('FONTSIZE', (0, 0), (-1, -1), 8),
                                   ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                                   ('BACKGROUND',(0,0),(-1,0),colors.lightgrey),
                                   ('ALIGN',(0,0),(-1,0),'CENTER'),
                                   ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                                   ('SPAN',(2,0),(3,0)),
                                   ('BOX', (0, 0), (-1, -1), 0.25, colors.black)]))


        t._argW[0] = 3 *inch
        t._argW[1] = 1.75 * inch
        t._argW[2] = 0.625 * inch
        t._argW[3] = 0.625 * inch
        t._argW[4] = 1 * inch
        t._argW[5] = 1 * inch
#        t._argH[1] = .4375 * inch



        elements.append(t)
        elements.append(Spacer(1, 0.2 * inch))
        elements.append(PageBreak())

        #    # write the document to disk
        #    doc.build(elements)

        ####tbd - figure out how to add a page break, and also add headers and footers
        self.docElements.extend(elements)
        return elements;

    def write_pdfpage(self):
        self.doc.build(self.docElements, onFirstPage=first_page_layout, onLaterPages=first_page_layout)

    ###############################################################################
    # writeSingleKataScoreSheet
    #  Fall 2020
    #  This method writes a single kata score sheet based on parameters provided
    #
    def writeSingleKataScoreSheet(self,event_time: str, division_name: str, division_type: str, gender: str, rank_label: str, minimum_age: int,
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

        assert division_type == 'Weapons' or division_type=='Forms', "Error: Invalid division_type"
        if division_type == 'Weapons':
            division_type_query='Weapons.str.contains("Weapons")'
        else:
            division_type_query='Events.str.contains("Forms")'

        if gender != '*':
            gender_query = 'Gender == "' + gender + '"'
            combined_query = f'({division_type_query}) and ({age_query}) and ({rank_query}) and ({gender_query})'
        else:
            combined_query = f'({division_type_query}) and ({age_query}) and ({rank_query})'

        # wmk=newDataFrameFromQuery(combined_query)
        # wmk = clean_df[
        #     ["Registrant_ID", "First_Name", "Last_Name", "Gender", "Dojo", "Age", "Rank", "Feet", "Inches", "Height",
        #      "Weight", "BMI", "Events", "Techniques", "Weapons", "Tickets"]].query(combined_query).sort_values("Age").sort_values("BMI")
        wmk = clean_df.query(combined_query).sort_values("Age").sort_values("BMI")


        ## update the hitcount every time we touch someone
        for index, row in wmk.iterrows():
            name = row['First_Name'] + " " + row['Last_Name']
            id = row['Registrant_ID']
            hc = clean_df.at[index, 'hitcount']
            newhc = hc + 1
            # logging.info(f'{id}:{name} has a row count of {newhc}')
            clean_df.at[index, 'hitcount'] = newhc

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


# define layout for first page
def first_page_layout(canvas, doc):
    canvas.saveState()

    #####
    # Logo
    logo = ImageReader('Z_LOGO_HalfInch.jpg')
    canvas.drawImage(logo, .25 * inch, 10.25 * inch, mask='auto')

    # #####
    # # Report Header
    # canvas.setFont('Times-Bold',28)
    # #    canvas.drawCentredString(PAGE_WIDTH/2.0, PDFReport.PAGE_HEIGHT-108, PDFReport.Title)
    # canvas.drawCentredString(KataScoreSheet.PAGE_WIDTH / 2.0, 10.5 * inch, KataScoreSheet.Title)
    # canvas.setFont('Times-Bold', 12)
    # canvas.drawCentredString(KataScoreSheet.PAGE_WIDTH / 2.0, 10.25 * inch, "Score Sheet")
    #
    # #####
    # # Ring and Divisional Details
    # y=10.75
    # canvas.setFont('Times-Bold', 12)
    # canvas.drawString(5.95 *inch, y * inch, "RING")
    # canvas.drawString(6.5 *inch, y * inch, KataScoreSheet.ring_number)
    # canvas.drawString(7*inch, y * inch, KataScoreSheet.event_time)
    # canvas.line(6.5 * inch, (y-0.02) * inch, 8.25 * inch, (y-0.02) * inch)
    #
    # y=10.55
    # canvas.setFont('Times-Bold', 12)
    # canvas.drawString(5.6 * inch, y * inch, "DIVISION")
    # canvas.setFont('Times-Bold', 10)
    # canvas.drawString(6.5 * inch, y * inch, KataScoreSheet.division_name)
    # canvas.line(6.5 * inch, (y-0.02) * inch, 8.25 * inch, (y-0.02) * inch)
    #
    # y=10.35
    # canvas.setFont('Times-Bold', 10)
    # canvas.drawString(6.5 * inch, y * inch, KataScoreSheet.age)
    # canvas.line(6.5 * inch, (y-0.02) * inch, 8.25 * inch, (y-0.02) * inch)
    #
    # y=10.15
    # canvas.setFont('Times-Bold', 12)
    # canvas.drawString(5.8 * inch, y * inch, "RANKS")
    # canvas.setFont('Times-Bold', 10)
    # canvas.drawString(6.5 * inch, y * inch, KataScoreSheet.belts)
    # canvas.line(6.5 * inch, (y-0.02) * inch, 8.25 * inch, (y-0.02) * inch)


    #####
    # Footer
    canvas.setFont('Times-Roman', 9)
    canvas.drawCentredString(KataScoreSheet.PAGE_WIDTH / 2.0, 0.25 * inch,
                      "Page: %d     Generated: %s     From file: %s" % (
                                 doc.page, KataScoreSheet.timestamp, KataScoreSheet.sourcefile))

    canvas.restoreState()

# define layout for subsequent pages
def later_page_layout(canvas, doc):
    canvas.saveState()
    #####
    # Logo
    #logo = ImageReader('Z_LOGO_HalfInch.jpg')
    #canvas.drawImage(logo, .25 * inch, 10.25 * inch, mask='auto')

    #####
    ## Report Header
    #canvas.setFont('Times-Bold',28)
    ##    canvas.drawCentredString(PAGE_WIDTH/2.0, PDFReport.PAGE_HEIGHT-108, PDFReport.Title)
    #canvas.drawCentredString(KataScoreSheet.PAGE_WIDTH / 2.0, 10.5 * inch, KataScoreSheet.Title)
    #canvas.setFont('Times-Bold', 12)
    #canvas.drawCentredString(KataScoreSheet.PAGE_WIDTH / 2.0, 10.25 * inch, "Score Sheet")

    # #####
    # # Ring and Divisional Details
    # y=10.75
    # canvas.setFont('Times-Bold', 12)
    # canvas.drawString(6.45 *inch, y * inch, "RING")
    # canvas.drawString(7 *inch, y * inch, KataScoreSheet.ring_number)
    # canvas.drawString(7.5*inch, y * inch, KataScoreSheet.event_time)
    # canvas.line(7 * inch, (y-0.02) * inch, 8.25 * inch, (y-0.02) * inch)
    #
    # y=10.55
    # canvas.drawString(6.1 * inch, y * inch, "DIVISION")
    # canvas.drawString(7 * inch, y * inch, KataScoreSheet.division_name)
    # canvas.line(7 * inch, (y-0.02) * inch, 8.25 * inch, (y-0.02) * inch)
    #
    # y=10.35
    # canvas.drawString(7 * inch, y * inch, KataScoreSheet.age)
    # canvas.line(7 * inch, (y-0.02) * inch, 8.25 * inch, (y-0.02) * inch)
    #
    # y=10.15
    # canvas.drawString(6.3 * inch, y * inch, "RANKS")
    # canvas.drawString(7 * inch, y * inch, KataScoreSheet.belts)
    # canvas.line(7 * inch, (y-0.02) * inch, 8.25 * inch, (y-0.02) * inch)


    # Footer
    canvas.setFont('Times-Roman', 9)
    canvas.drawCentredString(KataScoreSheet.PAGE_WIDTH / 2.0, 0.25 * inch,
                             "Page: %d     Generated: %s     From file: %s" % (
                                 doc.page, KataScoreSheet.timestamp, KataScoreSheet.sourcefile))

    canvas.restoreState()

# define layout for subsequent pages
def page_layout(canvas, doc):
    canvas.saveState()
    logo = ImageReader('Z_LOGO_HalfInch.jpg')
    canvas.drawImage(logo, .25 * inch, 7.5 * inch, mask='auto')
    canvas.setFont('Times-Roman', 9)
    canvas.drawString(inch * 3, 0.75 * inch,
                      "Page: %d     Generated: %s     From file: %s" % (
                          doc.page, KataScoreSheet.timestamp, KataScoreSheet.sourcefile))
    canvas.restoreState()


if __name__ == "__main__":
  #setup the Kata Score Sheet PDF
  kata_score_sheet=KataScoreSheet()
  KataScoreSheet.set_title("Forms")
  KataScoreSheet.set_sourcefile("testing//no//file//name")

  # # create a test data frame
  # index = ['a', 'b', 'c', 'd']
  # columns = ['one', 'two', 'three', 'four']
  # df = pd.DataFrame(np.random.randn(4, 4), index=index, columns=columns)
  # data = [df.columns[:, ].values.astype(str).tolist()] + df.values.tolist()

  # create a test data frame with what we will get passed
  columns = ['index', 'First Name', 'Last Name', 'Gender', 'Dojo', 'Age', 'Rank', 'Feet', 'Inches', 'Height', 'Weight',
             'BMI', 'Events', 'Weapons']
  data = [(255, 'Lucas', 'May', 'Male', 'CO- Parker', 10, 'Yellow', 4, 3, '4 ft. 3 in.', 52, 154,
           '2 Events - Forms & Sparring ($75)', 'None'),
          (194, 'jake', 'coleson', 'Male', 'CO- Cheyenne Mountain', 10, 'Yellow', 4, 0, '4', 60, 156,
           '2 Events - Forms & Sparring ($75)', 'Weapons ($35)'),
          (195, 'katie', 'coleson', 'Female', 'CO- Cheyenne Mountain', 12, 'Yellow', 4, 0, '4', 65.161,
           '2 Events - Forms & Sparring ($75)', 'Weapons ($35)')]
  df = pd.DataFrame(data, columns=columns)

  # # create a test data frame with what we want to present
  # columns=['Compettitors Name','Form','Scores','','Total','Place']
  # data=[('1) Lucas May, CO-Parker\n','','','','',''),
  #       ('2) Jake Coleson, CO-Cheyenne Mountain\n', '', '', '', '', ''),
  #       ('3) Kaitie Coleson, CO-Cheyenne Mountain\n', '', '', '', '', ''),
  #       ('4) Lucas May, CO-Parker\n', '', '', '', '', ''),
  #       ('5) Jake Coleson, CO-Cheyenne Mountain\n', '', '', '', '', ''),
  #       ('6) Jake Coleson, CO-Cheyenne Mountain\n', '', '', '', '', ''),
  #       ('7) Kaitie Coleson, CO-Cheyenne Mountain\n', '', '', '', '', ''),
  #       ('8) Lucas May, CO-Parker\n', '', '', '', '', ''),
  #       ('9) Jake Coleson, CO-Cheyenne Mountain\n', '', '', '', '', ''),
  #       ('11) Jake Coleson, CO-Cheyenne Mountain\n', '', '', '', '', ''),
  #       ('12) Kaitie Coleson, CO-Cheyenne Mountain\n', '', '', '', '', ''),
  #       ('13) Lucas May, CO-Parker\n', '', '', '', '', ''),
  #       ('14) Jake Coleson, CO-Cheyenne Mountain\n', '', '', '', '', ''),
  #       ('15) Jake Coleson, CO-Cheyenne Mountain\n', '', '', '', '', ''),
  #       ('16) Kaitie Coleson, CO-Cheyenne Mountain\n', '', '', '', '', ''),
  #       ('17) Lucas May, CO-Parker\n', '', '', '', '', ''),
  #       ('18) Jake Coleson, CO-Cheyenne Mountain\n', '', '', '', '', ''),
  #       ('19) Jake Coleson, CO-Cheyenne Mountain\n', '', '', '', '', ''),
  #       ('20) Kaitie Coleson, CO-Cheyenne Mountain\n', '', '', '', '', ''),
  #       ('21) Lucas May, CO-Parker\n', '', '', '', '', ''),
  #       ('22) Jake Coleson, CO-Cheyenne Mountain\n', '', '', '', '', ''),
  #       ('23) Jake Coleson, CO-Cheyenne Mountain\n', '', '', '', '', ''),
  #       ('24) Kaitie Coleson, CO-Cheyenne Mountain\n', '', '', '', '', ''),
  #       ('25) Kaitie Coleson, CO-Cheyenne Mountain\n', '', '', '', '', '')]
  # df = pd.DataFrame(data, columns=columns)

  kata_score_sheet.put_dataframe_on_pdfpage(df,"1","22:22","Senior Mens Kata","35-Older","Black")


  kata_score_sheet.write_pdfpage()

## setup test data frame
