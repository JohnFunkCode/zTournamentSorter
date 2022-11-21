# V 11/20/2022
# There are 6 patterns in the Denver Tournament Guide
#
# Pattern1 - ranking based on size of the division it would be use for: 
#  White, Yellow, Orange
#  Purple, Blue, Blue Stripe
#  Green, Green Stripe, Brown
#  Black
#
# Pattern2 - ranking based on size of the division it would be use for:
#    White, Yellow & Orange
#    Purple, Blue & Blue Stripe
#    Green, Green Stripe,
#    Brown
#    Black
#
# Pattern3 - ranking based on size of the division it would be use for:
#  White, Yellow
#  Orange
#  Purple
#  Blue, Blue Stripe
#  Green, Green Stripe, Brown
#
# Pattern4 - ranking based on size of the division it would be use for:
#    White
#    Yellow
#    Orange
#    Purple, Blue, Blue Stripe
#    Green, Green Stripe
#
# Pattern5 - ranking based on size of the division it would be use for:
#  White
#  Yellow
#  Orange
#  Purple
#  Blue, Blue Stripe
#  Green, Green Stripe, Brown
#
#
# Pattern6 - ranking based on size of the division it would be use for:
#  White, Yellow
#  Orange
#  Purple
#  Blue, Blue Stripe
#  Green, Green Stripe
#  Brown
#  Black

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
import domain_model.constants as constants



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


#Experimental
def newDataFrameFromQuery(query_string: str):
    #query_string='Rank == "White" and Rank == "Yellow" and Age >= 4 and Age =< 6'
    newdf = clean_df[["Registrant_ID","First_Name", "Last_Name", "Gender", "Dojo", "Age", "Rank", "Feet", "Inches", "Height", "Weight", "BMI",
    "Events", "Weapons"]].query(query_string).sort_values("Age").sort_values("BMI")

    ## update the hitcount every time we touch someone
    for index, row in newdf.iterrows():
        name = row['First_Name'] + " " + row['Last_Name']
        id= row['Registrant_ID']
        hc=clean_df.at[index,'hitcount']
        newhc = hc + 1
        #print(f'{id}:{name} has a row count of {newhc}')
        clean_df.at[index,'hitcount']=newhc
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
def writePattern1ToExcelViaQuery(filename: str, division_type: str, gender: str, minimum_age: int, maximum_age: int):
    fullpath = os.getcwd() + pathDelimiter() + "Sorted" + pathDelimiter() + filename
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
    wmk = newDataFrameFromQuery(combined_query)
    writeFormattedExcelSheet(wmk, writer, 'White, Yellow, Orange')

    rank_query = f"Rank == '{constants.PURPLE_BELT}' or Rank == '{constants.BLUE_BELT}' or Rank == '{constants.BLUE_STRIPE_BELT}'"
    combined_query= f'{division_type_query} and {age_query} {gender_query} and ({rank_query})'
    wmk = newDataFrameFromQuery(combined_query)
    writeFormattedExcelSheet(wmk, writer, 'Purple, Blue, Blue Stripe')

    rank_query = f"Rank == '{constants.GREEN_BELT}' or Rank == '{constants.GREEN_STRIPE_BELT}' or Rank == '{constants.FIRST_DEGREE_BROWN_BELT}' or Rank == '{constants.SECOND_DEGREE_BROWN_BELT}' or Rank == '{constants.THIRD_DEGREE_BROWN_BELT}'"
    combined_query= f'{division_type_query} and {age_query} {gender_query} and ({rank_query})'
    wmk = newDataFrameFromQuery(combined_query)
    writeFormattedExcelSheet(wmk, writer, 'Green, Green Stripe, Brown')

    rank_query = f"Rank == '{constants.FIRST_DEGREE_BLACK_BELT}' or Rank == '{constants.SECOND_DEGREE_BLACK_BELT}' or Rank == '{constants.THIRD_DEGREE_BLACK_BELT}' or Rank == '{constants.FOURTH_DEGREE_BLACK_BELT}' or Rank == '{constants.FIFTH_DEGREE_BLACK_BELT}' or Rank == '{constants.JUNIOR_BLACK_BELT}'"
    combined_query= f'{division_type_query} and {age_query} {gender_query} and ({rank_query})'
    wmk = newDataFrameFromQuery(combined_query)
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
def writePattern2ToExcelViaQuery(filename: str, division_type: str, gender: str, minimum_age: int, maximum_age: int):
    fullpath = os.getcwd() + pathDelimiter() + "Sorted" + pathDelimiter() + filename
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
    wmk = newDataFrameFromQuery(combined_query)
    writeFormattedExcelSheet(wmk, writer, 'White, Yellow, Orange')

    rank_query = f"Rank == '{constants.PURPLE_BELT}' or Rank == '{constants.BLUE_BELT}' or Rank == '{constants.BLUE_STRIPE_BELT}'"
    combined_query= f'{division_type_query} and {age_query} {gender_query} and ({rank_query})'
    wmk = newDataFrameFromQuery(combined_query)
    writeFormattedExcelSheet(wmk, writer, 'Purple, Blue, Blue Stripe')

    rank_query = f"Rank == '{constants.GREEN_BELT}' or Rank == '{constants.GREEN_STRIPE_BELT}'"
    combined_query= f'{division_type_query} and {age_query} {gender_query} and ({rank_query})'
    wmk = newDataFrameFromQuery(combined_query)
    writeFormattedExcelSheet(wmk, writer, 'Green, Green Stripe')


    rank_query = f"Rank == '{constants.FIRST_DEGREE_BROWN_BELT}' or Rank == '{constants.SECOND_DEGREE_BROWN_BELT}' or Rank == '{constants.THIRD_DEGREE_BROWN_BELT}'"
    combined_query= f'{division_type_query} and {age_query} {gender_query} and ({rank_query})'
    wmk = newDataFrameFromQuery(combined_query)
    writeFormattedExcelSheet(wmk, writer, 'Brown')

    rank_query = f"Rank == '{constants.FIRST_DEGREE_BLACK_BELT}' or Rank == '{constants.SECOND_DEGREE_BLACK_BELT}' or Rank == '{constants.THIRD_DEGREE_BLACK_BELT}' or Rank == '{constants.FOURTH_DEGREE_BLACK_BELT}' or Rank == '{constants.FIFTH_DEGREE_BLACK_BELT}' or Rank == '{constants.JUNIOR_BLACK_BELT}'"
    combined_query= f'{division_type_query} and {age_query} {gender_query} and ({rank_query})'
    wmk = newDataFrameFromQuery(combined_query)
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
def writePattern3ToExcelViaQuery(filename: str, division_type: str, gender: str, minimum_age: int, maximum_age: int):
    fullpath = os.getcwd() + pathDelimiter() + "Sorted" + pathDelimiter() + filename
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
    wmk = newDataFrameFromQuery(combined_query)
    writeFormattedExcelSheet(wmk, writer, 'White, Yellow')

    rank_query = f"Rank == '{constants.ORANGE_BELT}'"
    combined_query= f'{division_type_query} and {age_query} {gender_query} and ({rank_query})'
    wmk = newDataFrameFromQuery(combined_query)
    writeFormattedExcelSheet(wmk, writer, 'Orange')

    rank_query = f"Rank == '{constants.PURPLE_BELT}'"
    combined_query= f'{division_type_query} and {age_query} {gender_query} and ({rank_query})'
    wmk = newDataFrameFromQuery(combined_query)
    writeFormattedExcelSheet(wmk, writer, 'Purple')


    rank_query = f"Rank == '{constants.BLUE_BELT}' or Rank == '{constants.BLUE_STRIPE_BELT}'"
    combined_query= f'{division_type_query} and {age_query} {gender_query} and ({rank_query})'
    wmk = newDataFrameFromQuery(combined_query)
    writeFormattedExcelSheet(wmk, writer, 'Blue, Blue Stripe')


    rank_query = f"Rank == '{constants.GREEN_BELT}' or Rank == '{constants.GREEN_STRIPE_BELT}' or Rank == '{constants.FIRST_DEGREE_BROWN_BELT}' or Rank == '{constants.SECOND_DEGREE_BROWN_BELT}' or Rank == '{constants.THIRD_DEGREE_BROWN_BELT}'"
    combined_query= f'{division_type_query} and {age_query} {gender_query} and ({rank_query})'
    wmk = newDataFrameFromQuery(combined_query)
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
def writePattern4ToExcelViaQuery(filename: str, division_type: str, gender: str, minimum_age: int, maximum_age: int):
    fullpath = os.getcwd() + pathDelimiter() + "Sorted" + pathDelimiter() + filename
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

    wmk = newDataFrameFromQuery(combined_query)
    writeFormattedExcelSheet(wmk, writer, 'White')

    rank_query = f"Rank == '{constants.YELLOW_BELT}'"
    combined_query= f'{division_type_query} and {age_query} {gender_query} and ({rank_query})'
    wmk = newDataFrameFromQuery(combined_query)
    writeFormattedExcelSheet(wmk, writer, 'Yellow')

    rank_query = f"Rank == '{constants.ORANGE_BELT}'"
    combined_query= f'{division_type_query} and {age_query} {gender_query} and ({rank_query})'
    wmk = newDataFrameFromQuery(combined_query)
    writeFormattedExcelSheet(wmk, writer, 'Orange')

    rank_query = f"Rank == '{constants.PURPLE_BELT}' or Rank == '{constants.BLUE_BELT}' or Rank == '{constants.BLUE_STRIPE_BELT}'"
    combined_query= f'{division_type_query} and {age_query} {gender_query} and ({rank_query})'
    wmk = newDataFrameFromQuery(combined_query)
    writeFormattedExcelSheet(wmk, writer, 'Purple, Blue, Blue Stripe')


    rank_query = f"Rank == '{constants.GREEN_BELT}' or Rank == '{constants.GREEN_STRIPE_BELT}' or Rank == '{constants.FIRST_DEGREE_BROWN_BELT}' or Rank == '{constants.SECOND_DEGREE_BROWN_BELT}' or Rank == '{constants.THIRD_DEGREE_BROWN_BELT}'"
    combined_query= f'{division_type_query} and {age_query} {gender_query} and ({rank_query})'
    wmk = newDataFrameFromQuery(combined_query)
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
def writePattern5ToExcelViaQuery(filename: str, division_type: str, gender: str, minimum_age: int, maximum_age: int):
    fullpath = os.getcwd() + pathDelimiter() + "Sorted" + pathDelimiter() + filename
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

    wmk = newDataFrameFromQuery(combined_query)
    writeFormattedExcelSheet(wmk, writer, 'White')

    rank_query = f"Rank == '{constants.YELLOW_BELT}'"
    combined_query= f'{division_type_query} and {age_query} {gender_query} and ({rank_query})'
    wmk = newDataFrameFromQuery(combined_query)
    writeFormattedExcelSheet(wmk, writer, 'Yellow')

    rank_query = f"Rank == '{constants.ORANGE_BELT}'"
    combined_query= f'{division_type_query} and {age_query} {gender_query} and ({rank_query})'
    wmk = newDataFrameFromQuery(combined_query)
    writeFormattedExcelSheet(wmk, writer, 'Orange')

    rank_query = f"Rank == '{constants.PURPLE_BELT}'"
    combined_query= f'{division_type_query} and {age_query} {gender_query} and ({rank_query})'
    wmk = newDataFrameFromQuery(combined_query)
    writeFormattedExcelSheet(wmk, writer, 'Purple')


    rank_query = f"Rank == '{constants.BLUE_BELT}' or Rank == '{constants.BLUE_STRIPE_BELT}'"
    combined_query= f'{division_type_query} and {age_query} {gender_query} and ({rank_query})'
    wmk = newDataFrameFromQuery(combined_query)
    writeFormattedExcelSheet(wmk, writer, 'Blue, Blue Stripe')


    rank_query = f"Rank == '{constants.GREEN_BELT}' or Rank == '{constants.GREEN_STRIPE_BELT}' or Rank == '{constants.FIRST_DEGREE_BROWN_BELT}' or Rank == '{constants.SECOND_DEGREE_BROWN_BELT}' or Rank == '{constants.THIRD_DEGREE_BROWN_BELT}'"
    combined_query= f'{division_type_query} and {age_query} {gender_query} and ({rank_query})'
    wmk = newDataFrameFromQuery(combined_query)
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
def writePattern6ToExcelViaQuery(filename: str, division_type: str, gender: str, minimum_age: int, maximum_age: int):
    fullpath = os.getcwd() + pathDelimiter() + "Sorted" + pathDelimiter() + filename
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
    wmk = newDataFrameFromQuery(combined_query)
    writeFormattedExcelSheet(wmk, writer, 'White, Yellow')

    rank_query = f"Rank == '{constants.ORANGE_BELT}'"
    combined_query= f'{division_type_query} and {age_query} {gender_query} and ({rank_query})'
    wmk = newDataFrameFromQuery(combined_query)
    writeFormattedExcelSheet(wmk, writer, 'Orange')

    rank_query = f"Rank == '{constants.PURPLE_BELT}'"
    combined_query= f'{division_type_query} and {age_query} {gender_query} and ({rank_query})'
    wmk = newDataFrameFromQuery(combined_query)
    writeFormattedExcelSheet(wmk, writer, 'Purple')


    rank_query = f"Rank == '{constants.BLUE_BELT}' or Rank == '{constants.BLUE_STRIPE_BELT}'"
    combined_query= f'{division_type_query} and {age_query} {gender_query} and ({rank_query})'
    wmk = newDataFrameFromQuery(combined_query)
    writeFormattedExcelSheet(wmk, writer, 'Blue, Blue Stripe')


    rank_query = f"Rank == '{constants.GREEN_BELT}' or Rank == '{constants.GREEN_STRIPE_BELT}'"
    combined_query= f'{division_type_query} and {age_query} {gender_query} and ({rank_query})'
    wmk = newDataFrameFromQuery(combined_query)
    writeFormattedExcelSheet(wmk, writer, 'Green, Green Stripe')

    rank_query = f"Rank == '{constants.FIRST_DEGREE_BROWN_BELT}' or Rank == '{constants.SECOND_DEGREE_BROWN_BELT}' or Rank == '{constants.THIRD_DEGREE_BROWN_BELT}'"
    combined_query= f'{division_type_query} and {age_query} {gender_query} and ({rank_query})'
    wmk = newDataFrameFromQuery(combined_query)
    writeFormattedExcelSheet(wmk, writer, 'Brown')

    rank_query = f"Rank == '{constants.FIRST_DEGREE_BLACK_BELT}' or Rank == '{constants.SECOND_DEGREE_BLACK_BELT}' or Rank == '{constants.THIRD_DEGREE_BLACK_BELT}' or Rank == '{constants.FOURTH_DEGREE_BLACK_BELT}' or Rank == '{constants.FIFTH_DEGREE_BLACK_BELT}' or Rank == '{constants.JUNIOR_BLACK_BELT}'"
    combined_query= f'{division_type_query} and {age_query} {gender_query} and ({rank_query})'
    wmk = newDataFrameFromQuery(combined_query)
    writeFormattedExcelSheet(wmk, writer, 'Black')


    writer.close()
    time.sleep(constants.SLEEP_TIME)




###############################################################################
# writeSingleKataScoreSheetandDivisionReport
#  Provides a convenience wrapper that writes to both the division detail report and the kata score sheet in one line
#  This prevents a lot of duplication
def writeSingleKataScoreSheetandDivisionReport(event_time: str, division_name: str, gender: str, rank_label: str, minimum_age: int,maximum_age: int, rings: list, ranks: list,clean_df: pd.DataFrame):
    divison_detail_report_pdf.writeSingleDivisionDetailReport(event_time=event_time, division_name=division_name,division_type="Forms", gender=gender,rank_label=rank_label, minimum_age=minimum_age,maximum_age=maximum_age, rings=rings,ranks=ranks,clean_df=clean_df)
    kata_score_sheet.writeSingleKataScoreSheet(event_time=event_time, division_name=division_name,division_type="Forms", gender=gender,rank_label=rank_label, minimum_age=minimum_age, maximum_age=maximum_age, rings=rings,ranks=ranks, clean_df=clean_df)

###############################################################################
# write_single_sparring_treeShim
#  Provides a convenience wrapper that writes to both the division detail report and the sparring tree in one line
#  This prevents a lot of duplication
def writeSingleSparringTreeandDivisionReport(event_time: str, division_name, gender: str, rank_label: str, minimum_age: int, maximum_age: int, rings: list, ranks: list, clean_df : pd.DataFrame ):
    divison_detail_report_pdf.writeSingleDivisionDetailReport(event_time=event_time, division_name=division_name,division_type="Sparring", gender=gender,rank_label=rank_label, minimum_age=minimum_age,maximum_age=maximum_age, rings=rings,ranks=ranks,clean_df=clean_df)
    sparing_tree_pdf.write_single_sparring_tree(event_time=event_time, division_name=division_name, gender=gender,rank_label=rank_label, minimum_age=minimum_age, maximum_age=maximum_age, rings=rings,ranks=ranks, clean_df=clean_df)

###############################################################################
# writeSingleKataScoreSheetandDivisionReport
#  Provides a convenience wrapper that writes to both the division detail report and the kata score sheet in one line
#  This prevents a lot of duplication
def writeWeaponsDivisionToSingleKataScoreSheetandDivisionReport(event_time: str, division_name: str, gender: str, rank_label: str, minimum_age: int,maximum_age: int, rings: list, ranks: list,clean_df: pd.DataFrame):
    divison_detail_report_pdf.writeSingleDivisionDetailReport(event_time=event_time, division_name=division_name,division_type="Weapons", gender=gender,rank_label=rank_label, minimum_age=minimum_age,maximum_age=maximum_age, rings=rings,ranks=ranks,clean_df=clean_df)
    kata_score_sheet.writeSingleKataScoreSheet(               event_time=event_time, division_name=division_name,division_type="Weapons", gender=gender,rank_label=rank_label, minimum_age=minimum_age, maximum_age=maximum_age, rings=rings,ranks=ranks, clean_df=clean_df)


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
def writeWeaponsDivision1ToExcelViaQuery(filename: str, division_type: str, gender: str, minimum_age: int, maximum_age: int):

    fullpath = os.getcwd() + pathDelimiter() + "Sorted" + pathDelimiter() + filename
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
    wmk = newDataFrameFromQuery(combined_query)
    writeFormattedExcelSheet(wmk, writer, 'Weapons Division 1')

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
def writeWeaponsDivision2ToExcelViaQuery(filename: str, division_type: str, gender: str, minimum_age: int, maximum_age: int):

    fullpath = os.getcwd() + pathDelimiter() + "Sorted" + pathDelimiter() + filename
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
    wmk = newDataFrameFromQuery(combined_query)
    writeFormattedExcelSheet(wmk, writer, 'Weapons Division 2')

    writer.close()
    time.sleep(constants.SLEEP_TIME)


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
#  arguments:
#  filename - the filename without path to write
#  gender - gender used in the query 'male', 'female', or '*'
#  minimum_age - the minimum age used in the query
#  maximum_age - the maxinum age used in the query
#
def writeWeaponsDivision3ToExcelViaQuery(filename: str, division_type: str, gender: str, minimum_age: int, maximum_age: int):

    fullpath = os.getcwd() + pathDelimiter() + "Sorted" + pathDelimiter() + filename
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
    wmk = newDataFrameFromQuery(combined_query)
    writeFormattedExcelSheet(wmk, writer, 'Weapons Division 2')

    writer.close()
    time.sleep(constants.SLEEP_TIME)


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
#  arguments:
#  filename - the filename without path to write
#  gender - gender used in the query 'male', 'female', or '*'
#  minimum_age - the minimum age used in the query
#  maximum_age - the maxinum age used in the query
#
def writeWeaponsDivision4ToExcelViaQuery(filename: str, division_type: str, gender: str, minimum_age: int, maximum_age: int):

    fullpath = os.getcwd() + pathDelimiter() + "Sorted" + pathDelimiter() + filename
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
    wmk = newDataFrameFromQuery(combined_query)
    writeFormattedExcelSheet(wmk, writer, 'Weapons Division 4')

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
def writeWeaponsDivision5ToExcelViaQuery(filename: str, division_type: str, gender: str, minimum_age: int, maximum_age: int):

    fullpath = os.getcwd() + pathDelimiter() + "Sorted" + pathDelimiter() + filename
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
    wmk = newDataFrameFromQuery(combined_query)
    writeFormattedExcelSheet(wmk, writer, 'Weapons Division 5')

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
def writeWeaponsDivision6ToExcelViaQuery(filename: str, division_type: str, gender: str, minimum_age: int, maximum_age: int):

    fullpath = os.getcwd() + pathDelimiter() + "Sorted" + pathDelimiter() + filename
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
    wmk = newDataFrameFromQuery(combined_query)
    writeFormattedExcelSheet(wmk, writer, 'Weapons Division 5')

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
def writeWeaponsDivision7ToExcelViaQuery(filename: str, division_type: str, gender: str, minimum_age: int, maximum_age: int):

    fullpath = os.getcwd() + pathDelimiter() + "Sorted" + pathDelimiter() + filename
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
    wmk = newDataFrameFromQuery(combined_query)
    writeFormattedExcelSheet(wmk, writer, 'Weapons Division 7')

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
def writeWeaponsDivision8ToExcelViaQuery(filename: str, division_type: str, gender: str, minimum_age: int, maximum_age: int):

    fullpath = os.getcwd() + pathDelimiter() + "Sorted" + pathDelimiter() + filename
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
    wmk = newDataFrameFromQuery(combined_query)
    writeFormattedExcelSheet(wmk, writer, 'Weapons Division 8')

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
def writeWeaponsDivision9ToExcelViaQuery(filename: str, division_type: str, gender: str, minimum_age: int, maximum_age: int):

    fullpath = os.getcwd() + pathDelimiter() + "Sorted" + pathDelimiter() + filename
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
    wmk = newDataFrameFromQuery(combined_query)
    writeFormattedExcelSheet(wmk, writer, 'Weapons Division 8')

    writer.close()
    time.sleep(constants.SLEEP_TIME)


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

### Special Handling for files with less than 30 competitors- Added for Fall 2022 Tournament
if clean_df.shape[0] < 30:
    print("\u001b[31m*** Warning: Special Handling!  Printing Just One Kata Sheet and One Sparring Tree with the small data file provided!\u001b[0m")
    #divison_detail_report_pdf.writeSingleDivisionDetailReport(event_time="", division_name="",division_type="Forms", gender="*", rank_label="",minimum_age=1, maximum_age=constants.AGELESS, rings=[1],ranks=[constants.WHITE_BELT,constants.YELLOW_BELT,constants.ORANGE_BELT,constants.PURPLE_BELT,constants.BLUE_BELT,constants.BLUE_STRIPE_BELT,constants.GREEN_BELT,constants.GREEN_STRIPE_BELT,constants.THIRD_DEGREE_BROWN_BELT,constants.SECOND_DEGREE_BROWN_BELT,constants.FIRST_DEGREE_BROWN_BELT,constants.FIRST_DEGREE_BLACK_BELT,constants.SECOND_DEGREE_BLACK_BELT, constants.THIRD_DEGREE_BLACK_BELT,constants.FOURTH_DEGREE_BLACK_BELT,constants.FIFTH_DEGREE_BLACK_BELT,constants.JUNIOR_BLACK_BELT], clean_df=clean_df)
    writeSingleKataScoreSheetandDivisionReport(               event_time="", division_name="",                       gender="*", rank_label="",minimum_age=1, maximum_age=constants.AGELESS, rings=[''],ranks=[constants.WHITE_BELT,constants.YELLOW_BELT,constants.ORANGE_BELT,constants.PURPLE_BELT,constants.BLUE_BELT,constants.BLUE_STRIPE_BELT,constants.GREEN_BELT,constants.GREEN_STRIPE_BELT,constants.THIRD_DEGREE_BROWN_BELT,constants.SECOND_DEGREE_BROWN_BELT,constants.FIRST_DEGREE_BROWN_BELT,constants.FIRST_DEGREE_BLACK_BELT,constants.SECOND_DEGREE_BLACK_BELT, constants.THIRD_DEGREE_BLACK_BELT,constants.FOURTH_DEGREE_BLACK_BELT,constants.FIFTH_DEGREE_BLACK_BELT,constants.JUNIOR_BLACK_BELT], clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(              event_time="", division_name="",                       gender="*", rank_label="",minimum_age=1, maximum_age=constants.AGELESS, rings=[''],ranks=[constants.WHITE_BELT,constants.YELLOW_BELT,constants.ORANGE_BELT,constants.PURPLE_BELT,constants.BLUE_BELT,constants.BLUE_STRIPE_BELT,constants.GREEN_BELT,constants.GREEN_STRIPE_BELT,constants.THIRD_DEGREE_BROWN_BELT,constants.SECOND_DEGREE_BROWN_BELT,constants.FIRST_DEGREE_BROWN_BELT,constants.FIRST_DEGREE_BLACK_BELT,constants.SECOND_DEGREE_BLACK_BELT, constants.THIRD_DEGREE_BLACK_BELT,constants.FOURTH_DEGREE_BLACK_BELT,constants.FIFTH_DEGREE_BLACK_BELT,constants.JUNIOR_BLACK_BELT], clean_df=clean_df)
else:


    ### 9:00AM Events

    ###############################################################################
    # Kids Kata  - 4-6 year olds
    #
    writePattern4ToExcelViaQuery(filename="KidsKata.xlsx", division_type='Forms', gender="*",minimum_age=4, maximum_age=6)

    writeSingleKataScoreSheetandDivisionReport(event_time="9:00am",division_name="Kids Kata",gender="*",rank_label="White",                     minimum_age=4, maximum_age=6, rings=[1],  ranks=[constants.WHITE_BELT], clean_df=clean_df)
    writeSingleKataScoreSheetandDivisionReport(event_time="9:00am",division_name="Kids Kata",gender="*",rank_label="Yellow",                    minimum_age=4, maximum_age=6, rings=[2,3],ranks=[constants.YELLOW_BELT], clean_df=clean_df)
    writeSingleKataScoreSheetandDivisionReport(event_time="9:00am",division_name="Kids Kata",gender="*",rank_label="Orange",                    minimum_age=4, maximum_age=6, rings=[4,5],ranks=[constants.ORANGE_BELT], clean_df=clean_df)
    writeSingleKataScoreSheetandDivisionReport(event_time="9:00am",division_name="Kids Kata",gender="*",rank_label="Purple, Blue, Blue/Stripe", minimum_age=4, maximum_age=6, rings=[6],  ranks=[constants.PURPLE_BELT,constants.BLUE_BELT,constants.BLUE_STRIPE_BELT], clean_df=clean_df)
    writeSingleKataScoreSheetandDivisionReport(event_time="9:00am",division_name="Kids Kata",gender="*",rank_label="Green, Green/Stripe, Brown",minimum_age=4, maximum_age=6, rings=[7],  ranks=[constants.GREEN_BELT,constants.GREEN_STRIPE_BELT,constants.THIRD_DEGREE_BROWN_BELT,constants.SECOND_DEGREE_BROWN_BELT,constants.FIRST_DEGREE_BROWN_BELT], clean_df=clean_df)


    ###############################################################################
    # Youth Kata  - 7-8 year olds
    #
    writePattern5ToExcelViaQuery(filename="YouthKata.xlsx", division_type='Forms', gender="*",minimum_age=7, maximum_age=8)

    writeSingleKataScoreSheetandDivisionReport(event_time="9:00am",division_name="Youth Kata",gender="*",rank_label="White",                     minimum_age=7, maximum_age=8, rings=[8],    ranks=[constants.WHITE_BELT], clean_df=clean_df)
    writeSingleKataScoreSheetandDivisionReport(event_time="9:00am",division_name="Youth Kata",gender="*",rank_label="Yellow",                    minimum_age=7, maximum_age=8, rings=[9],    ranks=[constants.YELLOW_BELT], clean_df=clean_df)
    writeSingleKataScoreSheetandDivisionReport(event_time="9:00am",division_name="Youth Kata",gender="*",rank_label="Orange",                    minimum_age=7, maximum_age=8, rings=[10,11],ranks=[constants.ORANGE_BELT], clean_df=clean_df)
    writeSingleKataScoreSheetandDivisionReport(event_time="9:00am",division_name="Youth Kata",gender="*",rank_label="Purple",                    minimum_age=7, maximum_age=8, rings=[12,13],ranks=[constants.PURPLE_BELT], clean_df=clean_df)
    writeSingleKataScoreSheetandDivisionReport(event_time="9:00am",division_name="Youth Kata",gender="*",rank_label="Blue, Blue/Stripe",         minimum_age=7, maximum_age=8, rings=[14,15],ranks=[constants.BLUE_BELT,constants.BLUE_STRIPE_BELT], clean_df=clean_df)
    writeSingleKataScoreSheetandDivisionReport(event_time="9:00am",division_name="Youth Kata",gender="*",rank_label="Green, Green/Stripe, Brown",minimum_age=7, maximum_age=8, rings=[16],   ranks=[constants.GREEN_BELT,constants.GREEN_STRIPE_BELT,constants.THIRD_DEGREE_BROWN_BELT,constants.SECOND_DEGREE_BROWN_BELT,constants.FIRST_DEGREE_BROWN_BELT], clean_df=clean_df)

    ### 9:45 Events

    ###############################################################################
    # Kids Sparring Spreadsheet - 4-6 year olds
    #
    writePattern4ToExcelViaQuery(filename="KidsSparring.xlsx", division_type='Sparring', gender="*",minimum_age=4, maximum_age=6)

    writeSingleSparringTreeandDivisionReport(event_time="9:45am",division_name="Kids Sparring",gender="*", rank_label="White",                     minimum_age=4, maximum_age=6, rings=[1],     ranks=[constants.WHITE_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="9:45am",division_name="Kids Sparring",gender="*", rank_label="Yellow",                    minimum_age=4, maximum_age=6, rings=[2,3],  ranks=[constants.YELLOW_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="9:45am",division_name="Kids Sparring",gender="*", rank_label="Orange",                    minimum_age=4, maximum_age=6, rings=[4,5],  ranks=[constants.ORANGE_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="9:45am",division_name="Kids Sparring",gender="*", rank_label="Purple, Blue, Blue/Stripe", minimum_age=4, maximum_age=6, rings=[6],  ranks=[constants.PURPLE_BELT,constants.BLUE_BELT,constants.BLUE_STRIPE_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="9:45am",division_name="Kids Sparring",gender="*", rank_label="Green, Green/Stripe, Brown", minimum_age=4, maximum_age=6, rings=[7],  ranks=[constants.GREEN_BELT,constants.GREEN_STRIPE_BELT,constants.THIRD_DEGREE_BROWN_BELT,constants.SECOND_DEGREE_BROWN_BELT,constants.FIRST_DEGREE_BROWN_BELT],clean_df=clean_df)


    ###############################################################################
    # Boy's & Girl's Kata  - 9-11 year olds
    #
    writePattern6ToExcelViaQuery(filename="BoysGirlsKata.xlsx", division_type='Forms', gender="*",minimum_age=9, maximum_age=11)

    writeSingleKataScoreSheetandDivisionReport(event_time="9:45am",division_name="Boy's & Girl's Kata",gender="*", rank_label="White, Yellow",         minimum_age=9, maximum_age=11, rings=[8],     ranks=[constants.WHITE_BELT,constants.YELLOW_BELT], clean_df=clean_df)
    writeSingleKataScoreSheetandDivisionReport(event_time="9:45am",division_name="Boy's & Girl's Kata",gender="*", rank_label="Orange",                minimum_age=9, maximum_age=11, rings=[9],     ranks=[constants.ORANGE_BELT], clean_df=clean_df)
    writeSingleKataScoreSheetandDivisionReport(event_time="9:45am",division_name="Boy's & Girl's Kata",gender="*", rank_label="Purple",                minimum_age=9, maximum_age=11, rings=[10,11], ranks=[constants.PURPLE_BELT], clean_df=clean_df)
    writeSingleKataScoreSheetandDivisionReport(event_time="9:45am",division_name="Boy's & Girl's Kata",gender="*", rank_label="Blue, Blue w/Stripe",   minimum_age=9, maximum_age=11, rings=[12,13], ranks=[constants.BLUE_BELT,constants.BLUE_STRIPE_BELT], clean_df=clean_df)
    writeSingleKataScoreSheetandDivisionReport(event_time="9:45am",division_name="Boy's & Girl's Kata",gender="*", rank_label="Green, Green w/Stripe", minimum_age=9, maximum_age=11, rings=[15],    ranks=[constants.GREEN_BELT,constants.GREEN_STRIPE_BELT], clean_df=clean_df)
    writeSingleKataScoreSheetandDivisionReport(event_time="9:45am",division_name="Boy's & Girl's Kata",gender="*", rank_label="Brown",                 minimum_age=9, maximum_age=11, rings=[16],    ranks=[constants.THIRD_DEGREE_BROWN_BELT,constants.SECOND_DEGREE_BROWN_BELT,constants.FIRST_DEGREE_BROWN_BELT], clean_df=clean_df)
    writeSingleKataScoreSheetandDivisionReport(event_time="9:45am",division_name="Boy's & Girl's Kata",gender="*", rank_label="Jr. Black",             minimum_age=9, maximum_age=11, rings=[17],    ranks=[constants.FIRST_DEGREE_BLACK_BELT,constants.SECOND_DEGREE_BLACK_BELT, constants.THIRD_DEGREE_BLACK_BELT,constants.FOURTH_DEGREE_BLACK_BELT,constants.FIFTH_DEGREE_BLACK_BELT,constants.JUNIOR_BLACK_BELT], clean_df=clean_df)

    ### 10:30 Events

    ###############################################################################
    # Youth Girl's Sparring  - 7-8 year olds
    #
    writePattern3ToExcelViaQuery(filename="YouthGirlSparring.xlsx", division_type='Forms', gender="Female",minimum_age=7, maximum_age=8)

    writeSingleSparringTreeandDivisionReport(event_time="10:30am",division_name="Youth Girl's Sparring",gender="Female", rank_label="White, Yellow",             minimum_age=7, maximum_age=8, rings=[1], ranks=[constants.WHITE_BELT,constants.YELLOW_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="10:30am",division_name="Youth Girl's Sparring",gender="Female", rank_label="Orange",                    minimum_age=7, maximum_age=8, rings=[2], ranks=[constants.ORANGE_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="10:30am",division_name="Youth Girl's Sparring",gender="Female", rank_label="Purple",                    minimum_age=7, maximum_age=8, rings=[3], ranks=[constants.PURPLE_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="10:30am",division_name="Youth Girl's Sparring",gender="Female", rank_label="Blue, Blue/Stripe",         minimum_age=7, maximum_age=8, rings=[4], ranks=[constants.BLUE_BELT,constants.BLUE_STRIPE_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="10:30am",division_name="Youth Girl's Sparring",gender="Female", rank_label="Green, Green/Stripe, Brown",minimum_age=7, maximum_age=8, rings=[5], ranks=[constants.GREEN_BELT,constants.GREEN_STRIPE_BELT,constants.THIRD_DEGREE_BROWN_BELT,constants.SECOND_DEGREE_BROWN_BELT,constants.FIRST_DEGREE_BROWN_BELT],clean_df=clean_df)

    ###############################################################################
    # Youth Boy's Sparring - 7-8 year olds
    #
    writePattern3ToExcelViaQuery(filename="YouthBoysSparring.xlsx", division_type='Forms', gender="Male",minimum_age=7, maximum_age=8)

    writeSingleSparringTreeandDivisionReport(event_time="10:30am",division_name="Youth Boy's Sparring",gender="Male", rank_label="White, Yellow",             minimum_age=7, maximum_age=8, rings=[6], ranks=[constants.WHITE_BELT,constants.YELLOW_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="10:30am",division_name="Youth Boy's Sparring",gender="Male", rank_label="Orange",                    minimum_age=7, maximum_age=8, rings=[7], ranks=[constants.ORANGE_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="10:30am",division_name="Youth Boy's Sparring",gender="Male", rank_label="Purple",                    minimum_age=7, maximum_age=8, rings=[8], ranks=[constants.PURPLE_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="10:30am",division_name="Youth Boy's Sparring",gender="Male", rank_label="Blue, Blue/Stripe",         minimum_age=7, maximum_age=8, rings=[9], ranks=[constants.BLUE_BELT,constants.BLUE_STRIPE_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="10:30am",division_name="Youth Boy's Sparring",gender="Male", rank_label="Green, Green/Stripe, Brown",minimum_age=7, maximum_age=8, rings=[10], ranks=[constants.GREEN_BELT,constants.GREEN_STRIPE_BELT,constants.THIRD_DEGREE_BROWN_BELT,constants.SECOND_DEGREE_BROWN_BELT,constants.FIRST_DEGREE_BROWN_BELT],clean_df=clean_df)

    ###############################################################################
    # Girl's Sparring - 9-11 year olds
    #
    writePattern1ToExcelViaQuery(filename="GirlsSparring.xlsx", division_type='Sparring', gender="Female",minimum_age=9, maximum_age=11)

    writeSingleSparringTreeandDivisionReport(event_time="10:30am",division_name="Girl's Sparring",gender="Female", rank_label="White, Yellow, Orange",     minimum_age=9, maximum_age=11, rings=[11], ranks=[constants.WHITE_BELT,constants.YELLOW_BELT,constants.ORANGE_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="10:30am",division_name="Girl's Sparring",gender="Female", rank_label="Purple, Blue, Blue/Stripe", minimum_age=9, maximum_age=11, rings=[12], ranks=[constants.PURPLE_BELT,constants.BLUE_BELT,constants.BLUE_STRIPE_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="10:30am",division_name="Girl's Sparring",gender="Female", rank_label="Green, Green/Stripe, Brown",minimum_age=9, maximum_age=11, rings=[13], ranks=[constants.GREEN_BELT,constants.GREEN_STRIPE_BELT,constants.THIRD_DEGREE_BROWN_BELT,constants.SECOND_DEGREE_BROWN_BELT,constants.FIRST_DEGREE_BROWN_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="10:30am",division_name="Girl's Sparring",gender="Female", rank_label="Jr. Black",                 minimum_age=9, maximum_age=11, rings=[14], ranks=[constants.JUNIOR_BLACK_BELT,constants.FIRST_DEGREE_BLACK_BELT,constants.SECOND_DEGREE_BLACK_BELT,constants.THIRD_DEGREE_BLACK_BELT,constants.FOURTH_DEGREE_BLACK_BELT,constants.FIFTH_DEGREE_BLACK_BELT],clean_df=clean_df)

    ### 11:15 Events

    ###############################################################################
    # Boy's Sparring - 9-11 year olds
    #
    writePattern6ToExcelViaQuery(filename="BoysSparring.xlsx", division_type='Sparring', gender="Male",minimum_age=9, maximum_age=11)

    writeSingleSparringTreeandDivisionReport(event_time="11:15am",division_name="Boy's Sparring",gender="Male", rank_label="White, Yellow",             minimum_age=9, maximum_age=11, rings=[1], ranks=[constants.WHITE_BELT,constants.YELLOW_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="11:15am",division_name="Boy's Sparring",gender="Male", rank_label="Orange",                    minimum_age=9, maximum_age=11, rings=[2], ranks=[constants.ORANGE_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="11:15am",division_name="Boy's Sparring",gender="Male", rank_label="Purple",                    minimum_age=9, maximum_age=11, rings=[3], ranks=[constants.PURPLE_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="11:15am",division_name="Boy's Sparring",gender="Male", rank_label="Blue, Blue/Stripe",         minimum_age=9, maximum_age=11, rings=[4,5], ranks=[constants.BLUE_BELT,constants.BLUE_STRIPE_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="11:15am",division_name="Boy's Sparring",gender="Male", rank_label="Green, Green/Stripe",       minimum_age=9, maximum_age=11, rings=[21], ranks=[constants.GREEN_BELT,constants.GREEN_STRIPE_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="11:15am",division_name="Boy's Sparring",gender="Male", rank_label="Brown",                     minimum_age=9, maximum_age=11, rings=[22], ranks=[constants.THIRD_DEGREE_BROWN_BELT,constants.SECOND_DEGREE_BROWN_BELT,constants.FIRST_DEGREE_BROWN_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="11:15am",division_name="Boy's Sparring",gender="Male", rank_label="Jr. Black",                 minimum_age=9, maximum_age=11, rings=[23], ranks=[constants.JUNIOR_BLACK_BELT,constants.FIRST_DEGREE_BLACK_BELT,constants.SECOND_DEGREE_BLACK_BELT,constants.THIRD_DEGREE_BLACK_BELT,constants.FOURTH_DEGREE_BLACK_BELT,constants.FIFTH_DEGREE_BLACK_BELT],clean_df=clean_df)

    ###############################################################################
    # Weapons Division 1 - 4-8 year olds
    #
    writeWeaponsDivision1ToExcelViaQuery(filename="WeaponsDivision1.xlsx", division_type='Weapons', gender="*",minimum_age=4, maximum_age=8)
    writeWeaponsDivisionToSingleKataScoreSheetandDivisionReport(event_time="11:15am",division_name="Weapons Division 1",gender="*", rank_label="White to Jr. Back", minimum_age=4, maximum_age=8, rings=['*TBA'],
                                               ranks=[constants.WHITE_BELT,constants.YELLOW_BELT,constants.ORANGE_BELT,constants.PURPLE_BELT,
                                                      constants.BLUE_BELT,constants.BLUE_STRIPE_BELT,
                                                      constants.GREEN_BELT,constants.GREEN_STRIPE_BELT,
                                                      constants.THIRD_DEGREE_BROWN_BELT,constants.SECOND_DEGREE_BROWN_BELT,constants.FIRST_DEGREE_BROWN_BELT,
                                                      constants.JUNIOR_BLACK_BELT],
                                               clean_df= clean_df)


    ###############################################################################
    # Weapons Division 2 - 9-11 year olds White - Blue W/Green Stripe
    #
    writeWeaponsDivision2ToExcelViaQuery(filename="WeaponsDivision2.xlsx", division_type='Weapons', gender="*",minimum_age=9, maximum_age=11)
    writeWeaponsDivisionToSingleKataScoreSheetandDivisionReport(event_time="11:15am",division_name="Weapons Division 2-new",gender="*", rank_label="White to Blue w/Green Stripe", minimum_age=9, maximum_age=11, rings=['*TBA'],
                                                                ranks=[constants.WHITE_BELT,constants.YELLOW_BELT,
                                                                       constants.ORANGE_BELT,constants.PURPLE_BELT,
                                                                       constants.BLUE_BELT,constants.BLUE_STRIPE_BELT],
                                                                clean_df= clean_df)


    ###############################################################################
    #  WeaponsDivision3  - 9-11 year olds Green - Jr. Black
    #
    writeWeaponsDivision3ToExcelViaQuery(filename="WeaponsDivision3.xlsx", division_type='Weapons', gender="*",minimum_age=9, maximum_age=11)
    writeWeaponsDivisionToSingleKataScoreSheetandDivisionReport(event_time="11:15am",division_name="Weapons Division 3-new",gender="*", rank_label="Green - Jr. Black", minimum_age=9, maximum_age=11, rings=['*TBA'],
                                                                ranks=[constants.GREEN_BELT,
                                                                       constants.GREEN_STRIPE_BELT,
                                                                       constants.THIRD_DEGREE_BROWN_BELT,
                                                                       constants.SECOND_DEGREE_BROWN_BELT,
                                                                       constants.FIRST_DEGREE_BROWN_BELT,
                                                                       constants.JUNIOR_BLACK_BELT],
                                               clean_df= clean_df)




    ### 1:30 Events

    ###############################################################################
    # Men And Women's Kata - 18-39 year olds
    #
    writePattern6ToExcelViaQuery(filename="MenAndWomensKata.xlsx", division_type='Forms', gender="*",minimum_age=18, maximum_age=39)

    writeSingleKataScoreSheetandDivisionReport(event_time="1:30pm",division_name="Men's & Women's Kata",gender="*", rank_label="White, Yellow",         minimum_age=18, maximum_age=39, rings=[1], ranks=[constants.WHITE_BELT,constants.YELLOW_BELT], clean_df=clean_df)
    writeSingleKataScoreSheetandDivisionReport(event_time="1:30pm",division_name="Men's & Women's Kata",gender="*", rank_label="Orange",                minimum_age=18, maximum_age=39, rings=[2], ranks=[constants.ORANGE_BELT], clean_df=clean_df)
    writeSingleKataScoreSheetandDivisionReport(event_time="1:30pm",division_name="Men's & Women's Kata",gender="*", rank_label="Purple",                minimum_age=18, maximum_age=39, rings=[3], ranks=[constants.PURPLE_BELT], clean_df=clean_df)
    writeSingleKataScoreSheetandDivisionReport(event_time="1:30pm",division_name="Men's & Women's Kata",gender="*", rank_label="Blue, Blue w/Stripe",   minimum_age=18, maximum_age=39, rings=[4], ranks=[constants.BLUE_BELT,constants.BLUE_STRIPE_BELT], clean_df=clean_df)
    writeSingleKataScoreSheetandDivisionReport(event_time="1:30pm",division_name="Men's & Women's Kata",gender="*", rank_label="Green, Green w/Stripe", minimum_age=18, maximum_age=39, rings=[5], ranks=[constants.GREEN_BELT,constants.GREEN_STRIPE_BELT], clean_df=clean_df)
    writeSingleKataScoreSheetandDivisionReport(event_time="1:30pm",division_name="Men's & Women's Kata",gender="*", rank_label="Brown",                 minimum_age=18, maximum_age=39, rings=[6], ranks=[constants.THIRD_DEGREE_BROWN_BELT,constants.SECOND_DEGREE_BROWN_BELT,constants.FIRST_DEGREE_BROWN_BELT], clean_df=clean_df)
    writeSingleKataScoreSheetandDivisionReport(event_time="1:30pm",division_name="Men's & Women's Kata",gender="*", rank_label="Black",                 minimum_age=18, maximum_age=39, rings=[7], ranks=[constants.FIRST_DEGREE_BLACK_BELT,constants.SECOND_DEGREE_BLACK_BELT, constants.THIRD_DEGREE_BLACK_BELT,constants.FOURTH_DEGREE_BLACK_BELT,constants.FIFTH_DEGREE_BLACK_BELT,constants.JUNIOR_BLACK_BELT], clean_df=clean_df)


    ###############################################################################
    # Teen Kata - 12-14 year olds
    #
    writePattern6ToExcelViaQuery(filename="TeenKata.xlsx", division_type='Forms', gender="*",minimum_age=12, maximum_age=14)

    writeSingleKataScoreSheetandDivisionReport(event_time="1:30pm",division_name="Teen Kata",gender="*", rank_label="White, Yellow",         minimum_age=12, maximum_age=14, rings=[8],     ranks=[constants.WHITE_BELT,constants.YELLOW_BELT], clean_df=clean_df)
    writeSingleKataScoreSheetandDivisionReport(event_time="1:30pm",division_name="Teen Kata",gender="*", rank_label="Orange",                minimum_age=12, maximum_age=14, rings=[9],     ranks=[constants.ORANGE_BELT], clean_df=clean_df)
    writeSingleKataScoreSheetandDivisionReport(event_time="1:30pm",division_name="Teen Kata",gender="*", rank_label="Purple",                minimum_age=12, maximum_age=14, rings=[10],    ranks=[constants.PURPLE_BELT], clean_df=clean_df)
    writeSingleKataScoreSheetandDivisionReport(event_time="1:30pm",division_name="Teen Kata",gender="*", rank_label="Blue, Blue w/Stripe",   minimum_age=12, maximum_age=14, rings=[11,12], ranks=[constants.BLUE_BELT,constants.BLUE_STRIPE_BELT], clean_df=clean_df)
    writeSingleKataScoreSheetandDivisionReport(event_time="1:30pm",division_name="Teen Kata",gender="*", rank_label="Green, Green w/Stripe", minimum_age=12, maximum_age=14, rings=[13,14], ranks=[constants.GREEN_BELT,constants.GREEN_STRIPE_BELT], clean_df=clean_df)
    writeSingleKataScoreSheetandDivisionReport(event_time="1:30pm",division_name="Teen Kata",gender="*", rank_label="Brown",                 minimum_age=12, maximum_age=14, rings=[15],    ranks=[constants.THIRD_DEGREE_BROWN_BELT,constants.SECOND_DEGREE_BROWN_BELT,constants.FIRST_DEGREE_BROWN_BELT], clean_df=clean_df)
    writeSingleKataScoreSheetandDivisionReport(event_time="1:30pm",division_name="Teen Kata",gender="*", rank_label="Jr. Black",             minimum_age=12, maximum_age=14, rings=[16],    ranks=[constants.FIRST_DEGREE_BLACK_BELT,constants.SECOND_DEGREE_BLACK_BELT, constants.THIRD_DEGREE_BLACK_BELT,constants.FOURTH_DEGREE_BLACK_BELT,constants.FIFTH_DEGREE_BLACK_BELT,constants.JUNIOR_BLACK_BELT], clean_df=clean_df)

    ### 2:15 Events

    ###############################################################################
    # Senior Men's Sparring - 40+ year olds
    #
    writePattern1ToExcelViaQuery(filename="SeniorMensSparring.xlsx", division_type='Sparring', gender="Male",minimum_age=40, maximum_age=constants.AGELESS)

    writeSingleSparringTreeandDivisionReport(event_time="2:15pm",division_name="Sr. Men's Sparring",gender="Male", rank_label="White, Yellow, Orange",     minimum_age=40, maximum_age=constants.AGELESS, rings=[1], ranks=[constants.WHITE_BELT,constants.YELLOW_BELT,constants.ORANGE_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="2:15pm",division_name="Sr. Men's Sparring",gender="Male", rank_label="Purple, Blue, Blue/Stripe", minimum_age=40, maximum_age=constants.AGELESS, rings=[2], ranks=[constants.PURPLE_BELT,constants.BLUE_BELT,constants.BLUE_STRIPE_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="2:15pm",division_name="Sr. Men's Sparring",gender="Male", rank_label="Green, Green/Stripe, Brown",minimum_age=40, maximum_age=constants.AGELESS, rings=[3], ranks=[constants.GREEN_BELT,constants.GREEN_STRIPE_BELT,constants.THIRD_DEGREE_BROWN_BELT,constants.SECOND_DEGREE_BROWN_BELT,constants.FIRST_DEGREE_BROWN_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="2:15pm",division_name="Sr. Men's Sparring",gender="Male", rank_label="Black",                     minimum_age=40, maximum_age=constants.AGELESS, rings=[4], ranks=[constants.JUNIOR_BLACK_BELT,constants.FIRST_DEGREE_BLACK_BELT,constants.SECOND_DEGREE_BLACK_BELT,constants.THIRD_DEGREE_BLACK_BELT,constants.FOURTH_DEGREE_BLACK_BELT,constants.FIFTH_DEGREE_BLACK_BELT],clean_df=clean_df)

    ###############################################################################
    # Senior Women's Sparring - 40+ year olds
    #
    writePattern1ToExcelViaQuery(filename="SeniorWomensSparring.xlsx", division_type='Sparring', gender="Female",minimum_age=40, maximum_age=constants.AGELESS)

    writeSingleSparringTreeandDivisionReport(event_time="2:15pm",division_name="Sr. Women's Sparring",gender="Female", rank_label="White, Yellow, Orange",     minimum_age=40, maximum_age=constants.AGELESS, rings=[5], ranks=[constants.WHITE_BELT,constants.YELLOW_BELT,constants.ORANGE_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="2:15pm",division_name="Sr. Women's Sparring",gender="Female", rank_label="Purple, Blue, Blue/Stripe", minimum_age=40, maximum_age=constants.AGELESS, rings=[6], ranks=[constants.PURPLE_BELT,constants.BLUE_BELT,constants.BLUE_STRIPE_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="2:15pm",division_name="Sr. Women's Sparring",gender="Female", rank_label="Green, Green/Stripe, Brown",minimum_age=40, maximum_age=constants.AGELESS, rings=[7], ranks=[constants.GREEN_BELT,constants.GREEN_STRIPE_BELT,constants.THIRD_DEGREE_BROWN_BELT,constants.SECOND_DEGREE_BROWN_BELT,constants.FIRST_DEGREE_BROWN_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="2:15pm",division_name="Sr. Women's Sparring",gender="Female", rank_label="Black",                     minimum_age=40, maximum_age=constants.AGELESS, rings=[8], ranks=[constants.JUNIOR_BLACK_BELT,constants.FIRST_DEGREE_BLACK_BELT,constants.SECOND_DEGREE_BLACK_BELT,constants.THIRD_DEGREE_BLACK_BELT,constants.FOURTH_DEGREE_BLACK_BELT,constants.FIFTH_DEGREE_BLACK_BELT],clean_df=clean_df)

    ###############################################################################
    # Young Adult Kata - 15-17 year olds
    #
    writePattern1ToExcelViaQuery(filename="YoungAdultKata.xlsx", division_type='Forms', gender="*",minimum_age=15, maximum_age=17)

    writeSingleKataScoreSheetandDivisionReport(event_time="2:15pm",division_name="Young Adult Kata",gender="*",rank_label="White,Yellow,Orange",       minimum_age=15, maximum_age=17, rings=[9],  ranks=[constants.WHITE_BELT,constants.YELLOW_BELT,constants.ORANGE_BELT], clean_df=clean_df)
    writeSingleKataScoreSheetandDivisionReport(event_time="2:15pm",division_name="Young Adult Kata",gender="*",rank_label="Purple, Blue, Blue/Stripe", minimum_age=15, maximum_age=17, rings=[10], ranks=[constants.PURPLE_BELT,constants.BLUE_BELT,constants.BLUE_STRIPE_BELT], clean_df=clean_df)
    writeSingleKataScoreSheetandDivisionReport(event_time="2:15pm",division_name="Young Adult Kata",gender="*",rank_label="Green, Green/Stripe, Brown",minimum_age=15, maximum_age=17, rings=[11], ranks=[constants.GREEN_BELT,constants.GREEN_STRIPE_BELT,constants.THIRD_DEGREE_BROWN_BELT,constants.SECOND_DEGREE_BROWN_BELT,constants.FIRST_DEGREE_BROWN_BELT], clean_df=clean_df)
    writeSingleKataScoreSheetandDivisionReport(event_time="2:15pm",division_name="Young Adult Kata",gender="*",rank_label="Jr. Black & Black",         minimum_age=15, maximum_age=17, rings=[12], ranks=[constants.FIRST_DEGREE_BLACK_BELT,constants.SECOND_DEGREE_BLACK_BELT, constants.THIRD_DEGREE_BLACK_BELT,constants.FOURTH_DEGREE_BLACK_BELT,constants.FIFTH_DEGREE_BLACK_BELT,constants.JUNIOR_BLACK_BELT], clean_df=clean_df)


    ###############################################################################
    # Teen Girl's Sparring - 12-14 year olds
    #
    writePattern1ToExcelViaQuery(filename="TeenGirlSparring.xlsx", division_type='Sparring', gender="Female",minimum_age=12, maximum_age=14)

    writeSingleSparringTreeandDivisionReport(event_time="2:15pm",division_name="Teen Girl's Sparring",gender="Female", rank_label="White, Yellow, Orange",     minimum_age=12, maximum_age=14, rings=[13], ranks=[constants.WHITE_BELT,constants.YELLOW_BELT,constants.ORANGE_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="2:15pm",division_name="Teen Girl's Sparring",gender="Female", rank_label="Purple, Blue, Blue/Stripe", minimum_age=12, maximum_age=14, rings=[14], ranks=[constants.PURPLE_BELT,constants.BLUE_BELT,constants.BLUE_STRIPE_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="2:15pm",division_name="Teen Girl's Sparring",gender="Female", rank_label="Green, Green/Stripe, Brown",minimum_age=12, maximum_age=14, rings=[15], ranks=[constants.GREEN_BELT,constants.GREEN_STRIPE_BELT,constants.THIRD_DEGREE_BROWN_BELT,constants.SECOND_DEGREE_BROWN_BELT,constants.FIRST_DEGREE_BROWN_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="2:15pm",division_name="Teen Girl's Sparring",gender="Female", rank_label="Jr. Black",                 minimum_age=12, maximum_age=14, rings=[16], ranks=[constants.JUNIOR_BLACK_BELT,constants.FIRST_DEGREE_BLACK_BELT,constants.SECOND_DEGREE_BLACK_BELT,constants.THIRD_DEGREE_BLACK_BELT,constants.FOURTH_DEGREE_BLACK_BELT,constants.FIFTH_DEGREE_BLACK_BELT],clean_df=clean_df)


    ### 3:00 Events

    ###############################################################################
    #  Men's Sparring - 18-39 year olds
    #
    writePattern1ToExcelViaQuery(filename="MensSparring.xlsx", division_type='Sparring', gender="Male",minimum_age=18, maximum_age=39)

    writeSingleSparringTreeandDivisionReport(event_time="3:00pm",division_name="Men's Sparring",gender="Male", rank_label="White, Yellow, Orange",     minimum_age=18, maximum_age=39, rings=[1], ranks=[constants.WHITE_BELT,constants.YELLOW_BELT,constants.ORANGE_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="3:00pm",division_name="Men's Sparring",gender="Male", rank_label="Purple, Blue, Blue/Stripe", minimum_age=18, maximum_age=39, rings=[2], ranks=[constants.PURPLE_BELT,constants.BLUE_BELT,constants.BLUE_STRIPE_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="3:00pm",division_name="Men's Sparring",gender="Male", rank_label="Green, Green/Stripe, Brown",minimum_age=18, maximum_age=39, rings=[3], ranks=[constants.GREEN_BELT,constants.GREEN_STRIPE_BELT,constants.THIRD_DEGREE_BROWN_BELT,constants.SECOND_DEGREE_BROWN_BELT,constants.FIRST_DEGREE_BROWN_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="3:00pm",division_name="Men's Sparring",gender="Male", rank_label="Black",                     minimum_age=18, maximum_age=39, rings=[4], ranks=[constants.JUNIOR_BLACK_BELT,constants.FIRST_DEGREE_BLACK_BELT,constants.SECOND_DEGREE_BLACK_BELT,constants.THIRD_DEGREE_BLACK_BELT,constants.FOURTH_DEGREE_BLACK_BELT,constants.FIFTH_DEGREE_BLACK_BELT],clean_df=clean_df)

    ###############################################################################
    #  Teen Boy's Sparring - 12-14 year olds
    #
    writePattern2ToExcelViaQuery(filename="TeenBoysSparring.xlsx", division_type='Sparring', gender="Male",minimum_age=12, maximum_age=14)

    writeSingleSparringTreeandDivisionReport(event_time="3:00pm",division_name="Teen Boy's Sparring",gender="Male", rank_label="White, Yellow, Orange",      minimum_age=12, maximum_age=14, rings=[5], ranks=[constants.WHITE_BELT,constants.YELLOW_BELT,constants.ORANGE_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="3:00pm",division_name="Teen Boy's Sparring",gender="Male", rank_label="Purple, Blue, Blue/Stripe",  minimum_age=12, maximum_age=14, rings=[6], ranks=[constants.PURPLE_BELT,constants.BLUE_BELT,constants.BLUE_STRIPE_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="3:00pm",division_name="Teen Boy's Sparring",gender="Male", rank_label="Green, Green/Stripe",        minimum_age=12, maximum_age=14, rings=[7], ranks=[constants.GREEN_BELT,constants.GREEN_STRIPE_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="3:00pm",division_name="Teen Boy's Sparring",gender="Male", rank_label="Brown",                      minimum_age=12, maximum_age=14, rings=[8], ranks=[constants.THIRD_DEGREE_BROWN_BELT,constants.SECOND_DEGREE_BROWN_BELT,constants.FIRST_DEGREE_BROWN_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="3:00pm",division_name="Teen Boy's Sparring",gender="Male", rank_label="Jr. Black",                  minimum_age=12, maximum_age=14, rings=[9], ranks=[constants.JUNIOR_BLACK_BELT,constants.FIRST_DEGREE_BLACK_BELT,constants.SECOND_DEGREE_BLACK_BELT,constants.THIRD_DEGREE_BLACK_BELT,constants.FOURTH_DEGREE_BLACK_BELT,constants.FIFTH_DEGREE_BLACK_BELT],clean_df=clean_df)

    ###############################################################################
    #  Young Adult Men's Sparring - 15-17 year olds
    #
    writePattern2ToExcelViaQuery(filename="YoungAdultMensSparring.xlsx", division_type='Sparring', gender="Male",minimum_age=15, maximum_age=17)

    writeSingleSparringTreeandDivisionReport(event_time="3:00pm",division_name="Young Adult Men's Sparring",gender="Male", rank_label="White, Yellow, Orange",     minimum_age=15, maximum_age=17, rings=[10], ranks=[constants.WHITE_BELT,constants.YELLOW_BELT,constants.ORANGE_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="3:00pm",division_name="Young Adult Men's Sparring",gender="Male", rank_label="Purple, Blue, Blue/Stripe", minimum_age=15, maximum_age=17, rings=[11], ranks=[constants.PURPLE_BELT,constants.BLUE_BELT,constants.BLUE_STRIPE_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="3:00pm",division_name="Young Adult Men's Sparring",gender="Male", rank_label="Green, Green/Stripe",       minimum_age=15, maximum_age=17, rings=[12], ranks=[constants.GREEN_BELT,constants.GREEN_STRIPE_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="3:00pm",division_name="Young Adult Men's Sparring",gender="Male", rank_label="Brown",                     minimum_age=15, maximum_age=17, rings=[13], ranks=[constants.THIRD_DEGREE_BROWN_BELT,constants.SECOND_DEGREE_BROWN_BELT,constants.FIRST_DEGREE_BROWN_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="3:00pm",division_name="Young Adult Men's Sparring",gender="Male", rank_label="Jr. Black & Black",         minimum_age=15, maximum_age=17, rings=[14], ranks=[constants.JUNIOR_BLACK_BELT,constants.FIRST_DEGREE_BLACK_BELT,constants.SECOND_DEGREE_BLACK_BELT,constants.THIRD_DEGREE_BLACK_BELT,constants.FOURTH_DEGREE_BLACK_BELT,constants.FIFTH_DEGREE_BLACK_BELT],clean_df=clean_df)


    ###############################################################################
    #  Women's Sparring - 18-39 year olds
    #
    writePattern1ToExcelViaQuery(filename="WomensSparring.xlsx", division_type='Sparring', gender="Female",minimum_age=18, maximum_age=39)

    writeSingleSparringTreeandDivisionReport(event_time="3:00pm",division_name="Women's Sparring",gender="Female", rank_label="White, Yellow, Orange",     minimum_age=18, maximum_age=39, rings=[15], ranks=[constants.WHITE_BELT,constants.YELLOW_BELT,constants.ORANGE_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="3:00pm",division_name="Women's Sparring",gender="Female", rank_label="Purple, Blue, Blue/Stripe", minimum_age=18, maximum_age=39, rings=[16], ranks=[constants.PURPLE_BELT,constants.BLUE_BELT,constants.BLUE_STRIPE_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="3:00pm",division_name="Women's Sparring",gender="Female", rank_label="Green, Green/Stripe, Brown",minimum_age=18, maximum_age=39, rings=[17], ranks=[constants.GREEN_BELT,constants.GREEN_STRIPE_BELT,constants.THIRD_DEGREE_BROWN_BELT,constants.SECOND_DEGREE_BROWN_BELT,constants.FIRST_DEGREE_BROWN_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="3:00pm",division_name="Women's Sparring",gender="Female", rank_label="Black",                     minimum_age=18, maximum_age=39, rings=[18], ranks=[constants.JUNIOR_BLACK_BELT,constants.FIRST_DEGREE_BLACK_BELT,constants.SECOND_DEGREE_BLACK_BELT,constants.THIRD_DEGREE_BLACK_BELT,constants.FOURTH_DEGREE_BLACK_BELT,constants.FIFTH_DEGREE_BLACK_BELT],clean_df=clean_df)


    ### 3:45 Events

    ###############################################################################
    # Senior Kata - 40+ year olds
    #
    writePattern6ToExcelViaQuery(filename="SeniorKata.xlsx", division_type='Forms', gender="*",minimum_age=40, maximum_age=constants.AGELESS)

    writeSingleKataScoreSheetandDivisionReport(event_time="3:45pm",division_name="Senior Kata",gender="*", rank_label="White, Yellow",         minimum_age=40, maximum_age=constants.AGELESS, rings=[1], ranks=[constants.WHITE_BELT,constants.YELLOW_BELT], clean_df=clean_df)
    writeSingleKataScoreSheetandDivisionReport(event_time="3:45pm",division_name="Senior Kata",gender="*", rank_label="Orange",                minimum_age=40, maximum_age=constants.AGELESS, rings=[2], ranks=[constants.ORANGE_BELT], clean_df=clean_df)
    writeSingleKataScoreSheetandDivisionReport(event_time="3:45pm",division_name="Senior Kata",gender="*", rank_label="Purple",                minimum_age=40, maximum_age=constants.AGELESS, rings=[3], ranks=[constants.PURPLE_BELT], clean_df=clean_df)
    writeSingleKataScoreSheetandDivisionReport(event_time="3:45pm",division_name="Senior Kata",gender="*", rank_label="Blue, Blue w/Stripe",   minimum_age=40, maximum_age=constants.AGELESS, rings=[4], ranks=[constants.BLUE_BELT,constants.BLUE_STRIPE_BELT], clean_df=clean_df)
    writeSingleKataScoreSheetandDivisionReport(event_time="3:45pm",division_name="Senior Kata",gender="*", rank_label="Green, Green w/Stripe", minimum_age=40, maximum_age=constants.AGELESS, rings=[5], ranks=[constants.GREEN_BELT,constants.GREEN_STRIPE_BELT], clean_df=clean_df)
    writeSingleKataScoreSheetandDivisionReport(event_time="3:45pm",division_name="Senior Kata",gender="*", rank_label="Brown",                 minimum_age=40, maximum_age=constants.AGELESS, rings=[6], ranks=[constants.THIRD_DEGREE_BROWN_BELT,constants.SECOND_DEGREE_BROWN_BELT,constants.FIRST_DEGREE_BROWN_BELT], clean_df=clean_df)
    writeSingleKataScoreSheetandDivisionReport(event_time="3:45pm",division_name="Senior Kata",gender="*", rank_label="Black",                 minimum_age=40, maximum_age=constants.AGELESS, rings=[7], ranks=[constants.FIRST_DEGREE_BLACK_BELT,constants.SECOND_DEGREE_BLACK_BELT, constants.THIRD_DEGREE_BLACK_BELT,constants.FOURTH_DEGREE_BLACK_BELT,constants.FIFTH_DEGREE_BLACK_BELT,constants.JUNIOR_BLACK_BELT], clean_df=clean_df)



    ###############################################################################
    #  Young Adult Women's Sparring - 15-17 year olds
    #
    writePattern1ToExcelViaQuery(filename="YoungAdultWomensSparring.xlsx", division_type='Sparring', gender="Female",minimum_age=15, maximum_age=17)

    writeSingleSparringTreeandDivisionReport(event_time="3:45pm",division_name="Young Adult Women's Sparring",gender="Female", rank_label="White, Yellow, Orange",     minimum_age=15, maximum_age=17, rings=[8], ranks=[constants.WHITE_BELT,constants.YELLOW_BELT,constants.ORANGE_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="3:45pm",division_name="Young Adult Women's Sparring",gender="Female", rank_label="Purple, Blue, Blue/Stripe", minimum_age=15, maximum_age=17, rings=[9], ranks=[constants.PURPLE_BELT,constants.BLUE_BELT,constants.BLUE_STRIPE_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="3:45pm",division_name="Young Adult Women's Sparring",gender="Female", rank_label="Green, Green/Stripe, Brown",minimum_age=15, maximum_age=17, rings=[10], ranks=[constants.GREEN_BELT,constants.GREEN_STRIPE_BELT,constants.THIRD_DEGREE_BROWN_BELT,constants.SECOND_DEGREE_BROWN_BELT,constants.FIRST_DEGREE_BROWN_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="3:45pm",division_name="Young Adult Women's Sparring",gender="Female", rank_label="Jr. Black & Black",         minimum_age=15, maximum_age=17, rings=[11], ranks=[constants.JUNIOR_BLACK_BELT,constants.FIRST_DEGREE_BLACK_BELT,constants.SECOND_DEGREE_BLACK_BELT,constants.THIRD_DEGREE_BLACK_BELT,constants.FOURTH_DEGREE_BLACK_BELT,constants.FIFTH_DEGREE_BLACK_BELT],clean_df=clean_df)


    ### 4:15 Events

    ###############################################################################
    #  WeaponsDivision4 12-17 White-Blue Stripe year olds
    #
    writeWeaponsDivision4ToExcelViaQuery(filename="WeaponsDivision4.xlsx", division_type='Weapons', gender="*",minimum_age=12, maximum_age=17)
    writeWeaponsDivisionToSingleKataScoreSheetandDivisionReport(event_time="4:15pm",
                                                                division_name="Weapons Division 4-new",
                                                                gender="*",
                                                                rank_label="White - Blue w/Green Stripe",
                                                                minimum_age=12, maximum_age=17,
                                                                rings=['*TBA'],
                                                                ranks=[constants.WHITE_BELT,constants.YELLOW_BELT,
                                                                       constants.ORANGE_BELT,constants.PURPLE_BELT,
                                                                       constants.BLUE_BELT,constants.BLUE_STRIPE_BELT],
                                                                clean_df= clean_df)


    ###############################################################################
    #  WeaponsDivision5 18+ year olds
    #
    writeWeaponsDivision5ToExcelViaQuery(filename="WeaponsDivision5.xlsx", division_type='Weapons', gender="*",minimum_age=18, maximum_age=constants.AGELESS)
    writeWeaponsDivisionToSingleKataScoreSheetandDivisionReport(event_time="4:15pm",
                                                                division_name="Weapons Division 5-new",
                                                                gender="*",
                                                                rank_label="White - Blue w/Green Stripe",
                                                                minimum_age=18, maximum_age=constants.AGELESS,
                                                                rings=['*TBA'],
                                                                ranks=[constants.WHITE_BELT,constants.YELLOW_BELT,
                                                                       constants.ORANGE_BELT,constants.PURPLE_BELT,
                                                                       constants.BLUE_BELT,constants.BLUE_STRIPE_BELT],
                                                                clean_df= clean_df)

    ###############################################################################
    #  WeaponsDivision6 12+ year olds green belts
    #
    writeWeaponsDivision6ToExcelViaQuery(filename="WeaponsDivision6.xlsx", division_type='Weapons', gender="*",minimum_age=12, maximum_age=constants.AGELESS)
    writeWeaponsDivisionToSingleKataScoreSheetandDivisionReport(event_time="4:15pm",
                                                                division_name="Weapons Division 6-new",
                                                                gender="*",
                                                                rank_label="Green, Green w/Brown Stripe",
                                                                minimum_age=12,maximum_age=constants.AGELESS,
                                                                rings=['*TBA'],
                                                                ranks=[constants.GREEN_BELT,
                                                                       constants.GREEN_STRIPE_BELT],
                                                                clean_df=clean_df)

    ###############################################################################
    #  WeaponsDivision7 12+ year olds brown belts
    #
    writeWeaponsDivision7ToExcelViaQuery(filename="WeaponsDivision7.xlsx", division_type='Weapons', gender="*",minimum_age=12, maximum_age=constants.AGELESS)
    writeWeaponsDivisionToSingleKataScoreSheetandDivisionReport(event_time="4:15pm",
                                                                division_name="Weapons Division 7-new",
                                                                gender="*",
                                                                rank_label="Brown",
                                                                minimum_age=12,maximum_age=constants.AGELESS,
                                                                rings=['*TBA'],
                                                                ranks=[constants.THIRD_DEGREE_BROWN_BELT,
                                                                       constants.SECOND_DEGREE_BROWN_BELT,
                                                                       constants.FIRST_DEGREE_BROWN_BELT],
                                                                clean_df=clean_df)

    ###############################################################################
    #  WeaponsDivision8 12+ Black
    #
    writeWeaponsDivision8ToExcelViaQuery(filename="WeaponsDivision8.xlsx", division_type='Weapons', gender="*",minimum_age=12, maximum_age=17)
    writeWeaponsDivisionToSingleKataScoreSheetandDivisionReport(event_time="4:15pm",
                                                                division_name="Weapons Division 8-new",
                                                                gender="*",
                                                                rank_label="Jr. Back & Black",
                                                                minimum_age=12,maximum_age=17,
                                                                rings=['*TBA'],
                                                                ranks=[constants.JUNIOR_BLACK_BELT,
                                                                       constants.FIRST_DEGREE_BLACK_BELT,constants.SECOND_DEGREE_BLACK_BELT,constants.THIRD_DEGREE_BLACK_BELT,constants.FOURTH_DEGREE_BLACK_BELT,constants.FIFTH_DEGREE_BLACK_BELT],
                                                                clean_df=clean_df)

    ###############################################################################
    #  WeaponsDivision9 18+ year olds
    #
    writeWeaponsDivision9ToExcelViaQuery(filename="WeaponsDivision9.xlsx", division_type='Weapons', gender="*",minimum_age=18, maximum_age=constants.AGELESS)
    writeWeaponsDivisionToSingleKataScoreSheetandDivisionReport(event_time="4:15pm",
                                                                division_name="Weapons Division 9-new",
                                                                gender="*",
                                                                rank_label="Black",
                                                                minimum_age=18,maximum_age=constants.AGELESS,
                                                                rings=['*TBA'],
                                                                ranks=[constants.JUNIOR_BLACK_BELT,constants.FIRST_DEGREE_BLACK_BELT,constants.SECOND_DEGREE_BLACK_BELT,constants.THIRD_DEGREE_BLACK_BELT,constants.FOURTH_DEGREE_BLACK_BELT,constants.FIFTH_DEGREE_BLACK_BELT],
                                                                clean_df=clean_df)

print(time.strftime("%X") + " Saving PDFs to disk")
divison_detail_report_pdf.write_pdfpage()
kata_score_sheet.write_pdfpage()
sparing_tree_pdf.close()

#print hitcount warnings
if clean_df.shape[0] > 30:
    print("\u001b[31mWarning: Investigate these entries in the spreadsheet!  They didn't get put into any events:")
    for index, row in clean_df.iterrows():
        name = row['First_Name'] + " " + row['Last_Name']
        events = row['Events']
        hc = row['hitcount']
        if hc < 1 :
            # print("  " + name + ": " + str(hc))
            print(f'   Name:{name} Events:{events} <---was put in {hc} events')
    print('\u001b[0m')

localtime = time.asctime(time.localtime(time.time()))
print(time.strftime("%X") + " Done!")
