#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed April 23 2023

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
# import FileHandlingUtilities  #<--un-comment for stand alone testing


class TechniqueScoreSheet(object):
    def __init__(self,title:str, sourcefile:str,output_folder_path:str):
        self.filename_with_path=str(pathlib.Path(output_folder_path + reports.FileHandlingUtilities.pathDelimiter() +'TechniqueScoreSheet.pdf')) #<--comment out for stand alone testing
        # self.filename_with_path=str(pathlib.Path(output_folder_path + FileHandlingUtilities.pathDelimiter() +'TechniqueScoreSheet.pdf'))   #<--un-comment for stand alone testing

        # self.doc = SimpleDocTemplate("TechniqueScoreSheet.pdf", pagesize=portrait(letter),topMargin=0, bottomMargin=0)
        self.doc = SimpleDocTemplate(self.filename_with_path, pagesize=portrait(letter),topMargin=0, bottomMargin=0, leftMargin=0, rightMargin=0)
        self.docElements = []
        #setup the package scoped global variables we need
        now = datetime.datetime.now()
        TechniqueScoreSheet.timestamp = now.strftime("%Y-%m-%d %H:%M")
        # TechniqueScoreSheet.sourcefile = "not initialized"
        TechniqueScoreSheet.sourcefile = sourcefile
        TechniqueScoreSheet.pageinfo = "not initialized"
        # TechniqueScoreSheet.Title = "not initialized"
        TechniqueScoreSheet.Title = title
        TechniqueScoreSheet.PAGE_HEIGHT = 11 * inch
        TechniqueScoreSheet.PAGE_WIDTH = 8.5 * inch
        TechniqueScoreSheet.styles = getSampleStyleSheet()   #sample style sheet doesn't seem to be used
        TechniqueScoreSheet.ring_number= "not initialized"
        TechniqueScoreSheet.event_time= "not initialized"
        TechniqueScoreSheet.division_name= "not initialized"
        TechniqueScoreSheet.age= "not initialized"
        TechniqueScoreSheet.belts= "not initialized"

    @staticmethod
    def set_title(title):
        TechniqueScoreSheet.Title = title

    @staticmethod
    def set_pageInfo(pageinfo):
        TechniqueScoreSheet.pageinfo = pageinfo

    @staticmethod
    def set_sourcefile(sourcefile):
        TechniqueScoreSheet.sourcefile = sourcefile

    def convert_inputdf_to_outputdf(self,inputdf):
        # columns = ['competitors Name', 'Technique', 'Scores', '', 'Total', 'Place']
        columns = ['Competitors Name']
        data=[]
        outputdf = pd.DataFrame(data, columns=columns)

        counter=1
        for index, row in inputdf.iterrows():
            outputdf.at[index, 'Competitors Name'] = f"{counter}) {inputdf.at[index, 'First_Name']} {inputdf.at[index, 'Last_Name']} \n"
            counter = counter+1

        return outputdf

    def put_dataframe_on_pdfpage(self, inputdf, ring_number, event_time, division_name, age, belts, split_warning_text=None):
        # put args in class variables so the static page header functions can use them
        TechniqueScoreSheet.ring_number = ring_number
        TechniqueScoreSheet.event_time = event_time
        TechniqueScoreSheet.division_name = division_name
        TechniqueScoreSheet.age = age
        TechniqueScoreSheet.belts = belts
        if(split_warning_text is None):
            TechniqueScoreSheet.split_warning_text = ""
        else:
            TechniqueScoreSheet.split_warning_text = split_warning_text

        elements = []

        headerdata1 = [[TechniqueScoreSheet.Title, 'Score Sheet']]
        t = Table(headerdata1)
        # remember table styles attributes specified as From (Column,Row), To (Column,Row)
        # - see reportlab users guide chapter 7, page 78 for details
        t.setStyle(TableStyle([('FONTNAME', (0, 0), (1, -1), "Times-Bold"),
                               ('TEXTCOLOR', (0, 0), (1, -1), colors.black),
                               ('FONTSIZE', (0, 0), (1, -1), 20),
                               ('ALIGN', (0, 0), (1, 0), 'CENTER'),
                               ('LEADING', (0, 0), (1, -1), 9)]))

        elements.append(t)
        elements.append(Spacer(1, 0.2 * inch))

        headerdata3 = [[split_warning_text]]
        t = Table(headerdata3)
        t.setStyle(TableStyle([('FONTNAME', (0, 0), (1, -1), "Times-Bold"),
                               ('TEXTCOLOR', (0, 0), (1, -1), colors.red),
                               ('FONTSIZE', (0, 0), (1, -1), 10),
                               ('ALIGN', (0, 0), (1, 0), 'CENTER'),
                               ('LEADING', (0, 0), (1, -1), 9)]))
        elements.append(t)
        elements.append(Spacer(width=1, height= -0.5 * inch))


        if inputdf.shape[0] > constants.TOO_MANY_COMPETITORS:
            logging.warning("\u001b[31m*** {} {} Ring:{} has too many competitors. It has {}\u001b[0m".format(event_time,division_name,ring_number,inputdf.shape[0]))

        # if split_warning_text is None:
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

        t.setStyle(TableStyle([('FONTNAME', (0, 0), (1, -1), "Times-Bold"),
                               ('TEXTCOLOR', (0, 0), (1, -1), colors.black),
                               ('FONTSIZE', (0, 0), (1, -1), 10),
                               ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
                               ('ALIGN', (1, 0), (1, -1), 'LEFT'),
                               ('LEADING', (0, 0), (1, -1), 7)]))

        t.hAlign = 'RIGHT'
        elements.append(t)
        elements.append(Spacer(width=1, height=0.3 * inch))

        # Data Frame
        outputdf=self.convert_inputdf_to_outputdf(inputdf)

        #  Convert data frame to a list format
        data_list = [outputdf.columns[:, ].values.astype(str).tolist()] + outputdf.values.tolist()

        t = Table(data_list)
        t.hAlign = 'LEFT'

        if len(data_list) > constants.TOO_MANY_COMPETITORS +1:
            t.setStyle(TableStyle([('FONTNAME', (0, 0), (-1, -1), "Helvetica"),
                                   ('FONTSIZE', (0, 0), (-1, -1), 8),
                                   ('TEXTCOLOR', (0, 0), (-1, -1), colors.red),
                                   # ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                                   ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                                   ('ALIGN', (0, 0), (-1, 0), 'LEFT')]))
                                   # ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                                   # ('SPAN', (2, 0), (3, 0)),
                                   # ('BOX', (0, 0), (-1, -1), 0.25, colors.black)]))
        else:
            t.setStyle(TableStyle([('FONTNAME', (0, 0), (-1, -1), "Helvetica"),
                                   ('FONTSIZE', (0, 0), (-1, -1), 8),
                                   ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                                   # ('BACKGROUND',(0,0),(-1,0),colors.lightgrey),
                                   ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                                   ('ALIGN',(0,0),(-1,0),'LEFT')]))
                                   # ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                                   # ('SPAN',(2,0),(3,0)),
                                   # ('BOX', (0, 0), (-1, -1), 0.25, colors.black)]))

        # set the width of the columns
        t._argW[0] = 2.5 *inch

        elements.append(t)
        elements.append(Spacer(1, 0.2 * inch))
        elements.append(PageBreak())

        #    # write the document to disk
        #    doc.build(elements)

        self.docElements.extend(elements)
        return elements;

    def write_pdfpage(self):
        self.doc.build(self.docElements, onFirstPage=first_page_layout, onLaterPages=first_page_layout)

    ###############################################################################
    # writeSingleTechniqueScoreSheet
    #  Fall 2020
    #  This method writes a single kata score sheet based on parameters provided
    #
    def writeSingleTechniqueScoreSheet(self, event_time: str, division_name: str, division_type: str, gender: str, rank_label: str, minimum_age: int,
                                       maximum_age: int, rings: list, ranks: list, clean_df: pandas.DataFrame):
        if (maximum_age == constants.AGELESS):
            age_label = '{0}+'.format(minimum_age)
        else:
            age_label = '{0} - {1}'.format(minimum_age, maximum_age)

        # Hack for 3 year olds
        if minimum_age == 4:
            minimum_age = 2

        #logging.info("Generating Technique Score PDF for " + event_time + " " + division_name + " " + age_label)
        logging.info(f'Generating {division_type} Score PDF for {event_time} {division_name} {age_label} {rank_label}')
        self.set_title(f'{division_type}')

        age_query = 'Age >={0} and Age <={1}'.format(minimum_age, maximum_age)

        rank_query = ''
        for r in range(0, len(ranks)):
            rank_query = rank_query + 'Rank =="' + ranks[r] + '"'
            if r < len(ranks) - 1:  # Add ' and ' to everything but the last one
                rank_query = rank_query + ' or '

        assert  division_type == 'Techniques', "Error: Invalid division_type"
        division_type_query = 'Events.str.contains("Technique")'

        if gender != '*':
            gender_query = 'Gender == "' + gender + '"'
            combined_query = f'({division_type_query}) and ({age_query}) and ({rank_query}) and ({gender_query})'
        else:
            combined_query = f'({division_type_query}) and ({age_query}) and ({rank_query})'

        # division_competitors=newDataFrameFromQuery(combined_query)
        # division_competitors = clean_df[
        # ["Registrant_ID", "First_Name", "Last_Name", "Gender", "Dojo", "Age", "Rank", "Feet", "Inches", "Height",
        #  "Weight", "BMI", "Events", "Weapons", "Tickets"]].query(combined_query).sort_values("Age").sort_values("BMI")
        division_competitors = clean_df.query(combined_query).sort_values("Age").sort_values("BMI")

        ## update the hitcount every time we touch someone
        for index, row in division_competitors.iterrows():
            name = row['First_Name'] + " " + row['Last_Name']
            id = row['Registrant_ID']
            hc = clean_df.at[index, 'hitcount']
            newhc = hc + 1
            # logging.info(f'{id}:{name} has a row count of {newhc}')
            clean_df.at[index, 'hitcount'] = newhc

        # automatic split logic
        number_of_rings = len(rings)
        highest_ring_number_specified = rings[-1][0]
        if type(highest_ring_number_specified) is str:
            highest_ring_number_specified = rings[0][0] #We may want to throw an error here, but S. Liz wants it to print *TBD


        # if (number_of_rings > 1):  # means we want to use autosplit
        if rings[0][1].upper() == 'AUTO':  # means we want to use autosplit
            import domain_model.name_partitioner
            np = domain_model.name_partitioner.NamePartionioner()
            partition_boundaries = np.get_optimum_partition_boundaries(the_data=division_competitors,
                                                                       min_number_of_partitions=number_of_rings,
                                                                       max_entries_per_partition=20)
            print(partition_boundaries)
            new_ring_info = []
            ring_number = rings[0][0]
            for partition in partition_boundaries:
                # in case we have more partitions than rings, we need to handle it gracefully
                if (ring_number > highest_ring_number_specified):
                    ring_number_to_display = '*TBA'
                else:
                    ring_number_to_display = str(ring_number)
                new_ring_info.append([ring_number_to_display, partition[0], partition[1]])
                ring_number = ring_number + 1
            print(new_ring_info)
            if (len(new_ring_info) < len(rings)):
                logging.warning(
                    f'Automatic ring configuration for {event_time} {division_name} {age_label} {rank_label} - original rings: {rings} new rings:{new_ring_info} - results in using less rings than planned!')
            if (len(new_ring_info) > len(rings)):
                logging.warning(
                    f'Automatic ring configuration for {event_time} {division_name} {age_label} {rank_label} - original rings: {rings} new rings:{new_ring_info}  - results in using MORE rings than planned!')
            if (len(new_ring_info) == len(rings)):
                logging.info(
                    f'Automatic ring configuration in for {event_time} {division_name} {age_label} {rank_label} - original rings: {rings} new rings:{new_ring_info}  - no change in the number of rings used!')

            rings = new_ring_info

        for info in rings:
            # ring = info.get('ring')
            # starting_letter = info.get('startingLetter')
            # ending_letter = info.get('endingLetter')
            ring=info[0]
            starting_letter=info[1]
            ending_letter=info[2]
            # Extract the first letter of the 'Last_Name' column
            division_competitors['First_Letter'] = division_competitors['Last_Name'].str[0]

            # Apply the conditions on the 'First_Letter' column
            filtered_competitors = division_competitors[(division_competitors['First_Letter'] >= starting_letter) & (division_competitors['First_Letter'] <= ending_letter) | (division_competitors['First_Letter'] >= starting_letter.lower()) & (division_competitors['First_Letter'] <= ending_letter.lower())]
            if len(rings) > 1:  # more than 1 ring means we split
                self.put_dataframe_on_pdfpage(filtered_competitors, str(ring), event_time, division_name, age_label, f'{rank_label} ({starting_letter}-{ending_letter})', f'*** PLEASE NOTE - These are contestants {starting_letter}-{ending_letter}')
            else:
                self.put_dataframe_on_pdfpage(filtered_competitors, str(ring), event_time, division_name, age_label, rank_label)

        # if len(rings) > 1:  # more than 1 ring means we split
        #     # filter to only keep contestants who's last name fall into the first alphabetic split
        #     first_alphabetic_split = division_competitors[division_competitors['Last_Name'].str.contains(constants.FIRST_ALPHABETIC_SPLIT_REGEX)]
        #
        #     # filter to only keep contestants who's last name fall into the second alphabetic split
        #     second_alphabetic_split = division_competitors[division_competitors['Last_Name'].str.contains(constants.SECOND_ALPHABETIC_SPLIT_REGEX)]
        #
        #     self.put_dataframe_on_pdfpage(first_alphabetic_split, str(rings[0]), event_time, division_name,
        #                                               age_label,
        #                                               rank_label + " (" + constants.FIRST_ALPHABETIC_SPLIT_LABEL + ")",
        #                                               "*** PLEASE NOTE - These are contestants " + constants.FIRST_ALPHABETIC_SPLIT_LABEL)
        #
        #     self.put_dataframe_on_pdfpage(second_alphabetic_split, str(rings[1]), event_time,
        #                                               division_name, age_label,
        #                                               rank_label + "  (" + constants.SECOND_ALPHABETIC_SPLIT_LABEL + ")",
        #                                               "*** PLEASE NOTE - These are contestants " + constants.SECOND_ALPHABETIC_SPLIT_LABEL)
        # else:
        #     self.put_dataframe_on_pdfpage(division_competitors, str(rings[0]), event_time, division_name, age_label,
        #                                               rank_label)


# define layout for first page
def first_page_layout(canvas, doc):
    canvas.saveState()

    #####
    # Background Template Image
    backgroundImageFilename='reports'+reports.FileHandlingUtilities.pathDelimiter()+'technique_score_sheet_template-300dpi.png'  #<--comment out for stand alone testing
    # backgroundImageFilename='technique_score_sheet_template-600dpi.png'  #<--un-comment for stand alone testing
    background = ImageReader(backgroundImageFilename)
    canvas.drawImage(background, 0 * inch, 0 * inch, mask='auto', width=TechniqueScoreSheet.PAGE_WIDTH, height=TechniqueScoreSheet.PAGE_HEIGHT)

    # #####
    # # Logo
    # logo = ImageReader('Z_LOGO_HalfInch.jpg')
    # canvas.drawImage(logo, .25 * inch, 10.25 * inch, mask='auto')

    #####
    # Footer
    canvas.setFont('Times-Roman', 9)
    canvas.setFillColor(colors.black)
    canvas.drawCentredString(TechniqueScoreSheet.PAGE_WIDTH / 2.0, 0.25 * inch,
                      "Page: %d     Generated: %s     From file: %s" % (
                                 doc.page, TechniqueScoreSheet.timestamp, TechniqueScoreSheet.sourcefile))

    canvas.restoreState()

# define layout for subsequent pages
def later_page_layout(canvas, doc):
    canvas.saveState()

    # Footer
    canvas.setFont('Times-Roman', 9)
    canvas.drawCentredString(TechniqueScoreSheet.PAGE_WIDTH / 2.0, 0.25 * inch,
                             "Page: %d     Generated: %s     From file: %s" % (
                                 doc.page, TechniqueScoreSheet.timestamp, TechniqueScoreSheet.sourcefile))

    canvas.restoreState()

# define layout for subsequent pages
def page_layout(canvas, doc):
    canvas.saveState()
    # logo = ImageReader('Z_LOGO_HalfInch.jpg')
    # canvas.drawImage(logo, .25 * inch, 7.5 * inch, mask='auto')
    canvas.setFont('Times-Roman', 9)
    canvas.drawString(inch * 3, 0.75 * inch,
                      "Page: %d     Generated: %s     From file: %s" % (
                          doc.page, TechniqueScoreSheet.timestamp, TechniqueScoreSheet.sourcefile))
    canvas.restoreState()


if __name__ == "__main__":
  #setup the Kata Score Sheet PDF
  technique_score_sheet=TechniqueScoreSheet("Techniques", "test", "test files")


  # create a test data frame with what we will get passed
  columns = ['index', 'First_Name', 'Last_Name', 'Gender', 'Dojo', 'Age', 'Rank', 'Feet', 'Inches', 'Height', 'Weight',
             'BMI', 'Events', 'Weapons']
  data = [(255, 'Lucas', 'May', 'Male', 'CO- Parker', 10, 'Yellow', 4, 3, '4 ft. 3 in.', 52, 154,
           '2 Events - Forms & Sparring ($75)', 'None'),
          # (195, 'Katie', 'Coleson', 'Female', 'CO- Cheyenne Mountain', 12, 'Yellow', 4, 0, '4', 65.161,
          #  '2 Events - Forms & Sparring ($75)', 'Weapons ($35)'),
          (195, 'Angela', 'Payne', 'Female', 'CO- Cheyenne Mountain', 12, 'Yellow', 4, 0, '4', 65.161,
           '2 Events - Forms & Sparring ($75)', 'Weapons ($35)'),
          (195, 'Emily', 'Nielsen', 'Female', 'CO- Cheyenne Mountain', 12, 'Yellow', 4, 0, '4', 65.161,
          '2 Events - Forms & Sparring ($75)', 'Weapons ($35)'),
          (195, 'Alec', 'Harbaugh', 'Female', 'CO- Cheyenne Mountain', 12, 'Yellow', 4, 0, '4', 65.161,
           '2 Events - Forms & Sparring ($75)', 'Weapons ($35)'),
          (195, 'MJ', 'Ortiz', 'Female', 'CO- Cheyenne Mountain', 12, 'Yellow', 4, 0, '4', 65.161,
           '2 Events - Forms & Sparring ($75)', 'Weapons ($35)'),
          (195, 'Arav', 'Lukhey', 'Female', 'CO- Cheyenne Mountain', 12, 'Yellow', 4, 0, '4', 65.161,
           '2 Events - Forms & Sparring ($75)', 'Weapons ($35)'),
          (195, 'Jacob', 'Gibberson', 'Female', 'CO- Cheyenne Mountain', 12, 'Yellow', 4, 0, '4', 65.161,
           '2 Events - Forms & Sparring ($75)', 'Weapons ($35)'),
          (195, 'Angelique', 'Hutchins', 'Female', 'CO- Cheyenne Mountain', 12, 'Yellow', 4, 0, '4', 65.161,
           '2 Events - Forms & Sparring ($75)', 'Weapons ($35)'),
          (195, 'Malakai', 'Ruybal', 'Female', 'CO- Cheyenne Mountain', 12, 'Yellow', 4, 0, '4', 65.161,
           '2 Events - Forms & Sparring ($75)', 'Weapons ($35)'),
          (195, 'Visha', 'Hari', 'Female', 'CO- Cheyenne Mountain', 12, 'Yellow', 4, 0, '4', 65.161,
           '2 Events - Forms & Sparring ($75)', 'Weapons ($35)'),
          (195, 'Margaret', 'Buttery', 'Female', 'CO- Cheyenne Mountain', 12, 'Yellow', 4, 0, '4', 65.161,
           '2 Events - Forms & Sparring ($75)', 'Weapons ($35)'),
          (195, 'Constanta', 'Diaz Martinez', 'Female', 'CO- Cheyenne Mountain', 12, 'Yellow', 4, 0, '4', 65.161,
           '2 Events - Forms & Sparring ($75)', 'Weapons ($35)'),
          (195, 'Akshith', 'Naveenkumar', 'Female', 'CO- Cheyenne Mountain', 12, 'Yellow', 4, 0, '4', 65.161,
           '2 Events - Forms & Sparring ($75)', 'Weapons ($35)'),
          (195, 'Kalpak', 'Shankaregowda', 'Female', 'CO- Cheyenne Mountain', 12, 'Yellow', 4, 0, '4', 65.161,
           '2 Events - Forms & Sparring ($75)', 'Weapons ($35)'),
          (195, 'Emerson', 'Colwell', 'Female', 'CO- Cheyenne Mountain', 12, 'Yellow', 4, 0, '4', 65.161,
           '2 Events - Forms & Sparring ($75)', 'Weapons ($35)'),
          (195, 'Jeffery Jr', 'Merriman', 'Female', 'CO- Cheyenne Mountain', 12, 'Yellow', 4, 0, '4', 65.161,
           '2 Events - Forms & Sparring ($75)', 'Weapons ($35)'),
          (195, 'Farah', 'Mohamed-Sadik', 'Female', 'CO- Cheyenne Mountain', 12, 'Yellow', 4, 0, '4', 65.161,
           '2 Events - Forms & Sparring ($75)', 'Weapons ($35)'),
          (195, 'Joshua', 'Betournay', 'Female', 'CO- Cheyenne Mountain', 12, 'Yellow', 4, 0, '4', 65.161,
           '2 Events - Forms & Sparring ($75)', 'Weapons ($35)'),
          (195, 'Anirudh', 'Maheshkumar', 'Female', 'CO- Cheyenne Mountain', 12, 'Yellow', 4, 0, '4', 65.161,
           '2 Events - Forms & Sparring ($75)', 'Weapons ($35)'),
                  (195, 'Maria Jose', 'Acevedo Peck', 'Female', 'CO- Cheyenne Mountain', 12, 'Yellow', 4, 0, '4', 65.161,
           '2 Events - Forms & Sparring ($75)', 'Weapons ($35)')]
  df = pd.DataFrame(data, columns=columns)


  technique_score_sheet.put_dataframe_on_pdfpage(df,"1","22:22","Senior Mens Kata","35-Older","Black","*** PLEASE NOTE - These are contestants A-M")


  technique_score_sheet.write_pdfpage()

