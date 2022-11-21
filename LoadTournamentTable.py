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


# ###############################################################################
# # NewDataFrameFromMask()
# #  arguments:  mask to apply
# #  return:   new data frame
# #
# def newDataFrameFromMask(mask):
#     newdf = clean_df[
#         ["Registrant_ID","First_Name", "Last_Name", "Gender", "Dojo", "Age", "Rank", "Feet", "Inches", "Height", "Weight", "BMI",
#          "Events", "Weapons"]][mask].sort_values("Age")
#     newdf.sort_values('BMI', inplace=True)
#
#     ## update the hitcount every time we touch someone
#     for index, row in clean_df[mask].iterrows():
#         name = row['First_Name'] + " " + row['Last_Name']
#         hc = row['hitcount']
#         newhc = hc + 1
#         #    print name + " has a row count of " + str(newhc)
#         clean_df.at[index, 'hitcount'] = newhc
#
#     return newdf

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


# ###############################################################################
# # write event to file
# #  arguments:
# #  filename - the filename without path to write
# #  compsitMask - a mask made up of everything but the belts that you want
# #
# def writeEventToFile(filename, compositMask):
#     #    fullpath = os.getcwd() + "\\Sorted\\" + filename  #Windows
#     #    fullpath = os.getcwd() + "/Sorted/" + filename  #Mac
#     fullpath = os.getcwd() + pathDelimiter() + "Sorted" + pathDelimiter() + filename
#     writer = pd.ExcelWriter(fullpath)
#
#     print(time.strftime("%X") + " Generating " + fullpath)
#
#     mask = mask_WhiteBelt & compositMask
#     wmk = newDataFrameFromMask(mask)
#     writeFormattedExcelSheet(wmk, writer, 'White')
#
#     mask = mask_YellowBelt & compositMask
#     wmk = newDataFrameFromMask(mask)
#     writeFormattedExcelSheet(wmk, writer, 'Yellow')
#
#     mask = mask_OrangeBelt & compositMask
#     wmk = newDataFrameFromMask(mask)
#     writeFormattedExcelSheet(wmk, writer, 'Orange')
#
#     mask = mask_PurpleBelt & compositMask
#     wmk = newDataFrameFromMask(mask)
#     writeFormattedExcelSheet(wmk, writer, 'Purple')
#
#     mask = mask_AllBlueBelt & compositMask
#     wmk = newDataFrameFromMask(mask)
#     writeFormattedExcelSheet(wmk, writer, 'Blue')
#
#     mask = mask_AllGreenBelt & compositMask
#     wmk = newDataFrameFromMask(mask)
#     writeFormattedExcelSheet(wmk, writer, 'Green')
#
#     mask = mask_AllBrownBelt & compositMask
#     wmk = newDataFrameFromMask(mask)
#     writeFormattedExcelSheet(wmk, writer, 'Brown')
#
#     mask = mask_AllBlackBelt & compositMask
#     wmk = newDataFrameFromMask(mask)
#     writeFormattedExcelSheet(wmk, writer, 'Black')
#
#     # writer.save()
#     writer.close()
#     time.sleep(constants.SLEEP_TIME)


# ###############################################################################
# # writePattern1ToExcel
# #  This method provides a re-usable method to write output to excel
# #  The Pattern it writes is:
# #    White, Yellow, Orange
# #    Purple, Blue, Blue Stripe
# #    Green, Green Stripe, Brown
# #    Black
# #
# #  arguments:
# #  filename - the filename without path to write
# #  compsitMask - a mask made up of everything but the belts that you want
# #
# def writePattern1ToExcel(filename, compositMask):
#     fullpath = os.getcwd() + pathDelimiter() + "Sorted" + pathDelimiter() + filename
#     writer = pd.ExcelWriter(fullpath)
#     print(time.strftime("%X") + " Generating " + fullpath)
#
#     mask1 = mask_WhiteBelt & compositMask
#     mask2 = mask_YellowBelt & compositMask
#     mask3 = mask_OrangeBelt & compositMask
#     mask = mask1 | mask2 | mask3
#     wmk = newDataFrameFromMask(mask)
#     writeFormattedExcelSheet(wmk, writer, 'White, Yellow, Orange')
#
#     #    mask= mask_OrangeBelt & compositMask
#     #    wmk=newDataFrameFromMask( mask )
#
#     #    mask= mask_PurpleBelt & compositMask
#     #    wmk=newDataFrameFromMask( mask )
#
#     mask1 = mask_PurpleBelt & compositMask
#     mask2 = mask_AllBlueBelt & compositMask
#     mask = mask1 | mask2
#     wmk = newDataFrameFromMask(mask)
#     writeFormattedExcelSheet(wmk, writer, 'Purple, Blue, Blue Stripe')
#
#     mask1 = mask_AllBrownBelt & compositMask
#     mask2 = mask_AllGreenBelt & compositMask
#     mask = mask1 | mask2
#     wmk = newDataFrameFromMask(mask)
#     writeFormattedExcelSheet(wmk, writer, 'Green, Green Stripe, Brown')
#
#     #    mask= mask_AllBrownBelt & compositMask
#     #    wmk=newDataFrameFromMask( mask )
#
#     mask = mask_AllBlackBelt & compositMask
#     wmk = newDataFrameFromMask(mask)
#     writeFormattedExcelSheet(wmk, writer, 'Black')
#
#     # writer.save()
#     writer.close()
#     time.sleep(constants.SLEEP_TIME)


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


# ###############################################################################
# # writePattern2ToExcel
# #  This method provides a re-usable method to write output to excel
# #  The Pattern it writes is:
# #    White, Yellow & Orange
# #    Purple, Blue & Blue Stripe
# #    Green, Green Stripe,
# #    Brown
# #    Black
# #
# #  arguments:
# #  filename - the filename without path to write
# #  compsitMask - a mask made up of everything but the belts that you want
# #
# def writePattern2ToExcel(filename, compositMask):
#     fullpath = os.getcwd() + pathDelimiter() + "Sorted" + pathDelimiter() + filename
#     writer = pd.ExcelWriter(fullpath)
#     print(time.strftime("%X") + " Generating " + fullpath)
#
#     mask1 = mask_WhiteBelt & compositMask
#     mask2 = mask_YellowBelt & compositMask
#     mask3 = mask_OrangeBelt & compositMask
#     mask = mask1 | mask2 | mask3
#     wmk = newDataFrameFromMask(mask)
#     writeFormattedExcelSheet(wmk, writer, 'White, Yellow & Orange')
#
#     mask1 = mask_PurpleBelt & compositMask
#     mask2 = mask_AllBlueBelt & compositMask
#     mask = mask1 | mask2
#     wmk = newDataFrameFromMask(mask)
#     writeFormattedExcelSheet(wmk, writer, 'Purple, Blue & Blue Stripe')
#
#     mask = mask_AllGreenBelt & compositMask
#     wmk = newDataFrameFromMask(mask)
#     writeFormattedExcelSheet(wmk, writer, 'Green, Green Stripe')
#
#     mask = mask_AllBrownBelt & compositMask
#     wmk = newDataFrameFromMask(mask)
#     writeFormattedExcelSheet(wmk, writer, 'Brown')
#
#
#     mask = mask_AllBlackBelt & compositMask
#     wmk = newDataFrameFromMask(mask)
#     writeFormattedExcelSheet(wmk, writer, 'Black')
#
#     # writer.save()
#     writer.close()
#     time.sleep(constants.SLEEP_TIME)


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


# ###############################################################################
# # writePattern3ToExcel
# #  This method provides a re-usable method to write output to excel
# #  The Pattern it writes is:
# #    White, Yellow
# #    Orange
# #    Purple
# #    Blue, Blue Stripe
# #    Green, Green Stripe, Brown
# #
# #  arguments:
# #  filename - the filename without path to write
# #  compsitMask - a mask made up of everything but the belts that you want
# def writePattern3ToExcel(filename, compositMask):
#     fullpath = os.getcwd() + pathDelimiter() + "Sorted" + pathDelimiter() + filename
#     writer = pd.ExcelWriter(fullpath)
#     print(time.strftime("%X") + " Generating " + fullpath)
#
#     mask1 = mask_WhiteBelt & compositMask
#     mask2 = mask_YellowBelt & compositMask
#     mask = mask1 | mask2
#     wmk = newDataFrameFromMask(mask)
#     writeFormattedExcelSheet(wmk, writer, 'White, Yellow')
#
#     mask = mask_OrangeBelt & compositMask
#     wmk = newDataFrameFromMask(mask)
#     writeFormattedExcelSheet(wmk, writer, 'Orange')
#
#     mask = mask_PurpleBelt & compositMask
#     wmk = newDataFrameFromMask(mask)
#     writeFormattedExcelSheet(wmk, writer, 'Purple')
#
#     mask = mask_AllBlueBelt & compositMask
#     wmk = newDataFrameFromMask(mask)
#     writeFormattedExcelSheet(wmk, writer, 'Blue, Blue Stripe')
#
#     mask1 = mask_AllGreenBelt & compositMask
#     mask2 = mask_AllBrownBelt & compositMask
#     mask = mask1 | mask2
#     wmk = newDataFrameFromMask(mask)
#     writeFormattedExcelSheet(wmk, writer, 'Green, Green Stripe, Brown')
#
#     # writer.save()
#     writer.close()
#     time.sleep(constants.SLEEP_TIME)


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



# ###############################################################################
# # writePattern4ToExcel
# #  This method provides a re-usable method to write output to excel
# #  The Pattern it writes is:
# #    White
# #    Yellow
# #    Orange
# #    Purple, Blue, Blue Stripe
# #    Green, Green Stripe
# #
# #  arguments:
# #  filename - the filename without path to write
# #  compsitMask - a mask made up of everything but the belts that you want
# def writePattern4ToExcel(filename, compositMask):
#     fullpath = os.getcwd() + pathDelimiter() + "Sorted" + pathDelimiter() + filename
#     writer = pd.ExcelWriter(fullpath, engine='xlsxwriter')
#     print(time.strftime("%X") + " Generating " + fullpath)
#
#     mask = mask_WhiteBelt & compositMask
#     wmk = newDataFrameFromMask(mask)
#     writeFormattedExcelSheet(wmk, writer, 'White')
#
#     mask = mask_YellowBelt & compositMask
#     wmk = newDataFrameFromMask(mask)
#     writeFormattedExcelSheet(wmk, writer, 'Yellow')
#
#     mask = mask_OrangeBelt & compositMask
#     wmk = newDataFrameFromMask(mask)
#     writeFormattedExcelSheet(wmk, writer, 'Orange')
#
#     mask1 = mask_PurpleBelt & compositMask
#     mask2 = mask_AllBlueBelt & compositMask
#     mask = mask1 | mask2
#     wmk = newDataFrameFromMask(mask)
#     writeFormattedExcelSheet(wmk, writer, 'Purple, Blue, Blue Stripe')
#
#     mask1 = mask_AllGreenBelt & compositMask
#     mask2 = mask_AllBrownBelt & compositMask
#     mask = mask1 | mask2
#     wmk = newDataFrameFromMask(mask)
#     writeFormattedExcelSheet(wmk, writer, 'Green, Green Stripe, Brown')
#     #
#     #    mask= mask_AllBlackBelt & compositMask
#     #    wmk=newDataFrameFromMask( mask )
#
#     # writer.save()
#     writer.close()
#     time.sleep(constants.SLEEP_TIME)

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


# ###############################################################################
# # writePattern5ToExcel
# #  This method provides a re-usable method to write output to excel
# #  The Pattern it writes is:
# #    White
# #    Yellow
# #    Orange
# #    Purple
# #    Blue, Blue Stripe
# #    Green, Green Stripe, Brown
# #
# #  arguments:
# #  filename - the filename without path to write
# #  compsitMask - a mask made up of everything but the belts that you want
# def writePattern5ToExcel(filename, compositMask):
#     fullpath = os.getcwd() + pathDelimiter() + "Sorted" + pathDelimiter() + filename
#     writer = pd.ExcelWriter(fullpath)
#     print(time.strftime("%X") + " Generating " + fullpath)
#
#     mask = mask_WhiteBelt & compositMask
#     wmk = newDataFrameFromMask(mask)
#     writeFormattedExcelSheet(wmk, writer, 'White')
#
#     mask = mask_YellowBelt & compositMask
#     wmk = newDataFrameFromMask(mask)
#     writeFormattedExcelSheet(wmk, writer, 'Yellow')
#
#     mask = mask_OrangeBelt & compositMask
#     wmk = newDataFrameFromMask(mask)
#     writeFormattedExcelSheet(wmk, writer, 'Orange')
#
#     mask = mask_PurpleBelt & compositMask
#     wmk = newDataFrameFromMask(mask)
#     writeFormattedExcelSheet(wmk, writer, 'Purple')
#
#     mask = mask_AllBlueBelt & compositMask
#     wmk = newDataFrameFromMask(mask)
#     writeFormattedExcelSheet(wmk, writer, 'Blue, Blue Stripe')
#
#     mask1 = mask_AllGreenBelt & compositMask
#     mask2 = mask_AllBrownBelt & compositMask
#     mask = mask1 | mask2
#     wmk = newDataFrameFromMask(mask)
#     writeFormattedExcelSheet(wmk, writer, 'Green, Green Stripe, Brown')
#
#     # writer.save()
#     writer.close()
#     time.sleep(constants.SLEEP_TIME)

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



# ###############################################################################
# # writePattern6ToExcel
# #  This method provides a re-usable method to write output to excel
# #  The Pattern it writes is:
# #    White, Yellow
# #    Orange
# #    Purple
# #    Blue, Blue Stripe
# #    Green, Green Stripe
# #    Brown
# #    Black
# #
# #  arguments:
# #  filename - the filename without path to write
# #  compsitMask - a mask made up of everything but the belts that you want
# #
# def writePattern6ToExcel(filename, compositMask):
#     fullpath = os.getcwd() + pathDelimiter() + "Sorted" + pathDelimiter() + filename
#     writer = pd.ExcelWriter(fullpath)
#     print(time.strftime("%X") + " Generating " + fullpath)
#
#     mask1 = mask_WhiteBelt & compositMask
#     mask2 = mask_YellowBelt & compositMask
#     mask = mask1 | mask2
#     wmk = newDataFrameFromMask(mask)
#     writeFormattedExcelSheet(wmk, writer, 'White, Yellow')
#
#     mask = mask_OrangeBelt & compositMask
#     wmk = newDataFrameFromMask(mask)
#     writeFormattedExcelSheet(wmk, writer, 'Orange')
#
#     mask = mask_PurpleBelt & compositMask
#     wmk = newDataFrameFromMask(mask)
#     writeFormattedExcelSheet(wmk, writer, 'Purple')
#
#     mask = mask_AllBlueBelt & compositMask
#     wmk = newDataFrameFromMask(mask)
#     writeFormattedExcelSheet(wmk, writer, 'Blue, Blue Stripe')
#
#     mask = mask_AllGreenBelt & compositMask
#     wmk = newDataFrameFromMask(mask)
#     writeFormattedExcelSheet(wmk, writer, 'Green, Green Stripe')
#
#     mask = mask_AllBrownBelt & compositMask
#     wmk = newDataFrameFromMask(mask)
#     writeFormattedExcelSheet(wmk, writer, 'Brown')
#
#     mask = mask_AllBlackBelt & compositMask
#     wmk = newDataFrameFromMask(mask)
#     writeFormattedExcelSheet(wmk, writer, 'Black')
#
#     # writer.save()
#     writer.close()
#     time.sleep(constants.SLEEP_TIME)

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



# ###############################################################################
# # writeWeaponsDivision1ToExcel
# #  arguments:
# #  filename - the filename without path to write
# #  compsitMask - a mask made up of everything but the belts that you want
# #
# def writeWeaponsDivision1ToExcel(filename, compositMask):
#     fullpath = os.getcwd() + pathDelimiter() + "Sorted" + pathDelimiter() + filename
#     writer = pd.ExcelWriter(fullpath)
#     print(time.strftime("%X") + " Generating " + fullpath)
#
#     mask1 = mask_WhiteBelt & compositMask
#     mask2 = mask_YellowBelt & compositMask
#     mask3 = mask_OrangeBelt & compositMask
#     mask4 = mask_PurpleBelt & compositMask
#     mask5 = mask_AllBlueBelt & compositMask
#     mask6 = mask_AllGreenBelt & compositMask
#     mask7 = mask_AllBrownBelt & compositMask
#     mask8 = mask_AllBlackBelt & compositMask
#
#     mask = mask1 | mask2 | mask3 | mask4 | mask5 | mask6 | mask7 | mask8
#
#     wmk = newDataFrameFromMask(mask)
#     writeFormattedExcelSheet(wmk, writer, 'Weapons Division 1')
#
#     # writer.save()
#     writer.close()
#     time.sleep(constants.SLEEP_TIME)

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


# ###############################################################################
# # writeWeaponsDivision1ToDetailReport
# #
# def writeWeaponsDivision1ToDetailReport(event_time, division_name, age, compositMask):
#     print(time.strftime("%X") + " Generating Detail Report PDF for " + event_time + " " + division_name + " " + age)
#
#     DivisionDetailReportPDF.DivisionDetailReportPDF.set_title("Weapons")
#
#     mask1 = mask_WhiteBelt & compositMask
#     mask2 = mask_YellowBelt & compositMask
#     mask3 = mask_OrangeBelt & compositMask
#     mask4 = mask_PurpleBelt & compositMask
#     mask5 = mask_AllBlueBelt & compositMask
#     mask6 = mask_AllGreenBelt & compositMask
#     mask7 = mask_AllBrownBelt & compositMask
#     mask8 = mask_AllBlackBelt & compositMask
#
#     mask = mask1 | mask2 | mask3 | mask4 | mask5 | mask6 | mask7 | mask8
#
#     wmk = newDataFrameFromMask(mask)
#     divison_detail_report_pdf.put_dataframe_on_pdfpage(wmk, "*TBA", event_time, division_name, age, "White - Jr. Black")


# ###############################################################################
# # writeWeaponsDivision1ToKataScoreSheet
# #
# def writeWeaponsDivision1ToKataScoreSheet(event_time, division_name, age, compositMask):
#     print(time.strftime("%X") + " Generating Kata Score Sheet PDF for " + event_time + " " + division_name + " " + age)
#
#     kata_score_sheet_pdf.KataScoreSheetPDF.set_title("Weapons")
#
#     mask1 = mask_WhiteBelt & compositMask
#     mask2 = mask_YellowBelt & compositMask
#     mask3 = mask_OrangeBelt & compositMask
#     mask4 = mask_PurpleBelt & compositMask
#     mask5 = mask_AllBlueBelt & compositMask
#     mask6 = mask_AllGreenBelt & compositMask
#     mask7 = mask_AllBrownBelt & compositMask
#     mask8 = mask_AllBlackBelt & compositMask
#
#     mask = mask1 | mask2 | mask3 | mask4 | mask5 | mask6 | mask7 | mask8
#
#     wmk = newDataFrameFromMask(mask)
#     kata_score_sheet.put_dataframe_on_pdfpage(wmk, "*TBA", event_time, division_name, age, "White - Jr. Black")


# ###############################################################################
# # writeWeaponsDivision2ToExcel
# #  arguments:
# #  filename - the filename without path to write
# #  compsitMask - a mask made up of everything but the belts that you want
# #
# def writeWeaponsDivision2ToExcel(filename, compositMask):
#     fullpath = os.getcwd() + pathDelimiter() + "Sorted" + pathDelimiter() + filename
#     writer = pd.ExcelWriter(fullpath)
#     print(time.strftime("%X") + " Generating " + fullpath)
#
#     mask1 = mask_WhiteBelt & compositMask
#     mask2 = mask_YellowBelt & compositMask
#     mask3 = mask_OrangeBelt & compositMask
#     mask4 = mask_PurpleBelt & compositMask
#     mask5 = mask_AllBlueBelt & compositMask
#     #    mask6= mask_AllGreenBelt & compositMask
#     #    mask7= mask_AllBrownBelt & compositMask
#     #    mask8= mask_AllBlackBelt & compositMask
#
#     #    mask = mask1 | mask2 | mask3 | mask4 | mask5 | mask6 | mask7 | mask8
#     mask = mask1 | mask2 | mask3 | mask4 | mask5
#
#     wmk = newDataFrameFromMask(mask)
#     #    wmk.to_excel(writer,'Weapons Division 2')
#     writeFormattedExcelSheet(wmk, writer, 'Weapons Division 2')
#
#     # writer.save()
#     writer.close()
#     time.sleep(constants.SLEEP_TIME)

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

    # rank_query = f"Rank == '{constants.WHITE_BELT}' or Rank == '{constants.YELLOW_BELT}'"
    # rank_query = f"Rank == '{constants.ORANGE_BELT}'"
    # rank_query = f"Rank == '{constants.PURPLE_BELT}'"
    # rank_query = f"Rank == '{constants.BLUE_BELT}' or Rank == '{constants.BLUE_STRIPE_BELT}'"
    # rank_query = f"Rank == '{constants.GREEN_BELT}' or Rank == '{constants.GREEN_STRIPE_BELT}'"
    # rank_query = f"Rank == '{constants.FIRST_DEGREE_BROWN_BELT}' or Rank == '{constants.SECOND_DEGREE_BROWN_BELT}' or Rank == '{constants.THIRD_DEGREE_BROWN_BELT}'"
    # rank_query = f"Rank == '{constants.FIRST_DEGREE_BLACK_BELT}' or Rank == '{constants.SECOND_DEGREE_BLACK_BELT}' or Rank == '{constants.THIRD_DEGREE_BLACK_BELT}' or Rank == '{constants.FOURTH_DEGREE_BLACK_BELT}' or Rank == '{constants.FIFTH_DEGREE_BLACK_BELT}' or Rank == '{constants.JUNIOR_BLACK_BELT}'"

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


# ###############################################################################
# # writeWeaponsDivision3ToExcel
# #  arguments:
# #  filename - the filename without path to write
# #  compsitMask - a mask made up of everything but the belts that you want
# #
# def writeWeaponsDivision3ToExcel(filename, compositMask):
#     fullpath = os.getcwd() + pathDelimiter() + "Sorted" + pathDelimiter() + filename
#     writer = pd.ExcelWriter(fullpath)
#     print(time.strftime("%X") + " Generating " + fullpath)
#
#     mask1 = mask_AllGreenBelt & compositMask
#     mask2 = mask_AllBrownBelt & compositMask
#     mask3 = mask_AllBlackBelt & compositMask
#
#     mask = mask1 | mask2 | mask3
#
#     wmk = newDataFrameFromMask(mask)
#     writeFormattedExcelSheet(wmk, writer, 'Weapons Division 3')
#
#     # writer.save()
#     writer.close()
#     time.sleep(constants.SLEEP_TIME)

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


# ###############################################################################
# # writeWeaponsDivision4ToExcel
# #  arguments:
# #  filename - the filename without path to write
# #  compsitMask - a mask made up of everything but the belts that you want
# #
# def writeWeaponsDivision4ToExcel(filename, compositMask):
#     fullpath = os.getcwd() + pathDelimiter() + "Sorted" + pathDelimiter() + filename
#     writer = pd.ExcelWriter(fullpath)
#     print(time.strftime("%X") + " Generating " + fullpath)
#
#     mask1 = mask_WhiteBelt & compositMask
#     mask2 = mask_YellowBelt & compositMask
#     mask3 = mask_OrangeBelt & compositMask
#     mask4 = mask_PurpleBelt & compositMask
#     mask5 = mask_AllBlueBelt & compositMask
#
#     mask = mask1 | mask2 | mask3 | mask4 | mask5
#
#     wmk = newDataFrameFromMask(mask)
#     writeFormattedExcelSheet(wmk, writer, 'Weapons Division 4')
#
#     # writer.save()
#     writer.close()
#     time.sleep(constants.SLEEP_TIME)

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



# ###############################################################################
# # writeWeaponsDivision4ToDetailReport
# #
# def writeWeaponsDivision4ToDetailReport(event_time, division_name, age, compositMask):
#     print(time.strftime("%X") + " Generating Detail Report PDF for " + event_time + " " + division_name + " " + age)
#
#     DivisionDetailReportPDF.DivisionDetailReportPDF.set_title("Weapons")
#
#     mask1 = mask_WhiteBelt & compositMask
#     mask2 = mask_YellowBelt & compositMask
#     mask3 = mask_OrangeBelt & compositMask
#     mask4 = mask_PurpleBelt & compositMask
#     mask5 = mask_AllBlueBelt & compositMask
#
#     mask = mask1 | mask2 | mask3 | mask4 | mask5
#
#     wmk = newDataFrameFromMask(mask)
#     divison_detail_report_pdf.put_dataframe_on_pdfpage(wmk, "*TBA", event_time, division_name, age,
#                                                        "White - Blue w/Green Stripe")


# ###############################################################################
# # writeWeaponsDivision4ToKataScoreSheet
# #
# def writeWeaponsDivision4ToKataScoreSheet(event_time, division_name, age, compositMask):
#     print(time.strftime("%X") + " Generating Kata Score Sheet PDF for " + event_time + " " + division_name + " " + age)
#
#     kata_score_sheet_pdf.KataScoreSheetPDF.set_title("Weapons")
#
#     mask1 = mask_WhiteBelt & compositMask
#     mask2 = mask_YellowBelt & compositMask
#     mask3 = mask_OrangeBelt & compositMask
#     mask4 = mask_PurpleBelt & compositMask
#     mask5 = mask_AllBlueBelt & compositMask
#
#     mask = mask1 | mask2 | mask3 | mask4 | mask5
#
#     wmk = newDataFrameFromMask(mask)
#     kata_score_sheet.put_dataframe_on_pdfpage(wmk, "*TBA", event_time, division_name, age, "White - Blue w/Green Stripe")


# ###############################################################################
# #  writeWeaponsDivision5ToExcel  18+ year Blue and Green
# #  arguments:
# #  filename - the filename without path to write
# #  compsitMask - a mask made up of everything but the belts that you want
# #
# def writeWeaponsDivision5ToExcel(filename, compositMask):
#     fullpath = os.getcwd() + pathDelimiter() + "Sorted" + pathDelimiter() + filename
#     print(time.strftime("%X") + " Generating " + fullpath)
#     writer = pd.ExcelWriter(fullpath)
#
#     mask1 = mask_WhiteBelt & compositMask
#     mask2 = mask_YellowBelt & compositMask
#     mask3 = mask_OrangeBelt & compositMask
#     mask4 = mask_PurpleBelt & compositMask
#     mask5 = mask_AllBlueBelt & compositMask
#
#     mask = mask1 | mask2 | mask3 | mask4 | mask5
#
#     wmk = newDataFrameFromMask(mask)
#     writeFormattedExcelSheet(wmk, writer, 'Weapons Division 5')
#
#     #writer.save()
#     writer.close()
#     time.sleep(constants.SLEEP_TIME)

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



# ###############################################################################
# # writeWeaponsDivision5ToDetailReport
# #
# def writeWeaponsDivision5ToDetailReport(event_time, division_name, age, compositMask):
#     print(time.strftime("%X") + " Generating Detail Report PDF for " + event_time + " " + division_name + " " + age)
#
#     DivisionDetailReportPDF.DivisionDetailReportPDF.set_title("Weapons")
#
#     mask1 = mask_WhiteBelt & compositMask
#     mask2 = mask_YellowBelt & compositMask
#     mask3 = mask_OrangeBelt & compositMask
#     mask4 = mask_PurpleBelt & compositMask
#     mask5 = mask_AllBlueBelt & compositMask
#
#     mask = mask1 | mask2 | mask3 | mask4 | mask5
#
#     wmk = newDataFrameFromMask(mask)
#
#     divison_detail_report_pdf.put_dataframe_on_pdfpage(wmk, "*TBA", event_time, division_name, age,
#                                                        "White - Blue w/Green Stripe")
#

# ###############################################################################
# # writeWeaponsDivision5ToKataScoreSheet
# #
# def writeWeaponsDivision5ToKataScoreSheet(event_time, division_name, age, compositMask):
#     print(time.strftime("%X") + " Generating Kata Score Sheet PDF for " + event_time + " " + division_name + " " + age)
#
#     kata_score_sheet_pdf.KataScoreSheetPDF.set_title("Weapons")
#
#     mask1 = mask_WhiteBelt & compositMask
#     mask2 = mask_YellowBelt & compositMask
#     mask3 = mask_OrangeBelt & compositMask
#     mask4 = mask_PurpleBelt & compositMask
#     mask5 = mask_AllBlueBelt & compositMask
#
#     mask = mask1 | mask2 | mask3 | mask4 | mask5
#
#     wmk = newDataFrameFromMask(mask)
#
#     kata_score_sheet.put_dataframe_on_pdfpage(wmk, "*TBA", event_time, division_name, age, "White - Blue w/Green Stripe")


# ###############################################################################
# #  writeWeaponsDivision6ToExcel
# #  arguments:
# #  filename - the filename without path to write
# #  compsitMask - a mask made up of everything but the belts that you want
# #
# def writeWeaponsDivision6ToFile(filename, compositMask):
#     fullpath = os.getcwd() + pathDelimiter() + "Sorted" + pathDelimiter() + filename
#     writer = pd.ExcelWriter(fullpath)
#     print(time.strftime("%X") + " Generating " + fullpath)
#
#     mask1 = mask_AllGreenBelt & compositMask
#     # mask2= mask_AllBrownBelt & compositMask
#     mask = mask1  # | mask2
#     wmk = newDataFrameFromMask(mask)
#     writeFormattedExcelSheet(wmk, writer, 'Weapons Division 6')
#
#     ##writer.save()
#     writer.close()
#     time.sleep(constants.SLEEP_TIME)

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


# ###############################################################################
# # writeWeaponsDivision6ToDetailReport
# #
# def writeWeaponsDivision6ToDetailReport(event_time, division_name, age, compositMask):
#     print(time.strftime("%X") + " Generating Detail Report PDF for " + event_time + " " + division_name + " " + age)
#
#     DivisionDetailReportPDF.DivisionDetailReportPDF.set_title("Weapons")
#
#     mask1 = mask_AllGreenBelt & compositMask
#     # mask2= mask_AllBrownBelt & compositMask
#     mask = mask1  # | mask2
#     wmk = newDataFrameFromMask(mask)
#
#     divison_detail_report_pdf.put_dataframe_on_pdfpage(wmk, "*TBA", event_time, division_name, age, "Green")


# ###############################################################################
# # writeWeaponsDivision6ToKataScoreSheet
# #
# def writeWeaponsDivision6ToKataScoreSheet(event_time, division_name, age, compositMask):
#     print(time.strftime("%X") + " Generating Kata Score Sheet PDF for " + event_time + " " + division_name + " " + age)
#
#     kata_score_sheet_pdf.KataScoreSheetPDF.set_title("Weapons")
#
#     mask1 = mask_AllGreenBelt & compositMask
#     # mask2= mask_AllBrownBelt & compositMask
#     mask = mask1  # | mask2
#     wmk = newDataFrameFromMask(mask)
#
#     kata_score_sheet.put_dataframe_on_pdfpage(wmk, "tba", event_time, division_name, age, "Green")


# ###############################################################################
# #  writeWeaponsDivision7ToExcel
# #  arguments:
# #  filename - the filename without path to write
# #  compsitMask - a mask made up of everything but the belts that you want
# #
# def writeWeaponsDivision7ToFile(filename, compositMask):
#     fullpath = os.getcwd() + pathDelimiter() + "Sorted" + pathDelimiter() + filename
#     writer = pd.ExcelWriter(fullpath)
#     print(time.strftime("%X") + " Generating " + fullpath)
#
#     mask = mask_AllBrownBelt & compositMask
#     wmk = newDataFrameFromMask(mask)
#     writeFormattedExcelSheet(wmk, writer, 'Weapons Division 7')
#
#     #writer.save()
#     writer.close()
#     time.sleep(constants.SLEEP_TIME)

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


# ###############################################################################
# # writeWeaponsDivision7ToDetailReport
# #
# def writeWeaponsDivision7ToDetailReport(event_time, division_name, age, compositMask):
#     print(time.strftime("%X") + " Generating Detail Report PDF for " + event_time + " " + division_name + " " + age)
#
#     DivisionDetailReportPDF.DivisionDetailReportPDF.set_title("Weapons")
#
#     mask = mask_AllBrownBelt & compositMask
#     wmk = newDataFrameFromMask(mask)
#
#     divison_detail_report_pdf.put_dataframe_on_pdfpage(wmk, "*TBA", event_time, division_name, age, "Brown")


# ###############################################################################
# # writeWeaponsDivision7ToKataScoreSheet
# #
# def writeWeaponsDivision7ToKataScoreSheet(event_time, division_name, age, compositMask):
#     print(time.strftime("%X") + " Generating Kata Score Sheet PDF for " + event_time + " " + division_name + " " + age)
#
#     kata_score_sheet_pdf.KataScoreSheetPDF.set_title("Weapons")
#
#     #  mask1= mask_AllGreenBelt & compositMask
#     mask = mask_AllBrownBelt & compositMask
#     wmk = newDataFrameFromMask(mask)
#
#     kata_score_sheet.put_dataframe_on_pdfpage(wmk, "tba", event_time, division_name, age, "Brown")


# ###############################################################################
# #  writeWeaponsDivision8ToExcel
# #  arguments:
# #  filename - the filename without path to write
# #  compsitMask - a mask made up of everything but the belts that you want
# #
# def writeWeaponsDivision8ToFile(filename, compositMask):
#     fullpath = os.getcwd() + pathDelimiter() + "Sorted" + pathDelimiter() + filename
#     writer = pd.ExcelWriter(fullpath)
#     print(time.strftime("%X") + " Generating " + fullpath)
#
#     mask1 = mask_AllBlackBelt & compositMask
#     mask = mask1
#     wmk = newDataFrameFromMask(mask)
#     writeFormattedExcelSheet(wmk, writer, 'Weapons Division 8')
#
#     # writer.save()
#     writer.close()
#     time.sleep(constants.SLEEP_TIME)


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

# ###############################################################################
# # writeWeaponsDivision8ToDetailReport
# #
# def writeWeaponsDivision8ToDetailReport(event_time, division_name, age, compositMask):
#     print(time.strftime("%X") + " Generating Detail Report PDF for " + event_time + " " + division_name + " " + age)
#
#     DivisionDetailReportPDF.DivisionDetailReportPDF.set_title("Weapons")
#
#     mask1 = mask_AllBlackBelt & compositMask
#     mask = mask1
#     wmk = newDataFrameFromMask(mask)
#
#     divison_detail_report_pdf.put_dataframe_on_pdfpage(wmk, "*TBA", event_time, division_name, age, "Jr Black & Black")


# ###############################################################################
# # writeWeaponsDivision8ToKataScoreSheet
# #
# def writeWeaponsDivision8ToKataScoreSheet(event_time, division_name, age, compositMask):
#     print(time.strftime("%X") + " Generating Kata Score Sheet PDF for " + event_time + " " + division_name + " " + age)
#
#     kata_score_sheet_pdf.KataScoreSheetPDF.set_title("Weapons")
#
#     mask1 = mask_AllBlackBelt & compositMask
#     mask = mask1
#     wmk = newDataFrameFromMask(mask)
#
#     kata_score_sheet.put_dataframe_on_pdfpage(wmk, "tba", event_time, division_name, age, "Jr. Black & Black")

# ###############################################################################
# #  writeWeaponsDivision9ToExcel
# #  arguments:
# #  filename - the filename without path to write
# #  compsitMask - a mask made up of everything but the belts that you want
# #
# def writeWeaponsDivision9ToFile(filename, compositMask):
#     fullpath = os.getcwd() + pathDelimiter() + "Sorted" + pathDelimiter() + filename
#     writer = pd.ExcelWriter(fullpath)
#     print(time.strftime("%X") + " Generating " + fullpath)
#
#     mask1 = mask_AllBlackBelt & compositMask
#     mask = mask1
#     wmk = newDataFrameFromMask(mask)
#     writeFormattedExcelSheet(wmk, writer, 'Weapons Division 9')
#
#     # writer.save()
#     writer.close()
#     time.sleep(constants.SLEEP_TIME)

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



# ###############################################################################
# # writeWeaponsDivision9ToDetailReport
# #
# def writeWeaponsDivision9ToDetailReport(event_time, division_name, age, compositMask):
#     print(time.strftime("%X") + " Generating Detail Report PDF for " + event_time + " " + division_name + " " + age)
#
#     DivisionDetailReportPDF.DivisionDetailReportPDF.set_title("Weapons")
#
#     mask1 = mask_AllBlackBelt & compositMask
#     mask = mask1
#     wmk = newDataFrameFromMask(mask)
#
#     divison_detail_report_pdf.put_dataframe_on_pdfpage(wmk, "*TBA", event_time, division_name, age, "Black")


# ###############################################################################
# # writeWeaponsDivision9ToKataScoreSheet
# #
# def writeWeaponsDivision9ToKataScoreSheet(event_time, division_name, age, compositMask):
#     print(time.strftime("%X") + " Generating Kata Score Sheet PDF for " + event_time + " " + division_name + " " + age)
#
#     kata_score_sheet_pdf.KataScoreSheetPDF.set_title("Weapons")
#
#     mask1 = mask_AllBlackBelt & compositMask
#     mask = mask1
#     wmk = newDataFrameFromMask(mask)
#
#     kata_score_sheet.put_dataframe_on_pdfpage(wmk, "tba", event_time, division_name, age, "Black")


# def writeSparingTreeToExcel(filename, compositMask):
#     fullpath = os.getcwd() + pathDelimiter() + "Sorted" + pathDelimiter() + filename
#     writer = pd.ExcelWriter(fullpath)
#     print(time.strftime("%X") + " Generating " + fullpath)
#
#     wmk = newDataFrameFromMask(compositMask)
#
#     byDojo = wmk.groupby('Dojo')
#
#     print(byDojo.size())
#
#     # writer.save()
#     writer.close()
#     time.sleep(constants.SLEEP_TIME)


###############################################################################
#
# Main Function
#

# get the filename from the environment var named  tourname_filename

#assert False
# Last thing you did is update the hit counter
# The next thing you need to do is remove all the weapons division code that doesnt use queries - look for composit mask
# Once thats done check that all references to compositMask are commented out, and everything still works.  Then you
# can comment out all the masking.
# Once that all works - check it in, then go back and delete all the dead code

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


# ####################
# # Filtering        #
# ####################
#
#
# ###############################################################################
# #  Define all the atomic masks for filtering
#
# # Atomic masks for Belts
# mask_WhiteBelt = clean_df['Rank'] == 'White'
# mask_YellowBelt = clean_df['Rank'] == 'Yellow'
# mask_OrangeBelt = clean_df['Rank'] == 'Orange'
# mask_PurpleBelt = clean_df['Rank'] == 'Purple'
# mask_BlueBelt = clean_df['Rank'] == 'Blue'
# mask_BlueStripeBelt = clean_df['Rank'] == 'Blue w/Stripe'
# mask_AllBlueBelt = mask_BlueBelt | mask_BlueStripeBelt  # all blue and blue stripe
# # testBluedf=newDataFrameFromMask( mask_AllBlueBelt )
# mask_GreenBelt = clean_df['Rank'] == 'Green'
# mask_GreenStripeBelt = clean_df['Rank'] == 'Green w/Stripe'
# mask_AllGreenBelt = mask_GreenBelt | mask_GreenStripeBelt  # all Green and Green stripe
# # testGreendf=newDataFrameFromMask( mask_AllGreenBelt )
# mask_3rdBrownBelt = clean_df['Rank'] == 'Brown 3rd Degree'
# mask_2ndBrownBelt = clean_df['Rank'] == 'Brown 2nd Degree'
# mask_1stBrownBelt = clean_df['Rank'] == 'Brown 1st Degree'
# mask_AllBrownBelt = mask_3rdBrownBelt | mask_2ndBrownBelt | mask_1stBrownBelt  # all 1st 2nd and 3rd Brown
# # testBrowndf=newDataFrameFromMask( mask_AllBrownBelt )
# mask_1stBlackBelt = clean_df['Rank'] == 'Black 1st Degree'
# mask_2ndBlackBelt = clean_df['Rank'] == 'Black 2nd Degree'
# mask_3rdBlackBelt = clean_df['Rank'] == 'Black 3rd Degree'
# mask_4thBlackBelt = clean_df['Rank'] == 'Black 4th Degree'
# mask_5thBlackBelt = clean_df['Rank'] == 'Black 5th Degree'
# mask_JrBlackBelt = clean_df['Rank'] == 'Black Junior'
# mask_AllBlackBelt = mask_1stBlackBelt | mask_2ndBlackBelt | mask_3rdBlackBelt | mask_4thBlackBelt | mask_5thBlackBelt | mask_JrBlackBelt  # all Jr, 1st, 2nd, and 3rd degree black
# # testBlackdf=newDataFrameFromMask( mask_AllBlackBelt )
#
# # Atomic mask for Gender
# mask_Male = clean_df['Gender'] == 'Male'
# mask_Female = clean_df['Gender'] == 'Female'
#
# # Atomic and composit mask for which event Sparring, Kata, Weapons
# mask_SparringAndForms = clean_df['Events'] == '2 Events - Forms & Sparring ($75)'
# mask_FormsOnly = clean_df['Events'] == '1 Event - Forms ($75)'
# mask_SparringOnly = clean_df['Events'] == '1 Event - Sparring ($75)'
# # Mask for Weapons
# mask_Weapons = clean_df['Weapons'] == 'Weapons ($35)'
# # testdf = clean_df[['First_Name', 'Last_Name', 'Gender', 'Rank', 'Age', 'Weight', 'Height', 'Events', 'Weapons']][mask_Weapons]
#
# # Composit Masks for Sparring or Forms
# mask_Sparring = mask_SparringAndForms | mask_SparringOnly
# mask_Forms = mask_SparringAndForms | mask_FormsOnly
# # testdf=cdf[['First_Name','Last_Name', 'Gender','Rank','Age','Competitor\'s Weight (in lbs.)?','Competitor\'s Height (in feet and inches)?','Events','Weapons']][mask_Forms]
#
# # Atomic mask for age groups found in the tournament guide
# # 4-6 used for kids kata, kids sparring,
# maskLowAge = clean_df["Age"] >= 3
# maskHighAge = clean_df["Age"] <= 6
# mask_Age4to6 = maskLowAge & maskHighAge
# # testdf=cdf[['First_Name','Last_Name', 'Gender','Rank','Age','Competitor\'s Weight (in lbs.)?','Competitor\'s Height (in feet and inches)?','Events','Weapons']][mask_Age4to6]
#
# # 7-9 used in Youth Kata, Young Girl's Sparring, Youth Boy's Sparring
# maskLowAge = clean_df["Age"] >= 7
# maskHighAge = clean_df["Age"] <= 9
# mask_Age7to9 = maskLowAge & maskHighAge
# # testdf=cdf[['First_Name','Last_Name', 'Gender','Rank','Age','Competitor\'s Weight (in lbs.)?','Competitor\'s Height (in feet and inches)?','Events','Weapons']][mask_Age7to9]
#
#
# # 4-8 used for Weapons Division 1 - new added for Fall 2017
# maskLowAge = clean_df["Age"] >= 4
# maskHighAge = clean_df["Age"] <= 8
# mask_Age4to8 = maskLowAge & maskHighAge
#
# # 7-8 used in Youth Kata, Young Girl's Sparring, Youth Boy's Sparring - new added for Fall 2017
# maskLowAge = clean_df["Age"] >= 7
# maskHighAge = clean_df["Age"] <= 8
# mask_Age7to8 = maskLowAge & maskHighAge
#
# # 9-11 used in Youth Kata, Young Girl's Sparring, Youth Boy's Sparring - new added for Fall 2017
# maskLowAge = clean_df["Age"] >= 9
# maskHighAge = clean_df["Age"] <= 11
# mask_Age9to11 = maskLowAge & maskHighAge
#
# # 12-14 used in Youth Kata, Young Girl's Sparring, Youth Boy's Sparring - new added for Fall 2017
# maskLowAge = clean_df["Age"] >= 12
# maskHighAge = clean_df["Age"] <= 14
# mask_Age12to14 = maskLowAge & maskHighAge
#
# # 12-17 used in Weapons Division 4 - new added for Fall 2017
# maskLowAge = clean_df["Age"] >= 12
# maskHighAge = clean_df["Age"] <= 17
# mask_Age12to17 = maskLowAge & maskHighAge
#
# # 15-17 used in Youth Kata, Young Girl's Sparring, Youth Boy's Sparring - new added for Fall 2017
# maskLowAge = clean_df["Age"] >= 15
# maskHighAge = clean_df["Age"] <= 17
# mask_Age15to17 = maskLowAge & maskHighAge
#
# # 10-12 used in Boy's Sparring, Boy's & Girl's Kata, Girl's Sparring
# maskLowAge = clean_df["Age"] >= 10
# maskHighAge = clean_df["Age"] <= 12
# mask_Age10to12 = maskLowAge & maskHighAge
# # testdf=cdf[['First_Name','Last_Name', 'Gender','Rank','Age','Competitor\'s Weight (in lbs.)?','Competitor\'s Height (in feet and inches)?','Events','Weapons']][mask_Age10to12]
#
# # 13-15 used in Teen Girl's Sparring, Teen Kata, Teen Boy's Sparring,
# maskLowAge = clean_df["Age"] >= 13
# maskHighAge = clean_df["Age"] <= 15
# mask_Age13to15 = maskLowAge & maskHighAge
# # testdf=cdf[['First_Name','Last_Name', 'Gender','Rank','Age','Competitor\'s Weight (in lbs.)?','Competitor\'s Height (in feet and inches)?','Events','Weapons']][mask_Age13to15]
#
# # 4-9 used in Weapons Division 1
# maskLowAge = clean_df["Age"] >= 4
# maskHighAge = clean_df["Age"] <= 9
# mask_Age4to9 = maskLowAge & maskHighAge
# # testdf=cdf[['First_Name','Last_Name', 'Gender','Rank','Age','Competitor\'s Weight (in lbs.)?','Competitor\'s Height (in feet and inches)?','Events','Weapons']][mask_Age4to9]
#
# # 18-39 used in Womans Sprring, Men and Women's Kata
# maskLowAge = clean_df["Age"] >= 18
# maskHighAge = clean_df["Age"] <= 39
# mask_Age18to39 = maskLowAge & maskHighAge
# # testdf=cdf[['First_Name','Last_Name', 'Gender','Rank','Age','Competitor\'s Weight (in lbs.)?','Competitor\'s Height (in feet and inches)?','Events','Weapons']][mask_Age18to39]
#
# # 40 plus used in Senior Men's Sparring, Senior Women's Sparring, Senior Kata
# mask_Age40Plus = clean_df["Age"] >= 40
# # testdf=cdf[['First_Name','Last_Name', 'Gender','Rank','Age','Competitor\'s Weight (in lbs.)?','Competitor\'s Height (in feet and inches)?','Events','Weapons']][mask_Age40Plus]
#
# # 16-17 used in Young Adult Kata, Young Men's Sparring, Young Adult Women's Sparring
# maskLowAge = clean_df["Age"] >= 16
# maskHighAge = clean_df["Age"] <= 17
# mask_Age16to17 = maskLowAge & maskHighAge
# # testdf=cdf[['First_Name','Last_Name', 'Gender','Rank','Age','Competitor\'s Weight (in lbs.)?','Competitor\'s Height (in feet and inches)?','Events','Weapons']][mask_Age16to17]
#
# # 13-17 used in Weapons Division 3
# maskLowAge = clean_df["Age"] >= 13
# maskHighAge = clean_df["Age"] <= 17
# mask_Age13to17 = maskLowAge & maskHighAge
# # testdf=cdf[['First_Name','Last_Name', 'Gender','Rank','Age','Competitor\'s Weight (in lbs.)?','Competitor\'s Height (in feet and inches)?','Events','Weapons']][mask_Age13to17]
#
# # 18 plus used in Weapons Division 4 and 5
# mask_Age18Plus = clean_df["Age"] >= 18
# # testdf=cdf[['First_Name','Last_Name', 'Gender','Rank','Age','Competitor\'s Weight (in lbs.)?','Competitor\'s Height (in feet and inches)?','Events','Weapons']][mask_Age18Plus]
#
# # 13 plus used in Weapons Division 6
# mask_Age13Plus = clean_df["Age"] >= 13
# # testdf=cdf[['First_Name','Last_Name', 'Gender','Rank','Age','Competitor\'s Weight (in lbs.)?','Competitor\'s Height (in feet and inches)?','Events','Weapons']][mask_Age13Plus]
#
# # 12 plus used in Weapons Division 6 and Weapons Division 7 - new added for Fall 2017
# mask_Age12Plus = clean_df["Age"] >= 12
# # testdf=cdf[['First_Name','Last_Name', 'Gender','Rank','Age','Competitor\'s Weight (in lbs.)?','Competitor\'s Height (in feet and inches)?','Events','Weapons']][mask_Age13Plus]


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
    # compositMask = mask_Forms & mask_Age4to6
    # writePattern4ToExcel("KidsKata.xlsx", compositMask)
    writePattern4ToExcelViaQuery(filename="KidsKata.xlsx", division_type='Forms', gender="*",minimum_age=4, maximum_age=6)

    writeSingleKataScoreSheetandDivisionReport(event_time="9:00am",division_name="Kids Kata",gender="*",rank_label="White",                     minimum_age=4, maximum_age=6, rings=[1],  ranks=[constants.WHITE_BELT], clean_df=clean_df)
    writeSingleKataScoreSheetandDivisionReport(event_time="9:00am",division_name="Kids Kata",gender="*",rank_label="Yellow",                    minimum_age=4, maximum_age=6, rings=[2,3],ranks=[constants.YELLOW_BELT], clean_df=clean_df)
    writeSingleKataScoreSheetandDivisionReport(event_time="9:00am",division_name="Kids Kata",gender="*",rank_label="Orange",                    minimum_age=4, maximum_age=6, rings=[4,5],ranks=[constants.ORANGE_BELT], clean_df=clean_df)
    writeSingleKataScoreSheetandDivisionReport(event_time="9:00am",division_name="Kids Kata",gender="*",rank_label="Purple, Blue, Blue/Stripe", minimum_age=4, maximum_age=6, rings=[6],  ranks=[constants.PURPLE_BELT,constants.BLUE_BELT,constants.BLUE_STRIPE_BELT], clean_df=clean_df)
    writeSingleKataScoreSheetandDivisionReport(event_time="9:00am",division_name="Kids Kata",gender="*",rank_label="Green, Green/Stripe, Brown",minimum_age=4, maximum_age=6, rings=[7],  ranks=[constants.GREEN_BELT,constants.GREEN_STRIPE_BELT,constants.THIRD_DEGREE_BROWN_BELT,constants.SECOND_DEGREE_BROWN_BELT,constants.FIRST_DEGREE_BROWN_BELT], clean_df=clean_df)


    ###############################################################################
    # Youth Kata  - 7-8 year olds
    #
    # compositMask = mask_Forms & mask_Age7to8
    # writePattern5ToExcel("YouthKata.xlsx", compositMask)
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
    # compositMask = mask_Sparring & mask_Age4to6
    # writePattern4ToExcel("KidsSparring.xlsx", compositMask)
    writePattern4ToExcelViaQuery(filename="KidsSparring.xlsx", division_type='Sparring', gender="*",minimum_age=4, maximum_age=6)

    writeSingleSparringTreeandDivisionReport(event_time="9:45am",division_name="Kids Sparring",gender="*", rank_label="White",                     minimum_age=4, maximum_age=6, rings=[1],     ranks=[constants.WHITE_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="9:45am",division_name="Kids Sparring",gender="*", rank_label="Yellow",                    minimum_age=4, maximum_age=6, rings=[2,3],  ranks=[constants.YELLOW_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="9:45am",division_name="Kids Sparring",gender="*", rank_label="Orange",                    minimum_age=4, maximum_age=6, rings=[4,5],  ranks=[constants.ORANGE_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="9:45am",division_name="Kids Sparring",gender="*", rank_label="Purple, Blue, Blue/Stripe", minimum_age=4, maximum_age=6, rings=[6],  ranks=[constants.PURPLE_BELT,constants.BLUE_BELT,constants.BLUE_STRIPE_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="9:45am",division_name="Kids Sparring",gender="*", rank_label="Green, Green/Stripe, Brown", minimum_age=4, maximum_age=6, rings=[7],  ranks=[constants.GREEN_BELT,constants.GREEN_STRIPE_BELT,constants.THIRD_DEGREE_BROWN_BELT,constants.SECOND_DEGREE_BROWN_BELT,constants.FIRST_DEGREE_BROWN_BELT],clean_df=clean_df)


    ###############################################################################
    # Boy's & Girl's Kata  - 9-11 year olds
    #
    # compositMask = mask_Forms & mask_Age9to11
    # writePattern6ToExcel("BoysGirlsKata.xlsx", compositMask)
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
    # compositMask = mask_Sparring & mask_Female & mask_Age7to8
    # writePattern3ToExcel("YouthGirlSparring.xlsx", compositMask)
    writePattern3ToExcelViaQuery(filename="YouthGirlSparring.xlsx", division_type='Forms', gender="Female",minimum_age=7, maximum_age=8)

    writeSingleSparringTreeandDivisionReport(event_time="10:30am",division_name="Youth Girl's Sparring",gender="Female", rank_label="White, Yellow",             minimum_age=7, maximum_age=8, rings=[1], ranks=[constants.WHITE_BELT,constants.YELLOW_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="10:30am",division_name="Youth Girl's Sparring",gender="Female", rank_label="Orange",                    minimum_age=7, maximum_age=8, rings=[2], ranks=[constants.ORANGE_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="10:30am",division_name="Youth Girl's Sparring",gender="Female", rank_label="Purple",                    minimum_age=7, maximum_age=8, rings=[3], ranks=[constants.PURPLE_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="10:30am",division_name="Youth Girl's Sparring",gender="Female", rank_label="Blue, Blue/Stripe",         minimum_age=7, maximum_age=8, rings=[4], ranks=[constants.BLUE_BELT,constants.BLUE_STRIPE_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="10:30am",division_name="Youth Girl's Sparring",gender="Female", rank_label="Green, Green/Stripe, Brown",minimum_age=7, maximum_age=8, rings=[5], ranks=[constants.GREEN_BELT,constants.GREEN_STRIPE_BELT,constants.THIRD_DEGREE_BROWN_BELT,constants.SECOND_DEGREE_BROWN_BELT,constants.FIRST_DEGREE_BROWN_BELT],clean_df=clean_df)

    ###############################################################################
    # Youth Boy's Sparring - 7-8 year olds
    #
    # compositMask = mask_Sparring & mask_Male & mask_Age7to8
    # writePattern3ToExcel("YouthBoysSparring.xlsx", compositMask)
    writePattern3ToExcelViaQuery(filename="YouthBoysSparring.xlsx", division_type='Forms', gender="Male",minimum_age=7, maximum_age=8)

    writeSingleSparringTreeandDivisionReport(event_time="10:30am",division_name="Youth Boy's Sparring",gender="Male", rank_label="White, Yellow",             minimum_age=7, maximum_age=8, rings=[6], ranks=[constants.WHITE_BELT,constants.YELLOW_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="10:30am",division_name="Youth Boy's Sparring",gender="Male", rank_label="Orange",                    minimum_age=7, maximum_age=8, rings=[7], ranks=[constants.ORANGE_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="10:30am",division_name="Youth Boy's Sparring",gender="Male", rank_label="Purple",                    minimum_age=7, maximum_age=8, rings=[8], ranks=[constants.PURPLE_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="10:30am",division_name="Youth Boy's Sparring",gender="Male", rank_label="Blue, Blue/Stripe",         minimum_age=7, maximum_age=8, rings=[9], ranks=[constants.BLUE_BELT,constants.BLUE_STRIPE_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="10:30am",division_name="Youth Boy's Sparring",gender="Male", rank_label="Green, Green/Stripe, Brown",minimum_age=7, maximum_age=8, rings=[10], ranks=[constants.GREEN_BELT,constants.GREEN_STRIPE_BELT,constants.THIRD_DEGREE_BROWN_BELT,constants.SECOND_DEGREE_BROWN_BELT,constants.FIRST_DEGREE_BROWN_BELT],clean_df=clean_df)

    ###############################################################################
    # Girl's Sparring - 9-11 year olds
    #
    # compositMask = mask_Sparring & mask_Age9to11 & mask_Female
    # writePattern1ToExcel("GirlsSparring.xlsx", compositMask)
    writePattern1ToExcelViaQuery(filename="GirlsSparring.xlsx", division_type='Sparring', gender="Female",minimum_age=9, maximum_age=11)

    writeSingleSparringTreeandDivisionReport(event_time="10:30am",division_name="Girl's Sparring",gender="Female", rank_label="White, Yellow, Orange",     minimum_age=9, maximum_age=11, rings=[11], ranks=[constants.WHITE_BELT,constants.YELLOW_BELT,constants.ORANGE_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="10:30am",division_name="Girl's Sparring",gender="Female", rank_label="Purple, Blue, Blue/Stripe", minimum_age=9, maximum_age=11, rings=[12], ranks=[constants.PURPLE_BELT,constants.BLUE_BELT,constants.BLUE_STRIPE_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="10:30am",division_name="Girl's Sparring",gender="Female", rank_label="Green, Green/Stripe, Brown",minimum_age=9, maximum_age=11, rings=[13], ranks=[constants.GREEN_BELT,constants.GREEN_STRIPE_BELT,constants.THIRD_DEGREE_BROWN_BELT,constants.SECOND_DEGREE_BROWN_BELT,constants.FIRST_DEGREE_BROWN_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="10:30am",division_name="Girl's Sparring",gender="Female", rank_label="Jr. Black",                 minimum_age=9, maximum_age=11, rings=[14], ranks=[constants.JUNIOR_BLACK_BELT,constants.FIRST_DEGREE_BLACK_BELT,constants.SECOND_DEGREE_BLACK_BELT,constants.THIRD_DEGREE_BLACK_BELT,constants.FOURTH_DEGREE_BLACK_BELT,constants.FIFTH_DEGREE_BLACK_BELT],clean_df=clean_df)

    ### 11:15 Events

    ###############################################################################
    # Boy's Sparring - 9-11 year olds
    #
    # compositMask = mask_Sparring & mask_Age9to11 & mask_Male
    # writePattern6ToExcel("BoysSparring.xlsx", compositMask)
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
    # compositMask = mask_Weapons & mask_Age4to8
    # writeWeaponsDivision1ToExcel("WeaponsDivision1.xlsx", compositMask)
    writeWeaponsDivision1ToExcelViaQuery(filename="WeaponsDivision1.xlsx", division_type='Weapons', gender="*",minimum_age=4, maximum_age=8)

    # writeWeaponsDivision1ToDetailReport("11:15am", "Weapons Division 1", "4-8", compositMask)
    # writeWeaponsDivision1ToKataScoreSheet("11:15am", "Weapons Division 1", "4-8", compositMask)
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
    # compositMask = mask_Weapons & mask_Age9to11
    # writeWeaponsDivision2ToExcel("WeaponsDivision2.xlsx", compositMask)
    writeWeaponsDivision2ToExcelViaQuery(filename="WeaponsDivision2.xlsx", division_type='Weapons', gender="*",minimum_age=9, maximum_age=11)

    # writeWeaponsDivision2ToDetailReport("11:15am", "Weapons Division 2: White - Blue Stripe", "9-11", compositMask)
    # writeWeaponsDivision2ToKataScoreSheet("11:15am", "Weapons Division 2: White - Blue Stripe", "9-11", compositMask)


    writeWeaponsDivisionToSingleKataScoreSheetandDivisionReport(event_time="11:15am",division_name="Weapons Division 2-new",gender="*", rank_label="White to Blue w/Green Stripe", minimum_age=9, maximum_age=11, rings=['*TBA'],
                                                                ranks=[constants.WHITE_BELT,constants.YELLOW_BELT,
                                                                       constants.ORANGE_BELT,constants.PURPLE_BELT,
                                                                       constants.BLUE_BELT,constants.BLUE_STRIPE_BELT],
                                                                clean_df= clean_df)


    ###############################################################################
    #  WeaponsDivision3  - 9-11 year olds Green - Jr. Black
    #
    # compositMask = mask_Weapons & mask_Age9to11
    # writeWeaponsDivision3ToExcel("WeaponsDivision3.xlsx", compositMask)
    writeWeaponsDivision3ToExcelViaQuery(filename="WeaponsDivision3.xlsx", division_type='Weapons', gender="*",minimum_age=9, maximum_age=11)

    # writeWeaponsDivision3ToDetailReport("11:15pm", "Weapons Division 3 Green - Jr. Black", "9-11", compositMask)
    # writeWeaponsDivision3ToKataScoreSheet("11:15pm", "Weapons Division 3 Green - Jr. Black", "9-11", compositMask)

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
    # compositMask = mask_Forms & mask_Age18to39
    # writePattern6ToExcel("MenAndWomensKata.xlsx", compositMask)
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
    # compositMask = mask_Forms & mask_Age12to14
    # writePattern6ToExcel("TeenKata.xlsx", compositMask)
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
    # compositMask = mask_Sparring & mask_Male & mask_Age40Plus
    # writePattern1ToExcel("SeniorMensSparring.xlsx", compositMask)
    writePattern1ToExcelViaQuery(filename="SeniorMensSparring.xlsx", division_type='Sparring', gender="Male",minimum_age=40, maximum_age=constants.AGELESS)

    writeSingleSparringTreeandDivisionReport(event_time="2:15pm",division_name="Sr. Men's Sparring",gender="Male", rank_label="White, Yellow, Orange",     minimum_age=40, maximum_age=constants.AGELESS, rings=[1], ranks=[constants.WHITE_BELT,constants.YELLOW_BELT,constants.ORANGE_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="2:15pm",division_name="Sr. Men's Sparring",gender="Male", rank_label="Purple, Blue, Blue/Stripe", minimum_age=40, maximum_age=constants.AGELESS, rings=[2], ranks=[constants.PURPLE_BELT,constants.BLUE_BELT,constants.BLUE_STRIPE_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="2:15pm",division_name="Sr. Men's Sparring",gender="Male", rank_label="Green, Green/Stripe, Brown",minimum_age=40, maximum_age=constants.AGELESS, rings=[3], ranks=[constants.GREEN_BELT,constants.GREEN_STRIPE_BELT,constants.THIRD_DEGREE_BROWN_BELT,constants.SECOND_DEGREE_BROWN_BELT,constants.FIRST_DEGREE_BROWN_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="2:15pm",division_name="Sr. Men's Sparring",gender="Male", rank_label="Black",                     minimum_age=40, maximum_age=constants.AGELESS, rings=[4], ranks=[constants.JUNIOR_BLACK_BELT,constants.FIRST_DEGREE_BLACK_BELT,constants.SECOND_DEGREE_BLACK_BELT,constants.THIRD_DEGREE_BLACK_BELT,constants.FOURTH_DEGREE_BLACK_BELT,constants.FIFTH_DEGREE_BLACK_BELT],clean_df=clean_df)

    ###############################################################################
    # Senior Women's Sparring - 40+ year olds
    #
    # compositMask = mask_Sparring & mask_Female & mask_Age40Plus
    # writePattern1ToExcel("SeniorWomensSparring.xlsx", compositMask)
    writePattern1ToExcelViaQuery(filename="SeniorWomensSparring.xlsx", division_type='Sparring', gender="Female",minimum_age=40, maximum_age=constants.AGELESS)

    writeSingleSparringTreeandDivisionReport(event_time="2:15pm",division_name="Sr. Women's Sparring",gender="Female", rank_label="White, Yellow, Orange",     minimum_age=40, maximum_age=constants.AGELESS, rings=[5], ranks=[constants.WHITE_BELT,constants.YELLOW_BELT,constants.ORANGE_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="2:15pm",division_name="Sr. Women's Sparring",gender="Female", rank_label="Purple, Blue, Blue/Stripe", minimum_age=40, maximum_age=constants.AGELESS, rings=[6], ranks=[constants.PURPLE_BELT,constants.BLUE_BELT,constants.BLUE_STRIPE_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="2:15pm",division_name="Sr. Women's Sparring",gender="Female", rank_label="Green, Green/Stripe, Brown",minimum_age=40, maximum_age=constants.AGELESS, rings=[7], ranks=[constants.GREEN_BELT,constants.GREEN_STRIPE_BELT,constants.THIRD_DEGREE_BROWN_BELT,constants.SECOND_DEGREE_BROWN_BELT,constants.FIRST_DEGREE_BROWN_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="2:15pm",division_name="Sr. Women's Sparring",gender="Female", rank_label="Black",                     minimum_age=40, maximum_age=constants.AGELESS, rings=[8], ranks=[constants.JUNIOR_BLACK_BELT,constants.FIRST_DEGREE_BLACK_BELT,constants.SECOND_DEGREE_BLACK_BELT,constants.THIRD_DEGREE_BLACK_BELT,constants.FOURTH_DEGREE_BLACK_BELT,constants.FIFTH_DEGREE_BLACK_BELT],clean_df=clean_df)

    ###############################################################################
    # Young Adult Kata - 15-17 year olds
    #
    # compositMask = mask_Forms & mask_Age15to17
    # writePattern1ToExcel("YoungAdultKata.xlsx", compositMask)
    writePattern1ToExcelViaQuery(filename="YoungAdultKata.xlsx", division_type='Forms', gender="*",minimum_age=15, maximum_age=17)

    writeSingleKataScoreSheetandDivisionReport(event_time="2:15pm",division_name="Young Adult Kata",gender="*",rank_label="White,Yellow,Orange",       minimum_age=15, maximum_age=17, rings=[9],  ranks=[constants.WHITE_BELT,constants.YELLOW_BELT,constants.ORANGE_BELT], clean_df=clean_df)
    writeSingleKataScoreSheetandDivisionReport(event_time="2:15pm",division_name="Young Adult Kata",gender="*",rank_label="Purple, Blue, Blue/Stripe", minimum_age=15, maximum_age=17, rings=[10], ranks=[constants.PURPLE_BELT,constants.BLUE_BELT,constants.BLUE_STRIPE_BELT], clean_df=clean_df)
    writeSingleKataScoreSheetandDivisionReport(event_time="2:15pm",division_name="Young Adult Kata",gender="*",rank_label="Green, Green/Stripe, Brown",minimum_age=15, maximum_age=17, rings=[11], ranks=[constants.GREEN_BELT,constants.GREEN_STRIPE_BELT,constants.THIRD_DEGREE_BROWN_BELT,constants.SECOND_DEGREE_BROWN_BELT,constants.FIRST_DEGREE_BROWN_BELT], clean_df=clean_df)
    writeSingleKataScoreSheetandDivisionReport(event_time="2:15pm",division_name="Young Adult Kata",gender="*",rank_label="Jr. Black & Black",         minimum_age=15, maximum_age=17, rings=[12], ranks=[constants.FIRST_DEGREE_BLACK_BELT,constants.SECOND_DEGREE_BLACK_BELT, constants.THIRD_DEGREE_BLACK_BELT,constants.FOURTH_DEGREE_BLACK_BELT,constants.FIFTH_DEGREE_BLACK_BELT,constants.JUNIOR_BLACK_BELT], clean_df=clean_df)


    ###############################################################################
    # Teen Girl's Sparring - 12-14 year olds
    #
    # compositMask = mask_Sparring & mask_Female & mask_Age12to14
    # writePattern1ToExcel("TeenGirlSparring.xlsx", compositMask)
    writePattern1ToExcelViaQuery(filename="TeenGirlSparring.xlsx", division_type='Sparring', gender="Female",minimum_age=12, maximum_age=14)

    writeSingleSparringTreeandDivisionReport(event_time="2:15pm",division_name="Teen Girl's Sparring",gender="Female", rank_label="White, Yellow, Orange",     minimum_age=12, maximum_age=14, rings=[13], ranks=[constants.WHITE_BELT,constants.YELLOW_BELT,constants.ORANGE_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="2:15pm",division_name="Teen Girl's Sparring",gender="Female", rank_label="Purple, Blue, Blue/Stripe", minimum_age=12, maximum_age=14, rings=[14], ranks=[constants.PURPLE_BELT,constants.BLUE_BELT,constants.BLUE_STRIPE_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="2:15pm",division_name="Teen Girl's Sparring",gender="Female", rank_label="Green, Green/Stripe, Brown",minimum_age=12, maximum_age=14, rings=[15], ranks=[constants.GREEN_BELT,constants.GREEN_STRIPE_BELT,constants.THIRD_DEGREE_BROWN_BELT,constants.SECOND_DEGREE_BROWN_BELT,constants.FIRST_DEGREE_BROWN_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="2:15pm",division_name="Teen Girl's Sparring",gender="Female", rank_label="Jr. Black",                 minimum_age=12, maximum_age=14, rings=[16], ranks=[constants.JUNIOR_BLACK_BELT,constants.FIRST_DEGREE_BLACK_BELT,constants.SECOND_DEGREE_BLACK_BELT,constants.THIRD_DEGREE_BLACK_BELT,constants.FOURTH_DEGREE_BLACK_BELT,constants.FIFTH_DEGREE_BLACK_BELT],clean_df=clean_df)


    ### 3:00 Events

    ###############################################################################
    #  Men's Sparring - 18-39 year olds
    #
    # compositMask = mask_Sparring & mask_Male & mask_Age18to39
    # writePattern1ToExcel("MensSparring.xlsx", compositMask)
    writePattern1ToExcelViaQuery(filename="MensSparring.xlsx", division_type='Sparring', gender="Male",minimum_age=18, maximum_age=39)

    writeSingleSparringTreeandDivisionReport(event_time="3:00pm",division_name="Men's Sparring",gender="Male", rank_label="White, Yellow, Orange",     minimum_age=18, maximum_age=39, rings=[1], ranks=[constants.WHITE_BELT,constants.YELLOW_BELT,constants.ORANGE_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="3:00pm",division_name="Men's Sparring",gender="Male", rank_label="Purple, Blue, Blue/Stripe", minimum_age=18, maximum_age=39, rings=[2], ranks=[constants.PURPLE_BELT,constants.BLUE_BELT,constants.BLUE_STRIPE_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="3:00pm",division_name="Men's Sparring",gender="Male", rank_label="Green, Green/Stripe, Brown",minimum_age=18, maximum_age=39, rings=[3], ranks=[constants.GREEN_BELT,constants.GREEN_STRIPE_BELT,constants.THIRD_DEGREE_BROWN_BELT,constants.SECOND_DEGREE_BROWN_BELT,constants.FIRST_DEGREE_BROWN_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="3:00pm",division_name="Men's Sparring",gender="Male", rank_label="Black",                     minimum_age=18, maximum_age=39, rings=[4], ranks=[constants.JUNIOR_BLACK_BELT,constants.FIRST_DEGREE_BLACK_BELT,constants.SECOND_DEGREE_BLACK_BELT,constants.THIRD_DEGREE_BLACK_BELT,constants.FOURTH_DEGREE_BLACK_BELT,constants.FIFTH_DEGREE_BLACK_BELT],clean_df=clean_df)

    ###############################################################################
    #  Teen Boy's Sparring - 12-14 year olds
    #
    # compositMask = mask_Sparring & mask_Male & mask_Age12to14
    # writePattern2ToExcel("TeenBoysSparring.xlsx", compositMask)
    writePattern2ToExcelViaQuery(filename="TeenBoysSparring.xlsx", division_type='Sparring', gender="Male",minimum_age=12, maximum_age=14)

    writeSingleSparringTreeandDivisionReport(event_time="3:00pm",division_name="Teen Boy's Sparring",gender="Male", rank_label="White, Yellow, Orange",      minimum_age=12, maximum_age=14, rings=[5], ranks=[constants.WHITE_BELT,constants.YELLOW_BELT,constants.ORANGE_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="3:00pm",division_name="Teen Boy's Sparring",gender="Male", rank_label="Purple, Blue, Blue/Stripe",  minimum_age=12, maximum_age=14, rings=[6], ranks=[constants.PURPLE_BELT,constants.BLUE_BELT,constants.BLUE_STRIPE_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="3:00pm",division_name="Teen Boy's Sparring",gender="Male", rank_label="Green, Green/Stripe",        minimum_age=12, maximum_age=14, rings=[7], ranks=[constants.GREEN_BELT,constants.GREEN_STRIPE_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="3:00pm",division_name="Teen Boy's Sparring",gender="Male", rank_label="Brown",                      minimum_age=12, maximum_age=14, rings=[8], ranks=[constants.THIRD_DEGREE_BROWN_BELT,constants.SECOND_DEGREE_BROWN_BELT,constants.FIRST_DEGREE_BROWN_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="3:00pm",division_name="Teen Boy's Sparring",gender="Male", rank_label="Jr. Black",                  minimum_age=12, maximum_age=14, rings=[9], ranks=[constants.JUNIOR_BLACK_BELT,constants.FIRST_DEGREE_BLACK_BELT,constants.SECOND_DEGREE_BLACK_BELT,constants.THIRD_DEGREE_BLACK_BELT,constants.FOURTH_DEGREE_BLACK_BELT,constants.FIFTH_DEGREE_BLACK_BELT],clean_df=clean_df)

    ###############################################################################
    #  Young Adult Men's Sparring - 15-17 year olds
    #
    # compositMask = mask_Sparring & mask_Male & mask_Age15to17
    # writePattern2ToExcel("YoungAdultMensSparring.xlsx", compositMask)
    writePattern2ToExcelViaQuery(filename="YoungAdultMensSparring.xlsx", division_type='Sparring', gender="Male",minimum_age=15, maximum_age=17)

    writeSingleSparringTreeandDivisionReport(event_time="3:00pm",division_name="Young Adult Men's Sparring",gender="Male", rank_label="White, Yellow, Orange",     minimum_age=15, maximum_age=17, rings=[10], ranks=[constants.WHITE_BELT,constants.YELLOW_BELT,constants.ORANGE_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="3:00pm",division_name="Young Adult Men's Sparring",gender="Male", rank_label="Purple, Blue, Blue/Stripe", minimum_age=15, maximum_age=17, rings=[11], ranks=[constants.PURPLE_BELT,constants.BLUE_BELT,constants.BLUE_STRIPE_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="3:00pm",division_name="Young Adult Men's Sparring",gender="Male", rank_label="Green, Green/Stripe",       minimum_age=15, maximum_age=17, rings=[12], ranks=[constants.GREEN_BELT,constants.GREEN_STRIPE_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="3:00pm",division_name="Young Adult Men's Sparring",gender="Male", rank_label="Brown",                     minimum_age=15, maximum_age=17, rings=[13], ranks=[constants.THIRD_DEGREE_BROWN_BELT,constants.SECOND_DEGREE_BROWN_BELT,constants.FIRST_DEGREE_BROWN_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="3:00pm",division_name="Young Adult Men's Sparring",gender="Male", rank_label="Jr. Black & Black",         minimum_age=15, maximum_age=17, rings=[14], ranks=[constants.JUNIOR_BLACK_BELT,constants.FIRST_DEGREE_BLACK_BELT,constants.SECOND_DEGREE_BLACK_BELT,constants.THIRD_DEGREE_BLACK_BELT,constants.FOURTH_DEGREE_BLACK_BELT,constants.FIFTH_DEGREE_BLACK_BELT],clean_df=clean_df)


    ###############################################################################
    #  Women's Sparring - 18-39 year olds
    #
    # compositMask = mask_Sparring & mask_Female & mask_Age18to39
    # writePattern1ToExcel("WomensSparring.xlsx", compositMask)
    writePattern1ToExcelViaQuery(filename="WomensSparring.xlsx", division_type='Sparring', gender="Female",minimum_age=18, maximum_age=39)

    writeSingleSparringTreeandDivisionReport(event_time="3:00pm",division_name="Women's Sparring",gender="Female", rank_label="White, Yellow, Orange",     minimum_age=18, maximum_age=39, rings=[15], ranks=[constants.WHITE_BELT,constants.YELLOW_BELT,constants.ORANGE_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="3:00pm",division_name="Women's Sparring",gender="Female", rank_label="Purple, Blue, Blue/Stripe", minimum_age=18, maximum_age=39, rings=[16], ranks=[constants.PURPLE_BELT,constants.BLUE_BELT,constants.BLUE_STRIPE_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="3:00pm",division_name="Women's Sparring",gender="Female", rank_label="Green, Green/Stripe, Brown",minimum_age=18, maximum_age=39, rings=[17], ranks=[constants.GREEN_BELT,constants.GREEN_STRIPE_BELT,constants.THIRD_DEGREE_BROWN_BELT,constants.SECOND_DEGREE_BROWN_BELT,constants.FIRST_DEGREE_BROWN_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="3:00pm",division_name="Women's Sparring",gender="Female", rank_label="Black",                     minimum_age=18, maximum_age=39, rings=[18], ranks=[constants.JUNIOR_BLACK_BELT,constants.FIRST_DEGREE_BLACK_BELT,constants.SECOND_DEGREE_BLACK_BELT,constants.THIRD_DEGREE_BLACK_BELT,constants.FOURTH_DEGREE_BLACK_BELT,constants.FIFTH_DEGREE_BLACK_BELT],clean_df=clean_df)


    ### 3:45 Events

    ###############################################################################
    # Senior Kata - 40+ year olds
    #
    # compositMask = mask_Forms & mask_Age40Plus
    # writePattern6ToExcel("SeniorKata.xlsx", compositMask)
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
    # compositMask = mask_Sparring & mask_Female & mask_Age15to17
    # writePattern1ToExcel("YoungAdultWomensSparring.xlsx", compositMask)
    writePattern1ToExcelViaQuery(filename="YoungAdultWomensSparring.xlsx", division_type='Sparring', gender="Female",minimum_age=15, maximum_age=17)

    writeSingleSparringTreeandDivisionReport(event_time="3:45pm",division_name="Young Adult Women's Sparring",gender="Female", rank_label="White, Yellow, Orange",     minimum_age=15, maximum_age=17, rings=[8], ranks=[constants.WHITE_BELT,constants.YELLOW_BELT,constants.ORANGE_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="3:45pm",division_name="Young Adult Women's Sparring",gender="Female", rank_label="Purple, Blue, Blue/Stripe", minimum_age=15, maximum_age=17, rings=[9], ranks=[constants.PURPLE_BELT,constants.BLUE_BELT,constants.BLUE_STRIPE_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="3:45pm",division_name="Young Adult Women's Sparring",gender="Female", rank_label="Green, Green/Stripe, Brown",minimum_age=15, maximum_age=17, rings=[10], ranks=[constants.GREEN_BELT,constants.GREEN_STRIPE_BELT,constants.THIRD_DEGREE_BROWN_BELT,constants.SECOND_DEGREE_BROWN_BELT,constants.FIRST_DEGREE_BROWN_BELT],clean_df=clean_df)
    writeSingleSparringTreeandDivisionReport(event_time="3:45pm",division_name="Young Adult Women's Sparring",gender="Female", rank_label="Jr. Black & Black",         minimum_age=15, maximum_age=17, rings=[11], ranks=[constants.JUNIOR_BLACK_BELT,constants.FIRST_DEGREE_BLACK_BELT,constants.SECOND_DEGREE_BLACK_BELT,constants.THIRD_DEGREE_BLACK_BELT,constants.FOURTH_DEGREE_BLACK_BELT,constants.FIFTH_DEGREE_BLACK_BELT],clean_df=clean_df)


    ### 4:15 Events

    ###############################################################################
    #  WeaponsDivision4 12-17 White-Blue Stripe year olds
    #
    # compositMask = mask_Weapons & mask_Age12to17
    # writeWeaponsDivision4ToExcel("WeaponsDivision4.xlsx", compositMask)
    writeWeaponsDivision4ToExcelViaQuery(filename="WeaponsDivision4.xlsx", division_type='Weapons', gender="*",minimum_age=12, maximum_age=17)

    # writeWeaponsDivision4ToDetailReport("4:15pm", "Weapons Division 4", "12 - 17", compositMask)
    # writeWeaponsDivision4ToKataScoreSheet("4:15pm", "Weapons Division 4", "12 - 17", compositMask)

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
    # compositMask = mask_Weapons & mask_Age18Plus
    # writeWeaponsDivision5ToExcel("WeaponsDivision5.xlsx", compositMask)
    writeWeaponsDivision5ToExcelViaQuery(filename="WeaponsDivision5.xlsx", division_type='Weapons', gender="*",minimum_age=18, maximum_age=constants.AGELESS)

    # writeWeaponsDivision5ToDetailReport("4:15pm", "Weapons Division 5", "18+", compositMask)
    # writeWeaponsDivision5ToKataScoreSheet("4:15pm", "Weapons Division 5", "18+", compositMask)

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
    # compositMask = mask_Weapons & mask_Age12Plus
    # writeWeaponsDivision6ToFile("WeaponsDivision6.xlsx", compositMask)
    writeWeaponsDivision6ToExcelViaQuery(filename="WeaponsDivision6.xlsx", division_type='Weapons', gender="*",minimum_age=12, maximum_age=constants.AGELESS)

    # writeWeaponsDivision6ToDetailReport("4:15pm", "Weapons Division 6", "12+", compositMask)
    # writeWeaponsDivision6ToKataScoreSheet("4:15pm", "Weapons Division 6", "12+", compositMask)

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
    # compositMask = mask_Weapons & mask_Age12Plus
    # writeWeaponsDivision7ToFile("WeaponsDivision7.xlsx", compositMask)
    writeWeaponsDivision7ToExcelViaQuery(filename="WeaponsDivision7.xlsx", division_type='Weapons', gender="*",minimum_age=12, maximum_age=constants.AGELESS)

    # writeWeaponsDivision7ToDetailReport("4:15pm", "Weapons Division 7", "12+", compositMask)
    # writeWeaponsDivision7ToKataScoreSheet("4:15pm", "Weapons Division 7", "12+", compositMask)

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
    # compositMask = mask_Weapons & mask_Age12to17
    # writeWeaponsDivision8ToFile("WeaponsDivision8.xlsx", compositMask)
    writeWeaponsDivision8ToExcelViaQuery(filename="WeaponsDivision8.xlsx", division_type='Weapons', gender="*",minimum_age=12, maximum_age=17)


    # writeWeaponsDivision8ToDetailReport("4:15pm", "Weapons Division 8", "12-17", compositMask)
    # writeWeaponsDivision8ToKataScoreSheet("4:15pm", "Weapons Division 8", "12-17", compositMask)

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
    # compositMask = mask_Weapons & mask_Age18Plus
    # writeWeaponsDivision9ToFile("WeaponsDivision9.xlsx", compositMask)
    writeWeaponsDivision9ToExcelViaQuery(filename="WeaponsDivision9.xlsx", division_type='Weapons', gender="*",minimum_age=18, maximum_age=constants.AGELESS)

    # writeWeaponsDivision9ToDetailReport("4:15pm", "Weapons Division 9", "18+", compositMask)
    # writeWeaponsDivision9ToKataScoreSheet("4:15pm", "Weapons Division 9", "18+", compositMask)

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
