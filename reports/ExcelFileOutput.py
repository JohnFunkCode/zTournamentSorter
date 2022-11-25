#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: john funk
"""

import os
import time
import pandas as pd
import reports.FileHandlingUtilities
import domain_model.constants as constants


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
from domain_model import constants as constants


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
# writePattern1ToExcelViaQuery
#  This method provides a re-usable method to write output to excel
#  The Pattern it writes is:
#    White, Yellow
#    Orange
#    Purple
#    Blue, Blue Stripe
#    Green, Green Stripe, Brown
#
#  arguments:
#  filename - the filename without path to write
#  gender - gender used in the query 'male', 'female', or '*'
#  minimum_age - the minimum age used in the query
#  maximum_age - the maxinum age used in the query
#  writePattern4ToExcel(filename="KidsKata.xlsx", gender="*",minimum_age=4, maximum_age=6)
def writePattern1ToExcelViaQuery(filename: str, division_type: str, gender: str, minimum_age: int, maximum_age: int,clean_df: pd.DataFrame):
    fullpath = os.getcwd() + reports.FileHandlingUtilities.pathDelimiter() + "Sorted" + reports.FileHandlingUtilities.pathDelimiter() + filename
    writer = pd.ExcelWriter(fullpath, engine='xlsxwriter')
    print(time.strftime("%X") + " Generating " + fullpath)

    # Hack for 3 year olds
    if minimum_age == 4:
        minimum_age = 2

    age_query = 'Age >={0} and Age <={1}'.format(minimum_age, maximum_age)

    if gender == '*':
        gender_query = ''
    else:
        gender_query = 'and Gender == "' + gender + '"'

    assert division_type == 'Weapons' or division_type == 'Sparring' or division_type == 'Forms', "Error: Invalid division_type"
    if division_type == 'Weapons':
        division_type_query = 'Weapons.str.contains("Weapons")'
    else:
        division_type_query = 'Events.str.contains("' + division_type + '")'

    rank_query = f"Rank == '{constants.WHITE_BELT}' or Rank == '{constants.YELLOW_BELT}' or Rank == '{constants.ORANGE_BELT}'"
    combined_query= f'{division_type_query} and {age_query} {gender_query} and ({rank_query})'
    wmk = reports.FileHandlingUtilities.newDataFrameFromQuery(clean_df=clean_df,query_string=combined_query)
    writeFormattedExcelSheet(wmk, writer, 'White, Yellow, Orange')

    rank_query = f"Rank == '{constants.PURPLE_BELT}' or Rank == '{constants.BLUE_BELT}' or Rank == '{constants.BLUE_STRIPE_BELT}'"
    combined_query= f'{division_type_query} and {age_query} {gender_query} and ({rank_query})'
    wmk = reports.FileHandlingUtilities.newDataFrameFromQuery(clean_df=clean_df,query_string=combined_query)
    writeFormattedExcelSheet(wmk, writer, 'Purple, Blue, Blue Stripe')

    rank_query = f"Rank == '{constants.GREEN_BELT}' or Rank == '{constants.GREEN_STRIPE_BELT}' or Rank == '{constants.FIRST_DEGREE_BROWN_BELT}' or Rank == '{constants.SECOND_DEGREE_BROWN_BELT}' or Rank == '{constants.THIRD_DEGREE_BROWN_BELT}'"
    combined_query= f'{division_type_query} and {age_query} {gender_query} and ({rank_query})'
    wmk = reports.FileHandlingUtilities.newDataFrameFromQuery(clean_df=clean_df,query_string=combined_query)
    writeFormattedExcelSheet(wmk, writer, 'Green, Green Stripe, Brown')

    rank_query = f"Rank == '{constants.FIRST_DEGREE_BLACK_BELT}' or Rank == '{constants.SECOND_DEGREE_BLACK_BELT}' or Rank == '{constants.THIRD_DEGREE_BLACK_BELT}' or Rank == '{constants.FOURTH_DEGREE_BLACK_BELT}' or Rank == '{constants.FIFTH_DEGREE_BLACK_BELT}' or Rank == '{constants.JUNIOR_BLACK_BELT}'"
    combined_query= f'{division_type_query} and {age_query} {gender_query} and ({rank_query})'
    wmk = reports.FileHandlingUtilities.newDataFrameFromQuery(clean_df=clean_df,query_string=combined_query)
    writeFormattedExcelSheet(wmk, writer, 'Black')

    writer.close()
    time.sleep(constants.SLEEP_TIME)


###############################################################################
# writePattern2ToExcelViaQuery
#  This method provides a re-usable method to write output to excel
#  The Pattern it writes is:
#    White, Yellow & Orange
#    Purple, Blue & Blue Stripe
#    Green, Green Stripe,
#    Brown
#    Black
#
#  arguments:
#  filename - the filename without path to write
#  gender - gender used in the query 'male', 'female', or '*'
#  minimum_age - the minimum age used in the query
#  maximum_age - the maxinum age used in the query
#  writePattern4ToExcel(filename="KidsKata.xlsx", gender="*",minimum_age=4, maximum_age=6)
def writePattern2ToExcelViaQuery(filename: str, division_type: str, gender: str, minimum_age: int, maximum_age: int,clean_df: pd.DataFrame):
    fullpath = os.getcwd() + reports.FileHandlingUtilities.pathDelimiter() + "Sorted" + reports.FileHandlingUtilities.pathDelimiter() + filename
    writer = pd.ExcelWriter(fullpath, engine='xlsxwriter')
    print(time.strftime("%X") + " Generating " + fullpath)

    # Hack for 3 year olds
    if minimum_age == 4:
        minimum_age = 2

    age_query = 'Age >={0} and Age <={1}'.format(minimum_age, maximum_age)

    if gender == '*':
        gender_query = ''
    else:
        gender_query = 'and Gender == "' + gender + '"'


    assert division_type == 'Weapons' or division_type == 'Sparring' or division_type == 'Forms', "Error: Invalid division_type"
    if division_type == 'Weapons':
        division_type_query = 'Weapons.str.contains("Weapons")'
    else:
        division_type_query = 'Events.str.contains("' + division_type + '")'

    rank_query = f"Rank == '{constants.WHITE_BELT}' or Rank == '{constants.YELLOW_BELT}' or Rank == '{constants.ORANGE_BELT}'"
    combined_query= f'{division_type_query} and {age_query} {gender_query} and ({rank_query})'
    wmk = reports.FileHandlingUtilities.newDataFrameFromQuery(clean_df=clean_df,query_string=combined_query)
    writeFormattedExcelSheet(wmk, writer, 'White, Yellow, Orange')

    rank_query = f"Rank == '{constants.PURPLE_BELT}' or Rank == '{constants.BLUE_BELT}' or Rank == '{constants.BLUE_STRIPE_BELT}'"
    combined_query= f'{division_type_query} and {age_query} {gender_query} and ({rank_query})'
    wmk = reports.FileHandlingUtilities.newDataFrameFromQuery(clean_df=clean_df,query_string=combined_query)
    writeFormattedExcelSheet(wmk, writer, 'Purple, Blue, Blue Stripe')

    rank_query = f"Rank == '{constants.GREEN_BELT}' or Rank == '{constants.GREEN_STRIPE_BELT}'"
    combined_query= f'{division_type_query} and {age_query} {gender_query} and ({rank_query})'
    wmk = reports.FileHandlingUtilities.newDataFrameFromQuery(clean_df=clean_df,query_string=combined_query)
    writeFormattedExcelSheet(wmk, writer, 'Green, Green Stripe')


    rank_query = f"Rank == '{constants.FIRST_DEGREE_BROWN_BELT}' or Rank == '{constants.SECOND_DEGREE_BROWN_BELT}' or Rank == '{constants.THIRD_DEGREE_BROWN_BELT}'"
    combined_query= f'{division_type_query} and {age_query} {gender_query} and ({rank_query})'
    wmk = reports.FileHandlingUtilities.newDataFrameFromQuery(clean_df=clean_df,query_string=combined_query)
    writeFormattedExcelSheet(wmk, writer, 'Brown')

    rank_query = f"Rank == '{constants.FIRST_DEGREE_BLACK_BELT}' or Rank == '{constants.SECOND_DEGREE_BLACK_BELT}' or Rank == '{constants.THIRD_DEGREE_BLACK_BELT}' or Rank == '{constants.FOURTH_DEGREE_BLACK_BELT}' or Rank == '{constants.FIFTH_DEGREE_BLACK_BELT}' or Rank == '{constants.JUNIOR_BLACK_BELT}'"
    combined_query= f'{division_type_query} and {age_query} {gender_query} and ({rank_query})'
    wmk = reports.FileHandlingUtilities.newDataFrameFromQuery(clean_df=clean_df,query_string=combined_query)
    writeFormattedExcelSheet(wmk, writer, 'Black')


    writer.close()
    time.sleep(constants.SLEEP_TIME)


###############################################################################
# writePattern3ToExcelViaQuery
#  This method provides a re-usable method to write output to excel
#  The Pattern it writes is:
#    White, Yellow
#    Orange
#    Purple
#    Blue, Blue Stripe
#    Green, Green Stripe, Brown
#
#  arguments:
#  filename - the filename without path to write
#  gender - gender used in the query 'male', 'female', or '*'
#  minimum_age - the minimum age used in the query
#  maximum_age - the maxinum age used in the query
#  writePattern4ToExcel(filename="KidsKata.xlsx", gender="*",minimum_age=4, maximum_age=6)
def writePattern3ToExcelViaQuery(filename: str, division_type: str, gender: str, minimum_age: int, maximum_age: int,clean_df: pd.DataFrame):
    fullpath = os.getcwd() + reports.FileHandlingUtilities.pathDelimiter() + "Sorted" + reports.FileHandlingUtilities.pathDelimiter() + filename
    writer = pd.ExcelWriter(fullpath, engine='xlsxwriter')
    print(time.strftime("%X") + " Generating " + fullpath)

    # Hack for 3 year olds
    if minimum_age == 4:
        minimum_age = 2

    age_query = 'Age >={0} and Age <={1}'.format(minimum_age, maximum_age)

    if gender == '*':
        gender_query = ''
    else:
        gender_query = 'and Gender == "' + gender + '"'


    assert division_type == 'Weapons' or division_type == 'Sparring' or division_type == 'Forms', "Error: Invalid division_type"
    if division_type == 'Weapons':
        division_type_query = 'Weapons.str.contains("Weapons")'
    else:
        division_type_query = 'Events.str.contains("' + division_type + '")'

    rank_query = f"Rank == '{constants.WHITE_BELT}' or Rank == '{constants.YELLOW_BELT}'"
    combined_query= f'{division_type_query} and {age_query} {gender_query} and ({rank_query})'
    wmk = reports.FileHandlingUtilities.newDataFrameFromQuery(clean_df=clean_df,query_string=combined_query)
    writeFormattedExcelSheet(wmk, writer, 'White, Yellow')

    rank_query = f"Rank == '{constants.ORANGE_BELT}'"
    combined_query= f'{division_type_query} and {age_query} {gender_query} and ({rank_query})'
    wmk = reports.FileHandlingUtilities.newDataFrameFromQuery(clean_df=clean_df,query_string=combined_query)
    writeFormattedExcelSheet(wmk, writer, 'Orange')

    rank_query = f"Rank == '{constants.PURPLE_BELT}'"
    combined_query= f'{division_type_query} and {age_query} {gender_query} and ({rank_query})'
    wmk = reports.FileHandlingUtilities.newDataFrameFromQuery(clean_df=clean_df,query_string=combined_query)
    writeFormattedExcelSheet(wmk, writer, 'Purple')


    rank_query = f"Rank == '{constants.BLUE_BELT}' or Rank == '{constants.BLUE_STRIPE_BELT}'"
    combined_query= f'{division_type_query} and {age_query} {gender_query} and ({rank_query})'
    wmk = reports.FileHandlingUtilities.newDataFrameFromQuery(clean_df=clean_df,query_string=combined_query)
    writeFormattedExcelSheet(wmk, writer, 'Blue, Blue Stripe')


    rank_query = f"Rank == '{constants.GREEN_BELT}' or Rank == '{constants.GREEN_STRIPE_BELT}' or Rank == '{constants.FIRST_DEGREE_BROWN_BELT}' or Rank == '{constants.SECOND_DEGREE_BROWN_BELT}' or Rank == '{constants.THIRD_DEGREE_BROWN_BELT}'"
    combined_query= f'{division_type_query} and {age_query} {gender_query} and ({rank_query})'
    wmk = reports.FileHandlingUtilities.newDataFrameFromQuery(clean_df=clean_df,query_string=combined_query)
    writeFormattedExcelSheet(wmk, writer, 'Green, Green Stripe, Brown')

    writer.close()
    time.sleep(constants.SLEEP_TIME)


###############################################################################
# writePattern4ToExcelViaQuery
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
#  gender - gender used in the query 'male', 'female', or '*'
#  minimum_age - the minimum age used in the query
#  maximum_age - the maxinum age used in the query
#  writePattern4ToExcel(filename="KidsKata.xlsx", gender="*",minimum_age=4, maximum_age=6)
def writePattern4ToExcelViaQuery(filename: str, division_type: str, gender: str, minimum_age: int, maximum_age: int,clean_df: pd.DataFrame):
    fullpath = os.getcwd() + reports.FileHandlingUtilities.pathDelimiter() + "Sorted" + reports.FileHandlingUtilities.pathDelimiter() + filename
    writer = pd.ExcelWriter(fullpath, engine='xlsxwriter')
    print(time.strftime("%X") + " Generating " + fullpath)

    # Hack for 3 year olds
    if minimum_age == 4:
        minimum_age = 2

    age_query = 'Age >={0} and Age <={1}'.format(minimum_age, maximum_age)

    if gender == '*':
        gender_query = ''
    else:
        gender_query = 'and Gender == "' + gender + '"'


    assert division_type == 'Weapons' or division_type == 'Sparring' or division_type == 'Forms', "Error: Invalid division_type"
    if division_type == 'Weapons':
        division_type_query = 'Weapons.str.contains("Weapons")'
    else:
        division_type_query = 'Events.str.contains("' + division_type + '")'

    rank_query = f"Rank == '{constants.WHITE_BELT}'"
    combined_query= f'{division_type_query} and {age_query} {gender_query} and ({rank_query})'

    wmk = reports.FileHandlingUtilities.newDataFrameFromQuery(clean_df=clean_df,query_string=combined_query)
    writeFormattedExcelSheet(wmk, writer, 'White')

    rank_query = f"Rank == '{constants.YELLOW_BELT}'"
    combined_query= f'{division_type_query} and {age_query} {gender_query} and ({rank_query})'
    wmk = reports.FileHandlingUtilities.newDataFrameFromQuery(clean_df=clean_df,query_string=combined_query)
    writeFormattedExcelSheet(wmk, writer, 'Yellow')

    rank_query = f"Rank == '{constants.ORANGE_BELT}'"
    combined_query= f'{division_type_query} and {age_query} {gender_query} and ({rank_query})'
    wmk = reports.FileHandlingUtilities.newDataFrameFromQuery(clean_df=clean_df,query_string=combined_query)
    writeFormattedExcelSheet(wmk, writer, 'Orange')

    rank_query = f"Rank == '{constants.PURPLE_BELT}' or Rank == '{constants.BLUE_BELT}' or Rank == '{constants.BLUE_STRIPE_BELT}'"
    combined_query= f'{division_type_query} and {age_query} {gender_query} and ({rank_query})'
    wmk = reports.FileHandlingUtilities.newDataFrameFromQuery(clean_df=clean_df,query_string=combined_query)
    writeFormattedExcelSheet(wmk, writer, 'Purple, Blue, Blue Stripe')


    rank_query = f"Rank == '{constants.GREEN_BELT}' or Rank == '{constants.GREEN_STRIPE_BELT}' or Rank == '{constants.FIRST_DEGREE_BROWN_BELT}' or Rank == '{constants.SECOND_DEGREE_BROWN_BELT}' or Rank == '{constants.THIRD_DEGREE_BROWN_BELT}'"
    combined_query= f'{division_type_query} and {age_query} {gender_query} and ({rank_query})'
    wmk = reports.FileHandlingUtilities.newDataFrameFromQuery(clean_df=clean_df,query_string=combined_query)
    writeFormattedExcelSheet(wmk, writer, 'Green, Green Stripe, Brown')

    # writer.save()
    writer.close()
    time.sleep(constants.SLEEP_TIME)


###############################################################################
# writePattern5ToExcelViaQuery
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
#  gender - gender used in the query 'male', 'female', or '*'
#  minimum_age - the minimum age used in the query
#  maximum_age - the maxinum age used in the query
#  writePattern4ToExcel(filename="KidsKata.xlsx", gender="*",minimum_age=4, maximum_age=6)
def writePattern5ToExcelViaQuery(filename: str, division_type: str, gender: str, minimum_age: int, maximum_age: int,clean_df: pd.DataFrame):
    fullpath = os.getcwd() + reports.FileHandlingUtilities.pathDelimiter() + "Sorted" + reports.FileHandlingUtilities.pathDelimiter() + filename
    writer = pd.ExcelWriter(fullpath, engine='xlsxwriter')
    print(time.strftime("%X") + " Generating " + fullpath)

    # Hack for 3 year olds
    if minimum_age == 4:
        minimum_age = 2

    age_query = 'Age >={0} and Age <={1}'.format(minimum_age, maximum_age)

    if gender == '*':
        gender_query = ''
    else:
        gender_query = 'and Gender == "' + gender + '"'


    assert division_type == 'Weapons' or division_type == 'Sparring' or division_type == 'Forms', "Error: Invalid division_type"
    if division_type == 'Weapons':
        division_type_query = 'Weapons.str.contains("Weapons")'
    else:
        division_type_query = 'Events.str.contains("' + division_type + '")'

    rank_query = f"Rank == '{constants.WHITE_BELT}'"
    combined_query= f'{division_type_query} and {age_query} {gender_query} and ({rank_query})'

    wmk = reports.FileHandlingUtilities.newDataFrameFromQuery(clean_df=clean_df,query_string=combined_query)
    writeFormattedExcelSheet(wmk, writer, 'White')

    rank_query = f"Rank == '{constants.YELLOW_BELT}'"
    combined_query= f'{division_type_query} and {age_query} {gender_query} and ({rank_query})'
    wmk = reports.FileHandlingUtilities.newDataFrameFromQuery(clean_df=clean_df,query_string=combined_query)
    writeFormattedExcelSheet(wmk, writer, 'Yellow')

    rank_query = f"Rank == '{constants.ORANGE_BELT}'"
    combined_query= f'{division_type_query} and {age_query} {gender_query} and ({rank_query})'
    wmk = reports.FileHandlingUtilities.newDataFrameFromQuery(clean_df=clean_df,query_string=combined_query)
    writeFormattedExcelSheet(wmk, writer, 'Orange')

    rank_query = f"Rank == '{constants.PURPLE_BELT}'"
    combined_query= f'{division_type_query} and {age_query} {gender_query} and ({rank_query})'
    wmk = reports.FileHandlingUtilities.newDataFrameFromQuery(clean_df=clean_df,query_string=combined_query)
    writeFormattedExcelSheet(wmk, writer, 'Purple')


    rank_query = f"Rank == '{constants.BLUE_BELT}' or Rank == '{constants.BLUE_STRIPE_BELT}'"
    combined_query= f'{division_type_query} and {age_query} {gender_query} and ({rank_query})'
    wmk = reports.FileHandlingUtilities.newDataFrameFromQuery(clean_df=clean_df,query_string=combined_query)
    writeFormattedExcelSheet(wmk, writer, 'Blue, Blue Stripe')


    rank_query = f"Rank == '{constants.GREEN_BELT}' or Rank == '{constants.GREEN_STRIPE_BELT}' or Rank == '{constants.FIRST_DEGREE_BROWN_BELT}' or Rank == '{constants.SECOND_DEGREE_BROWN_BELT}' or Rank == '{constants.THIRD_DEGREE_BROWN_BELT}'"
    combined_query= f'{division_type_query} and {age_query} {gender_query} and ({rank_query})'
    wmk = reports.FileHandlingUtilities.newDataFrameFromQuery(clean_df=clean_df,query_string=combined_query)
    writeFormattedExcelSheet(wmk, writer, 'Green, Green Stripe, Brown')

    writer.close()
    time.sleep(constants.SLEEP_TIME)

###############################################################################
# writePattern6ToExcelViaQuery
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
#  gender - gender used in the query 'male', 'female', or '*'
#  minimum_age - the minimum age used in the query
#  maximum_age - the maxinum age used in the query
#  writePattern4ToExcel(filename="KidsKata.xlsx", gender="*",minimum_age=4, maximum_age=6)
def writePattern6ToExcelViaQuery(filename: str, division_type: str, gender: str, minimum_age: int, maximum_age: int,clean_df: pd.DataFrame):
    fullpath = os.getcwd() + reports.FileHandlingUtilities.pathDelimiter() + "Sorted" + reports.FileHandlingUtilities.pathDelimiter() + filename
    writer = pd.ExcelWriter(fullpath, engine='xlsxwriter')
    print(time.strftime("%X") + " Generating " + fullpath)

    # Hack for 3 year olds
    if minimum_age == 4:
        minimum_age = 2

    age_query = 'Age >={0} and Age <={1}'.format(minimum_age, maximum_age)

    if gender == '*':
        gender_query = ''
    else:
        gender_query = 'and Gender == "' + gender + '"'


    assert division_type == 'Weapons' or division_type == 'Sparring' or division_type == 'Forms', "Error: Invalid division_type"
    if division_type == 'Weapons':
        division_type_query = 'Weapons.str.contains("Weapons")'
    else:
        division_type_query = 'Events.str.contains("' + division_type + '")'

    rank_query = f"Rank == '{constants.WHITE_BELT}' or Rank == '{constants.YELLOW_BELT}'"
    combined_query= f'{division_type_query} and {age_query} {gender_query} and ({rank_query})'
    wmk = reports.FileHandlingUtilities.newDataFrameFromQuery(clean_df=clean_df,query_string=combined_query)
    writeFormattedExcelSheet(wmk, writer, 'White, Yellow')

    rank_query = f"Rank == '{constants.ORANGE_BELT}'"
    combined_query= f'{division_type_query} and {age_query} {gender_query} and ({rank_query})'
    wmk = reports.FileHandlingUtilities.newDataFrameFromQuery(clean_df=clean_df,query_string=combined_query)
    writeFormattedExcelSheet(wmk, writer, 'Orange')

    rank_query = f"Rank == '{constants.PURPLE_BELT}'"
    combined_query= f'{division_type_query} and {age_query} {gender_query} and ({rank_query})'
    wmk = reports.FileHandlingUtilities.newDataFrameFromQuery(clean_df=clean_df,query_string=combined_query)
    writeFormattedExcelSheet(wmk, writer, 'Purple')


    rank_query = f"Rank == '{constants.BLUE_BELT}' or Rank == '{constants.BLUE_STRIPE_BELT}'"
    combined_query= f'{division_type_query} and {age_query} {gender_query} and ({rank_query})'
    wmk = reports.FileHandlingUtilities.newDataFrameFromQuery(clean_df=clean_df,query_string=combined_query)
    writeFormattedExcelSheet(wmk, writer, 'Blue, Blue Stripe')


    rank_query = f"Rank == '{constants.GREEN_BELT}' or Rank == '{constants.GREEN_STRIPE_BELT}'"
    combined_query= f'{division_type_query} and {age_query} {gender_query} and ({rank_query})'
    wmk = reports.FileHandlingUtilities.newDataFrameFromQuery(clean_df=clean_df,query_string=combined_query)
    writeFormattedExcelSheet(wmk, writer, 'Green, Green Stripe')

    rank_query = f"Rank == '{constants.FIRST_DEGREE_BROWN_BELT}' or Rank == '{constants.SECOND_DEGREE_BROWN_BELT}' or Rank == '{constants.THIRD_DEGREE_BROWN_BELT}'"
    combined_query= f'{division_type_query} and {age_query} {gender_query} and ({rank_query})'
    wmk = reports.FileHandlingUtilities.newDataFrameFromQuery(clean_df=clean_df,query_string=combined_query)
    writeFormattedExcelSheet(wmk, writer, 'Brown')

    rank_query = f"Rank == '{constants.FIRST_DEGREE_BLACK_BELT}' or Rank == '{constants.SECOND_DEGREE_BLACK_BELT}' or Rank == '{constants.THIRD_DEGREE_BLACK_BELT}' or Rank == '{constants.FOURTH_DEGREE_BLACK_BELT}' or Rank == '{constants.FIFTH_DEGREE_BLACK_BELT}' or Rank == '{constants.JUNIOR_BLACK_BELT}'"
    combined_query= f'{division_type_query} and {age_query} {gender_query} and ({rank_query})'
    wmk = reports.FileHandlingUtilities.newDataFrameFromQuery(clean_df=clean_df,query_string=combined_query)
    writeFormattedExcelSheet(wmk, writer, 'Black')


    writer.close()
    time.sleep(constants.SLEEP_TIME)

###############################################################################
# writeWeaponsDivision1ToExcel
#  arguments:
#  filename - the filename without path to write
#  arguments:
#  filename - the filename without path to write
#  gender - gender used in the query 'male', 'female', or '*'
#  minimum_age - the minimum age used in the query
#  maximum_age - the maxinum age used in the query
#
def writeWeaponsDivision1ToExcelViaQuery(filename: str, division_type: str, gender: str, minimum_age: int, maximum_age: int, clean_df: pd.DataFrame):

    fullpath = os.getcwd() + reports.FileHandlingUtilities.pathDelimiter() + "Sorted" + reports.FileHandlingUtilities.pathDelimiter() + filename
    writer = pd.ExcelWriter(fullpath)
    print(time.strftime("%X") + " Generating " + fullpath)

    # Hack for 3 year olds
    if minimum_age == 4:
        minimum_age = 2

    age_query = 'Age >={0} and Age <={1}'.format(minimum_age, maximum_age)

    if gender == '*':
        gender_query = ''
    else:
        gender_query = 'and Gender == "' + gender + '"'


    assert division_type == 'Weapons' or division_type == 'Sparring' or division_type == 'Forms', "Error: Invalid division_type"
    if division_type == 'Weapons':
        division_type_query = 'Weapons.str.contains("Weapons")'
    else:
        division_type_query = 'Events.str.contains("' + division_type + '")'

    combined_query= f'{division_type_query} and {age_query} {gender_query}'
    wmk = reports.FileHandlingUtilities.newDataFrameFromQuery(clean_df=clean_df,query_string=combined_query)
    reports.ExcelFileOutput.writeFormattedExcelSheet(wmk, writer, 'Weapons Division 1')

    writer.close()
    time.sleep(constants.SLEEP_TIME)


###############################################################################
# writeWeaponsDivision2ToExcel
#  arguments:
#  filename - the filename without path to write
#  arguments:
#  filename - the filename without path to write
#  gender - gender used in the query 'male', 'female', or '*'
#  minimum_age - the minimum age used in the query
#  maximum_age - the maxinum age used in the query
#
def writeWeaponsDivision2ToExcelViaQuery(filename: str, division_type: str, gender: str, minimum_age: int, maximum_age: int,clean_df: pd.DataFrame):

    fullpath = os.getcwd() + reports.FileHandlingUtilities.pathDelimiter() + "Sorted" + reports.FileHandlingUtilities.pathDelimiter() + filename
    writer = pd.ExcelWriter(fullpath)
    print(time.strftime("%X") + " Generating " + fullpath)

    # Hack for 3 year olds
    if minimum_age == 4:
        minimum_age = 2

    age_query = 'Age >={0} and Age <={1}'.format(minimum_age, maximum_age)

    if gender == '*':
        gender_query = ''
    else:
        gender_query = 'and Gender == "' + gender + '"'


    assert division_type == 'Weapons' or division_type == 'Sparring' or division_type == 'Forms', "Error: Invalid division_type"
    if division_type == 'Weapons':
        division_type_query = 'Weapons.str.contains("Weapons")'
    else:
        division_type_query = 'Events.str.contains("' + division_type + '")'


    rank_query = f"Rank == '{constants.WHITE_BELT}' or Rank == '{constants.YELLOW_BELT}' or Rank == '{constants.ORANGE_BELT}' or Rank == '{constants.PURPLE_BELT}' or Rank == '{constants.BLUE_BELT}' or Rank == '{constants.BLUE_STRIPE_BELT}'"

    combined_query= f'{division_type_query} and {age_query} {gender_query} and ({rank_query})'
    wmk = reports.FileHandlingUtilities.newDataFrameFromQuery(clean_df=clean_df, query_string=combined_query)
    reports.ExcelFileOutput.writeFormattedExcelSheet(wmk, writer, 'Weapons Division 2')

    writer.close()
    time.sleep(constants.SLEEP_TIME)


###############################################################################
# writeWeaponsDivision3ToExcel
#  arguments:
#  filename - the filename without path to write
#  arguments:
#  filename - the filename without path to write
#  gender - gender used in the query 'male', 'female', or '*'
#  minimum_age - the minimum age used in the query
#  maximum_age - the maxinum age used in the query
#
def writeWeaponsDivision3ToExcelViaQuery(filename: str, division_type: str, gender: str, minimum_age: int, maximum_age: int,clean_df: pd.DataFrame):

    fullpath = os.getcwd() + reports.FileHandlingUtilities.pathDelimiter() + "Sorted" + reports.FileHandlingUtilities.pathDelimiter() + filename
    writer = pd.ExcelWriter(fullpath)
    print(time.strftime("%X") + " Generating " + fullpath)

    # Hack for 3 year olds
    if minimum_age == 4:
        minimum_age = 2

    age_query = 'Age >={0} and Age <={1}'.format(minimum_age, maximum_age)

    if gender == '*':
        gender_query = ''
    else:
        gender_query = 'and Gender == "' + gender + '"'


    assert division_type == 'Weapons' or division_type == 'Sparring' or division_type == 'Forms', "Error: Invalid division_type"
    if division_type == 'Weapons':
        division_type_query = 'Weapons.str.contains("Weapons")'
    else:
        division_type_query = 'Events.str.contains("' + division_type + '")'




    rank_query = f"Rank == '{constants.GREEN_BELT}' or Rank == '{constants.GREEN_STRIPE_BELT}'"
    rank_query = f"{rank_query} or Rank == '{constants.FIRST_DEGREE_BROWN_BELT}' or Rank == '{constants.SECOND_DEGREE_BROWN_BELT}' or Rank == '{constants.THIRD_DEGREE_BROWN_BELT}'"
    rank_query = f"{rank_query} or Rank == '{constants.FIRST_DEGREE_BLACK_BELT}' or Rank == '{constants.SECOND_DEGREE_BLACK_BELT}' or Rank == '{constants.THIRD_DEGREE_BLACK_BELT}' or Rank == '{constants.FOURTH_DEGREE_BLACK_BELT}' or Rank == '{constants.FIFTH_DEGREE_BLACK_BELT}' or Rank == '{constants.JUNIOR_BLACK_BELT}'"

    combined_query= f'{division_type_query} and {age_query} {gender_query} and ({rank_query})'
    wmk = reports.FileHandlingUtilities.newDataFrameFromQuery(clean_df=clean_df, query_string=combined_query)
    reports.ExcelFileOutput.writeFormattedExcelSheet(wmk, writer, 'Weapons Division 2')

    writer.close()
    time.sleep(constants.SLEEP_TIME)


###############################################################################
# writeWeaponsDivision4ToExcel
#  arguments:
#  filename - the filename without path to write
#  arguments:
#  filename - the filename without path to write
#  gender - gender used in the query 'male', 'female', or '*'
#  minimum_age - the minimum age used in the query
#  maximum_age - the maxinum age used in the query
#
def writeWeaponsDivision4ToExcelViaQuery(filename: str, division_type: str, gender: str, minimum_age: int, maximum_age: int,clean_df: pd.DataFrame):

    fullpath = os.getcwd() + reports.FileHandlingUtilities.pathDelimiter() + "Sorted" + reports.FileHandlingUtilities.pathDelimiter() + filename
    writer = pd.ExcelWriter(fullpath)
    print(time.strftime("%X") + " Generating " + fullpath)

    # Hack for 3 year olds
    if minimum_age == 4:
        minimum_age = 2

    age_query = 'Age >={0} and Age <={1}'.format(minimum_age, maximum_age)

    if gender == '*':
        gender_query = ''
    else:
        gender_query = 'and Gender == "' + gender + '"'


    assert division_type == 'Weapons' or division_type == 'Sparring' or division_type == 'Forms', "Error: Invalid division_type"
    if division_type == 'Weapons':
        division_type_query = 'Weapons.str.contains("Weapons")'
    else:
        division_type_query = 'Events.str.contains("' + division_type + '")'

    rank_query = f"Rank == '{constants.WHITE_BELT}' or Rank == '{constants.YELLOW_BELT}' or Rank == '{constants.ORANGE_BELT}' or Rank == '{constants.PURPLE_BELT}' or Rank == '{constants.BLUE_BELT}' or Rank == '{constants.BLUE_STRIPE_BELT}'"
    combined_query= f'{division_type_query} and {age_query} {gender_query} and ({rank_query})'
    wmk = reports.FileHandlingUtilities.newDataFrameFromQuery(clean_df=clean_df, query_string=combined_query)
    reports.ExcelFileOutput.writeFormattedExcelSheet(wmk, writer, 'Weapons Division 4')

    writer.close()
    time.sleep(constants.SLEEP_TIME)


###############################################################################
# writeWeaponsDivision5ToExcel
#  arguments:
#  filename - the filename without path to write
#  arguments:
#  filename - the filename without path to write
#  gender - gender used in the query 'male', 'female', or '*'
#  minimum_age - the minimum age used in the query
#  maximum_age - the maxinum age used in the query
#
def writeWeaponsDivision5ToExcelViaQuery(filename: str, division_type: str, gender: str, minimum_age: int, maximum_age: int,clean_df: pd.DataFrame):

    fullpath = os.getcwd() + reports.FileHandlingUtilities.pathDelimiter() + "Sorted" + reports.FileHandlingUtilities.pathDelimiter() + filename
    writer = pd.ExcelWriter(fullpath)
    print(time.strftime("%X") + " Generating " + fullpath)

    # Hack for 3 year olds
    if minimum_age == 4:
        minimum_age = 2

    age_query = 'Age >={0} and Age <={1}'.format(minimum_age, maximum_age)

    if gender == '*':
        gender_query = ''
    else:
        gender_query = 'and Gender == "' + gender + '"'


    assert division_type == 'Weapons' or division_type == 'Sparring' or division_type == 'Forms', "Error: Invalid division_type"
    if division_type == 'Weapons':
        division_type_query = 'Weapons.str.contains("Weapons")'
    else:
        division_type_query = 'Events.str.contains("' + division_type + '")'

    rank_query = f"Rank == '{constants.WHITE_BELT}' or Rank == '{constants.YELLOW_BELT}' or Rank == '{constants.ORANGE_BELT}' or Rank == '{constants.PURPLE_BELT}' or Rank == '{constants.BLUE_BELT}' or Rank == '{constants.BLUE_STRIPE_BELT}'"
    combined_query= f'{division_type_query} and {age_query} {gender_query} and ({rank_query})'
    wmk = reports.FileHandlingUtilities.newDataFrameFromQuery(clean_df=clean_df, query_string=combined_query)
    reports.ExcelFileOutput.writeFormattedExcelSheet(wmk, writer, 'Weapons Division 5')

    writer.close()
    time.sleep(constants.SLEEP_TIME)



###############################################################################
# writeWeaponsDivision6ToExcel
#  arguments:
#  filename - the filename without path to write
#  arguments:
#  filename - the filename without path to write
#  gender - gender used in the query 'male', 'female', or '*'
#  minimum_age - the minimum age used in the query
#  maximum_age - the maxinum age used in the query
#
def writeWeaponsDivision6ToExcelViaQuery(filename: str, division_type: str, gender: str, minimum_age: int, maximum_age: int,clean_df: pd.DataFrame):

    fullpath = os.getcwd() + reports.FileHandlingUtilities.pathDelimiter() + "Sorted" + reports.FileHandlingUtilities.pathDelimiter() + filename
    writer = pd.ExcelWriter(fullpath)
    print(time.strftime("%X") + " Generating " + fullpath)

    # Hack for 3 year olds
    if minimum_age == 4:
        minimum_age = 2

    age_query = 'Age >={0} and Age <={1}'.format(minimum_age, maximum_age)

    if gender == '*':
        gender_query = ''
    else:
        gender_query = 'and Gender == "' + gender + '"'


    assert division_type == 'Weapons' or division_type == 'Sparring' or division_type == 'Forms', "Error: Invalid division_type"
    if division_type == 'Weapons':
        division_type_query = 'Weapons.str.contains("Weapons")'
    else:
        division_type_query = 'Events.str.contains("' + division_type + '")'

    rank_query = f"Rank == '{constants.GREEN_BELT}' or Rank == '{constants.GREEN_STRIPE_BELT}'"
    combined_query= f'{division_type_query} and {age_query} {gender_query} and ({rank_query})'
    wmk = reports.FileHandlingUtilities.newDataFrameFromQuery(clean_df=clean_df, query_string=combined_query)
    reports.ExcelFileOutput.writeFormattedExcelSheet(wmk, writer, 'Weapons Division 5')

    writer.close()
    time.sleep(constants.SLEEP_TIME)



###############################################################################
# writeWeaponsDivision7ToExcel
#  arguments:
#  filename - the filename without path to write
#  arguments:
#  filename - the filename without path to write
#  gender - gender used in the query 'male', 'female', or '*'
#  minimum_age - the minimum age used in the query
#  maximum_age - the maxinum age used in the query
#
def writeWeaponsDivision7ToExcelViaQuery(filename: str, division_type: str, gender: str, minimum_age: int, maximum_age: int,clean_df: pd.DataFrame):

    fullpath = os.getcwd() + reports.FileHandlingUtilities.pathDelimiter() + "Sorted" + reports.FileHandlingUtilities.pathDelimiter() + filename
    writer = pd.ExcelWriter(fullpath)
    print(time.strftime("%X") + " Generating " + fullpath)

    # Hack for 3 year olds
    if minimum_age == 4:
        minimum_age = 2

    age_query = 'Age >={0} and Age <={1}'.format(minimum_age, maximum_age)

    if gender == '*':
        gender_query = ''
    else:
        gender_query = 'and Gender == "' + gender + '"'


    assert division_type == 'Weapons' or division_type == 'Sparring' or division_type == 'Forms', "Error: Invalid division_type"
    if division_type == 'Weapons':
        division_type_query = 'Weapons.str.contains("Weapons")'
    else:
        division_type_query = 'Events.str.contains("' + division_type + '")'


    rank_query = f"Rank == '{constants.THIRD_DEGREE_BROWN_BELT}' or Rank == '{constants.SECOND_DEGREE_BROWN_BELT}' or Rank == '{constants.FIRST_DEGREE_BROWN_BELT}'"
    combined_query= f'{division_type_query} and {age_query} {gender_query} and ({rank_query})'
    wmk = reports.FileHandlingUtilities.newDataFrameFromQuery(clean_df=clean_df, query_string=combined_query)
    reports.ExcelFileOutput.writeFormattedExcelSheet(wmk, writer, 'Weapons Division 7')

    writer.close()
    time.sleep(constants.SLEEP_TIME)




###############################################################################
# writeWeaponsDivision8ToExcel
#  arguments:
#  filename - the filename without path to write
#  arguments:
#  filename - the filename without path to write
#  gender - gender used in the query 'male', 'female', or '*'
#  minimum_age - the minimum age used in the query
#  maximum_age - the maxinum age used in the query
#
def writeWeaponsDivision8ToExcelViaQuery(filename: str, division_type: str, gender: str, minimum_age: int, maximum_age: int,clean_df: pd.DataFrame):

    fullpath = os.getcwd() + reports.FileHandlingUtilities.pathDelimiter() + "Sorted" + reports.FileHandlingUtilities.pathDelimiter() + filename
    writer = pd.ExcelWriter(fullpath)
    print(time.strftime("%X") + " Generating " + fullpath)

    # Hack for 3 year olds
    if minimum_age == 4:
        minimum_age = 2

    age_query = 'Age >={0} and Age <={1}'.format(minimum_age, maximum_age)

    if gender == '*':
        gender_query = ''
    else:
        gender_query = 'and Gender == "' + gender + '"'


    assert division_type == 'Weapons' or division_type == 'Sparring' or division_type == 'Forms', "Error: Invalid division_type"
    if division_type == 'Weapons':
        division_type_query = 'Weapons.str.contains("Weapons")'
    else:
        division_type_query = 'Events.str.contains("' + division_type + '")'


    rank_query = f"Rank == '{constants.FIRST_DEGREE_BLACK_BELT}' or Rank == '{constants.SECOND_DEGREE_BLACK_BELT}' or Rank == '{constants.THIRD_DEGREE_BLACK_BELT}' or Rank == '{constants.FOURTH_DEGREE_BLACK_BELT}' or Rank == '{constants.FIFTH_DEGREE_BLACK_BELT}' or Rank == '{constants.JUNIOR_BLACK_BELT}'"
    combined_query= f'{division_type_query} and {age_query} {gender_query} and ({rank_query})'
    wmk = reports.FileHandlingUtilities.newDataFrameFromQuery(clean_df=clean_df, query_string=combined_query)
    reports.ExcelFileOutput.writeFormattedExcelSheet(wmk, writer, 'Weapons Division 8')

    writer.close()
    time.sleep(constants.SLEEP_TIME)


###############################################################################
# writeWeaponsDivision8ToExcel
#  arguments:
#  filename - the filename without path to write
#  arguments:
#  filename - the filename without path to write
#  gender - gender used in the query 'male', 'female', or '*'
#  minimum_age - the minimum age used in the query
#  maximum_age - the maxinum age used in the query
#
def writeWeaponsDivision9ToExcelViaQuery(filename: str, division_type: str, gender: str, minimum_age: int, maximum_age: int,clean_df: pd.DataFrame):

    fullpath = os.getcwd() + reports.FileHandlingUtilities.pathDelimiter() + "Sorted" + reports.FileHandlingUtilities.pathDelimiter() + filename
    writer = pd.ExcelWriter(fullpath)
    print(time.strftime("%X") + " Generating " + fullpath)

    # Hack for 3 year olds
    if minimum_age == 4:
        minimum_age = 2

    age_query = 'Age >={0} and Age <={1}'.format(minimum_age, maximum_age)

    if gender == '*':
        gender_query = ''
    else:
        gender_query = 'and Gender == "' + gender + '"'


    assert division_type == 'Weapons' or division_type == 'Sparring' or division_type == 'Forms', "Error: Invalid division_type"
    if division_type == 'Weapons':
        division_type_query = 'Weapons.str.contains("Weapons")'
    else:
        division_type_query = 'Events.str.contains("' + division_type + '")'


    rank_query = f"Rank == '{constants.FIRST_DEGREE_BLACK_BELT}' or Rank == '{constants.SECOND_DEGREE_BLACK_BELT}' or Rank == '{constants.THIRD_DEGREE_BLACK_BELT}' or Rank == '{constants.FOURTH_DEGREE_BLACK_BELT}' or Rank == '{constants.FIFTH_DEGREE_BLACK_BELT}' or Rank == '{constants.JUNIOR_BLACK_BELT}'"
    combined_query= f'{division_type_query} and {age_query} {gender_query} and ({rank_query})'
    wmk = reports.FileHandlingUtilities.newDataFrameFromQuery(clean_df=clean_df, query_string=combined_query)
    reports.ExcelFileOutput.writeFormattedExcelSheet(wmk, writer, 'Weapons Division 8')

    writer.close()
    time.sleep(constants.SLEEP_TIME)
