# V 10/1/2017 - Changed reports to use new age groups for Fall 2017 Tournament

# There are 6 patterns in the Denver Tournament Guide
#
# Pattern1
#
#
# Pattern2
#  White
#  Yellow
#  Orange
#  Purple, Blue, Blue Stripe
#  Green, Green Stripe, Brown
#
# Pattern3
#  White
#  Yellow
#  Orange
#  Purple
#  Blue, Blue Stripe
#  Green, Green Stripe, Brown
#
# Pattern4
#  White, Yellow, Orange
#  Purple, Blue, Blue Stripe
#  Green, Green Stripe, Brown
#  Black
#
# Pattern5
#  White, Yellow
#  Orange
#  Purple
#  Blue, Blue Stripe
#  Green, Green Stripe, Brown
#
# Pattern6
#  White, Yellow
#  Orange
#  Purple
#  Blue, Blue Stripe
#  Green, Green Stripe
#  Brown
#  Black
#
# Pattern7
#  White, Yellow & Orange
#  Purple, Blue & Blue Stripe
#  Green, Green Stripe, Brown
#  Black
#
#   Feautres to add:
# Split the 9:45 boys & Girls Kata into a-m and m-z
# Make the headings look better
# generate the output to the same directory as the input - and look for the logos in a subdirectory based on where code is launched from
# Add functionality to touch people every time they are used, and print the stats - print anyone who didn't get touched.
# Summary Stats - how many people of each belt, how many sparring, how may forms, how many weaponds
# Event Stats - how many people in each event as per the event guide
#

import os
import time
from tkinter import Tk
from tkinter.filedialog import askopenfilename

import pandas as pd

from cleaninput import cleaninput
from cleaninput import rename_colums as RN

from reports import DivisionDetailReportPDF
from reports import KataScoreSheetPDF as kata_score_sheet_pdf
import reports.sparring_tree.sparring_tree_report
import domain_model.competitors



###############################################################################
# pathDelimiter()
#  arguments:  none
#  return:   "\\" if it's windows, "/" if it's unix
#
def pathDelimiter():
    path = os.getcwd()
    if "\\" in path:
        delimiter = "\\"  # Windows
    else:
        delimiter = "/"  # Unix
    return delimiter


###############################################################################
# NewDataFrameFromMask()
#  arguments:  mask to apply
#  return:   new data frame
#
def newDataFrameFromMask(mask):
    newdf = clean_df[
        ["Registrant_ID","First_Name", "Last_Name", "Gender", "Dojo", "Age", "Rank", "Feet", "Inches", "Height", "Weight", "BMI",
         "Events", "Weapons"]][mask].sort_values("Age")
    newdf.sort_values('BMI', inplace=True)

    ## update the hitcount every time we touch someone
    for index, row in clean_df[mask].iterrows():
        name = row['First_Name'] + " " + row['Last_Name']
        hc = row['hitcount']
        newhc = hc + 1
        #    print name + " has a row count of " + str(newhc)
        clean_df.at[index, 'hitcount'] = newhc

    return newdf


###############################################################################
# writeFormattedExcelSheet
#  This method writes a dataframe, to the given excel writer, and given sheet name
#
#
#  arguments:
#  data frame to be written to
#  excel writer - that is ready to write to
#  sheet name
#
def writeFormattedExcelSheet(df, writer, sheetname):
    df.to_excel(writer, sheetname)

    ##setup the spreadsheet to make it easy to print
    #    set_border(1)
    workbook = writer.book
    worksheet = writer.sheets[sheetname]

    # define some formats
    align_center = workbook.add_format()
    align_center.set_align('center')
    align_center.set_border(1)

    align_left = workbook.add_format()
    align_left.set_align('left')
    align_left.set_border(1)

    full_border = workbook.add_format()
    full_border.set_border(1)

    # set the format of a few columns
    worksheet.set_column('A:O', 0, full_border)  # column A:O is everything

    worksheet.set_column('A:A', 5, align_left)  # column A is the index
    worksheet.set_column('B:B', 15)  # column B is First Name
    worksheet.set_column('C:C', 20)  # column C is Last Name
    worksheet.set_column('D:D', 7)  # column D is Gender
    worksheet.set_column('E:E', 20)  # column E is Dojo
    worksheet.set_column('F:F', 3, align_center)  # column F is age
    worksheet.set_column('G:G', 15)  # column G is rank
    worksheet.set_column('H:H', 4, align_center)  # column G is feet
    worksheet.set_column('I:I', 5, align_center)  # column I is Inches
    worksheet.set_column('K:K', 6, align_center)  # column K is Weight
    worksheet.set_column('L:L', 4, align_center)  # column L is BMI
    worksheet.set_column('M:M', 25)  # column M is Events
    worksheet.set_column('N:N', 12)  # column N is Weapons


###############################################################################
# write event to file
#  arguments:
#  filename - the filename without path to write
#  compsitMask - a mask made up of everything but the belts that you want
#
def writeEventToFile(filename, compositMask):
    #    fullpath = os.getcwd() + "\\Sorted\\" + filename  #Windows
    #    fullpath = os.getcwd() + "/Sorted/" + filename  #Mac
    fullpath = os.getcwd() + pathDelimiter() + "Sorted" + pathDelimiter() + filename
    writer = pd.ExcelWriter(fullpath)

    print(time.strftime("%X") + " Generating " + fullpath)

    mask = mask_WhiteBelt & compositMask
    wmk = newDataFrameFromMask(mask)
    writeFormattedExcelSheet(wmk, writer, 'White')

    mask = mask_YellowBelt & compositMask
    wmk = newDataFrameFromMask(mask)
    writeFormattedExcelSheet(wmk, writer, 'Yellow')

    mask = mask_OrangeBelt & compositMask
    wmk = newDataFrameFromMask(mask)
    writeFormattedExcelSheet(wmk, writer, 'Orange')

    mask = mask_PurpleBelt & compositMask
    wmk = newDataFrameFromMask(mask)
    writeFormattedExcelSheet(wmk, writer, 'Purple')

    mask = mask_AllBlueBelt & compositMask
    wmk = newDataFrameFromMask(mask)
    writeFormattedExcelSheet(wmk, writer, 'Blue')

    mask = mask_AllGreenBelt & compositMask
    wmk = newDataFrameFromMask(mask)
    writeFormattedExcelSheet(wmk, writer, 'Green')

    mask = mask_AllBrownBelt & compositMask
    wmk = newDataFrameFromMask(mask)
    writeFormattedExcelSheet(wmk, writer, 'Brown')

    mask = mask_AllBlackBelt & compositMask
    wmk = newDataFrameFromMask(mask)
    writeFormattedExcelSheet(wmk, writer, 'Black')

    writer.save()
    time.sleep(1)


###############################################################################
# writePattern1ToExcel
#  This method provides a re-usable method to write output to excel
#  The Pattern it writes is:
#    White
#    Yellow
#    Orange
#    Purple, Blue, Blue Stripe
#    Green, Green Stripe
#
#  arguments:
#  filename - the filename without path to write
#  compsitMask - a mask made up of everything but the belts that you want
def writePattern1ToExcel(filename, compositMask):
    fullpath = os.getcwd() + pathDelimiter() + "Sorted" + pathDelimiter() + filename
    writer = pd.ExcelWriter(fullpath, engine='xlsxwriter')
    print(time.strftime("%X") + " Generating " + fullpath)

    mask = mask_WhiteBelt & compositMask
    wmk = newDataFrameFromMask(mask)
    writeFormattedExcelSheet(wmk, writer, 'White')

    mask = mask_YellowBelt & compositMask
    wmk = newDataFrameFromMask(mask)
    writeFormattedExcelSheet(wmk, writer, 'Yellow')

    mask = mask_OrangeBelt & compositMask
    wmk = newDataFrameFromMask(mask)
    writeFormattedExcelSheet(wmk, writer, 'Orange')

    mask1 = mask_PurpleBelt & compositMask
    mask2 = mask_AllBlueBelt & compositMask
    mask = mask1 | mask2
    wmk = newDataFrameFromMask(mask)
    writeFormattedExcelSheet(wmk, writer, 'Purple, Blue, Blue Stripe')

    mask1 = mask_AllGreenBelt & compositMask
    mask2 = mask_AllBrownBelt & compositMask
    mask = mask1 | mask2
    wmk = newDataFrameFromMask(mask)
    writeFormattedExcelSheet(wmk, writer, 'Green, Green Stripe, Brown')
    #
    #    mask= mask_AllBlackBelt & compositMask
    #    wmk=newDataFrameFromMask( mask )

    writer.save()
    time.sleep(1)


###############################################################################
# writePattern1ToDvisionDetailReport
#  This method provides a re-usable method to write output to PDF
#  The Pattern it writes is:
#    White
#    Yellow
#    Orange
#    Purple, Blue, Blue Stripe
#    Green, Green Stripe, Brown
#
#  arguments:
#  filename - the filename without path to write
#  compsitMask - a mask made up of everything but the belts that you want
def writePattern1ToDivisionDetailReport(starting_ring, event_time, division_name, age, compositMask):
    print(time.strftime("%X") + " Generating Detail Report PDF for " + event_time + " " + division_name + " " + age)

    DivisionDetailReportPDF.DivisionDetailReportPDF.set_title(division_name)

    mask = mask_WhiteBelt & compositMask
    wmk = newDataFrameFromMask(mask)
    divison_detail_report_pdf.put_dataframe_on_pdfpage(wmk, str(starting_ring), event_time, division_name, age, "White")

    mask = mask_YellowBelt & compositMask
    wmk = newDataFrameFromMask(mask)
    divison_detail_report_pdf.put_dataframe_on_pdfpage(wmk, str(starting_ring + 1), event_time, division_name, age,
                                                       "Yellow")

    mask = mask_OrangeBelt & compositMask
    wmk = newDataFrameFromMask(mask)
    divison_detail_report_pdf.put_dataframe_on_pdfpage(wmk, str(starting_ring + 2), event_time, division_name, age,
                                                       "Orange")

    mask1 = mask_PurpleBelt & compositMask
    mask2 = mask_AllBlueBelt & compositMask
    mask = mask1 | mask2
    wmk = newDataFrameFromMask(mask)
    divison_detail_report_pdf.put_dataframe_on_pdfpage(wmk, str(starting_ring + 3), event_time, division_name, age,
                                                       "Purple, Blue, Blue Stripe")

    mask1 = mask_AllGreenBelt & compositMask
    mask2 = mask_AllBrownBelt & compositMask
    mask = mask1 | mask2
    wmk = newDataFrameFromMask(mask)
    divison_detail_report_pdf.put_dataframe_on_pdfpage(wmk, str(starting_ring + 4), event_time, division_name, age,
                                                       "Green, Green Stripe, Brown")
    #    mask= mask_AllBlackBelt & compositMask
    #    wmk=newDataFrameFromMask( mask )
    #    pdf_report.put_dataframe_on_pdfpage(wmk, str(starting_ring+5), time, division_name, age, "Black")


###############################################################################
# writePattern1ToDvisionDetailReport
#  This method provides a re-usable method to write output to PDF
#  The Pattern it writes is:
#    White
#    Yellow
#    Orange
#    Purple, Blue, Blue Stripe
#    Green, Green Stripe, Brown
#
#  arguments:
#  filename - the filename without path to write
#  compsitMask - a mask made up of everything but the belts that you want
def writePattern1WithSplitToDivisionDetailReport(starting_ring, event_time, division_name, age, compositMask):
    print(time.strftime("%X") + " Generating Detail Report PDF for " + event_time + " " + division_name + " " + age)

    DivisionDetailReportPDF.DivisionDetailReportPDF.set_title(division_name)

    mask = mask_WhiteBelt & compositMask
    wmk = newDataFrameFromMask(mask)
    divison_detail_report_pdf.put_dataframe_on_pdfpage(wmk, str(starting_ring), event_time, division_name, age, "White")

    mask = mask_YellowBelt & compositMask
    wmk = newDataFrameFromMask(mask)
    #    divison_detail_report_pdf.put_dataframe_on_pdfpage(wmk, str(starting_ring + 1), event_time, division_name, age, "Yellow")

    # filter to only keep the ones that start with a-l A-L
    pattern = r'^[a-lA-L]'  # ^ means starts wtih [a-l][A-L] means letters in the set a-l
    AtoL = wmk[wmk['Last_Name'].str.contains(pattern)]

    # filter to only keep the ones that start with m-z M-Z
    pattern = r'^[m-zM-Z]'  # ^ means starts wtih [m-z][M-Z] means letters in the set m-z
    MtoZ = wmk[wmk['Last_Name'].str.contains(pattern)]

    divison_detail_report_pdf.put_dataframe_on_pdfpage(AtoL, str(starting_ring + 1), event_time, division_name, age,
                                                       "Yellow (A-L)",
                                                       "*** PLEASE NOTE - These are contestants A - L")
    divison_detail_report_pdf.put_dataframe_on_pdfpage(MtoZ, str(starting_ring + 2), event_time, division_name, age,
                                                       "Yellow (M-Z)",
                                                       "*** PLEASE NOTE - These are contestants M - Z")

    mask = mask_OrangeBelt & compositMask
    wmk = newDataFrameFromMask(mask)
    #    divison_detail_report_pdf.put_dataframe_on_pdfpage(wmk, str(starting_ring + 2), event_time, division_name, age, "Orange")

    # filter to only keep the ones that start with a-l A-L
    pattern = r'^[a-lA-L]'  # ^ means starts wtih [a-l][A-L] means letters in the set a-l
    AtoL = wmk[wmk['Last_Name'].str.contains(pattern)]

    # filter to only keep the ones that start with m-z M-Z
    pattern = r'^[m-zM-Z]'  # ^ means starts wtih [m-z][M-Z] means letters in the set m-z
    MtoZ = wmk[wmk['Last_Name'].str.contains(pattern)]

    divison_detail_report_pdf.put_dataframe_on_pdfpage(AtoL, str(starting_ring + 3), event_time, division_name, age,
                                                       "Orange (A-L)",
                                                       "*** PLEASE NOTE - These are contestants A - L")
    divison_detail_report_pdf.put_dataframe_on_pdfpage(MtoZ, str(starting_ring + 4), event_time, division_name, age,
                                                       "Orange (M-Z)",
                                                       "*** PLEASE NOTE - These are contestants M - Z")

    mask1 = mask_PurpleBelt & compositMask
    mask2 = mask_AllBlueBelt & compositMask
    mask = mask1 | mask2
    wmk = newDataFrameFromMask(mask)
    divison_detail_report_pdf.put_dataframe_on_pdfpage(wmk, str(starting_ring + 5), event_time, division_name, age,
                                                       "Purple, Blue, Blue Stripe")

    mask1 = mask_AllGreenBelt & compositMask
    mask2 = mask_AllBrownBelt & compositMask
    mask = mask1 | mask2
    wmk = newDataFrameFromMask(mask)
    divison_detail_report_pdf.put_dataframe_on_pdfpage(wmk, str(starting_ring + 6), event_time, division_name, age,
                                                       "Green, Green Stripe, Brown")
    #    mask= mask_AllBlackBelt & compositMask
    #    wmk=newDataFrameFromMask( mask )
    #    pdf_report.put_dataframe_on_pdfpage(wmk, str(starting_ring+5), time, division_name, age, "Black")


###############################################################################
# writePattern1ToKataScoreSheet
#  This method provides a re-usable method to write output to PDF
#  The Pattern it writes is:
#    White
#    Yellow
#    Orange
#    Purple, Blue, Blue Stripe
#    Green, Green Stripe, Brown
#
#  arguments:
#  filename - the filename without path to write
#  compsitMask - a mask made up of everything but the belts that you want
def writePattern1ToKataScoreSheet(starting_ring, event_time, division_name, age, compositMask):
    print(time.strftime("%X") + " Generating Detail Report PDF for " + event_time + " " + division_name + " " + age)

    kata_score_sheet_pdf.KataScoreSheetPDF.set_title("Forms")

    mask = mask_WhiteBelt & compositMask
    wmk = newDataFrameFromMask(mask)
    kata_score_sheet.put_dataframe_on_pdfpage(wmk, str(starting_ring), event_time, division_name, age, "White")

    mask = mask_YellowBelt & compositMask
    wmk = newDataFrameFromMask(mask)
    kata_score_sheet.put_dataframe_on_pdfpage(wmk, str(starting_ring + 1), event_time, division_name, age, "Yellow")

    mask = mask_OrangeBelt & compositMask
    wmk = newDataFrameFromMask(mask)
    kata_score_sheet.put_dataframe_on_pdfpage(wmk, str(starting_ring + 2), event_time, division_name, age, "Orange")

    mask1 = mask_PurpleBelt & compositMask
    mask2 = mask_AllBlueBelt & compositMask
    mask = mask1 | mask2
    wmk = newDataFrameFromMask(mask)
    kata_score_sheet.put_dataframe_on_pdfpage(wmk, str(starting_ring + 3), event_time, division_name, age,
                                              "Purple, Blue, Blue Stripe")

    mask1 = mask_AllGreenBelt & compositMask
    mask2 = mask_AllBrownBelt & compositMask
    mask = mask1 | mask2
    wmk = newDataFrameFromMask(mask)
    kata_score_sheet.put_dataframe_on_pdfpage(wmk, str(starting_ring + 4), event_time, division_name, age,
                                              "Green, Green Stripe, Brown")
    #    mask= mask_AllBlackBelt & compositMask
    #    wmk=newDataFrameFromMask( mask )
    #    kata_score_sheet.put_dataframe_on_pdfpage(wmk, str(starting_ring+5), time, division_name, age, "Black")


###############################################################################
# writePattern1WithSplitToKataScoreSheet
#  This method provides a re-usable method to write output to PDF
#  The Pattern it writes is:
#    White
#    Yellow
#    Orange
#    Purple, Blue, Blue Stripe
#    Green, Green Stripe, Brown
#
#  arguments:
#  filename - the filename without path to write
#  compsitMask - a mask made up of everything but the belts that you want
def writePattern1WithSplitToKataScoreSheet(starting_ring, event_time, division_name, age, compositMask):
    print(time.strftime("%X") + " Generating Detail Report PDF for " + event_time + " " + division_name + " " + age)

    kata_score_sheet_pdf.KataScoreSheetPDF.set_title("Forms")

    mask = mask_WhiteBelt & compositMask
    wmk = newDataFrameFromMask(mask)
    kata_score_sheet.put_dataframe_on_pdfpage(wmk, str(starting_ring), event_time, division_name, age, "White")

    mask = mask_YellowBelt & compositMask
    wmk = newDataFrameFromMask(mask)
    #    kata_score_sheet.put_dataframe_on_pdfpage(wmk, str(starting_ring + 1), event_time, division_name, age, "Yellow")

    # filter to only keep the ones that start with a-l A-L
    pattern = r'^[a-lA-L]'  # ^ means starts wtih [a-l][A-L] means letters in the set a-l
    AtoL = wmk[wmk['Last_Name'].str.contains(pattern)]

    # filter to only keep the ones that start with m-z M-Z
    pattern = r'^[m-zM-Z]'  # ^ means starts wtih [m-z][M-Z] means letters in the set m-z
    MtoZ = wmk[wmk['Last_Name'].str.contains(pattern)]

    kata_score_sheet.put_dataframe_on_pdfpage(AtoL, str(starting_ring + 1), event_time, division_name, age,
                                              "Yellow (A-L)",
                                              "*** PLEASE NOTE - These are contestants A - L")
    kata_score_sheet.put_dataframe_on_pdfpage(MtoZ, str(starting_ring + 2), event_time, division_name, age,
                                              "Yellow (M-Z)",
                                              "*** PLEASE NOTE - These are contestants M - Z")

    mask = mask_OrangeBelt & compositMask
    wmk = newDataFrameFromMask(mask)
    #   kata_score_sheet.put_dataframe_on_pdfpage(wmk, str(starting_ring + 2), event_time, division_name, age, "Orange")

    # filter to only keep the ones that start with a-l A-L
    pattern = r'^[a-lA-L]'  # ^ means starts wtih [a-l][A-L] means letters in the set a-l
    AtoL = wmk[wmk['Last_Name'].str.contains(pattern)]

    # filter to only keep the ones that start with m-z M-Z
    pattern = r'^[m-zM-Z]'  # ^ means starts wtih [m-z][M-Z] means letters in the set m-z
    MtoZ = wmk[wmk['Last_Name'].str.contains(pattern)]

    kata_score_sheet.put_dataframe_on_pdfpage(AtoL, str(starting_ring + 3), event_time, division_name, age,
                                              "Orange (A-L)",
                                              "*** PLEASE NOTE - These are contestants A - L")
    kata_score_sheet.put_dataframe_on_pdfpage(MtoZ, str(starting_ring + 4), event_time, division_name, age,
                                              "Orange (M-Z)",
                                              "*** PLEASE NOTE - These are contestants M - Z")

    mask1 = mask_PurpleBelt & compositMask
    mask2 = mask_AllBlueBelt & compositMask
    mask = mask1 | mask2
    wmk = newDataFrameFromMask(mask)
    kata_score_sheet.put_dataframe_on_pdfpage(wmk, str(starting_ring + 5), event_time, division_name, age,
                                              "Purple, Blue, Blue Stripe")

    mask1 = mask_AllGreenBelt & compositMask
    mask2 = mask_AllBrownBelt & compositMask
    mask = mask1 | mask2
    wmk = newDataFrameFromMask(mask)
    kata_score_sheet.put_dataframe_on_pdfpage(wmk, str(starting_ring + 6), event_time, division_name, age,
                                              "Green, Green Stripe, Brown")
    #    mask= mask_AllBlackBelt & compositMask
    #    wmk=newDataFrameFromMask( mask )
    #    kata_score_sheet.put_dataframe_on_pdfpage(wmk, str(starting_ring+5), time, division_name, age, "Black")


###############################################################################
# writePattern2ToExcel
#  This method provides a re-usable method to write output to excel
#  The Pattern it writes is:
#    White
#    Yellow
#    Orange
#    Purple, Blue, Blue Stripe
#    Green, Green Stripe, Brown
#
#  arguments:
#  filename - the filename without path to write
#  compsitMask - a mask made up of everything but the belts that you want
def writePattern2ToExcel(filename, compositMask):
    fullpath = os.getcwd() + pathDelimiter() + "Sorted" + pathDelimiter() + filename
    writer = pd.ExcelWriter(fullpath)
    print(time.strftime("%X") + " Generating " + fullpath)

    mask = mask_WhiteBelt & compositMask
    wmk = newDataFrameFromMask(mask)
    writeFormattedExcelSheet(wmk, writer, 'White')

    mask = mask_YellowBelt & compositMask
    wmk = newDataFrameFromMask(mask)
    writeFormattedExcelSheet(wmk, writer, 'Yellow')

    mask = mask_OrangeBelt & compositMask
    wmk = newDataFrameFromMask(mask)
    writeFormattedExcelSheet(wmk, writer, 'Orange')

    mask1 = mask_PurpleBelt & compositMask
    mask2 = mask_AllBlueBelt & compositMask
    mask = mask1 | mask2
    wmk = newDataFrameFromMask(mask)
    writeFormattedExcelSheet(wmk, writer, 'Purple, Blue, Blue Stripe')

    mask1 = mask_AllGreenBelt & compositMask
    mask2 = mask_AllBrownBelt & compositMask
    mask = mask1 | mask2
    wmk = newDataFrameFromMask(mask)
    writeFormattedExcelSheet(wmk, writer, 'Green, Green Stripe, Brown')

    #
    #    mask= mask_AllBlackBelt & compositMask
    #    wmk=newDataFrameFromMask( mask )
    #    wmk.to_excel(writer,'Black')

    writer.save()
    time.sleep(1)


###############################################################################
# writePattern2ToDetailReport
#  This method provides a re-usable method to write output to PDF
#  The Pattern it writes is:
#    White
#    Yellow
#    Orange
#    Purple, Blue, Blue Stripe
#    Green, Green Stripe
#
#  arguments:
def writePattern2ToDetailReport(starting_ring, event_time, division_name, age, compositMask):
    print(time.strftime("%X") + " Generating Detail Report PDF for " + event_time + " " + division_name + " " + age)

    DivisionDetailReportPDF.DivisionDetailReportPDF.set_title(division_name)

    mask = mask_WhiteBelt & compositMask
    wmk = newDataFrameFromMask(mask)
    divison_detail_report_pdf.put_dataframe_on_pdfpage(wmk, str(starting_ring), event_time, division_name, age, "White")

    mask = mask_YellowBelt & compositMask
    wmk = newDataFrameFromMask(mask)
    divison_detail_report_pdf.put_dataframe_on_pdfpage(wmk, str(starting_ring + 1), event_time, division_name, age,
                                                       "Yellow")

    mask = mask_OrangeBelt & compositMask
    wmk = newDataFrameFromMask(mask)
    divison_detail_report_pdf.put_dataframe_on_pdfpage(wmk, str(starting_ring + 2), event_time, division_name, age,
                                                       "Orange")

    mask1 = mask_PurpleBelt & compositMask
    mask2 = mask_AllBlueBelt & compositMask
    mask = mask1 | mask2
    wmk = newDataFrameFromMask(mask)
    divison_detail_report_pdf.put_dataframe_on_pdfpage(wmk, str(starting_ring + 3), event_time, division_name, age,
                                                       "Purple, Blue, Blue Stripe")

    mask1 = mask_AllGreenBelt & compositMask
    mask2 = mask_AllBrownBelt & compositMask
    mask = mask1 | mask2
    wmk = newDataFrameFromMask(mask)
    divison_detail_report_pdf.put_dataframe_on_pdfpage(wmk, str(starting_ring + 4), event_time, division_name, age,
                                                       "Green, Green Stripe, Brown")


#
#    mask= mask_AllBlackBelt & compositMask
#    wmk=newDataFrameFromMask( mask )
#    divison_detail_report_pdf.put_dataframe_on_pdfpage(wmk, str(starting_ring + 5), time, division_name, age, "Black")


###############################################################################
# writePattern2ToKataScoreSheet
#  This method provides a re-usable method to write output to PDF
#  The Pattern it writes is:
#    White
#    Yellow
#    Orange
#    Purple, Blue, Blue Stripe
#    Green, Green Stripe
#
#  arguments:
def writePattern2ToKataScoreSheet(starting_ring, event_time, division_name, age, compositMask):
    print(time.strftime("%X") + " Generating Detail Report PDF for " + event_time + " " + division_name + " " + age)

    kata_score_sheet_pdf.KataScoreSheetPDF.set_title("Forms")

    mask = mask_WhiteBelt & compositMask
    wmk = newDataFrameFromMask(mask)
    kata_score_sheet.put_dataframe_on_pdfpage(wmk, str(starting_ring), event_time, division_name, age, "White")

    mask = mask_YellowBelt & compositMask
    wmk = newDataFrameFromMask(mask)
    kata_score_sheet.put_dataframe_on_pdfpage(wmk, str(starting_ring + 1), event_time, division_name, age, "Yellow")

    mask = mask_OrangeBelt & compositMask
    wmk = newDataFrameFromMask(mask)
    kata_score_sheet.put_dataframe_on_pdfpage(wmk, str(starting_ring + 2), event_time, division_name, age, "Orange")

    mask1 = mask_PurpleBelt & compositMask
    mask2 = mask_AllBlueBelt & compositMask
    mask = mask1 | mask2
    wmk = newDataFrameFromMask(mask)
    kata_score_sheet.put_dataframe_on_pdfpage(wmk, str(starting_ring + 3), event_time, division_name, age,
                                              "Purple, Blue, Blue Stripe")

    mask1 = mask_AllGreenBelt & compositMask
    mask2 = mask_AllBrownBelt & compositMask
    mask = mask1 | mask2
    wmk = newDataFrameFromMask(mask)
    kata_score_sheet.put_dataframe_on_pdfpage(wmk, str(starting_ring + 4), event_time, division_name, age,
                                              "Green, Green Stripe, Brown")


#
#    mask= mask_AllBlackBelt & compositMask
#    wmk=newDataFrameFromMask( mask )
#    kata_score_sheet.put_dataframe_on_pdfpage(wmk, str(starting_ring + 5), time, division_name, age, "Black")


###############################################################################
# writePattern3ToExcel
#  This method provides a re-usable method to write output to excel
#  The Pattern it writes is:
#    White
#    Yellow
#    Orange
#    Purple
#    Blue, Blue Stripe
#    Green, Green Stripe, Brown
#
#  arguments:
#  filename - the filename without path to write
#  compsitMask - a mask made up of everything but the belts that you want
def writePattern3ToExcel(filename, compositMask):
    fullpath = os.getcwd() + pathDelimiter() + "Sorted" + pathDelimiter() + filename
    writer = pd.ExcelWriter(fullpath)
    print(time.strftime("%X") + " Generating " + fullpath)

    mask = mask_WhiteBelt & compositMask
    wmk = newDataFrameFromMask(mask)
    writeFormattedExcelSheet(wmk, writer, 'White')

    mask = mask_YellowBelt & compositMask
    wmk = newDataFrameFromMask(mask)
    writeFormattedExcelSheet(wmk, writer, 'Yellow')

    mask = mask_OrangeBelt & compositMask
    wmk = newDataFrameFromMask(mask)
    writeFormattedExcelSheet(wmk, writer, 'Orange')

    mask = mask_PurpleBelt & compositMask
    wmk = newDataFrameFromMask(mask)
    writeFormattedExcelSheet(wmk, writer, 'Purple')

    mask = mask_AllBlueBelt & compositMask
    wmk = newDataFrameFromMask(mask)
    writeFormattedExcelSheet(wmk, writer, 'Blue, Blue Stripe')

    mask1 = mask_AllGreenBelt & compositMask
    mask2 = mask_AllBrownBelt & compositMask
    mask = mask1 | mask2
    wmk = newDataFrameFromMask(mask)
    writeFormattedExcelSheet(wmk, writer, 'Green, Green Stripe, Brown')

    writer.save()
    time.sleep(1)


###############################################################################
# writePattern3ToDetailReport
#  This method provides a re-usable method to write output to PDF
#  The Pattern it writes is:
#    White
#    Yellow
#    Orange
#    Purple
#    Blue, Blue Stripe
#    Green, Green Stripe, Brown
#
def writePattern3ToDetailReport(starting_ring, event_time, division_name, age, compositMask):
    print(time.strftime("%X") + " Generating Detail Report PDF for " + event_time + " " + division_name + " " + age)

    DivisionDetailReportPDF.DivisionDetailReportPDF.set_title(division_name)

    mask = mask_WhiteBelt & compositMask
    wmk = newDataFrameFromMask(mask)
    divison_detail_report_pdf.put_dataframe_on_pdfpage(wmk, str(starting_ring), event_time, division_name, age, "White")

    mask = mask_YellowBelt & compositMask
    wmk = newDataFrameFromMask(mask)
    divison_detail_report_pdf.put_dataframe_on_pdfpage(wmk, str(starting_ring + 1), event_time, division_name, age,
                                                       "Yellow")

    mask = mask_OrangeBelt & compositMask
    wmk = newDataFrameFromMask(mask)
    divison_detail_report_pdf.put_dataframe_on_pdfpage(wmk, str(starting_ring + 2), event_time, division_name, age,
                                                       "Orange")

    mask = mask_PurpleBelt & compositMask
    wmk = newDataFrameFromMask(mask)
    divison_detail_report_pdf.put_dataframe_on_pdfpage(wmk, str(starting_ring + 3), event_time, division_name, age,
                                                       "Purple")

    mask = mask_AllBlueBelt & compositMask
    wmk = newDataFrameFromMask(mask)
    divison_detail_report_pdf.put_dataframe_on_pdfpage(wmk, str(starting_ring + 4), event_time, division_name, age,
                                                       "Blue, Blue Stripe")

    mask1 = mask_AllGreenBelt & compositMask
    mask2 = mask_AllBrownBelt & compositMask
    mask = mask1 | mask2
    wmk = newDataFrameFromMask(mask)
    divison_detail_report_pdf.put_dataframe_on_pdfpage(wmk, str(starting_ring + 5), event_time, division_name, age,
                                                       "Green, Green Stripe, Brown")


###############################################################################
# writePattern3WithSplitToDetailReport
#  This method provides a re-usable method to write output to PDF
#  The Pattern it writes is:
#    White
#    Yellow
#    Orange
#    Purple
#    Blue, Blue Stripe
#    Green, Green Stripe, Brown
#
def writePattern3WithSplitToDetailReport(starting_ring, event_time, division_name, age, compositMask):
    print(time.strftime("%X") + " Generating Detail Report PDF for " + event_time + " " + division_name + " " + age)

    DivisionDetailReportPDF.DivisionDetailReportPDF.set_title(division_name)

    mask = mask_WhiteBelt & compositMask
    wmk = newDataFrameFromMask(mask)
    divison_detail_report_pdf.put_dataframe_on_pdfpage(wmk, str(starting_ring), event_time, division_name, age, "White")

    mask = mask_YellowBelt & compositMask
    wmk = newDataFrameFromMask(mask)
    divison_detail_report_pdf.put_dataframe_on_pdfpage(wmk, str(starting_ring + 1), event_time, division_name, age,
                                                       "Yellow")

    mask = mask_OrangeBelt & compositMask
    wmk = newDataFrameFromMask(mask)
    #    divison_detail_report_pdf.put_dataframe_on_pdfpage(wmk, str(starting_ring + 3), event_time, division_name, age, "Orange")

    # filter to only keep the ones that start with a-l A-L
    pattern = r'^[a-lA-L]'  # ^ means starts wtih [a-l][A-L] means letters in the set a-l
    AtoL = wmk[wmk['Last_Name'].str.contains(pattern)]

    # filter to only keep the ones that start with m-z M-Z
    pattern = r'^[m-zM-Z]'  # ^ means starts wtih [m-z][M-Z] means letters in the set m-z
    MtoZ = wmk[wmk['Last_Name'].str.contains(pattern)]

    divison_detail_report_pdf.put_dataframe_on_pdfpage(AtoL, str(starting_ring + 2), event_time, division_name, age,
                                                       "Orange (A-L)",
                                                       "*** PLEASE NOTE - These are contestants A - L")
    divison_detail_report_pdf.put_dataframe_on_pdfpage(MtoZ, str(starting_ring + 2), event_time, division_name, age,
                                                       "Orange (M-Z)",
                                                       "*** PLEASE NOTE - These are contestants M - Z")

    mask = mask_PurpleBelt & compositMask
    wmk = newDataFrameFromMask(mask)
    #    divison_detail_report_pdf.put_dataframe_on_pdfpage(wmk, str(starting_ring + 5), event_time, division_name, age, "Purple")

    # filter to only keep the ones that start with a-l A-L
    pattern = r'^[a-lA-L]'  # ^ means starts wtih [a-l][A-L] means letters in the set a-l
    AtoL = wmk[wmk['Last_Name'].str.contains(pattern)]

    # filter to only keep the ones that start with m-z M-Z
    pattern = r'^[m-zM-Z]'  # ^ means starts wtih [m-z][M-Z] means letters in the set m-z
    MtoZ = wmk[wmk['Last_Name'].str.contains(pattern)]

    divison_detail_report_pdf.put_dataframe_on_pdfpage(AtoL, str(starting_ring + 4), event_time, division_name, age,
                                                       "Purple (A-L)",
                                                       "*** PLEASE NOTE - These are contestants A - L")
    divison_detail_report_pdf.put_dataframe_on_pdfpage(MtoZ, str(starting_ring + 5), event_time, division_name, age,
                                                       "Purple (M-Z)",
                                                       "*** PLEASE NOTE - These are contestants M - Z")

    mask = mask_AllBlueBelt & compositMask
    wmk = newDataFrameFromMask(mask)
    divison_detail_report_pdf.put_dataframe_on_pdfpage(wmk, str(starting_ring + 6), event_time, division_name, age,
                                                       "Blue, Blue Stripe")

    mask1 = mask_AllGreenBelt & compositMask
    mask2 = mask_AllBrownBelt & compositMask
    mask = mask1 | mask2
    wmk = newDataFrameFromMask(mask)
    divison_detail_report_pdf.put_dataframe_on_pdfpage(wmk, str(starting_ring + 7), event_time, division_name, age,
                                                       "Green, Green Stripe, Brown")


###############################################################################
# writePattern3ToKataScoreSheet
#  This method provides a re-usable method to write output to PDF
#  The Pattern it writes is:
#    White
#    Yellow
#    Orange
#    Purple
#    Blue, Blue Stripe
#    Green, Green Stripe, Brown
#
def writePatternSplitToKataScoreSheet(starting_ring, event_time, division_name, age, compositMask):
    print(time.strftime("%X") + " Generating Detail Report PDF for " + event_time + " " + division_name + " " + age)

    kata_score_sheet_pdf.KataScoreSheetPDF.set_title("Forms")

    mask = mask_WhiteBelt & compositMask
    wmk = newDataFrameFromMask(mask)
    kata_score_sheet.put_dataframe_on_pdfpage(wmk, str(starting_ring), event_time, division_name, age, "White")

    mask = mask_YellowBelt & compositMask
    wmk = newDataFrameFromMask(mask)
    kata_score_sheet.put_dataframe_on_pdfpage(wmk, str(starting_ring + 1), event_time, division_name, age, "Yellow")

    mask = mask_OrangeBelt & compositMask
    wmk = newDataFrameFromMask(mask)
    kata_score_sheet.put_dataframe_on_pdfpage(wmk, str(starting_ring + 2), event_time, division_name, age, "Orange")

    mask = mask_PurpleBelt & compositMask
    wmk = newDataFrameFromMask(mask)
    kata_score_sheet.put_dataframe_on_pdfpage(wmk, str(starting_ring + 3), event_time, division_name, age, "Purple")

    mask = mask_AllBlueBelt & compositMask
    wmk = newDataFrameFromMask(mask)
    kata_score_sheet.put_dataframe_on_pdfpage(wmk, str(starting_ring + 4), event_time, division_name, age,
                                              "Blue, Blue Stripe")

    mask1 = mask_AllGreenBelt & compositMask
    mask2 = mask_AllBrownBelt & compositMask
    mask = mask1 | mask2
    wmk = newDataFrameFromMask(mask)
    kata_score_sheet.put_dataframe_on_pdfpage(wmk, str(starting_ring + 5), event_time, division_name, age,
                                              "Green, Green Stripe, Brown")


###############################################################################
# writePattern3WithSplitToKataScoreSheet
#  This method provides a re-usable method to write output to PDF
#  The Pattern it writes is:
#    White
#    Yellow
#    Orange
#    Purple
#    Blue, Blue Stripe
#    Green, Green Stripe, Brown
#
def writePattern3WithSplitToKataScoreSheet(starting_ring, event_time, division_name, age, compositMask):
    print(time.strftime("%X") + " Generating Detail Report PDF for " + event_time + " " + division_name + " " + age)

    kata_score_sheet_pdf.KataScoreSheetPDF.set_title("Forms")

    mask = mask_WhiteBelt & compositMask
    wmk = newDataFrameFromMask(mask)
    kata_score_sheet.put_dataframe_on_pdfpage(wmk, str(starting_ring), event_time, division_name, age, "White")

    mask = mask_YellowBelt & compositMask
    wmk = newDataFrameFromMask(mask)
    kata_score_sheet.put_dataframe_on_pdfpage(wmk, str(starting_ring + 1), event_time, division_name, age, "Yellow")

    mask = mask_OrangeBelt & compositMask
    wmk = newDataFrameFromMask(mask)
    #    kata_score_sheet.put_dataframe_on_pdfpage(wmk, str(starting_ring + 2), event_time, division_name, age, "Orange")

    # filter to only keep the ones that start with a-l A-L
    pattern = r'^[a-lA-L]'  # ^ means starts wtih [a-l][A-L] means letters in the set a-l
    AtoL = wmk[wmk['Last_Name'].str.contains(pattern)]

    # filter to only keep the ones that start with m-z M-Z
    pattern = r'^[m-zM-Z]'  # ^ means starts wtih [m-z][M-Z] means letters in the set m-z
    MtoZ = wmk[wmk['Last_Name'].str.contains(pattern)]

    kata_score_sheet.put_dataframe_on_pdfpage(AtoL, str(starting_ring + 2), event_time, division_name, age,
                                              "Orange (A-L)",
                                              "*** PLEASE NOTE - These are contestants A - L")
    kata_score_sheet.put_dataframe_on_pdfpage(MtoZ, str(starting_ring + 3), event_time, division_name, age,
                                              "Orange (M-Z)",
                                              "*** PLEASE NOTE - These are contestants M - Z")

    mask = mask_PurpleBelt & compositMask
    wmk = newDataFrameFromMask(mask)
    #   kata_score_sheet.put_dataframe_on_pdfpage(wmk, str(starting_ring + 5), event_time, division_name, age, "Purple")

    # filter to only keep the ones that start with a-l A-L
    pattern = r'^[a-lA-L]'  # ^ means starts wtih [a-l][A-L] means letters in the set a-l
    AtoL = wmk[wmk['Last_Name'].str.contains(pattern)]

    # filter to only keep the ones that start with m-z M-Z
    pattern = r'^[m-zM-Z]'  # ^ means starts wtih [m-z][M-Z] means letters in the set m-z
    MtoZ = wmk[wmk['Last_Name'].str.contains(pattern)]

    kata_score_sheet.put_dataframe_on_pdfpage(AtoL, str(starting_ring + 4), event_time, division_name, age,
                                              "Purple (A-L)",
                                              "*** PLEASE NOTE - These are contestants A - L")
    kata_score_sheet.put_dataframe_on_pdfpage(MtoZ, str(starting_ring + 5), event_time, division_name, age,
                                              "Purple (M-Z)",
                                              "*** PLEASE NOTE - These are contestants M - Z")

    mask = mask_AllBlueBelt & compositMask
    wmk = newDataFrameFromMask(mask)
    kata_score_sheet.put_dataframe_on_pdfpage(wmk, str(starting_ring + 6), event_time, division_name, age,
                                              "Blue, Blue Stripe")

    mask1 = mask_AllGreenBelt & compositMask
    mask2 = mask_AllBrownBelt & compositMask
    mask = mask1 | mask2
    wmk = newDataFrameFromMask(mask)
    kata_score_sheet.put_dataframe_on_pdfpage(wmk, str(starting_ring + 7), event_time, division_name, age,
                                              "Green, Green Stripe, Brown")


###############################################################################
# writePattern4ToExcel
#  This method provides a re-usable method to write output to excel
#  The Pattern it writes is:
#    White, Yellow, Orange
#    Purple, Blue, Blue Stripe
#    Green, Green Stripe, Brown
#    Black
#
#  arguments:
#  filename - the filename without path to write
#  compsitMask - a mask made up of everything but the belts that you want
#
def writePattern4ToExcel(filename, compositMask):
    fullpath = os.getcwd() + pathDelimiter() + "Sorted" + pathDelimiter() + filename
    writer = pd.ExcelWriter(fullpath)
    print(time.strftime("%X") + " Generating " + fullpath)

    mask1 = mask_WhiteBelt & compositMask
    mask2 = mask_YellowBelt & compositMask
    mask3 = mask_OrangeBelt & compositMask
    mask = mask1 | mask2 | mask3
    wmk = newDataFrameFromMask(mask)
    writeFormattedExcelSheet(wmk, writer, 'White, Yellow, Orange')

    #    mask= mask_OrangeBelt & compositMask
    #    wmk=newDataFrameFromMask( mask )

    #    mask= mask_PurpleBelt & compositMask
    #    wmk=newDataFrameFromMask( mask )

    mask1 = mask_PurpleBelt & compositMask
    mask2 = mask_AllBlueBelt & compositMask
    mask = mask1 | mask2
    wmk = newDataFrameFromMask(mask)
    writeFormattedExcelSheet(wmk, writer, 'Purple, Blue, Blue Stripe')

    mask1 = mask_AllBrownBelt & compositMask
    mask2 = mask_AllGreenBelt & compositMask
    mask = mask1 | mask2
    wmk = newDataFrameFromMask(mask)
    writeFormattedExcelSheet(wmk, writer, 'Green, Green Stripe, Brown')

    #    mask= mask_AllBrownBelt & compositMask
    #    wmk=newDataFrameFromMask( mask )

    mask = mask_AllBlackBelt & compositMask
    wmk = newDataFrameFromMask(mask)
    writeFormattedExcelSheet(wmk, writer, 'Black')

    writer.save()
    time.sleep(1)


###############################################################################
# writePattern4ToDetailReport
#  This method provides a re-usable method to write output to PDF
#  The Pattern it writes is:
#    White, Yellow, Orange
#    Purple, Blue, Blue Stripe
#    Green, Green Stripe, Brown
#    Black
#
def writePattern4ToDetailReport(starting_ring, event_time, division_name, age, compositMask):
    print(time.strftime("%X") + " Generating Detail Report PDF for " + event_time + " " + division_name + " " + age)

    DivisionDetailReportPDF.DivisionDetailReportPDF.set_title(division_name)

    mask1 = mask_WhiteBelt & compositMask
    mask2 = mask_YellowBelt & compositMask
    mask3 = mask_OrangeBelt & compositMask
    mask = mask1 | mask2 | mask3
    wmk = newDataFrameFromMask(mask)
    divison_detail_report_pdf.put_dataframe_on_pdfpage(wmk, str(starting_ring), event_time, division_name, age,
                                                       "White, Yellow, Orange")

    #    mask= mask_OrangeBelt & compositMask
    #    wmk=newDataFrameFromMask( mask )
    #    wmk.to_excel(writer,'Orange')

    #    mask= mask_PurpleBelt & compositMask
    #    wmk=newDataFrameFromMask( mask )
    #    wmk.to_excel(writer,'Purple')

    mask1 = mask_PurpleBelt & compositMask
    mask2 = mask_AllBlueBelt & compositMask
    mask = mask1 | mask2
    wmk = newDataFrameFromMask(mask)
    divison_detail_report_pdf.put_dataframe_on_pdfpage(wmk, str(starting_ring + 1), event_time, division_name, age,
                                                       "Purple, Blue, Blue Stripe")

    mask1 = mask_AllBrownBelt & compositMask
    mask2 = mask_AllGreenBelt & compositMask
    mask = mask1 | mask2
    wmk = newDataFrameFromMask(mask)
    divison_detail_report_pdf.put_dataframe_on_pdfpage(wmk, str(starting_ring + 2), event_time, division_name, age,
                                                       "Green, Green Stripe, Brown")

    mask = mask_AllBlackBelt & compositMask
    wmk = newDataFrameFromMask(mask)
    divison_detail_report_pdf.put_dataframe_on_pdfpage(wmk, str(starting_ring + 3), event_time, division_name, age,
                                                       "Black")


###############################################################################
# writePattern4ToKataScoreSheet
#  This method provides a re-usable method to write output to PDF
#  The Pattern it writes is:
#    White, Yellow, Orange
#    Purple, Blue, Blue Stripe
#    Green, Green Stripe, Brown
#    Black
#
def writePattern4ToKataScoreSheet(starting_ring, event_time, division_name, age, compositMask):
    print(time.strftime("%X") + " Generating Detail Report PDF for " + event_time + " " + division_name + " " + age)

    kata_score_sheet_pdf.KataScoreSheetPDF.set_title("Forms")

    mask1 = mask_WhiteBelt & compositMask
    mask2 = mask_YellowBelt & compositMask
    mask3 = mask_OrangeBelt & compositMask
    mask = mask1 | mask2 | mask3
    wmk = newDataFrameFromMask(mask)
    kata_score_sheet.put_dataframe_on_pdfpage(wmk, str(starting_ring), event_time, division_name, age,
                                              "White, Yellow, Orange")

    #    mask= mask_OrangeBelt & compositMask
    #    wmk=newDataFrameFromMask( mask )
    #    wmk.to_excel(writer,'Orange')

    #    mask= mask_PurpleBelt & compositMask
    #    wmk=newDataFrameFromMask( mask )
    #    wmk.to_excel(writer,'Purple')

    mask1 = mask_PurpleBelt & compositMask
    mask2 = mask_AllBlueBelt & compositMask
    mask = mask1 | mask2
    wmk = newDataFrameFromMask(mask)
    kata_score_sheet.put_dataframe_on_pdfpage(wmk, str(starting_ring + 1), event_time, division_name, age,
                                              "Purple, Blue, Blue Stripe")

    mask1 = mask_AllBrownBelt & compositMask
    mask2 = mask_AllGreenBelt & compositMask
    mask = mask1 | mask2
    wmk = newDataFrameFromMask(mask)
    kata_score_sheet.put_dataframe_on_pdfpage(wmk, str(starting_ring + 2), event_time, division_name, age,
                                              "Green, Green Stripe, Brown")

    mask = mask_AllBlackBelt & compositMask
    wmk = newDataFrameFromMask(mask)
    kata_score_sheet.put_dataframe_on_pdfpage(wmk, str(starting_ring + 3), event_time, division_name, age, "Black")


###############################################################################
# writePattern5ToExcel
#  This method provides a re-usable method to write output to excel
#  The Pattern it writes is:
#    White, Yellow
#    Purple
#    Blue, Blue Stripe
#    Green, Green Stripe, Brown
#
#  arguments:
#  filename - the filename without path to write
#  compsitMask - a mask made up of everything but the belts that you want
def writePattern5ToExcel(filename, compositMask):
    fullpath = os.getcwd() + pathDelimiter() + "Sorted" + pathDelimiter() + filename
    writer = pd.ExcelWriter(fullpath)
    print(time.strftime("%X") + " Generating " + fullpath)

    mask1 = mask_WhiteBelt & compositMask
    mask2 = mask_YellowBelt & compositMask
    mask = mask1 | mask2
    wmk = newDataFrameFromMask(mask)
    writeFormattedExcelSheet(wmk, writer, 'White, Yellow')

    mask = mask_OrangeBelt & compositMask
    wmk = newDataFrameFromMask(mask)
    writeFormattedExcelSheet(wmk, writer, 'Orange')

    mask = mask_PurpleBelt & compositMask
    wmk = newDataFrameFromMask(mask)
    writeFormattedExcelSheet(wmk, writer, 'Purple')

    mask = mask_AllBlueBelt & compositMask
    wmk = newDataFrameFromMask(mask)
    writeFormattedExcelSheet(wmk, writer, 'Blue, Blue Stripe')

    mask1 = mask_AllGreenBelt & compositMask
    mask2 = mask_AllBrownBelt & compositMask
    mask = mask1 | mask2
    wmk = newDataFrameFromMask(mask)
    writeFormattedExcelSheet(wmk, writer, 'Green, Green Stripe, Brown')

    writer.save()
    time.sleep(1)


###############################################################################
# writePattern5ToDetailReport
#  This method provides a re-usable method to write output to PDF
#  The Pattern it writes is:
#    White, Yellow
#    Orange
#    Purple
#    Blue, Blue Stripe
#    Green, Green Stripe, Brown
#
def writePattern5ToDetailReport(starting_ring, event_time, division_name, age, compositMask):
    print(time.strftime("%X") + " Generating Detail Report PDF for " + event_time + " " + division_name + " " + age)

    DivisionDetailReportPDF.DivisionDetailReportPDF.set_title(division_name)

    mask1 = mask_WhiteBelt & compositMask
    mask2 = mask_YellowBelt & compositMask
    mask = mask1 | mask2
    wmk = newDataFrameFromMask(mask)
    divison_detail_report_pdf.put_dataframe_on_pdfpage(wmk, str(starting_ring), event_time, division_name, age,
                                                       "White, Yellow")

    mask = mask_OrangeBelt & compositMask
    wmk = newDataFrameFromMask(mask)
    divison_detail_report_pdf.put_dataframe_on_pdfpage(wmk, str(starting_ring + 1), event_time, division_name, age,
                                                       "Orange")

    mask = mask_PurpleBelt & compositMask
    wmk = newDataFrameFromMask(mask)
    divison_detail_report_pdf.put_dataframe_on_pdfpage(wmk, str(starting_ring + 2), event_time, division_name, age,
                                                       "Purple")

    mask = mask_AllBlueBelt & compositMask
    wmk = newDataFrameFromMask(mask)
    divison_detail_report_pdf.put_dataframe_on_pdfpage(wmk, str(starting_ring + 3), event_time, division_name, age,
                                                       "Blue, Blue Stripe")

    mask1 = mask_AllGreenBelt & compositMask
    mask2 = mask_AllBrownBelt & compositMask
    mask = mask1 | mask2
    wmk = newDataFrameFromMask(mask)
    divison_detail_report_pdf.put_dataframe_on_pdfpage(wmk, str(starting_ring + 4), event_time, division_name, age,
                                                       "Green, Green Stripe, Brown")


###############################################################################
# writePattern5ToKataScoreSheet
#  This method provides a re-usable method to write output to PDF
#  The Pattern it writes is:
#    White, Yellow
#    Purple
#    Blue, Blue Stripe
#    Green, Green Stripe, Brown
#
def writePattern5ToKataScoreSheet(starting_ring, event_time, division_name, age, compositMask):
    print(time.strftime("%X") + " Generating Detail Report PDF for " + event_time + " " + division_name + " " + age)

    kata_score_sheet_pdf.KataScoreSheetPDF.set_title("Forms")

    mask1 = mask_WhiteBelt & compositMask
    mask2 = mask_YellowBelt & compositMask
    mask = mask1 | mask2
    wmk = newDataFrameFromMask(mask)
    kata_score_sheet.put_dataframe_on_pdfpage(wmk, str(starting_ring), event_time, division_name, age, "White, Yellow")

    mask = mask_OrangeBelt & compositMask
    wmk = newDataFrameFromMask(mask)
    kata_score_sheet.put_dataframe_on_pdfpage(wmk, str(starting_ring + 1), event_time, division_name, age, "Orange")

    mask = mask_PurpleBelt & compositMask
    wmk = newDataFrameFromMask(mask)
    kata_score_sheet.put_dataframe_on_pdfpage(wmk, str(starting_ring + 2), event_time, division_name, age, "Purple")

    mask = mask_AllBlueBelt & compositMask
    wmk = newDataFrameFromMask(mask)
    kata_score_sheet.put_dataframe_on_pdfpage(wmk, str(starting_ring + 3), event_time, division_name, age,
                                              "Blue, Blue Stripe")

    mask1 = mask_AllGreenBelt & compositMask
    mask2 = mask_AllBrownBelt & compositMask
    mask = mask1 | mask2
    wmk = newDataFrameFromMask(mask)
    kata_score_sheet.put_dataframe_on_pdfpage(wmk, str(starting_ring + 4), event_time, division_name, age,
                                              "Green, Green Stripe, Brown")


###############################################################################
# writePattern6ToExcel
#  This method provides a re-usable method to write output to excel
#  The Pattern it writes is:
#    White, Yellow
#    Orange
#    Purple
#    Blue, Blue Stripe
#    Green, Green Stripe
#    Brown
#    Black
#
#  arguments:
#  filename - the filename without path to write
#  compsitMask - a mask made up of everything but the belts that you want
#
def writePattern6ToExcel(filename, compositMask):
    fullpath = os.getcwd() + pathDelimiter() + "Sorted" + pathDelimiter() + filename
    writer = pd.ExcelWriter(fullpath)
    print(time.strftime("%X") + " Generating " + fullpath)

    mask1 = mask_WhiteBelt & compositMask
    mask2 = mask_YellowBelt & compositMask
    mask = mask1 | mask2
    wmk = newDataFrameFromMask(mask)
    writeFormattedExcelSheet(wmk, writer, 'White, Yellow')

    mask = mask_OrangeBelt & compositMask
    wmk = newDataFrameFromMask(mask)
    writeFormattedExcelSheet(wmk, writer, 'Orange')

    mask = mask_PurpleBelt & compositMask
    wmk = newDataFrameFromMask(mask)
    writeFormattedExcelSheet(wmk, writer, 'Purple')

    mask = mask_AllBlueBelt & compositMask
    wmk = newDataFrameFromMask(mask)
    writeFormattedExcelSheet(wmk, writer, 'Blue, Blue Stripe')

    mask = mask_AllGreenBelt & compositMask
    wmk = newDataFrameFromMask(mask)
    writeFormattedExcelSheet(wmk, writer, 'Green, Green Stripe')

    mask = mask_AllBrownBelt & compositMask
    wmk = newDataFrameFromMask(mask)
    writeFormattedExcelSheet(wmk, writer, 'Brown')

    mask = mask_AllBlackBelt & compositMask
    wmk = newDataFrameFromMask(mask)
    writeFormattedExcelSheet(wmk, writer, 'Black')

    writer.save()
    time.sleep(1)


###############################################################################
# writePattern6ToDetailReport
#  This method provides a re-usable method to write output to PDF
#  The Pattern it writes is:
#    White, Yellow
#    Purple
#    Blue, Blue Stripe
#    Green, Green Stripe
#    Brown
#    Black
#
def writePattern6ToDetailReport(starting_ring, event_time, division_name, age, compositMask):
    print(time.strftime("%X") + " Generating Detail Report PDF for " + event_time + " " + division_name + " " + age)

    DivisionDetailReportPDF.DivisionDetailReportPDF.set_title(division_name)

    mask1 = mask_WhiteBelt & compositMask
    mask2 = mask_YellowBelt & compositMask
    mask = mask1 | mask2
    wmk = newDataFrameFromMask(mask)
    divison_detail_report_pdf.put_dataframe_on_pdfpage(wmk, str(starting_ring), event_time, division_name, age,
                                                       "White, Yellow")

    mask = mask_OrangeBelt & compositMask
    wmk = newDataFrameFromMask(mask)
    divison_detail_report_pdf.put_dataframe_on_pdfpage(wmk, str(starting_ring + 1), event_time, division_name, age,
                                                       "Orange")

    mask = mask_PurpleBelt & compositMask
    wmk = newDataFrameFromMask(mask)
    divison_detail_report_pdf.put_dataframe_on_pdfpage(wmk, str(starting_ring + 2), event_time, division_name, age,
                                                       "Purple")

    mask = mask_AllBlueBelt & compositMask
    wmk = newDataFrameFromMask(mask)
    divison_detail_report_pdf.put_dataframe_on_pdfpage(wmk, str(starting_ring + 3), event_time, division_name, age,
                                                       "Blue, Blue Stripe")

    mask = mask_AllGreenBelt & compositMask
    wmk = newDataFrameFromMask(mask)
    divison_detail_report_pdf.put_dataframe_on_pdfpage(wmk, str(starting_ring + 4), event_time, division_name, age,
                                                       "Green, Green Stripe")

    mask = mask_AllBrownBelt & compositMask
    wmk = newDataFrameFromMask(mask)
    divison_detail_report_pdf.put_dataframe_on_pdfpage(wmk, str(starting_ring + 5), event_time, division_name, age,
                                                       "Brown")

    mask = mask_AllBlackBelt & compositMask
    wmk = newDataFrameFromMask(mask)
    divison_detail_report_pdf.put_dataframe_on_pdfpage(wmk, str(starting_ring + 6), event_time, division_name, age,
                                                       "Black")


###############################################################################
# writePattern6ToKataScoreSheet
#  This method provides a re-usable method to write output to PDF
#  The Pattern it writes is:
#    White, Yellow
#    Orange
#    Purple
#    Blue, Blue Stripe
#    Green, Green Stripe
#    Brown
#    Black
#
def writePattern6ToKataScoreSheet(starting_ring, event_time, division_name, age, compositMask):
    print(time.strftime("%X") + " Generating Kata Score Sheet PDF for " + event_time + " " + division_name + " " + age)

    kata_score_sheet_pdf.KataScoreSheetPDF.set_title("Forms")

    mask1 = mask_WhiteBelt & compositMask
    mask2 = mask_YellowBelt & compositMask
    mask = mask1 | mask2
    wmk = newDataFrameFromMask(mask)
    kata_score_sheet.put_dataframe_on_pdfpage(wmk, str(starting_ring), event_time, division_name, age, "White, Yellow")

    mask = mask_OrangeBelt & compositMask
    wmk = newDataFrameFromMask(mask)
    kata_score_sheet.put_dataframe_on_pdfpage(wmk, str(starting_ring + 1), event_time, division_name, age, "Orange")

    mask = mask_PurpleBelt & compositMask
    wmk = newDataFrameFromMask(mask)
    kata_score_sheet.put_dataframe_on_pdfpage(wmk, str(starting_ring + 2), event_time, division_name, age, "Purple")

    mask = mask_AllBlueBelt & compositMask
    wmk = newDataFrameFromMask(mask)
    kata_score_sheet.put_dataframe_on_pdfpage(wmk, str(starting_ring + 3), event_time, division_name, age,
                                              "Blue, Blue Stripe")

    mask = mask_AllGreenBelt & compositMask
    wmk = newDataFrameFromMask(mask)
    kata_score_sheet.put_dataframe_on_pdfpage(wmk, str(starting_ring + 4), event_time, division_name, age,
                                              "Green, Green Stripe")

    mask = mask_AllBrownBelt & compositMask
    wmk = newDataFrameFromMask(mask)
    kata_score_sheet.put_dataframe_on_pdfpage(wmk, str(starting_ring + 5), event_time, division_name, age, "Brown")

    mask = mask_AllBlackBelt & compositMask
    wmk = newDataFrameFromMask(mask)
    kata_score_sheet.put_dataframe_on_pdfpage(wmk, str(starting_ring + 6), event_time, division_name, age, "Black")


###############################################################################
# writePattern6WithSplitToDetailReport
#  This method provides a re-usable method to write output to PDF
#  The Pattern it writes is:
#    White, Yellow
#    Orange
#    Purple
#    Blue, Blue Stripe
#    Green, Green Stripe
#    Brown
#    Black
#
def writePattern6WithSplitToDetailReport(starting_ring, event_time, division_name, age, compositMask):
    print(time.strftime("%X") + " Generating Detail Report PDF for " + event_time + " " + division_name + " " + age)

    DivisionDetailReportPDF.DivisionDetailReportPDF.set_title(division_name)

    mask1 = mask_WhiteBelt & compositMask
    mask2 = mask_YellowBelt & compositMask
    mask = mask1 | mask2
    wmk = newDataFrameFromMask(mask)
    divison_detail_report_pdf.put_dataframe_on_pdfpage(wmk, str(starting_ring), event_time, division_name, age,
                                                       "White, Yellow")

    mask = mask_OrangeBelt & compositMask
    wmk = newDataFrameFromMask(mask)
    divison_detail_report_pdf.put_dataframe_on_pdfpage(wmk, str(starting_ring + 1), event_time, division_name, age,
                                                       "Orange")

    mask = mask_PurpleBelt & compositMask
    wmk = newDataFrameFromMask(mask)
    divison_detail_report_pdf.put_dataframe_on_pdfpage(wmk, str(starting_ring + 2), event_time, division_name, age,
                                                       "Purple")

    mask = mask_AllBlueBelt & compositMask
    wmk = newDataFrameFromMask(mask)
    # filter to only keep the ones that start with a-l A-L
    pattern = r'^[a-lA-L]'  # ^ means starts wtih [a-l][A-L] means letters in the set a-l
    AtoL = wmk[wmk['Last_Name'].str.contains(pattern)]

    # filter to only keep the ones that start with m-z M-Z
    pattern = r'^[m-zM-Z]'  # ^ means starts wtih [m-z][M-Z] means letters in the set m-z
    MtoZ = wmk[wmk['Last_Name'].str.contains(pattern)]

    divison_detail_report_pdf.put_dataframe_on_pdfpage(AtoL, str(starting_ring + 3), event_time, division_name, age,
                                                       "Blue, Blue Stripe (A-L)",
                                                       "*** PLEASE NOTE - These are contestants A - L")
    divison_detail_report_pdf.put_dataframe_on_pdfpage(MtoZ, str(starting_ring + 4), event_time, division_name, age,
                                                       "Blue, Blue Stripe (M-Z)",
                                                       "*** PLEASE NOTE - These are contestants M - Z")

    mask = mask_AllGreenBelt & compositMask
    wmk = newDataFrameFromMask(mask)
    divison_detail_report_pdf.put_dataframe_on_pdfpage(wmk, str(starting_ring + 5), event_time, division_name, age,
                                                       "Green, Green Stripe")

    mask = mask_AllBrownBelt & compositMask
    wmk = newDataFrameFromMask(mask)
    divison_detail_report_pdf.put_dataframe_on_pdfpage(wmk, str(starting_ring + 6), event_time, division_name, age,
                                                       "Brown")

    mask = mask_AllBlackBelt & compositMask
    wmk = newDataFrameFromMask(mask)
    divison_detail_report_pdf.put_dataframe_on_pdfpage(wmk, str(starting_ring + 7), event_time, division_name, age,
                                                       "Black")


###############################################################################
# writePattern6WithSplitToKataScoreSheetlReport
#  This method provides a re-usable method to write output to PDF
#  The Pattern it writes is:
#    White, Yellow
#    Orange
#    Purple
#    Blue, Blue Stripe
#    Green, Green Stripe
#    Brown
#    Black
#
def writePattern6WithSplitToKataScoreSheetlReport(starting_ring, event_time, division_name, age, compositMask):
    print(time.strftime("%X") + " Generating Kata Score PDF for " + event_time + " " + division_name + " " + age)

    kata_score_sheet_pdf.KataScoreSheetPDF.set_title("Forms")

    mask1 = mask_WhiteBelt & compositMask
    mask2 = mask_YellowBelt & compositMask
    mask = mask1 | mask2
    wmk = newDataFrameFromMask(mask)
    kata_score_sheet.put_dataframe_on_pdfpage(wmk, str(starting_ring), event_time, division_name, age, "White, Yellow")

    mask = mask_OrangeBelt & compositMask
    wmk = newDataFrameFromMask(mask)
    kata_score_sheet.put_dataframe_on_pdfpage(wmk, str(starting_ring + 1), event_time, division_name, age, "Orange")

    mask = mask_PurpleBelt & compositMask
    wmk = newDataFrameFromMask(mask)
    kata_score_sheet.put_dataframe_on_pdfpage(wmk, str(starting_ring + 2), event_time, division_name, age, "Purple")

    mask = mask_AllBlueBelt & compositMask
    wmk = newDataFrameFromMask(mask)
    # filter to only keep the ones that start with a-l A-L
    pattern = r'^[a-lA-L]'  # ^ means starts wtih [a-l][A-L] means letters in the set a-l
    AtoL = wmk[wmk['Last_Name'].str.contains(pattern)]

    # filter to only keep the ones that start with m-z M-Z
    pattern = r'^[m-zM-Z]'  # ^ means starts wtih [m-z][M-Z] means letters in the set m-z
    MtoZ = wmk[wmk['Last_Name'].str.contains(pattern)]

    kata_score_sheet.put_dataframe_on_pdfpage(AtoL, str(starting_ring + 3), event_time, division_name, age,
                                              "Blue, Blue Stripe (A-L)",
                                              "*** PLEASE NOTE - These are contestants A - L")
    kata_score_sheet.put_dataframe_on_pdfpage(MtoZ, str(starting_ring + 4), event_time, division_name, age,
                                              "Blue, Blue Stripe (M-Z)",
                                              "*** PLEASE NOTE - These are contestants M - Z")

    mask = mask_AllGreenBelt & compositMask
    wmk = newDataFrameFromMask(mask)
    kata_score_sheet.put_dataframe_on_pdfpage(wmk, str(starting_ring + 5), event_time, division_name, age,
                                              "Green, Green Stripe")

    mask = mask_AllBrownBelt & compositMask
    wmk = newDataFrameFromMask(mask)
    kata_score_sheet.put_dataframe_on_pdfpage(wmk, str(starting_ring + 6), event_time, division_name, age, "Brown")

    mask = mask_AllBlackBelt & compositMask
    wmk = newDataFrameFromMask(mask)
    kata_score_sheet.put_dataframe_on_pdfpage(wmk, str(starting_ring + 7), event_time, division_name, age, "Black")


###############################################################################
# writePattern6WithSplitToKataScoreSheetlReport
#  This method provides a re-usable method to write output to PDF
#  The Pattern it writes is:
#    White, Yellow
#    Orange
#    Purple
#    Blue, Blue Stripe
#    Green, Green Stripe
#    Brown
#    Black
#
def writePattern6WithPurpleAndBlueSpitToKataScoreSheetlReport(starting_ring, event_time, division_name, age, compositMask):
    print(time.strftime("%X") + " Generating Kata Score PDF for " + event_time + " " + division_name + " " + age)

    kata_score_sheet_pdf.KataScoreSheetPDF.set_title("Forms")

    mask1 = mask_WhiteBelt & compositMask
    mask2 = mask_YellowBelt & compositMask
    mask = mask1 | mask2
    wmk = newDataFrameFromMask(mask)
    kata_score_sheet.put_dataframe_on_pdfpage(wmk, str(starting_ring), event_time, division_name, age, "White, Yellow")

    mask = mask_OrangeBelt & compositMask
    wmk = newDataFrameFromMask(mask)
    kata_score_sheet.put_dataframe_on_pdfpage(wmk, str(starting_ring + 1), event_time, division_name, age, "Orange")

    mask = mask_PurpleBelt & compositMask
    wmk = newDataFrameFromMask(mask)
  #  kata_score_sheet.put_dataframe_on_pdfpage(wmk, str(starting_ring + 2), event_time, division_name, age, "Purple")

    # filter to only keep the ones that start with a-l A-L
    pattern = r'^[a-lA-L]'  # ^ means starts wtih [a-l][A-L] means letters in the set a-l
    AtoL = wmk[wmk['Last_Name'].str.contains(pattern)]

    # filter to only keep the ones that start with m-z M-Z
    pattern = r'^[m-zM-Z]'  # ^ means starts wtih [m-z][M-Z] means letters in the set m-z
    MtoZ = wmk[wmk['Last_Name'].str.contains(pattern)]

    kata_score_sheet.put_dataframe_on_pdfpage(AtoL, str(starting_ring + 3), event_time, division_name, age,
                                              "Purple (A-L)",
                                              "*** PLEASE NOTE - These are contestants A - L")
    kata_score_sheet.put_dataframe_on_pdfpage(MtoZ, str(starting_ring + 4), event_time, division_name, age,
                                              "Purple (M-Z)",
                                              "*** PLEASE NOTE - These are contestants M - Z")

    mask = mask_AllBlueBelt & compositMask
    wmk = newDataFrameFromMask(mask)
    # filter to only keep the ones that start with a-l A-L
    pattern = r'^[a-lA-L]'  # ^ means starts wtih [a-l][A-L] means letters in the set a-l
    AtoL = wmk[wmk['Last_Name'].str.contains(pattern)]

    # filter to only keep the ones that start with m-z M-Z
    pattern = r'^[m-zM-Z]'  # ^ means starts wtih [m-z][M-Z] means letters in the set m-z
    MtoZ = wmk[wmk['Last_Name'].str.contains(pattern)]

    kata_score_sheet.put_dataframe_on_pdfpage(AtoL, str(starting_ring + 3), event_time, division_name, age,
                                              "Blue, Blue Stripe (A-L)",
                                              "*** PLEASE NOTE - These are contestants A - L")
    kata_score_sheet.put_dataframe_on_pdfpage(MtoZ, str(starting_ring + 4), event_time, division_name, age,
                                              "Blue, Blue Stripe (M-Z)",
                                              "*** PLEASE NOTE - These are contestants M - Z")

    mask = mask_AllGreenBelt & compositMask
    wmk = newDataFrameFromMask(mask)
    kata_score_sheet.put_dataframe_on_pdfpage(wmk, str(starting_ring + 5), event_time, division_name, age,
                                              "Green, Green Stripe")

    mask = mask_AllBrownBelt & compositMask
    wmk = newDataFrameFromMask(mask)
    kata_score_sheet.put_dataframe_on_pdfpage(wmk, str(starting_ring + 6), event_time, division_name, age, "Brown")

    mask = mask_AllBlackBelt & compositMask
    wmk = newDataFrameFromMask(mask)
    kata_score_sheet.put_dataframe_on_pdfpage(wmk, str(starting_ring + 7), event_time, division_name, age, "Black")


###############################################################################
# writePattern7ToExcel
#  This method provides a re-usable method to write output to excel
#  The Pattern it writes is:
#    White, Yellow & Orange
#    Purple, Blue & Blue Stripe
#    Green, Green Stripe, Brown
#    Black
#
#  arguments:
#  filename - the filename without path to write
#  compsitMask - a mask made up of everything but the belts that you want
#
def writePattern7ToExcel(filename, compositMask):
    fullpath = os.getcwd() + pathDelimiter() + "Sorted" + pathDelimiter() + filename
    writer = pd.ExcelWriter(fullpath)
    print(time.strftime("%X") + " Generating " + fullpath)

    mask1 = mask_WhiteBelt & compositMask
    mask2 = mask_YellowBelt & compositMask
    mask3 = mask_OrangeBelt & compositMask
    mask = mask1 | mask2 | mask3
    wmk = newDataFrameFromMask(mask)
    writeFormattedExcelSheet(wmk, writer, 'White, Yellow & Orange')

    mask1 = mask_PurpleBelt & compositMask
    mask2 = mask_AllBlueBelt & compositMask
    mask = mask1 | mask2
    wmk = newDataFrameFromMask(mask)
    writeFormattedExcelSheet(wmk, writer, 'Purple, Blue & Blue Stripe')

    mask1 = mask_AllGreenBelt & compositMask
    mask2 = mask_AllBrownBelt & compositMask
    mask = mask1 | mask2
    wmk = newDataFrameFromMask(mask)
    writeFormattedExcelSheet(wmk, writer, 'Green, Green Stripe, Brown')

    mask = mask_AllBlackBelt & compositMask
    wmk = newDataFrameFromMask(mask)
    writeFormattedExcelSheet(wmk, writer, 'Black')

    writer.save()
    time.sleep(1)


###############################################################################
# writePattern7ToDetailReport
#  This method provides a re-usable method to write output to PDF
#  The Pattern it writes is:
#    White, Yellow & Orange
#    Purple, Blue & Blue Stripe
#    Green, Green Stripe, Brown
#    Black
#
def writePattern7ToDetailReport(starting_ring, event_time, division_name, age, compositMask):
    print(time.strftime("%X") + " Generating Detail Report PDF for " + event_time + " " + division_name + " " + age)

    DivisionDetailReportPDF.DivisionDetailReportPDF.set_title(division_name)

    mask1 = mask_WhiteBelt & compositMask
    mask2 = mask_YellowBelt & compositMask
    mask3 = mask_OrangeBelt & compositMask
    mask = mask1 | mask2 | mask3
    wmk = newDataFrameFromMask(mask)
    divison_detail_report_pdf.put_dataframe_on_pdfpage(wmk, str(starting_ring), event_time, division_name, age,
                                                       "White, Yellow & Orange")

    mask1 = mask_PurpleBelt & compositMask
    mask2 = mask_AllBlueBelt & compositMask
    mask = mask1 | mask2
    wmk = newDataFrameFromMask(mask)
    divison_detail_report_pdf.put_dataframe_on_pdfpage(wmk, str(starting_ring + 1), event_time, division_name, age,
                                                       "Purple, Blue & Blue Stripe")

    mask1 = mask_AllGreenBelt & compositMask
    mask2 = mask_AllBrownBelt & compositMask
    mask = mask1 | mask2
    wmk = newDataFrameFromMask(mask)
    divison_detail_report_pdf.put_dataframe_on_pdfpage(wmk, str(starting_ring + 2), event_time, division_name, age,
                                                       "Green, Green Stripe, Brown")

    mask = mask_AllBlackBelt & compositMask
    wmk = newDataFrameFromMask(mask)
    divison_detail_report_pdf.put_dataframe_on_pdfpage(wmk, str(starting_ring + 3), event_time, division_name, age,
                                                       "Black")


###############################################################################
# writePattern7ToKataScoreSheet
#  This method provides a re-usable method to write output to PDF
#  The Pattern it writes is:
#    White, Yellow & Orange
#    Purple, Blue & Blue Stripe
#    Green, Green Stripe, Brown
#    Black
#
def writePattern7ToKataScoreSheet(starting_ring, event_time, division_name, age, compositMask):
    print(time.strftime("%X") + " Generating Kata Score Sheet PDF for " + event_time + " " + division_name + " " + age)

    kata_score_sheet_pdf.KataScoreSheetPDF.set_title("Forms")

    mask1 = mask_WhiteBelt & compositMask
    mask2 = mask_YellowBelt & compositMask
    mask3 = mask_OrangeBelt & compositMask
    mask = mask1 | mask2 | mask3
    wmk = newDataFrameFromMask(mask)
    kata_score_sheet_pdf.put_dataframe_on_pdfpage(wmk, str(starting_ring), event_time, division_name, age,
                                                  "White, Yellow & Orange")

    mask1 = mask_PurpleBelt & compositMask
    mask2 = mask_AllBlueBelt & compositMask
    mask = mask1 | mask2
    wmk = newDataFrameFromMask(mask)
    kata_score_sheet_pdf.put_dataframe_on_pdfpage(wmk, str(starting_ring + 1), event_time, division_name, age,
                                                  "Purple, Blue & Blue Stripe")

    mask1 = mask_AllGreenBelt & compositMask
    mask2 = mask_AllBrownBelt & compositMask
    mask = mask1 | mask2
    wmk = newDataFrameFromMask(mask)
    kata_score_sheet_pdf.put_dataframe_on_pdfpage(wmk, str(starting_ring + 2), event_time, division_name, age,
                                                  "Green, Green Stripe, Brown")

    mask = mask_AllBlackBelt & compositMask
    wmk = newDataFrameFromMask(mask)
    kata_score_sheet_pdf.put_dataframe_on_pdfpage(wmk, str(starting_ring + 3), event_time, division_name, age, "Black")


###############################################################################
# writeWeaponsDivision1ToExcel
#  arguments:
#  filename - the filename without path to write
#  compsitMask - a mask made up of everything but the belts that you want
#
def writeWeaponsDivision1ToExcel(filename, compositMask):
    fullpath = os.getcwd() + pathDelimiter() + "Sorted" + pathDelimiter() + filename
    writer = pd.ExcelWriter(fullpath)
    print(time.strftime("%X") + " Generating " + fullpath)

    mask1 = mask_WhiteBelt & compositMask
    mask2 = mask_YellowBelt & compositMask
    mask3 = mask_OrangeBelt & compositMask
    mask4 = mask_PurpleBelt & compositMask
    mask5 = mask_AllBlueBelt & compositMask
    mask6 = mask_AllGreenBelt & compositMask
    mask7 = mask_AllBrownBelt & compositMask
    mask8 = mask_AllBlackBelt & compositMask

    mask = mask1 | mask2 | mask3 | mask4 | mask5 | mask6 | mask7 | mask8

    wmk = newDataFrameFromMask(mask)
    writeFormattedExcelSheet(wmk, writer, 'Weapons Division 1')

    writer.save()
    time.sleep(1)


###############################################################################
# writeWeaponsDivision1ToDetailReport
#
def writeWeaponsDivision1ToDetailReport(event_time, division_name, age, compositMask):
    print(time.strftime("%X") + " Generating Detail Report PDF for " + event_time + " " + division_name + " " + age)

    DivisionDetailReportPDF.DivisionDetailReportPDF.set_title("Weapons")

    mask1 = mask_WhiteBelt & compositMask
    mask2 = mask_YellowBelt & compositMask
    mask3 = mask_OrangeBelt & compositMask
    mask4 = mask_PurpleBelt & compositMask
    mask5 = mask_AllBlueBelt & compositMask
    mask6 = mask_AllGreenBelt & compositMask
    mask7 = mask_AllBrownBelt & compositMask
    mask8 = mask_AllBlackBelt & compositMask

    mask = mask1 | mask2 | mask3 | mask4 | mask5 | mask6 | mask7 | mask8

    wmk = newDataFrameFromMask(mask)
    divison_detail_report_pdf.put_dataframe_on_pdfpage(wmk, "*TBA", event_time, division_name, age, "White - Jr. Black")


###############################################################################
# writeWeaponsDivision1ToKataScoreSheet
#
def writeWeaponsDivision1ToKataScoreSheet(event_time, division_name, age, compositMask):
    print(time.strftime("%X") + " Generating Kata Score Sheet PDF for " + event_time + " " + division_name + " " + age)

    kata_score_sheet_pdf.KataScoreSheetPDF.set_title("Weapons")

    mask1 = mask_WhiteBelt & compositMask
    mask2 = mask_YellowBelt & compositMask
    mask3 = mask_OrangeBelt & compositMask
    mask4 = mask_PurpleBelt & compositMask
    mask5 = mask_AllBlueBelt & compositMask
    mask6 = mask_AllGreenBelt & compositMask
    mask7 = mask_AllBrownBelt & compositMask
    mask8 = mask_AllBlackBelt & compositMask

    mask = mask1 | mask2 | mask3 | mask4 | mask5 | mask6 | mask7 | mask8

    wmk = newDataFrameFromMask(mask)
    kata_score_sheet.put_dataframe_on_pdfpage(wmk, "*TBA", event_time, division_name, age, "White - Jr. Black")


###############################################################################
# writeWeaponsDivision2ToExcel
#  arguments:
#  filename - the filename without path to write
#  compsitMask - a mask made up of everything but the belts that you want
#
def writeWeaponsDivision2ToExcel(filename, compositMask):
    fullpath = os.getcwd() + pathDelimiter() + "Sorted" + pathDelimiter() + filename
    writer = pd.ExcelWriter(fullpath)
    print(time.strftime("%X") + " Generating " + fullpath)

    mask1 = mask_WhiteBelt & compositMask
    mask2 = mask_YellowBelt & compositMask
    mask3 = mask_OrangeBelt & compositMask
    mask4 = mask_PurpleBelt & compositMask
    mask5 = mask_AllBlueBelt & compositMask
    #    mask6= mask_AllGreenBelt & compositMask
    #    mask7= mask_AllBrownBelt & compositMask
    #    mask8= mask_AllBlackBelt & compositMask

    #    mask = mask1 | mask2 | mask3 | mask4 | mask5 | mask6 | mask7 | mask8
    mask = mask1 | mask2 | mask3 | mask4 | mask5

    wmk = newDataFrameFromMask(mask)
    #    wmk.to_excel(writer,'Weapons Division 2')
    writeFormattedExcelSheet(wmk, writer, 'Weapons Division 2')

    writer.save()
    time.sleep(1)


###############################################################################
# writeWeaponsDivision2ToDetailReport
#
def writeWeaponsDivision2ToDetailReport(event_time, division_name, age, compositMask):
    print(time.strftime("%X") + " Generating Detail Report PDF for " + event_time + " " + division_name + " " + age)
    DivisionDetailReportPDF.DivisionDetailReportPDF.set_title("Weapons")

    mask1 = mask_WhiteBelt & compositMask
    mask2 = mask_YellowBelt & compositMask
    mask3 = mask_OrangeBelt & compositMask
    mask4 = mask_PurpleBelt & compositMask
    mask5 = mask_AllBlueBelt & compositMask
    #    mask6= mask_AllGreenBelt & compositMask
    #    mask7= mask_AllBrownBelt & compositMask
    #    mask8= mask_AllBlackBelt & compositMask

    #    mask = mask1 | mask2 | mask3 | mask4 | mask5 | mask6 | mask7 | mask8
    mask = mask1 | mask2 | mask3 | mask4 | mask5

    wmk = newDataFrameFromMask(mask)
    divison_detail_report_pdf.put_dataframe_on_pdfpage(wmk, "*TBA", event_time, division_name, age,
                                                       "White - Blue Stripe")


###############################################################################
# writeWeaponsDivision2ToKataScoreSheet
def writeWeaponsDivision2ToKataScoreSheet(event_time, division_name, age, compositMask):
    print(time.strftime("%X") + " Generating Kata Score Sheet PDF for " + event_time + " " + division_name + " " + age)

    kata_score_sheet_pdf.KataScoreSheetPDF.set_title("Weapons")

    mask1 = mask_WhiteBelt & compositMask
    mask2 = mask_YellowBelt & compositMask
    mask3 = mask_OrangeBelt & compositMask
    mask4 = mask_PurpleBelt & compositMask
    mask5 = mask_AllBlueBelt & compositMask
    #    mask6= mask_AllGreenBelt & compositMask
    #    mask7= mask_AllBrownBelt & compositMask
    #    mask8= mask_AllBlackBelt & compositMask

    #    mask = mask1 | mask2 | mask3 | mask4 | mask5 | mask6 | mask7 | mask8
    mask = mask1 | mask2 | mask3 | mask4 | mask5

    wmk = newDataFrameFromMask(mask)
    kata_score_sheet.put_dataframe_on_pdfpage(wmk, "*TBA", event_time, division_name, age, "White - Blue Stripe")


###############################################################################
# writeWeaponsDivision3ToExcel
#  arguments:
#  filename - the filename without path to write
#  compsitMask - a mask made up of everything but the belts that you want
#
def writeWeaponsDivision3ToExcel(filename, compositMask):
    fullpath = os.getcwd() + pathDelimiter() + "Sorted" + pathDelimiter() + filename
    writer = pd.ExcelWriter(fullpath)
    print(time.strftime("%X") + " Generating " + fullpath)

    mask1 = mask_AllGreenBelt & compositMask
    mask2 = mask_AllBrownBelt & compositMask
    mask3 = mask_AllBlackBelt & compositMask

    mask = mask1 | mask2 | mask3

    wmk = newDataFrameFromMask(mask)
    writeFormattedExcelSheet(wmk, writer, 'Weapons Division 3')

    writer.save()
    time.sleep(1)


###############################################################################
# writeWeaponsDivision3ToDetailReport
#
def writeWeaponsDivision3ToDetailReport(event_time, division_name, age, compositMask):
    print(time.strftime("%X") + " Generating Detail Report PDF for " + event_time + " " + division_name + " " + age)

    DivisionDetailReportPDF.DivisionDetailReportPDF.set_title("Weapons")

    mask1 = mask_AllGreenBelt & compositMask
    mask2 = mask_AllBrownBelt & compositMask
    mask3 = mask_AllBlackBelt & compositMask

    mask = mask1 | mask2 | mask3

    wmk = newDataFrameFromMask(mask)
    divison_detail_report_pdf.put_dataframe_on_pdfpage(wmk, "*TBA", event_time, division_name, age, "Green - Jr. Black")


###############################################################################
# writeWeaponsDivision3ToKataScoreSheet
#
def writeWeaponsDivision3ToKataScoreSheet(event_time, division_name, age, compositMask):
    print(time.strftime("%X") + " Generating Kata Score Sheet PDF for " + event_time + " " + division_name + " " + age)

    kata_score_sheet_pdf.KataScoreSheetPDF.set_title("Weapons")

    mask1 = mask_AllGreenBelt & compositMask
    mask2 = mask_AllBrownBelt & compositMask
    mask3 = mask_AllBlackBelt & compositMask

    mask = mask1 | mask2 | mask3

    wmk = newDataFrameFromMask(mask)
    kata_score_sheet.put_dataframe_on_pdfpage(wmk, "*TBA", event_time, division_name, age, "Green - Jr. Black")


###############################################################################
# writeWeaponsDivision4ToExcel
#  arguments:
#  filename - the filename without path to write
#  compsitMask - a mask made up of everything but the belts that you want
#
def writeWeaponsDivision4ToExcel(filename, compositMask):
    fullpath = os.getcwd() + pathDelimiter() + "Sorted" + pathDelimiter() + filename
    writer = pd.ExcelWriter(fullpath)
    print(time.strftime("%X") + " Generating " + fullpath)

    mask1 = mask_WhiteBelt & compositMask
    mask2 = mask_YellowBelt & compositMask
    mask3 = mask_OrangeBelt & compositMask
    mask4 = mask_PurpleBelt & compositMask
    mask5 = mask_AllBlueBelt & compositMask

    mask = mask1 | mask2 | mask3 | mask4 | mask5

    wmk = newDataFrameFromMask(mask)
    writeFormattedExcelSheet(wmk, writer, 'Weapons Division 4')

    writer.save()
    time.sleep(1)


###############################################################################
# writeWeaponsDivision4ToDetailReport
#
def writeWeaponsDivision4ToDetailReport(event_time, division_name, age, compositMask):
    print(time.strftime("%X") + " Generating Detail Report PDF for " + event_time + " " + division_name + " " + age)

    DivisionDetailReportPDF.DivisionDetailReportPDF.set_title("Weapons")

    mask1 = mask_WhiteBelt & compositMask
    mask2 = mask_YellowBelt & compositMask
    mask3 = mask_OrangeBelt & compositMask
    mask4 = mask_PurpleBelt & compositMask
    mask5 = mask_AllBlueBelt & compositMask

    mask = mask1 | mask2 | mask3 | mask4 | mask5

    wmk = newDataFrameFromMask(mask)
    divison_detail_report_pdf.put_dataframe_on_pdfpage(wmk, "*TBA", event_time, division_name, age,
                                                       "White - Blue Stripe")


###############################################################################
# writeWeaponsDivision4ToKataScoreSheet
#
def writeWeaponsDivision4ToKataScoreSheet(event_time, division_name, age, compositMask):
    print(time.strftime("%X") + " Generating Kata Score Sheet PDF for " + event_time + " " + division_name + " " + age)

    kata_score_sheet_pdf.KataScoreSheetPDF.set_title("Weapons")

    mask1 = mask_WhiteBelt & compositMask
    mask2 = mask_YellowBelt & compositMask
    mask3 = mask_OrangeBelt & compositMask
    mask4 = mask_PurpleBelt & compositMask
    mask5 = mask_AllBlueBelt & compositMask

    mask = mask1 | mask2 | mask3 | mask4 | mask5

    wmk = newDataFrameFromMask(mask)
    kata_score_sheet.put_dataframe_on_pdfpage(wmk, "*TBA", event_time, division_name, age, "White - Blue Stripe")


###############################################################################
#  writeWeaponsDivision5ToExcel  18+ year Blue and Green
#  arguments:
#  filename - the filename without path to write
#  compsitMask - a mask made up of everything but the belts that you want
#
def writeWeaponsDivision5ToExcel(filename, compositMask):
    fullpath = os.getcwd() + pathDelimiter() + "Sorted" + pathDelimiter() + filename
    print(time.strftime("%X") + " Generating " + fullpath)
    writer = pd.ExcelWriter(fullpath)

    mask1 = mask_WhiteBelt & compositMask
    mask2 = mask_YellowBelt & compositMask
    mask3 = mask_OrangeBelt & compositMask
    mask4 = mask_PurpleBelt & compositMask
    mask5 = mask_AllBlueBelt & compositMask

    mask = mask1 | mask2 | mask3 | mask4 | mask5

    wmk = newDataFrameFromMask(mask)
    writeFormattedExcelSheet(wmk, writer, 'Weapons Division 5')

    writer.save()
    time.sleep(1)


###############################################################################
# writeWeaponsDivision5ToDetailReport
#
def writeWeaponsDivision5ToDetailReport(event_time, division_name, age, compositMask):
    print(time.strftime("%X") + " Generating Detail Report PDF for " + event_time + " " + division_name + " " + age)

    DivisionDetailReportPDF.DivisionDetailReportPDF.set_title("Weapons")

    mask1 = mask_WhiteBelt & compositMask
    mask2 = mask_YellowBelt & compositMask
    mask3 = mask_OrangeBelt & compositMask
    mask4 = mask_PurpleBelt & compositMask
    mask5 = mask_AllBlueBelt & compositMask

    mask = mask1 | mask2 | mask3 | mask4 | mask5

    wmk = newDataFrameFromMask(mask)

    divison_detail_report_pdf.put_dataframe_on_pdfpage(wmk, "*TBA", event_time, division_name, age,
                                                       "White - Blue Stripe")


###############################################################################
# writeWeaponsDivision5ToKataScoreSheet
#
def writeWeaponsDivision5ToKataScoreSheet(event_time, division_name, age, compositMask):
    print(time.strftime("%X") + " Generating Kata Score Sheet PDF for " + event_time + " " + division_name + " " + age)

    kata_score_sheet_pdf.KataScoreSheetPDF.set_title("Weapons")

    mask1 = mask_WhiteBelt & compositMask
    mask2 = mask_YellowBelt & compositMask
    mask3 = mask_OrangeBelt & compositMask
    mask4 = mask_PurpleBelt & compositMask
    mask5 = mask_AllBlueBelt & compositMask

    mask = mask1 | mask2 | mask3 | mask4 | mask5

    wmk = newDataFrameFromMask(mask)

    kata_score_sheet.put_dataframe_on_pdfpage(wmk, "*TBA", event_time, division_name, age, "White - Blue Stripe")


###############################################################################
#  writeWeaponsDivision6ToExcel
#  arguments:
#  filename - the filename without path to write
#  compsitMask - a mask made up of everything but the belts that you want
#
def writeWeaponsDivision6ToFile(filename, compositMask):
    fullpath = os.getcwd() + pathDelimiter() + "Sorted" + pathDelimiter() + filename
    writer = pd.ExcelWriter(fullpath)
    print(time.strftime("%X") + " Generating " + fullpath)

    mask1 = mask_AllGreenBelt & compositMask
    # mask2= mask_AllBrownBelt & compositMask
    mask = mask1  # | mask2
    wmk = newDataFrameFromMask(mask)
    writeFormattedExcelSheet(wmk, writer, 'Weapons Division 6')

    writer.save()
    time.sleep(1)


###############################################################################
# writeWeaponsDivision6ToDetailReport
#
def writeWeaponsDivision6ToDetailReport(event_time, division_name, age, compositMask):
    print(time.strftime("%X") + " Generating Detail Report PDF for " + event_time + " " + division_name + " " + age)

    DivisionDetailReportPDF.DivisionDetailReportPDF.set_title("Weapons")

    mask1 = mask_AllGreenBelt & compositMask
    # mask2= mask_AllBrownBelt & compositMask
    mask = mask1  # | mask2
    wmk = newDataFrameFromMask(mask)

    divison_detail_report_pdf.put_dataframe_on_pdfpage(wmk, "*TBA", event_time, division_name, age, "Green")


###############################################################################
# writeWeaponsDivision6ToKataScoreSheet
#
def writeWeaponsDivision6ToKataScoreSheet(event_time, division_name, age, compositMask):
    print(time.strftime("%X") + " Generating Kata Score Sheet PDF for " + event_time + " " + division_name + " " + age)

    kata_score_sheet_pdf.KataScoreSheetPDF.set_title("Weapons")

    mask1 = mask_AllGreenBelt & compositMask
    # mask2= mask_AllBrownBelt & compositMask
    mask = mask1  # | mask2
    wmk = newDataFrameFromMask(mask)

    kata_score_sheet.put_dataframe_on_pdfpage(wmk, "tba", event_time, division_name, age, "Green")


###############################################################################
#  writeWeaponsDivision7ToExcel
#  arguments:
#  filename - the filename without path to write
#  compsitMask - a mask made up of everything but the belts that you want
#
def writeWeaponsDivision7ToFile(filename, compositMask):
    fullpath = os.getcwd() + pathDelimiter() + "Sorted" + pathDelimiter() + filename
    writer = pd.ExcelWriter(fullpath)
    print(time.strftime("%X") + " Generating " + fullpath)

    mask = mask_AllBrownBelt & compositMask
    wmk = newDataFrameFromMask(mask)
    writeFormattedExcelSheet(wmk, writer, 'Weapons Division 6b')

    writer.save()
    time.sleep(1)


###############################################################################
# writeWeaponsDivision7ToDetailReport
#
def writeWeaponsDivision7ToDetailReport(event_time, division_name, age, compositMask):
    print(time.strftime("%X") + " Generating Detail Report PDF for " + event_time + " " + division_name + " " + age)

    DivisionDetailReportPDF.DivisionDetailReportPDF.set_title("Weapons")

    mask = mask_AllBrownBelt & compositMask
    wmk = newDataFrameFromMask(mask)

    divison_detail_report_pdf.put_dataframe_on_pdfpage(wmk, "*TBA", event_time, division_name, age, "Brown")


###############################################################################
# writeWeaponsDivision7ToKataScoreSheet
#
def writeWeaponsDivision7ToKataScoreSheet(event_time, division_name, age, compositMask):
    print(time.strftime("%X") + " Generating Kata Score Sheet PDF for " + event_time + " " + division_name + " " + age)

    kata_score_sheet_pdf.KataScoreSheetPDF.set_title("Weapons")

    #  mask1= mask_AllGreenBelt & compositMask
    mask = mask_AllBrownBelt & compositMask
    wmk = newDataFrameFromMask(mask)

    kata_score_sheet.put_dataframe_on_pdfpage(wmk, "tba", event_time, division_name, age, "Brown")


###############################################################################
#  writeWeaponsDivision8ToExcel
#  arguments:
#  filename - the filename without path to write
#  compsitMask - a mask made up of everything but the belts that you want
#
def writeWeaponsDivision8ToFile(filename, compositMask):
    fullpath = os.getcwd() + pathDelimiter() + "Sorted" + pathDelimiter() + filename
    writer = pd.ExcelWriter(fullpath)
    print(time.strftime("%X") + " Generating " + fullpath)

    mask1 = mask_AllBlackBelt & compositMask
    mask = mask1
    wmk = newDataFrameFromMask(mask)
    writeFormattedExcelSheet(wmk, writer, 'Weapons Division 7')

    writer.save()
    time.sleep(1)


###############################################################################
# writeWeaponsDivision8ToDetailReport
#
def writeWeaponsDivision8ToDetailReport(event_time, division_name, age, compositMask):
    print(time.strftime("%X") + " Generating Detail Report PDF for " + event_time + " " + division_name + " " + age)

    DivisionDetailReportPDF.DivisionDetailReportPDF.set_title("Weapons")

    mask1 = mask_AllBlackBelt & compositMask
    mask = mask1
    wmk = newDataFrameFromMask(mask)

    divison_detail_report_pdf.put_dataframe_on_pdfpage(wmk, "*TBA", event_time, division_name, age, "Black")


###############################################################################
# writeWeaponsDivision8ToKataScoreSheet
#
def writeWeaponsDivision8ToKataScoreSheet(event_time, division_name, age, compositMask):
    print(time.strftime("%X") + " Generating Kata Score Sheet PDF for " + event_time + " " + division_name + " " + age)

    kata_score_sheet_pdf.KataScoreSheetPDF.set_title("Weapons")

    mask1 = mask_AllBlackBelt & compositMask
    mask = mask1
    wmk = newDataFrameFromMask(mask)

    kata_score_sheet.put_dataframe_on_pdfpage(wmk, "tba", event_time, division_name, age, "Black")


def writeSparingTreeToExcel(filename, compositMask):
    fullpath = os.getcwd() + pathDelimiter() + "Sorted" + pathDelimiter() + filename
    writer = pd.ExcelWriter(fullpath)
    print(time.strftime("%X") + " Generating " + fullpath)

    wmk = newDataFrameFromMask(compositMask)

    byDojo = wmk.groupby('Dojo')

    print(byDojo.size())

    writer.save()
    time.sleep(1)


###############################################################################
#
# Main Function
#

# get the filename from the environment var named  tourname_filename
filename = os.getenv("tournament_filename")

if filename is None:
    # Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    root = Tk()
    root.withdraw()  # we don't want a full GUI, so keep the root window from appearing
    root.update()  # Prevent the askfilename() window doesn't stay open
    filename = askopenfilename()
    root.update()  # Prevent the askfilename() window doesn't stay open
else:
    print("Using the file " + filename + "from the environment")

# filename = "C:\\Users\\Maria\\Downloads\\tournamentprojectmaterial\\RegistrantExport.csv"
# filename = "/users/johnfunk/CloudStation/TournamentProject/Clean_RegistrantExport_EM0393_20160411140713.csv"  # For Testing on John's machine

print(time.strftime("%X") + " Reading the data from:" + filename + "....")

#### SET Encoding to UTF-8 added 3/27/2022
if os.name == "nt":
    import _locale
    _locale._gdl_bak = _locale._getdefaultlocale
    _locale._getdefaultlocale = (lambda *args: (_locale._gdl_bak()[0], 'utf8'))

errorLogFileName = filename[0:len(filename) - 4] + "-Error.txt"
errorLogFile = open(errorLogFileName, "w")

cleaninput.clean_unicode_from_file(filename, errorLogFile)

raw_df = pd.read_csv(filename)

# rename all the columns in the dataframe to usable names
r = RN.RenameColumns(filename)
r.rename_all_columns()
renamed_df = r.get_dataframe_copy()

clean_df = cleaninput.clean_all_input_errors(renamed_df, errorLogFile)
del raw_df  # make sure we don't use the raw_df again

# create test data
clean_df.to_pickle("pickled_clean_dataframe.pkl")

#make sure the sorted directory exists
try:
    os.mkdir("sorted")
except:
    assert(1==1)
    #print("expected error")


####################
# Filtering        #
####################


###############################################################################
#  Define all the atomic masks

# Atomic masks for Belts
mask_WhiteBelt = clean_df['Rank'] == 'White'
mask_YellowBelt = clean_df['Rank'] == 'Yellow'
mask_OrangeBelt = clean_df['Rank'] == 'Orange'
mask_PurpleBelt = clean_df['Rank'] == 'Purple'
mask_BlueBelt = clean_df['Rank'] == 'Blue'
mask_BlueStripeBelt = clean_df['Rank'] == 'Blue w/Stripe'
mask_AllBlueBelt = mask_BlueBelt | mask_BlueStripeBelt  # all blue and blue stripe
# testBluedf=newDataFrameFromMask( mask_AllBlueBelt )
mask_GreenBelt = clean_df['Rank'] == 'Green'
mask_GreenStripeBelt = clean_df['Rank'] == 'Green w/Stripe'
mask_AllGreenBelt = mask_GreenBelt | mask_GreenStripeBelt  # all Green and Green stripe
# testGreendf=newDataFrameFromMask( mask_AllGreenBelt )
mask_3rdBrownBelt = clean_df['Rank'] == 'Brown 3rd Degree'
mask_2ndBrownBelt = clean_df['Rank'] == 'Brown 2nd Degree'
mask_1stBrownBelt = clean_df['Rank'] == 'Brown 1st Degree'
mask_AllBrownBelt = mask_3rdBrownBelt | mask_2ndBrownBelt | mask_1stBrownBelt  # all 1st 2nd and 3rd Brown
# testBrowndf=newDataFrameFromMask( mask_AllBrownBelt )
mask_1stBlackBelt = clean_df['Rank'] == 'Black 1st Degree'
mask_2ndBlackBelt = clean_df['Rank'] == 'Black 2nd Degree'
mask_3rdBlackBelt = clean_df['Rank'] == 'Black 3rd Degree'
mask_4thBlackBelt = clean_df['Rank'] == 'Black 4th Degree'
mask_5thBlackBelt = clean_df['Rank'] == 'Black 5th Degree'
mask_JrBlackBelt = clean_df['Rank'] == 'Black Junior'
mask_AllBlackBelt = mask_1stBlackBelt | mask_2ndBlackBelt | mask_3rdBlackBelt | mask_4thBlackBelt | mask_5thBlackBelt | mask_JrBlackBelt  # all Jr, 1st, 2nd, and 3rd degree black
# testBlackdf=newDataFrameFromMask( mask_AllBlackBelt )

# Atomic mask for Gender
mask_Male = clean_df['Gender'] == 'Male'
mask_Female = clean_df['Gender'] == 'Female'

# Atomic and composit mask for which event Sparring, Kata, Weapons
mask_SparringAndForms = clean_df['Events'] == '2 Events - Forms & Sparring ($75)'
mask_FormsOnly = clean_df['Events'] == '1 Event - Forms ($75)'
mask_SparringOnly = clean_df['Events'] == '1 Event - Sparring ($75)'
# Mask for Weapons
mask_Weapons = clean_df['Weapons'] == 'Weapons ($35)'
testdf = clean_df[['First_Name', 'Last_Name', 'Gender', 'Rank', 'Age', 'Weight', 'Height', 'Events', 'Weapons']][
    mask_Weapons]

# Composit Masks for Sparring or Forms
mask_Sparring = mask_SparringAndForms | mask_SparringOnly
mask_Forms = mask_SparringAndForms | mask_FormsOnly
# testdf=cdf[['First_Name','Last_Name', 'Gender','Rank','Age','Competitor\'s Weight (in lbs.)?','Competitor\'s Height (in feet and inches)?','Events','Weapons']][mask_Forms]

# Atomic mask for age groups found in the tournament guide
# 4-6 used for kids kata, kids sparring,
maskLowAge = clean_df["Age"] >= 3
maskHighAge = clean_df["Age"] <= 6
mask_Age4to6 = maskLowAge & maskHighAge
# testdf=cdf[['First_Name','Last_Name', 'Gender','Rank','Age','Competitor\'s Weight (in lbs.)?','Competitor\'s Height (in feet and inches)?','Events','Weapons']][mask_Age4to6]

# 7-9 used in Youth Kata, Young Girls Sparring, Youth Boys Sparring
maskLowAge = clean_df["Age"] >= 7
maskHighAge = clean_df["Age"] <= 9
mask_Age7to9 = maskLowAge & maskHighAge
# testdf=cdf[['First_Name','Last_Name', 'Gender','Rank','Age','Competitor\'s Weight (in lbs.)?','Competitor\'s Height (in feet and inches)?','Events','Weapons']][mask_Age7to9]


# 4-8 used for Weapons Division 1 - new added for Fall 2017
maskLowAge = clean_df["Age"] >= 4
maskHighAge = clean_df["Age"] <= 8
mask_Age4to8 = maskLowAge & maskHighAge

# 7-8 used in Youth Kata, Young Girls Sparring, Youth Boys Sparring - new added for Fall 2017
maskLowAge = clean_df["Age"] >= 7
maskHighAge = clean_df["Age"] <= 8
mask_Age7to8 = maskLowAge & maskHighAge

# 9-11 used in Youth Kata, Young Girls Sparring, Youth Boys Sparring - new added for Fall 2017
maskLowAge = clean_df["Age"] >= 9
maskHighAge = clean_df["Age"] <= 11
mask_Age9to11 = maskLowAge & maskHighAge

# 12-14 used in Youth Kata, Young Girls Sparring, Youth Boys Sparring - new added for Fall 2017
maskLowAge = clean_df["Age"] >= 12
maskHighAge = clean_df["Age"] <= 14
mask_Age12to14 = maskLowAge & maskHighAge

# 12-17 used in Weapons Division 4 - new added for Fall 2017
maskLowAge = clean_df["Age"] >= 12
maskHighAge = clean_df["Age"] <= 17
mask_Age12to17 = maskLowAge & maskHighAge

# 15-17 used in Youth Kata, Young Girls Sparring, Youth Boys Sparring - new added for Fall 2017
maskLowAge = clean_df["Age"] >= 15
maskHighAge = clean_df["Age"] <= 17
mask_Age15to17 = maskLowAge & maskHighAge

# 10-12 used in Boys Sparring, Boys & Girls Kata, Girls Sparring
maskLowAge = clean_df["Age"] >= 10
maskHighAge = clean_df["Age"] <= 12
mask_Age10to12 = maskLowAge & maskHighAge
# testdf=cdf[['First_Name','Last_Name', 'Gender','Rank','Age','Competitor\'s Weight (in lbs.)?','Competitor\'s Height (in feet and inches)?','Events','Weapons']][mask_Age10to12]

# 13-15 used in Teen Girls Sparring, Teen Kata, Teen Boys Sparring,
maskLowAge = clean_df["Age"] >= 13
maskHighAge = clean_df["Age"] <= 15
mask_Age13to15 = maskLowAge & maskHighAge
# testdf=cdf[['First_Name','Last_Name', 'Gender','Rank','Age','Competitor\'s Weight (in lbs.)?','Competitor\'s Height (in feet and inches)?','Events','Weapons']][mask_Age13to15]

# 4-9 used in Weapons Division 1
maskLowAge = clean_df["Age"] >= 4
maskHighAge = clean_df["Age"] <= 9
mask_Age4to9 = maskLowAge & maskHighAge
# testdf=cdf[['First_Name','Last_Name', 'Gender','Rank','Age','Competitor\'s Weight (in lbs.)?','Competitor\'s Height (in feet and inches)?','Events','Weapons']][mask_Age4to9]

# 18-39 used in Womans Sprring, Men and Womens Kata
maskLowAge = clean_df["Age"] >= 18
maskHighAge = clean_df["Age"] <= 39
mask_Age18to39 = maskLowAge & maskHighAge
# testdf=cdf[['First_Name','Last_Name', 'Gender','Rank','Age','Competitor\'s Weight (in lbs.)?','Competitor\'s Height (in feet and inches)?','Events','Weapons']][mask_Age18to39]

# 40 plus used in Senior Mens Sparring, Senior Womens Sparring, Senior Kata
mask_Age40Plus = clean_df["Age"] >= 40
# testdf=cdf[['First_Name','Last_Name', 'Gender','Rank','Age','Competitor\'s Weight (in lbs.)?','Competitor\'s Height (in feet and inches)?','Events','Weapons']][mask_Age40Plus]

# 16-17 used in Young Adult Kata, Young Mens Sparring, Young Adult Womens Sparring
maskLowAge = clean_df["Age"] >= 16
maskHighAge = clean_df["Age"] <= 17
mask_Age16to17 = maskLowAge & maskHighAge
# testdf=cdf[['First_Name','Last_Name', 'Gender','Rank','Age','Competitor\'s Weight (in lbs.)?','Competitor\'s Height (in feet and inches)?','Events','Weapons']][mask_Age16to17]

# 13-17 used in Weapons Division 3
maskLowAge = clean_df["Age"] >= 13
maskHighAge = clean_df["Age"] <= 17
mask_Age13to17 = maskLowAge & maskHighAge
# testdf=cdf[['First_Name','Last_Name', 'Gender','Rank','Age','Competitor\'s Weight (in lbs.)?','Competitor\'s Height (in feet and inches)?','Events','Weapons']][mask_Age13to17]

# 18 plus used in Weapons Division 4 and 5
mask_Age18Plus = clean_df["Age"] >= 18
# testdf=cdf[['First_Name','Last_Name', 'Gender','Rank','Age','Competitor\'s Weight (in lbs.)?','Competitor\'s Height (in feet and inches)?','Events','Weapons']][mask_Age18Plus]

# 13 plus used in Weapons Division 6
mask_Age13Plus = clean_df["Age"] >= 13
# testdf=cdf[['First_Name','Last_Name', 'Gender','Rank','Age','Competitor\'s Weight (in lbs.)?','Competitor\'s Height (in feet and inches)?','Events','Weapons']][mask_Age13Plus]

# 12 plus used in Weapons Division 6 and Weapons Division 7 - new added for Fall 2017
mask_Age12Plus = clean_df["Age"] >= 12
# testdf=cdf[['First_Name','Last_Name', 'Gender','Rank','Age','Competitor\'s Weight (in lbs.)?','Competitor\'s Height (in feet and inches)?','Events','Weapons']][mask_Age13Plus]


clean_df['hitcount'] = 0  # setup a new column for hit rate.

print(time.strftime("%X") + " Generating the output results...")

###############################################################################
# Setup a few things for the Division Detail PDF report
divison_detail_report_pdf = DivisionDetailReportPDF.DivisionDetailReportPDF()
DivisionDetailReportPDF.DivisionDetailReportPDF.set_title("Division Detail")
DivisionDetailReportPDF.DivisionDetailReportPDF.set_sourcefile(filename)

###############################################################################
# Setup a few things for the Kata Score Sheet PDF report
kata_score_sheet = kata_score_sheet_pdf.KataScoreSheetPDF()
kata_score_sheet_pdf.KataScoreSheetPDF.set_title("Forms")
kata_score_sheet_pdf.KataScoreSheetPDF.set_sourcefile(filename)

###############################################################################
# Setup a few things for the Sparring Tree PDF report
sparing_tree_pdf = reports.sparring_tree.sparring_tree_report.SparringTreeReportPDF()
sparing_tree_pdf.set_source_file( filename )

### 9AM Events

###############################################################################
# Kids Kata Spreadsheet - 4-6 year olds one sheet per rank
#
compositMask = mask_Forms & mask_Age4to6
writePattern1ToExcel("KidsKata.xlsx", compositMask)
writePattern1WithSplitToDivisionDetailReport(1, "9:00am", "Kids Kata", "4-6", compositMask)
writePattern1WithSplitToKataScoreSheet(1, "9:00am", "Kids Kata", "4-6", compositMask)

###############################################################################
# Youth Kata Spreadsheet - 7-8 year olds one sheet per rank
#
compositMask = mask_Forms & mask_Age7to8
writePattern3ToExcel("YouthKata.xlsx", compositMask)
writePattern3WithSplitToDetailReport(8, "9:00am", "Youth Kata", "7-8", compositMask)
writePattern3WithSplitToKataScoreSheet(8, "9:00am", "Youth Kata", "7-8", compositMask)

###############################################################################
# Boy's Sparring Spreadsheet - 9-11 year olds one sheet per rank
#
compositMask = mask_Sparring & mask_Age9to11 & mask_Male
writePattern6ToExcel("BoysSparring.xlsx", compositMask)
writePattern6WithSplitToDetailReport(16, "9:00am", "Boy's Sparring", "9-11", compositMask)


boys_sparring_data_frame = newDataFrameFromMask(compositMask)
boys_sparring_competitors = domain_model.competitors.Competitors(boys_sparring_data_frame)
sparing_tree_pdf.write_event_to_sparring_report_using_pattern_6([16, 17, 18, 19, 20, 21, 22], "9:00am",
                                                                "Boys Sparring 9-11", boys_sparring_competitors)
del boys_sparring_data_frame
del boys_sparring_competitors

### 9:45 Events

###############################################################################
# Kids Sparring Spreadsheet - 4-6 year olds one sheet per rank
#
compositMask = mask_Sparring & mask_Age4to6
writePattern2ToExcel("KidsSparring.xlsx", compositMask)
writePattern2ToDetailReport(1, "9:45am", "Kids Sparring", "4-6", compositMask)

kids_sparring_data_frame = newDataFrameFromMask(compositMask)
kids_sparring_competitors = domain_model.competitors.Competitors(kids_sparring_data_frame)
sparing_tree_pdf.write_event_to_sparring_report_using_pattern_1([1, 2, 3, 4, 5], "9:45am", "Kids Sparring 4-6",
                                                                kids_sparring_competitors)
del kids_sparring_data_frame
del kids_sparring_competitors

###############################################################################
# Boys & Girls Kata Spreadsheet - 9-11 year olds one sheet per rank
#
compositMask = mask_Forms & mask_Age9to11
writePattern6ToExcel("BoysGirlsKata.xlsx", compositMask)
# writePattern6ToPDF(6,"9:45am","Boy's & Girls Kata","9-11",compositMask)
writePattern6WithSplitToDetailReport(6, "9:45am", "Boys & Girls Kata", "9-11", compositMask)
writePattern6WithSplitToKataScoreSheetlReport(6, "9:45am", "Boys & Girls Kata", "9-11", compositMask)
writePattern6WithPurpleAndBlueSpitToKataScoreSheetlReport(6, "9:45am", "Boys & Girls Kata", "9-11", compositMask)

### 10:30 Events

###############################################################################
# Youth Girls Sparring Spreadsheet - 7-8 year olds one sheet per rank
#
compositMask = mask_Sparring & mask_Female & mask_Age7to8
writePattern5ToExcel("YouthGirlSparring.xlsx", compositMask)
writePattern5ToDetailReport(1, "10:30am", "Youth Girls Sparring", "7-8", compositMask)

youth_girl_sparring_data_frame = newDataFrameFromMask(compositMask)
youth_girl_sparring_competitors = domain_model.competitors.Competitors(youth_girl_sparring_data_frame)
sparing_tree_pdf.write_event_to_sparring_report_using_pattern_5([1, 2, 3, 4, 5], "10:30am", "Youth Girls Sparring 7-8",
                                                                youth_girl_sparring_competitors)
del youth_girl_sparring_data_frame
del youth_girl_sparring_competitors

###############################################################################
# Youth Boys Sparring Spreadsheet - 7-8 year olds one sheet per rank
#
compositMask = mask_Sparring & mask_Male & mask_Age7to8
writePattern5ToExcel("YouthBoysSparring.xlsx", compositMask)
writePattern5ToDetailReport(6, "10:30am", "Youth Boys Sparring", "7-8", compositMask)

youth_boy_sparring_data_frame = newDataFrameFromMask(compositMask)
youth_boy_sparring_competitors = domain_model.competitors.Competitors(youth_boy_sparring_data_frame)
sparing_tree_pdf.write_event_to_sparring_report_using_pattern_5([6, 7, 8, 9, 10], "10:30am", "Youth Boys Sparring 7-8",
                                                                youth_boy_sparring_competitors)
del youth_boy_sparring_data_frame
del youth_boy_sparring_competitors

###############################################################################
# Girl's Sparring Spreadsheet - 9-11 year olds one sheet per rank
#
compositMask = mask_Sparring & mask_Age9to11 & mask_Female
writePattern4ToExcel("GirlsSparring.xlsx", compositMask)
writePattern4ToDetailReport(11, "10:30am", "Girls Sparring", "9-11", compositMask)

girl_sparring_data_frame = newDataFrameFromMask(compositMask)
girl_sparring_competitors = domain_model.competitors.Competitors(girl_sparring_data_frame)
sparing_tree_pdf.write_event_to_sparring_report_using_pattern_4([11, 12, 13, 14], "10:30am", "Girls Sparring 9-11",
                                                                girl_sparring_competitors)
del girl_sparring_data_frame
del girl_sparring_competitors

### 11:15 Events

###############################################################################
# Teen Girls Sparring Spreadsheet - 12-14 year olds one sheet per rank
#
compositMask = mask_Sparring & mask_Female & mask_Age12to14
writePattern4ToExcel("TeenGirlSparring.xlsx", compositMask)
writePattern4ToDetailReport(1, "11:15am", "Teen Girls Sparring", "12-14", compositMask)

teen_girl_sparring_data_frame = newDataFrameFromMask(compositMask)
teen_girl_sparring_competitors = domain_model.competitors.Competitors(teen_girl_sparring_data_frame)
sparing_tree_pdf.write_event_to_sparring_report_using_pattern_4([1, 2, 3, 4], "11:15am", "Teen Girls Sparring 12-14",
                                                                teen_girl_sparring_competitors)
del teen_girl_sparring_data_frame
del teen_girl_sparring_competitors

###############################################################################
# Womans Sparring Spreadsheet - 18-39 year olds one sheet per rank
#
compositMask = mask_Sparring & mask_Female & mask_Age18to39
writePattern4ToExcel("WomensSparring.xlsx", compositMask)
writePattern4ToDetailReport(5, "11:15am", "Women's Sparring", "18-39", compositMask)

woman_sparring_data_frame = newDataFrameFromMask(compositMask)
woman_sparring_competitors = domain_model.competitors.Competitors(woman_sparring_data_frame)
sparing_tree_pdf.write_event_to_sparring_report_using_pattern_4([5, 6, 7, 8], "11:15am", "Woman's Sparring 18-39",
                                                                woman_sparring_competitors)
del woman_sparring_data_frame
del woman_sparring_competitors

###############################################################################
# Weapons Division 1 - 4-8 year olds one sheet per rank
#
compositMask = mask_Weapons & mask_Age4to8
writeWeaponsDivision1ToExcel("WeaponsDivision1.xlsx", compositMask)
writeWeaponsDivision1ToDetailReport("11:15am", "Weapons Division 1", "4-8", compositMask)
writeWeaponsDivision1ToKataScoreSheet("11:15am", "Weapons Division 1", "4-8", compositMask)

###############################################################################
# Weapons Division 2 - 10-12 year olds one sheet per rank
#
compositMask = mask_Weapons & mask_Age9to11
writeWeaponsDivision2ToExcel("WeaponsDivision2.xlsx", compositMask)
writeWeaponsDivision2ToDetailReport("11:15am", "Weapons Division 2: White - Blue Stripe", "9-11", compositMask)
writeWeaponsDivision2ToKataScoreSheet("11:15am", "Weapons Division 2: White - Blue Stripe", "9-11", compositMask)

###############################################################################
#  WeaponsDivision3 13-17 year olds one sheet per rank
#
compositMask = mask_Weapons & mask_Age9to11
writeWeaponsDivision3ToExcel("WeaponsDivision3.xlsx", compositMask)
writeWeaponsDivision3ToDetailReport("4:15pm", "Weapons Division 3 Green - Jr. Black", "9-11", compositMask)
writeWeaponsDivision3ToKataScoreSheet("4:15pm", "Weapons Division 3 Green - Jr. Black", "9-11", compositMask)

### 1:30 Events

###############################################################################
# Men And Womens Kata - 18-39 year olds one sheet per rank
#
compositMask = mask_Forms & mask_Age18to39
writePattern6ToExcel("MenAndWomensKata.xlsx", compositMask)
writePattern6ToDetailReport(1, "1:30pm", "Men & Womens Kata", "18-39", compositMask)
writePattern6ToKataScoreSheet(1, "1:30pm", "Men & Womens Kata", "18-39", compositMask)

###############################################################################
# Teen Kata - 12-14 year olds one sheet per rank
#
compositMask = mask_Forms & mask_Age12to14
writePattern6ToExcel("TeenKata.xlsx", compositMask)
writePattern6WithSplitToDetailReport(8, "1:30pm", "Teen Kata", "12-14", compositMask)
writePattern6WithSplitToKataScoreSheetlReport(8, "1:30pm", "Teen Kata", "12-14", compositMask)

### 2:15 Events

###############################################################################
# Senior Mens Sparring - 40+ year olds one sheet per rank
#
compositMask = mask_Sparring & mask_Male & mask_Age40Plus
writePattern4ToExcel("SeniorMensSparring.xlsx", compositMask)
writePattern4ToDetailReport(1, "2:15pm", "Senior Men's Sparring", "40 +", compositMask)

senior_men_sparring_data_frame = newDataFrameFromMask(compositMask)
senior_men_sparring_competitors = domain_model.competitors.Competitors(senior_men_sparring_data_frame)
sparing_tree_pdf.write_event_to_sparring_report_using_pattern_4([1, 2, 3, 4], "2:15pm", "Senior Men's Sparring 40+",
                                                                senior_men_sparring_competitors)
del senior_men_sparring_data_frame
del senior_men_sparring_competitors

###############################################################################
# Senior Womens Sparring - 40+ year olds one sheet per rank
#
compositMask = mask_Sparring & mask_Female & mask_Age40Plus
writePattern4ToExcel("SeniorWomensSparring.xlsx", compositMask)
writePattern4ToDetailReport(5, "2:15pm", "Senior Women's Sparring", "40 +", compositMask)

senior_woman_sparring_data_frame = newDataFrameFromMask(compositMask)
senior_woman_sparring_competitors = domain_model.competitors.Competitors(senior_woman_sparring_data_frame)
sparing_tree_pdf.write_event_to_sparring_report_using_pattern_4([5, 6, 7, 8], "2:15pm", "Senior Woman's Sparring 40+",
                                                                senior_woman_sparring_competitors)
del senior_woman_sparring_data_frame
del senior_woman_sparring_competitors

###############################################################################
# Young Adult Kata - 15-17 year olds one sheet per rank
#
compositMask = mask_Forms & mask_Age15to17
writePattern4ToExcel("YoungAdultKata.xlsx", compositMask)
writePattern4ToDetailReport(9, "2:15pm", "Young Adult Kata", "15-17", compositMask)
writePattern4ToKataScoreSheet(9, "2:15pm", "Young Adult Kata", "15-17", compositMask)

### 3:00 Events

###############################################################################
#  Mens Sparring - 18-39 year olds one sheet per rank
#
compositMask = mask_Sparring & mask_Male & mask_Age18to39
writePattern4ToExcel("MensSparring.xlsx", compositMask)
writePattern4ToDetailReport(1, "3:00pm", "Mens Sparring", "18-39", compositMask)

men_sparring_data_frame = newDataFrameFromMask(compositMask)
men_sparring_competitors = domain_model.competitors.Competitors(men_sparring_data_frame)
sparing_tree_pdf.write_event_to_sparring_report_using_pattern_4([1, 2, 3, 4], "3:00pm", "Men's Sparring 18-39",
                                                                men_sparring_competitors)
del men_sparring_data_frame
del men_sparring_competitors

###############################################################################
#  Teen Boys Sparring - 120-14 year olds one sheet per rank
#
compositMask = mask_Sparring & mask_Male & mask_Age12to14
writePattern4ToExcel("TeenBoysSparring.xlsx", compositMask)
writePattern4ToDetailReport(5, "3:00pm", "Teen Boys Sparring", "12-14", compositMask)

teen_boys_sparring_data_frame = newDataFrameFromMask(compositMask)
teen_boys_sparring_competitors = domain_model.competitors.Competitors(teen_boys_sparring_data_frame)
sparing_tree_pdf.write_event_to_sparring_report_using_pattern_4([5, 6, 7, 8], "3:00pm", "Teen Boy's Sparring 12-14",
                                                                teen_boys_sparring_competitors)
del teen_boys_sparring_data_frame
del teen_boys_sparring_competitors

###############################################################################
#  Young Adult Mens Sparring - 15-17 year olds one sheet per rank
#
compositMask = mask_Sparring & mask_Male & mask_Age15to17
writePattern4ToExcel("YoungAdultMensSparring.xlsx", compositMask)
writePattern4ToDetailReport(9, "3:00pm", "Young Adult Mens Sparring", "15-17", compositMask)

young_adult_men_sparring_data_frame = newDataFrameFromMask(compositMask)
young_adult_men_sparring_competitors = domain_model.competitors.Competitors(
    young_adult_men_sparring_data_frame)
sparing_tree_pdf.write_event_to_sparring_report_using_pattern_4([9, 10, 11, 12], "3:00pm",
                                                                "Young Adult Men's Sparring 15-17",
                                                                young_adult_men_sparring_competitors)
del young_adult_men_sparring_data_frame
del young_adult_men_sparring_competitors

### 3:45 Events

###############################################################################
# Senior Kata - 40+ year olds one sheet per rank
#
compositMask = mask_Forms & mask_Age40Plus
writePattern6ToExcel("SeniorKata.xlsx", compositMask)
writePattern6ToDetailReport(1, "3:45pm", "Senior Kata", "40+", compositMask)
writePattern6ToKataScoreSheet(1, "3:45pm", "Senior Kata", "40+", compositMask)

###############################################################################
#  Young Adult Womens Sparring - 15-17 year olds one sheet per rank
#
compositMask = mask_Sparring & mask_Female & mask_Age15to17
writePattern7ToExcel("YoungAdultWomensSparring.xlsx", compositMask)
writePattern7ToDetailReport(8, "3:45pm", "Young Adult Womens Sparring", "15-17", compositMask)

young_adult_women_sparring_data_frame = newDataFrameFromMask(compositMask)
young_adult_women_sparring_competitors = domain_model.competitors.Competitors(
    young_adult_women_sparring_data_frame)
sparing_tree_pdf.write_event_to_sparring_report_using_pattern_4([8, 9, 10, 11], "3:45pm",
                                                                "Young Adult Women's Sparring 15-17",
                                                                young_adult_women_sparring_competitors)
del young_adult_women_sparring_data_frame
del young_adult_women_sparring_competitors

### 4:15 Events

###############################################################################
#  WeaponsDivision4 12-17 White-Blue Stripe year olds one sheet per rank
#
compositMask = mask_Weapons & mask_Age12to17
writeWeaponsDivision4ToExcel("WeaponsDivision4.xlsx", compositMask)
writeWeaponsDivision4ToDetailReport("4:15pm", "Weapons Division 4", "12 - 17", compositMask)
writeWeaponsDivision4ToKataScoreSheet("4:15pm", "Weapons Division 4", "12 - 17", compositMask)

###############################################################################
#  WeaponsDivision5 18+ year olds one sheet per rank
#
compositMask = mask_Weapons & mask_Age18Plus
writeWeaponsDivision5ToExcel("WeaponsDivision5.xlsx", compositMask)
writeWeaponsDivision5ToDetailReport("4:15pm", "Weapons Division 5", "18+", compositMask)
writeWeaponsDivision5ToKataScoreSheet("4:15pm", "Weapons Division 5", "18+", compositMask)

###############################################################################
#  WeaponsDivision6 12+ year olds green belts
#
compositMask = mask_Weapons & mask_Age12Plus
writeWeaponsDivision6ToFile("WeaponsDivision6.xlsx", compositMask)
writeWeaponsDivision6ToDetailReport("4:15pm", "Weapons Division 6", "12+", compositMask)
writeWeaponsDivision6ToKataScoreSheet("4:15pm", "Weapons Division 6", "12+", compositMask)

###############################################################################
#  WeaponsDivision7 12+ year olds brown belts
#
compositMask = mask_Weapons & mask_Age12Plus
writeWeaponsDivision7ToFile("WeaponsDivision7.xlsx", compositMask)
writeWeaponsDivision7ToDetailReport("4:15pm", "Weapons Division 7", "12+", compositMask)
writeWeaponsDivision7ToKataScoreSheet("4:15pm", "Weapons Division 7", "12+", compositMask)

###############################################################################
#  WeaponsDivision8 12+ year olds one sheet per rank
#
compositMask = mask_Weapons & mask_Age12Plus
writeWeaponsDivision8ToFile("WeaponsDivision8.xlsx", compositMask)
writeWeaponsDivision8ToDetailReport("4:15pm", "Weapons Division 8", "12+", compositMask)
writeWeaponsDivision8ToKataScoreSheet("4:15pm", "Weapons Division 8", "12+", compositMask)

print(time.strftime("%X") + " Saving PDFs to disk")
divison_detail_report_pdf.write_pdfpage()
kata_score_sheet.write_pdfpage()
sparing_tree_pdf.close()

print("Here is how many times we touched each person:")
for index, row in clean_df.iterrows():
    name = row['First_Name'] + " " + row['Last_Name']
    hc = row['hitcount']
    print("  " + name + ": " + str(hc))

localtime = time.asctime(time.localtime(time.time()))
print(time.strftime("%X") + " Done!")
