# V18 - Make the spreadsheets print better
#
# There are 6 patterns in this Tournament Guide
#
#Pattern1
#  White
#  Yellow
#  Orange
#  Purple, Blue, Blue Stripe
#  Green, Green Stripe
#
#Pattern2
#  White
#  Yellow
#  Orange
#  Purple, Blue, Blue Stripe
#  Green, Green Stripe, Brown
#
#Pattern3
#  White
#  Yellow
#  Orange
#  Purple
#  Blue, Blue Stripe
#  Green, Green Stripe, Brown
#
#Pattern4
#  White, Yellow, Orange
#  Purple, Blue, Blue Stripe
#  Green, Green Stripe, Brown
#  Black
#
#Pattern5
#  White, Yellow
#  Orange
#  Purple
#  Blue, Blue Stripe
#  Green, Green Stripe, Brown
#
#Pattern6
#  White, Yellow
#  Orange
#  Purple
#  Blue, Blue Stripe
#  Green, Green Stripe
#  Brown
#  Black
#
#Pattern7
#  White, Yellow & Orange
#  Purple, Blue & Blue Stripe
#  Green, Green Stripe, Brown
#  Black
#
#   Feautres to add:
# Better error handling - loop through each record looking for bogus stuff and print an error message telling what's wrong with it
# Summary Stats - how many people of each belt, how many sparring, how may forms, how many weaponds
# Event Stats - how many people in each event as per the event guide
#

import pandas as pd
import numpy as np
from Tkinter import Tk
from tkFileDialog import askopenfilename
import os
import sys
#from pandas import ExcelWriter
#from pandas import XlsxWriter
import time

#import sys
#matplotlib inline


###############################################################################
# fixInput
#  This function scans indiviual rows looking for input errors
#  at first, it will just point out errors to the user
#  arguments:  none
#  return:   "\\" if it's windows, "/" if it's unix
#
def fixInput( inputDataFrame, errorLogFile ):
    errorCount = 0
    # first use Ria's technique to remove bogus lines from the data frame
    cleanDataFrame = df[np.isfinite(df['Registrant ID'])]

    #next check for non-numeric data in the age field
    for index, row in cleanDataFrame.iterrows():
        try:
            int(row['Competitor\'s Age?'])
        except ValueError:
            errorCount+=1
            errorString="Error: The row: "+str(row["Registrant ID"])+" "+str(row["First Name"])+" "+str(row["Last Name"])+ " has something other than a number in Age field"
            errorLogFile.write(errorString+"\r\f")
            print errorString

    #Test Rank - looking for 'Please Select'
    mask_NoBelt=(cleanDataFrame['Current Belt Rank?']=='Please Select')
    #df_NoBelt=cleanDataFrame[['Registrant ID','First Name','Last Name','Select Your Z Ultimate Studio','Email','Phone','Mobile Phone']][mask_NoBelt]
    df_NoBelt=cleanDataFrame[['Registrant ID','First Name','Last Name','Select Your Z Ultimate Studio']][mask_NoBelt]
    beltErrorCount = df_NoBelt.shape[0]
    if beltErrorCount > 0:
      errorCount+=beltErrorCount
      errorLogFile.write( "The Following People did not select a valid rank:\r\n" )
      print "The Following People did not select a valid rank:"
      for index, row in df_NoBelt.iterrows():
            errorString="Error: The row: "+str(row["Registrant ID"])+" "+str(row["First Name"])+" "+str(row["Last Name"])+ " has something other than a number in Age field"
            errorLogFile.write(errorString+"\r\f")
            print errorString


#        errorLogFile.write( "Error: The row: "+str(row["Registrant ID"])+" "+str(row["First Name"])+" "+str(row["Last Name"]) + " did not contain a valid rank " )


    #Convert weight to digits with regex and generate an error if not valid
    import re
    compiledRegex=re.compile('\d+')
    for index, row in cleanDataFrame.iterrows():
        rawWeightString=row['Competitor\'s Weight (eg. 73lbs.)?']
        matchList=compiledRegex.match(rawWeightString)
        cleanWeightString=matchList.group()
#        cleanDataFrame.loc[index,'Competitor\'s Weight (in lbs.)?']=cleanWeightString #try .at instead http://pandas.pydata.org/pandas-docs/stable/indexing.html#fast-scalar-value-getting-and-setting
        cleanDataFrame.at[index,'Competitor\'s Weight (eg. 73lbs.)?']=cleanWeightString #try .at instead http://pandas.pydata.org/pandas-docs/stable/indexing.html#fast-scalar-value-getting-and-setting

        #print cleanWeightString
        cleanWeight=int(cleanWeightString)
        if (0==cleanWeight) or (350 < cleanWeight):
            errorCount+=1
            errorString="Error: The row: "+str(row["Registrant ID"])+" "+str(row["First Name"])+" "+str(row["Last Name"])+ " has an invalid Weight field:" + rawWeightString
            errorLogFile.write(errorString+"\r\f")
            print errorString


#    #Check for non-numeric data in the Weight Field
#    for index, row in cleanDataFrame.iterrows():
#        try:
#            int(row['Competitor\'s Weight (eg. 73lbs.)?'])
#        except ValueError:
#            errorCount+=1
#            errorString="Error: The row: "+str(row["Registrant ID"])+" "+str(row["First Name"])+" "+str(row["Last Name"])+ " has something other than a number in Weight field"
#            errorLogFile.write(errorString+"\r\f")
#            print errorString

#good guide to Regex in Python: https://docs.python.org/2/howto/regex.html
#import re
#wString="98 lbs"
#p=re.compile('\d+')
#s=p.match(wString)
#print s.group()

 #Height - todo: make the error more usable
#    import re
    compiledRegex=re.compile('\d+')
    for index, row in cleanDataFrame.iterrows():
        splitString=row['Competitor\'s Height (e.g. 4 ft. 2 in. )?']
 #        print splitString
        matchList=compiledRegex.findall(splitString)
        l=len(matchList)
        if l>=2:
            feet=matchList[0]
            inches=matchList[1]
        if l==1:
            if(int(matchList[0])<12):
                #single digit less than 12
                feet=matchList[0]
                inches=0
            else:
                #single digit greater than 12
                feet= 0
                inches=matchList[0]
                if inches>12:
                    feet=int(inches)/12
                    inches=int(inches)%12
        if l==0:
            feet=0
            inches=0

        #resonability test
        if (int(feet) < 2) or (int(feet) > 7):
           #print splitString, "|", feet, "|", inches, "is not reasonable"
           errorCount+=1
           errorString="Error: The row: "+str(row["Registrant ID"])+" "+str(row["First Name"])+" "+str(row["Last Name"])+ " has bad data in the height field: " + splitString
           errorLogFile.write(errorString+"\r\f")
           print errorString

        #Write it to new columns in the data frame
        cleanDataFrame.loc[index,'Feet']=feet
        cleanDataFrame.loc[index,'Inches']=inches
        heightInInches = (int(feet)*12)+int(inches)
        cleanDataFrame.loc[index,'HeightInInches']=heightInInches
        bodyMassIndex=(heightInInches*2)+int(cleanDataFrame.loc[index,'Competitor\'s Weight (eg. 73lbs.)?'])
        cleanDataFrame.loc[index,'BMI']=bodyMassIndex
        #print splitString, "|", feet, "|", inches

#---test version
        cleanDataFrame.at[index,'Feet']=feet
        cleanDataFrame.at[index,'Inches']=inches
        heightInInches = (int(feet)*12)+int(inches)
        cleanDataFrame.at[index,'HeightInInches']=heightInInches
        bodyMassIndex=(heightInInches*2)+int(cleanDataFrame.loc[index,'Competitor\'s Weight (eg. 73lbs.)?'])
        cleanDataFrame.at[index,'BMI']=bodyMassIndex
        #print splitString, "|", feet, "|", inches




   # if there are errors exit
    if( errorCount > 0):
        errorLogFile.write( str(errorCount)+" "+"errors found" )
        errorLogFile.close()
        print str(errorCount)+" "+"errors found"
        sys.exit("Exiting - The input must be fixed manually")
    else:
         errorLogFile.write( "No errors found" )


    return cleanDataFrame



###############################################################################
# pathDelimiter()
#  arguments:  none
#  return:   "\\" if it's windows, "/" if it's unix
#
def pathDelimiter():
    path = os.getcwd()
    if ("\\" in path):
        delimiter = "\\" #Windows
    else:
        delimiter = "/" #Unix
    return delimiter


###############################################################################
# NewDataFrameFromMask()
#  arguments:  mask to apply
#  return:   new data frame
#
def newDataFrameFromMask( mask ):
#    newdf = cdf[["First Name", "Last Name", "Gender","Select Your Z Ultimate Studio","Out of State Studio Name", "Competitor\'s Age?", "Current Belt Rank?", "Competitor\'s Weight (in lbs.)?", "Competitor\'s Height (in feet and inches)?", "Choose Forms, Sparring or Both.", "Choose Weapons.","Parent or Guardian Name (if competitor is under 18)?","Phone","Mobile Phone"]][mask].sort("Competitor\'s Age?")
#    newdf = cdf[["First Name", "Last Name", "Gender","Select Your Z Ultimate Studio","Out of State Studio Name", "Competitor\'s Age?", "Current Belt Rank?", "Competitor\'s Weight (in lbs.)?", "Competitor\'s Height (in feet and inches)?", "Choose Forms, Sparring or Both.", "Choose Weapons."]][mask].sort("Competitor\'s Age?")
#    newdf = cdf[["First Name", "Last Name", "Gender","Select Your Z Ultimate Studio","Out of State Studio Name", "Competitor\'s Age?", "Current Belt Rank?", "Competitor\'s Weight (in lbs.)?", "Competitor\'s Height (in feet and inches)?", "Choose Forms, Sparring or Both.", "Choose Weapons."]][mask].sort_values("Competitor\'s Age?")
#    newdf = cdf[["First Name", "Last Name", "Gender","Select Your Z Ultimate Studio","Out of State Studio Name", "Competitor\'s Age?", "Current Belt Rank?", "Feet","Inches","HeightInInches","Competitor\'s Weight (in lbs.)?","BodyMassIndex", "Choose Forms, Sparring or Both.", "Choose Weapons."]][mask].sort_values("Competitor\'s Age?")
    newdf = cdf[["First Name", "Last Name", "Gender","Select Your Z Ultimate Studio","Out of State Studio Name", "Competitor\'s Age?", "Current Belt Rank?", "Feet","Inches","Competitor\'s Height (e.g. 4 ft. 2 in. )?","Competitor\'s Weight (eg. 73lbs.)?","BMI", "Choose Forms, Sparring or Both.", "Choose Weapons."]][mask].sort_values("Competitor\'s Age?")
    newdf.sort_values('BMI',inplace=True)
    newdf.rename(columns={'Select Your Z Ultimate Studio':'Dojo','Out of State Studio Name':'Out of State Dojo Name','Competitor\'s Age?':'Age','Current Belt Rank?':'Rank','Competitor\'s Height (e.g. 4 ft. 2 in. )?':'Height','Competitor\'s Weight (eg. 73lbs.)?':'Weight','Choose Forms, Sparring or Both.':'Events','Choose Weapons.':'Weapons'},inplace=True)
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
def writeFormattedExcelSheet( df, writer, sheetname ):
    df.to_excel(writer,sheetname)

    ##setup the spreadsheet to make it easy to print
    #    set_border(1)
    workbook = writer.book
    worksheet = writer.sheets[sheetname]

    #define some formats
    align_center=workbook.add_format()
    align_center.set_align('center')
    align_center.set_border(1)

    align_left=workbook.add_format()
    align_left.set_align('left')
    align_left.set_border(1)

    full_border=workbook.add_format()
    full_border.set_border(1)

    #set the format of a few columns
    worksheet.set_column('A:O',0,full_border)  #column A:O is everything

    worksheet.set_column('A:A',5,align_left)  #column A is the index
    worksheet.set_column('B:B',15)  #column B is First Name
    worksheet.set_column('C:C',20)  #column C is Last Name
    worksheet.set_column('D:D',7)  #column D is Gender
    worksheet.set_column('E:E',20)  #column E is Dojo
    worksheet.set_column('F:F',20)  #column F is Out of State Dojo
    worksheet.set_column('G:G',3,align_center)  #column G is age
    worksheet.set_column('H:H',15)  #column H is rank
    worksheet.set_column('I:I',4,align_center)  #column I is feet
    worksheet.set_column('J:J',5,align_center)  #column J is Inches
    worksheet.set_column('L:L',6,align_center)  #column L is Weight
    worksheet.set_column('M:M',4,align_center)  #column I is BMI
    worksheet.set_column('N:N',25)  #column I is Events
    worksheet.set_column('O:O',12)  #column I is Weapons


###############################################################################
# write event to file
#  arguments:
#  filename - the filename without path to write
#  compsitMask - a mask made up of everything but the belts that you want
#
def writeEventToFile( filename, compositMask ):
#    fullpath = os.getcwd() + "\\Sorted\\" + filename  #Windows
#    fullpath = os.getcwd() + "/Sorted/" + filename  #Mac
    fullpath = os.getcwd() + pathDelimiter() + "Sorted" + pathDelimiter() + filename
    writer=pd.ExcelWriter(fullpath)

    print "Generating " + fullpath

    mask= mask_WhiteBelt & compositMask
    wmk=newDataFrameFromMask( mask )
#    wmk.to_excel(writer,'White')
    writeFormattedExcelSheet(wmk,writer,'White')

    mask= mask_YellowBelt & compositMask
    wmk=newDataFrameFromMask( mask )
#    wmk.to_excel(writer,'Yellow')
    writeFormattedExcelSheet(wmk,writer,'Yellow')


    mask= mask_OrangeBelt & compositMask
    wmk=newDataFrameFromMask( mask )
#   wmk.to_excel(writer,'Orange')
    writeFormattedExcelSheet(wmk,writer,'Orange')

    mask= mask_PurpleBelt & compositMask
    wmk=newDataFrameFromMask( mask )
#    wmk.to_excel(writer,'Purple')
    writeFormattedExcelSheet(wmk,writer,'Purple')

    mask= mask_AllBlueBelt & compositMask
    wmk=newDataFrameFromMask( mask )
#    wmk.to_excel(writer,'Blue')
    writeFormattedExcelSheet(wmk,writer,'Blue')

    mask= mask_AllGreenBelt & compositMask
    wmk=newDataFrameFromMask( mask )
#    wmk.to_excel(writer,'Green')
    writeFormattedExcelSheet(wmk,writer,'Green')

    mask= mask_AllBrownBelt & compositMask
    wmk=newDataFrameFromMask( mask )
#   wmk.to_excel(writer,'Brown')
    writeFormattedExcelSheet(wmk,writer,'Brown')

    mask= mask_AllBlackBelt & compositMask
    wmk=newDataFrameFromMask( mask )
#    wmk.to_excel(writer,'Black')
    writeFormattedExcelSheet(wmk,writer,'Black')


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
def writePattern1ToExcel( filename, compositMask ):
    fullpath = os.getcwd() + pathDelimiter() + "Sorted" + pathDelimiter() + filename
    writer=pd.ExcelWriter(fullpath,engine='xlsxwriter')
    print "Generating " + fullpath

    mask= mask_WhiteBelt & compositMask
    wmk=newDataFrameFromMask( mask )
    writeFormattedExcelSheet(wmk,writer,'White')
#    wmk.to_excel(writer,'White')

    mask= mask_YellowBelt & compositMask
    wmk=newDataFrameFromMask( mask )
#    wmk.to_excel(writer,'Yellow')
    writeFormattedExcelSheet(wmk,writer,'Yellow')


    mask= mask_OrangeBelt & compositMask
    wmk=newDataFrameFromMask( mask )
  #  wmk.to_excel(writer,'Orange')
    writeFormattedExcelSheet(wmk,writer,'Orange')

    mask1 = mask_PurpleBelt & compositMask
    mask2 = mask_AllBlueBelt & compositMask
    mask = mask1 | mask2
    wmk=newDataFrameFromMask( mask )
 #   wmk.to_excel(writer,'Purple, Blue, Blue Stripe')
    writeFormattedExcelSheet(wmk,writer,'Purple, Blue, Blue Stripe')

    mask1 = mask_AllGreenBelt & compositMask
    mask2 = mask_AllBrownBelt & compositMask
    mask = mask1 | mask2
    wmk=newDataFrameFromMask( mask )
#    wmk.to_excel(writer,'Green, Green Stripe')
    writeFormattedExcelSheet(wmk,writer,'Green, Green Stripe, Brown')
#
#    mask= mask_AllBlackBelt & compositMask
#    wmk=newDataFrameFromMask( mask )
#    wmk.to_excel(writer,'Black')

    writer.save()
    time.sleep(1)

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
def writePattern2ToExcel( filename, compositMask ):
    fullpath = os.getcwd() + pathDelimiter() + "Sorted" + pathDelimiter() + filename
    writer=pd.ExcelWriter(fullpath)
    print "Generating " + fullpath

    mask= mask_WhiteBelt & compositMask
    wmk=newDataFrameFromMask( mask )
#    wmk.to_excel(writer,'White')
    writeFormattedExcelSheet(wmk,writer,'White')

    mask= mask_YellowBelt & compositMask
    wmk=newDataFrameFromMask( mask )
#    wmk.to_excel(writer,'Yellow')
    writeFormattedExcelSheet(wmk,writer,'Yellow')

    mask= mask_OrangeBelt & compositMask
    wmk=newDataFrameFromMask( mask )
#    wmk.to_excel(writer,'Orange')
    writeFormattedExcelSheet(wmk,writer,'Orange')

    mask1 = mask_PurpleBelt & compositMask
    mask2 = mask_AllBlueBelt & compositMask
    mask = mask1 | mask2
    wmk=newDataFrameFromMask( mask )
#    wmk.to_excel(writer,'Purple, Blue, Blue Stripe')
    writeFormattedExcelSheet(wmk,writer,'Purple, Blue, Blue Stripe')

    mask1 = mask_AllGreenBelt & compositMask
    mask2 = mask_AllBrownBelt & compositMask
    mask = mask1 | mask2
    wmk=newDataFrameFromMask( mask )
#    wmk.to_excel(writer,'Green, Green Stripe, Brown')
    writeFormattedExcelSheet(wmk,writer,'Green, Green Stripe, Brown')

#
#    mask= mask_AllBlackBelt & compositMask
#    wmk=newDataFrameFromMask( mask )
#    wmk.to_excel(writer,'Black')

    writer.save()
    time.sleep(1)

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
def writePattern3ToExcel( filename, compositMask ):
    fullpath = os.getcwd() + pathDelimiter() + "Sorted" + pathDelimiter() + filename
    writer=pd.ExcelWriter(fullpath)
    print "Generating " + fullpath

    mask= mask_WhiteBelt & compositMask
    wmk=newDataFrameFromMask( mask )
#    wmk.to_excel(writer,'White')
    writeFormattedExcelSheet(wmk,writer,'White')

    mask= mask_YellowBelt & compositMask
    wmk=newDataFrameFromMask( mask )
#    wmk.to_excel(writer,'Yellow')
    writeFormattedExcelSheet(wmk,writer,'Yellow')

    mask= mask_OrangeBelt & compositMask
    wmk=newDataFrameFromMask( mask )
#    wmk.to_excel(writer,'Orange')
    writeFormattedExcelSheet(wmk,writer,'Orange')

    mask = mask_PurpleBelt & compositMask
    wmk=newDataFrameFromMask( mask )
#    wmk.to_excel(writer,'Purple')
    writeFormattedExcelSheet(wmk,writer,'Purple')

    mask = mask_AllBlueBelt & compositMask
    wmk=newDataFrameFromMask( mask )
#    wmk.to_excel(writer,'Blue, Blue Stripe')
    writeFormattedExcelSheet(wmk,writer,'Blue, Blue Stripe')

    mask1 = mask_AllGreenBelt & compositMask
    mask2 = mask_AllBrownBelt & compositMask
    mask = mask1 | mask2
    wmk=newDataFrameFromMask( mask )
#    wmk.to_excel(writer,'Green, Green Stripe, Brown')
    writeFormattedExcelSheet(wmk,writer,'Green, Green Stripe, Brown')

    writer.save()
    time.sleep(1)


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
def writePattern4ToExcel( filename, compositMask ):
    fullpath = os.getcwd() + pathDelimiter() + "Sorted" + pathDelimiter() + filename
    writer=pd.ExcelWriter(fullpath)
    print "Generating " + fullpath

    mask1= mask_WhiteBelt & compositMask
    mask2= mask_YellowBelt & compositMask
    mask3= mask_OrangeBelt & compositMask
    mask = mask1 | mask2 | mask3
    wmk=newDataFrameFromMask( mask )
#    wmk.to_excel(writer,'White, Yellow, Orange')
    writeFormattedExcelSheet(wmk,writer,'White, Yellow, Orange')

#    mask= mask_OrangeBelt & compositMask
#    wmk=newDataFrameFromMask( mask )
#    wmk.to_excel(writer,'Orange')

#    mask= mask_PurpleBelt & compositMask
#    wmk=newDataFrameFromMask( mask )
#    wmk.to_excel(writer,'Purple')

    mask1= mask_PurpleBelt & compositMask
    mask2= mask_AllBlueBelt & compositMask
    mask = mask1 | mask2
    wmk=newDataFrameFromMask( mask )
#    wmk.to_excel(writer,'Purple, Blue, Blue Stripe')
    writeFormattedExcelSheet(wmk,writer,'Purple, Blue, Blue Stripe')

    mask1= mask_AllBrownBelt & compositMask
    mask2= mask_AllGreenBelt & compositMask
    mask = mask1 | mask2
    wmk=newDataFrameFromMask( mask )
#    wmk.to_excel(writer,'Green, Green Stripe, Brown')
    writeFormattedExcelSheet(wmk,writer,'Green, Green Stripe, Brown')

#    mask= mask_AllBrownBelt & compositMask
#    wmk=newDataFrameFromMask( mask )
#    wmk.to_excel(writer,'All Brown')

    mask= mask_AllBlackBelt & compositMask
    wmk=newDataFrameFromMask( mask )
#    wmk.to_excel(writer,'Black')
    writeFormattedExcelSheet(wmk,writer,'Black')

    writer.save()
    time.sleep(1)


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
def writePattern5ToExcel( filename, compositMask ):
    fullpath = os.getcwd() + pathDelimiter() + "Sorted" + pathDelimiter() + filename
    writer=pd.ExcelWriter(fullpath)
    print "Generating " + fullpath

    mask1= mask_WhiteBelt & compositMask
    mask2= mask_YellowBelt & compositMask
    mask = mask1 | mask2
    wmk=newDataFrameFromMask( mask )
#    wmk.to_excel(writer,'White, Yellow')
    writeFormattedExcelSheet(wmk,writer,'White, Yellow')

    mask= mask_OrangeBelt & compositMask
    wmk=newDataFrameFromMask( mask )
#    wmk.to_excel(writer,'Orange')
    writeFormattedExcelSheet(wmk,writer,'Orange')

    mask= mask_PurpleBelt & compositMask
    wmk=newDataFrameFromMask( mask )
#    wmk.to_excel(writer,'Purple')
    writeFormattedExcelSheet(wmk,writer,'Purple')

    mask = mask_AllBlueBelt & compositMask
    wmk=newDataFrameFromMask( mask )
#    wmk.to_excel(writer,'Blue, Blue Stripe')
    writeFormattedExcelSheet(wmk,writer,'Blue, Blue Stripe')

    mask1 = mask_AllGreenBelt & compositMask
    mask2 = mask_AllBrownBelt & compositMask
    mask = mask1 | mask2
    wmk=newDataFrameFromMask( mask )
#    wmk.to_excel(writer,'Green, Green Stripe, Brown')
    writeFormattedExcelSheet(wmk,writer,'Green, Green Stripe, Brown')

    writer.save()
    time.sleep(1)


###############################################################################
# writePattern6ToExcel
#  This method provides a re-usable method to write output to excel
#  The Pattern it writes is:
#    White, Yellow
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
def writePattern6ToExcel( filename, compositMask ):
    fullpath = os.getcwd() + pathDelimiter() + "Sorted" + pathDelimiter() + filename
    writer=pd.ExcelWriter(fullpath)
    print "Generating " + fullpath

    mask1= mask_WhiteBelt & compositMask
    mask2= mask_YellowBelt & compositMask
    mask = mask1 | mask2
    wmk=newDataFrameFromMask( mask )
#    wmk.to_excel(writer,'White, Yellow')
    writeFormattedExcelSheet(wmk,writer,'White, Yellow')

    mask= mask_OrangeBelt & compositMask
    wmk=newDataFrameFromMask( mask )
#    wmk.to_excel(writer,'Orange')
    writeFormattedExcelSheet(wmk,writer,'Orange')

    mask= mask_PurpleBelt & compositMask
    wmk=newDataFrameFromMask( mask )
#    wmk.to_excel(writer,'Purple')
    writeFormattedExcelSheet(wmk,writer,'Purple')

    mask = mask_AllBlueBelt & compositMask
    wmk=newDataFrameFromMask( mask )
#    wmk.to_excel(writer,'Blue, Blue Stripe')
    writeFormattedExcelSheet(wmk,writer,'Blue, Blue Stripe')

    mask = mask_AllGreenBelt & compositMask
    wmk=newDataFrameFromMask( mask )
#    wmk.to_excel(writer,'Green, Green Stripe')
    writeFormattedExcelSheet(wmk,writer,'Green, Green Stripe')

    mask = mask_AllBrownBelt & compositMask
    wmk=newDataFrameFromMask( mask )
#    wmk.to_excel(writer,'Brown')
    writeFormattedExcelSheet(wmk,writer,'Brown')

    mask= mask_AllBlackBelt & compositMask
    wmk=newDataFrameFromMask( mask )
#    wmk.to_excel(writer,'Black')
    writeFormattedExcelSheet(wmk,writer,'Black')

    writer.save()
    time.sleep(1)

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
def writePattern7ToExcel( filename, compositMask ):
    fullpath = os.getcwd() + pathDelimiter() + "Sorted" + pathDelimiter() + filename
    writer=pd.ExcelWriter(fullpath)
    print "Generating " + fullpath

    mask1= mask_WhiteBelt & compositMask
    mask2= mask_YellowBelt & compositMask
    mask3= mask_OrangeBelt & compositMask
    mask = mask1 | mask2 | mask3
    wmk=newDataFrameFromMask( mask )
#    wmk.to_excel(writer,'White, Yellow & Orange')
    writeFormattedExcelSheet(wmk,writer,'White, Yellow & Orange')

    mask1= mask_PurpleBelt & compositMask
    mask2= mask_AllBlueBelt & compositMask
    mask = mask1 | mask2
    wmk=newDataFrameFromMask( mask )
#    wmk.to_excel(writer,'Purple, Blue & Blue Stripe')
    writeFormattedExcelSheet(wmk,writer,'Purple, Blue & Blue Stripe')

    mask1= mask_AllGreenBelt & compositMask
    mask2= mask_AllBrownBelt & compositMask
    mask = mask1 | mask2
    wmk=newDataFrameFromMask( mask )
#    wmk.to_excel(writer,'Green, Green Stripe, Brown')
    writeFormattedExcelSheet(wmk,writer,'Green, Green Stripe, Brown')

    mask= mask_AllBlackBelt & compositMask
    wmk=newDataFrameFromMask( mask )
#    wmk.to_excel(writer,'Black')
    writeFormattedExcelSheet(wmk,writer,'Black')

    writer.save()
    time.sleep(1)

###############################################################################
# writeWeaponsDivision1ToExcel
#  arguments:
#  filename - the filename without path to write
#  compsitMask - a mask made up of everything but the belts that you want
#
def writeWeaponsDivision1ToExcel( filename, compositMask ):
    fullpath = os.getcwd() + pathDelimiter() + "Sorted" + pathDelimiter() + filename
    writer=pd.ExcelWriter(fullpath)
    print "Generating " + fullpath

    mask1= mask_WhiteBelt & compositMask
    mask2= mask_YellowBelt & compositMask
    mask3= mask_OrangeBelt & compositMask
    mask4= mask_PurpleBelt & compositMask
    mask5= mask_AllBlueBelt & compositMask
    mask6= mask_AllGreenBelt & compositMask
    mask7= mask_AllBrownBelt & compositMask
    mask8= mask_AllBlackBelt & compositMask

    mask = mask1 | mask2 | mask3 | mask4 | mask5 | mask6 | mask7 | mask8

    wmk=newDataFrameFromMask( mask )
#    wmk.to_excel(writer,'Weapons Division 1')
    writeFormattedExcelSheet(wmk,writer,'Weapons Division 1')

    writer.save()
    time.sleep(1)

###############################################################################
# writeWeaponsDivision2ToExcel
#  arguments:
#  filename - the filename without path to write
#  compsitMask - a mask made up of everything but the belts that you want
#
def writeWeaponsDivision2ToExcel( filename, compositMask ):
    fullpath = os.getcwd() + pathDelimiter() + "Sorted" + pathDelimiter() + filename
    writer=pd.ExcelWriter(fullpath)
    print "Generating " + fullpath

    mask1= mask_WhiteBelt & compositMask
    mask2= mask_YellowBelt & compositMask
    mask3= mask_OrangeBelt & compositMask
    mask4= mask_PurpleBelt & compositMask
    mask5= mask_AllBlueBelt & compositMask
    mask6= mask_AllGreenBelt & compositMask
    mask7= mask_AllBrownBelt & compositMask
    mask8= mask_AllBlackBelt & compositMask

    mask = mask1 | mask2 | mask3 | mask4 | mask5 | mask6 | mask7 | mask8

    wmk=newDataFrameFromMask( mask )
#    wmk.to_excel(writer,'Weapons Division 2')
    writeFormattedExcelSheet(wmk,writer,'Weapons Division 2')

    writer.save()
    time.sleep(1)


###############################################################################
# writeWeaponsDivision3ToFile
#  arguments:
#  filename - the filename without path to write
#  compsitMask - a mask made up of everything but the belts that you want
#
def writeWeaponsDivision3ToFile( filename, compositMask ):
    fullpath = os.getcwd() + pathDelimiter() + "Sorted" + pathDelimiter() + filename
    writer=pd.ExcelWriter(fullpath)
    print "Generating " + fullpath

    mask1= mask_WhiteBelt & compositMask
    mask2= mask_YellowBelt & compositMask
    mask3= mask_OrangeBelt & compositMask
    mask4= mask_PurpleBelt & compositMask
    mask5= mask_AllBlueBelt & compositMask
    mask6= mask_AllGreenBelt & compositMask

    mask = mask1 | mask2 | mask3 | mask4 | mask5 | mask6

    wmk=newDataFrameFromMask( mask )
#    wmk.to_excel(writer,'Weapons Division 3')
    writeFormattedExcelSheet(wmk,writer,'Weapons Division 3')

    writer.save()
    time.sleep(1)

###############################################################################
# writeWeaponsDivision4ToFile
#  arguments:
#  filename - the filename without path to write
#  compsitMask - a mask made up of everything but the belts that you want
#
def writeWeaponsDivision4ToFile( filename, compositMask ):
    fullpath = os.getcwd() + pathDelimiter() + "Sorted" + pathDelimiter() + filename
    writer=pd.ExcelWriter(fullpath)
    print "Generating " + fullpath

    mask1= mask_WhiteBelt & compositMask
    mask2= mask_YellowBelt & compositMask
    mask3= mask_OrangeBelt & compositMask
    mask4= mask_PurpleBelt & compositMask

    mask = mask1 | mask2 | mask3 | mask4

    wmk=newDataFrameFromMask( mask )
#    wmk.to_excel(writer,'Weapons Division 4')
    writeFormattedExcelSheet(wmk,writer,'Weapons Division 4')

    writer.save()
    time.sleep(1)

###############################################################################
#  writeWeaponsDivision5ToFile  18+ year Blue and Green
#  arguments:
#  filename - the filename without path to write
#  compsitMask - a mask made up of everything but the belts that you want
#
def writeWeaponsDivision5ToFile( filename, compositMask ):
    fullpath = os.getcwd() + pathDelimiter() + "Sorted" + pathDelimiter() + filename
    print "Generating " + fullpath
    writer=pd.ExcelWriter(fullpath)

    mask1 = mask_AllBlueBelt & compositMask
    mask2= mask_AllGreenBelt & compositMask
    mask = mask1 | mask2
    wmk=newDataFrameFromMask( mask )
#    wmk.to_excel(writer,'Weapons Division 5')
    writeFormattedExcelSheet(wmk,writer,'Weapons Division 5')

    writer.save()
    time.sleep(1)

###############################################################################
#  writeWeaponsDivision6ToFile
#  arguments:
#  filename - the filename without path to write
#  compsitMask - a mask made up of everything but the belts that you want
#
def writeWeaponsDivision6ToFile( filename, compositMask ):
    fullpath = os.getcwd() + pathDelimiter() + "Sorted" + pathDelimiter() + filename
    writer=pd.ExcelWriter(fullpath)
    print "Generating " + fullpath

    mask1= mask_AllBrownBelt & compositMask

    mask2= mask_AllBlackBelt & compositMask
    mask = mask1 | mask2
    wmk=newDataFrameFromMask( mask )
#    wmk.to_excel(writer,'Weapons Division 6')
    writeFormattedExcelSheet(wmk,writer,'Weapons Division 6')

    writer.save()
    time.sleep(1)

def writeSparingTreeToExcel( filename, compositMask):
    fullpath = os.getcwd() + pathDelimiter() + "Sorted" + pathDelimiter() + filename
    writer=pd.ExcelWriter(fullpath)
    print "Generating " + fullpath
    wmk=newDataFrameFromMask( compositMask )

#    byDojo = wmk.groupby('Select Your Z Ultimate Studio')
    byDojo = wmk.groupby('Dojo')

    print byDojo.size()

    writer.save()
    time.sleep(1)


###############################################################################
#
# Main Function
#
#Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
root = Tk()
root.withdraw() # we don't want a full GUI, so keep the root window from appearing
root.update() # Prevent the askfilename() window doesn't stay open
filename = askopenfilename()
root.update() # Prevent the askfilename() window doesn't stay open

#filename="/Volumes/1TB/Dropbox/TournamentProject/CleanRegistrantExport.csv" #For John Debugging
#filename = "C:\\Users\\Maria\\Downloads\\tournamentprojectmaterial\\RegistrantExport.csv"

print time.strftime("%X") + " Reading and processing the data...."


df=pd.read_csv(filename)
#cdf = df[np.isfinite(df['Registrant ID'])]

errorLogFileName=filename[0:len(filename)-4]+"-Error.txt"
errorLogFile= open(errorLogFileName, "w")

cdf = fixInput(df,errorLogFile)



###############################################################################
# test to see if the Age column is all numeric
#testdf = cdf.copy();
#try:
#  testdf[['Competitor\'s Age?']]=testdf[['Competitor\'s Age?']].astype(int)
#except ValueError:
#   print "The Age Column has non numeric data in it"
#   sys.exit("Exiting - The Age Column has non numeric data in it")
#print testdf.dtypes

################################################################################
##  Test Rank - looking for "Please Select"
#mask_NoBelt=(cdf['Current Belt Rank?']=='Please Select')
#df_NoBelt=cdf[['First Name','Last Name','Select Your Z Ultimate Studio','Email','Phone','Mobile Phone']][mask_NoBelt]
#errorCount = df_NoBelt.shape[0]
#if errorCount > 0:
#  print "The Following People did not select a valid rank:"
#  print df_NoBelt.values
#  sys.exit("Exiting - Not Everyone has a valid belt selected")



################################################################################
##  Test Event - looking for "Please Select"
#mask_NoEvent=cdf['Choose Forms, Sparring or Both.']=='Please Select'
#df_NoEvent=cdf[['First Name','Last Name','Select Your Z Ultimate Studio','Email','Phone','Mobile Phone']][mask_NoEvent]
#errorCount = df_NoEvent.shape[0]
#if errorCount > 0:
#  print "The Following People did not select a valid event:"
#  print df_NoEvent.values
#  sys.exit("Exiting - Not Everyone has a valid event")



####################
# Filtering        #
####################


###############################################################################
#  Define all the atomic masks

# Atomic masks for Belts
mask_WhiteBelt=cdf['Current Belt Rank?']=='White'
mask_YellowBelt=cdf['Current Belt Rank?']=='Yellow'
mask_OrangeBelt=cdf['Current Belt Rank?']=='Orange'
mask_PurpleBelt=cdf['Current Belt Rank?']=='Purple'
mask_BlueBelt=cdf['Current Belt Rank?']=='Blue'
mask_BlueStripeBelt=cdf['Current Belt Rank?']=='Blue w/Stripe'
mask_AllBlueBelt = mask_BlueBelt | mask_BlueStripeBelt #all blue and blue stripe
#testBluedf=newDataFrameFromMask( mask_AllBlueBelt )
mask_GreenBelt=cdf['Current Belt Rank?']=='Green'
mask_GreenStripeBelt=cdf['Current Belt Rank?']=='Green w/Stripe'
mask_AllGreenBelt = mask_GreenBelt | mask_GreenStripeBelt #all Green and Green stripe
#testGreendf=newDataFrameFromMask( mask_AllGreenBelt )
mask_3rdBrownBelt=cdf['Current Belt Rank?']=='Brown 3rd Degree'
mask_2ndBrownBelt=cdf['Current Belt Rank?']=='Brown 2nd Degree'
mask_1stBrownBelt=cdf['Current Belt Rank?']=='Brown 1st Degree'
mask_AllBrownBelt = mask_3rdBrownBelt | mask_2ndBrownBelt | mask_1stBrownBelt #all 1st 2nd and 3rd Brown
#testBrowndf=newDataFrameFromMask( mask_AllBrownBelt )
mask_1stBlackBelt=cdf['Current Belt Rank?']=='Black 1st Degree'
mask_2ndBlackBelt=cdf['Current Belt Rank?']=='Black 2nd Degree'
mask_3rdBlackBelt=cdf['Current Belt Rank?']=='Black 3rd Degree'
mask_AllBlackBelt = mask_1stBlackBelt | mask_2ndBlackBelt | mask_3rdBlackBelt #all 1st 2nd and 3rd Brown
#testBlackdf=newDataFrameFromMask( mask_AllBlackBelt )

# Atomic mask for Gender
mask_Male=cdf['Gender']=='Male'
mask_Female=cdf['Gender']=='Female'

# Atomic and composit mask for which event Sparring, Kata, Weapons
mask_SparringAndForms=cdf['Choose Forms, Sparring or Both.']=='2 Events - Forms & Sparring ($75)'
mask_FormsOnly=cdf['Choose Forms, Sparring or Both.']=='1 Event - Forms ($75)'
mask_SparringOnly=cdf['Choose Forms, Sparring or Both.']=='1 Event - Sparring ($75)'
# Mask for Weapons
mask_Weapons=cdf['Choose Weapons.']=='Weapons ($35)'
testdf=cdf[['First Name','Last Name', 'Gender','Current Belt Rank?','Competitor\'s Age?','Competitor\'s Weight (eg. 73lbs.)?','Competitor\'s Height (e.g. 4 ft. 2 in. )?','Choose Forms, Sparring or Both.','Choose Weapons.']][mask_Weapons]


# Composit Masks for Sparring or Forms
mask_Sparring= mask_SparringAndForms | mask_SparringOnly
mask_Forms= mask_SparringAndForms | mask_FormsOnly
#testdf=cdf[['First Name','Last Name', 'Gender','Current Belt Rank?','Competitor\'s Age?','Competitor\'s Weight (in lbs.)?','Competitor\'s Height (in feet and inches)?','Choose Forms, Sparring or Both.','Choose Weapons.']][mask_Forms]

# Atomic mask for age groups found in the tournament guide
# 4-6 used for kids kata, kids sparring,
maskLowAge=cdf["Competitor\'s Age?"]>=4
maskHighAge=cdf["Competitor\'s Age?"]<=6
mask_Age4to6 = maskLowAge & maskHighAge
#testdf=cdf[['First Name','Last Name', 'Gender','Current Belt Rank?','Competitor\'s Age?','Competitor\'s Weight (in lbs.)?','Competitor\'s Height (in feet and inches)?','Choose Forms, Sparring or Both.','Choose Weapons.']][mask_Age4to6]

# 7-9 used in Youth Kata, Young Girls Sparring, Youth Boys Sparring
maskLowAge=cdf["Competitor\'s Age?"]>=7
maskHighAge=cdf["Competitor\'s Age?"]<=9
mask_Age7to9 = maskLowAge & maskHighAge
#testdf=cdf[['First Name','Last Name', 'Gender','Current Belt Rank?','Competitor\'s Age?','Competitor\'s Weight (in lbs.)?','Competitor\'s Height (in feet and inches)?','Choose Forms, Sparring or Both.','Choose Weapons.']][mask_Age7to9]

# 10-12 used in Boys Sparring, Boys & Girls Kata, Girls Sparring
maskLowAge=cdf["Competitor\'s Age?"]>=10
maskHighAge=cdf["Competitor\'s Age?"]<=12
mask_Age10to12 = maskLowAge & maskHighAge
#testdf=cdf[['First Name','Last Name', 'Gender','Current Belt Rank?','Competitor\'s Age?','Competitor\'s Weight (in lbs.)?','Competitor\'s Height (in feet and inches)?','Choose Forms, Sparring or Both.','Choose Weapons.']][mask_Age10to12]

# 13-15 used in Teen Girls Sparring, Teen Kata, Teen Boys Sparring,
maskLowAge=cdf["Competitor\'s Age?"]>=13
maskHighAge=cdf["Competitor\'s Age?"]<=15
mask_Age13to15 = maskLowAge & maskHighAge
#testdf=cdf[['First Name','Last Name', 'Gender','Current Belt Rank?','Competitor\'s Age?','Competitor\'s Weight (in lbs.)?','Competitor\'s Height (in feet and inches)?','Choose Forms, Sparring or Both.','Choose Weapons.']][mask_Age13to15]

# 4-9 used in Weapons Division 1
maskLowAge=cdf["Competitor\'s Age?"]>=4
maskHighAge=cdf["Competitor\'s Age?"]<=9
mask_Age4to9 = maskLowAge & maskHighAge
#testdf=cdf[['First Name','Last Name', 'Gender','Current Belt Rank?','Competitor\'s Age?','Competitor\'s Weight (in lbs.)?','Competitor\'s Height (in feet and inches)?','Choose Forms, Sparring or Both.','Choose Weapons.']][mask_Age4to9]

# 18-39 used in Womans Sprring, Men and Womens Kata
maskLowAge=cdf["Competitor\'s Age?"]>=18
maskHighAge=cdf["Competitor\'s Age?"]<=39
mask_Age18to39 = maskLowAge & maskHighAge
#testdf=cdf[['First Name','Last Name', 'Gender','Current Belt Rank?','Competitor\'s Age?','Competitor\'s Weight (in lbs.)?','Competitor\'s Height (in feet and inches)?','Choose Forms, Sparring or Both.','Choose Weapons.']][mask_Age18to39]

# 40 plus used in Senior Mens Sparring, Senior Womens Sparring, Senior Kata
mask_Age40Plus=cdf["Competitor\'s Age?"]>=40
#testdf=cdf[['First Name','Last Name', 'Gender','Current Belt Rank?','Competitor\'s Age?','Competitor\'s Weight (in lbs.)?','Competitor\'s Height (in feet and inches)?','Choose Forms, Sparring or Both.','Choose Weapons.']][mask_Age40Plus]

# 16-17 used in Young Adult Kata, Young Mens Sparring, Young Adult Womens Sparring
maskLowAge=cdf["Competitor\'s Age?"]>=16
maskHighAge=cdf["Competitor\'s Age?"]<=17
mask_Age16to17 = maskLowAge & maskHighAge
#testdf=cdf[['First Name','Last Name', 'Gender','Current Belt Rank?','Competitor\'s Age?','Competitor\'s Weight (in lbs.)?','Competitor\'s Height (in feet and inches)?','Choose Forms, Sparring or Both.','Choose Weapons.']][mask_Age16to17]

# 13-17 used in Weapons Division 3
maskLowAge=cdf["Competitor\'s Age?"]>=13
maskHighAge=cdf["Competitor\'s Age?"]<=17
mask_Age13to17 = maskLowAge & maskHighAge
#testdf=cdf[['First Name','Last Name', 'Gender','Current Belt Rank?','Competitor\'s Age?','Competitor\'s Weight (in lbs.)?','Competitor\'s Height (in feet and inches)?','Choose Forms, Sparring or Both.','Choose Weapons.']][mask_Age13to17]

# 18 plus used in Weapons Division 4 and 5
mask_Age18Plus=cdf["Competitor\'s Age?"]>=18
#testdf=cdf[['First Name','Last Name', 'Gender','Current Belt Rank?','Competitor\'s Age?','Competitor\'s Weight (in lbs.)?','Competitor\'s Height (in feet and inches)?','Choose Forms, Sparring or Both.','Choose Weapons.']][mask_Age18Plus]

# 13 plus used in Weapons Division 6
mask_Age13Plus=cdf["Competitor\'s Age?"]>=13
#testdf=cdf[['First Name','Last Name', 'Gender','Current Belt Rank?','Competitor\'s Age?','Competitor\'s Weight (in lbs.)?','Competitor\'s Height (in feet and inches)?','Choose Forms, Sparring or Both.','Choose Weapons.']][mask_Age13Plus]

print time.strftime("%X") + " Generating the output results..."

###############################################################################
# Kids Kata Spreadsheet - 4-6 year olds one sheet per rank
#
compositMask=mask_Forms & mask_Age4to6
writePattern1ToExcel( "KidsKata.xlsx", compositMask )

### 9AM Events

###############################################################################
# Youth Kata Spreadsheet - 7-9 year olds one sheet per rank
#
compositMask=mask_Forms & mask_Age7to9
writePattern3ToExcel( "YouthKata.xlsx", compositMask )

###############################################################################
# Boy's Sparring Spreadsheet - 10-12 year olds one sheet per rank
#
compositMask=mask_Sparring & mask_Age10to12 & mask_Male
writePattern6ToExcel( "BoysSparring.xlsx", compositMask )
writeSparingTreeToExcel( "BoysSparringTree.xlsx", compositMask )

### 9:45 Events

###############################################################################
# Kids Sparring Spreadsheet - 4-6 year olds one sheet per rank
#
compositMask=mask_Sparring & mask_Age4to6
writePattern2ToExcel( "KidsSparring.xlsx", compositMask )

###############################################################################
# Boys & Girls Kata Spreadsheet - 10-12 year olds one sheet per rank
#
compositMask=mask_Forms & mask_Age10to12
writePattern6ToExcel( "BoysGilrsKata.xlsx", compositMask )

### 10:30 Events

###############################################################################
# Youth Girls Sparring Spreadsheet - 7-9 year olds one sheet per rank
#
compositMask=mask_Sparring & mask_Female & mask_Age7to9
writePattern5ToExcel( "YouthGirlSparring.xlsx", compositMask )

###############################################################################
# Youth Boys Sparring Spreadsheet - 7-9 year olds one sheet per rank
#
compositMask=mask_Sparring & mask_Male & mask_Age7to9
writePattern5ToExcel( "YouthBoysSparring.xlsx", compositMask )

###############################################################################
# Girl's Sparring Spreadsheet - 10-12 year olds one sheet per rank
#
compositMask=mask_Sparring & mask_Age10to12 & mask_Female
writePattern4ToExcel( "GirlsSparring.xlsx", compositMask )

### 11:15 Events

###############################################################################
# Teen Girls Sparring Spreadsheet - 13-15 year olds one sheet per rank
#
compositMask=mask_Sparring & mask_Female & mask_Age13to15
writePattern4ToExcel( "TeenGirlSparring.xlsx", compositMask )

###############################################################################
# Womans Sparring Spreadsheet - 18-39 year olds one sheet per rank
#
compositMask=mask_Sparring & mask_Female & mask_Age18to39
writePattern4ToExcel( "WomensSparring.xlsx", compositMask )

###############################################################################
# Weapons Division 1 - 13-15 year olds one sheet per rank
#
compositMask=mask_Weapons & mask_Age4to9
writeWeaponsDivision1ToExcel( "WeaponsDivision1.xlsx", compositMask )

###############################################################################
# Weapons Division 1 - 10-12 year olds one sheet per rank
#
compositMask=mask_Weapons & mask_Age10to12
writeWeaponsDivision2ToExcel( "WeaponsDivision2.xlsx", compositMask )

### 1:30 Events

###############################################################################
# Men And Womens Kata - 18-39 year olds one sheet per rank
#
compositMask=mask_Forms & mask_Age18to39
writePattern6ToExcel( "MenAndWomensKata.xlsx", compositMask )


###############################################################################
# Teen Kata - 13-15 year olds one sheet per rank
#
compositMask=mask_Forms & mask_Age13to15
writePattern6ToExcel( "TeenKata.xlsx", compositMask )

### 2:15 Events

###############################################################################
# Senior Mens Sparring - 40+ year olds one sheet per rank
#
compositMask=mask_Sparring & mask_Male & mask_Age40Plus
writePattern4ToExcel( "SeniorMensSparring.xlsx", compositMask )

###############################################################################
# Senior Womens Sparring - 40+ year olds one sheet per rank
#
compositMask=mask_Sparring & mask_Female & mask_Age40Plus
writePattern4ToExcel( "SeniorWomensSparring.xlsx", compositMask )


###############################################################################
# Young Adult Kata - 16-17 year olds one sheet per rank
#
compositMask=mask_Forms & mask_Age16to17
writePattern4ToExcel( "YoungAdultKata.xlsx", compositMask )

### 3:00 Events

###############################################################################
#  Mens Sparring - 18-39 year olds one sheet per rank
#
compositMask=mask_Sparring & mask_Male & mask_Age18to39
writePattern4ToExcel( "MensSparring.xlsx", compositMask )

###############################################################################
#  Teen Boys Sparring - 13-15 year olds one sheet per rank
#
compositMask=mask_Sparring & mask_Male & mask_Age13to15
writePattern4ToExcel( "TeenBoysSparring.xlsx", compositMask )

###############################################################################
#  Young Adult Mens Sparring - 16-17 year olds one sheet per rank
#
compositMask=mask_Sparring & mask_Male & mask_Age16to17
writePattern4ToExcel( "YoungAdultMensSparring.xlsx", compositMask )

### 3:45 Events

###############################################################################
# Senior Kata - 40+ year olds one sheet per rank
#
compositMask=mask_Forms & mask_Age40Plus
writePattern6ToExcel( "SeniorKata.xlsx", compositMask )

###############################################################################
#  Young Adult Womens Sparring - 16-17 year olds one sheet per rank
#
compositMask=mask_Sparring & mask_Female & mask_Age16to17
writePattern7ToExcel( "YoungAdultWomensSparring.xlsx", compositMask )

### 4:15 Events

###############################################################################
#  WeaponsDivision3 13-17 year olds one sheet per rank
#
compositMask=mask_Weapons & mask_Age13to17
writeWeaponsDivision3ToFile( "WeaponsDivision3.xlsx", compositMask )

###############################################################################
#  WeaponsDivision4 18+ year olds one sheet per rank
#
compositMask=mask_Weapons & mask_Age18Plus
writeWeaponsDivision4ToFile( "WeaponsDivision4.xlsx", compositMask )


###############################################################################
#  WeaponsDivision5 18+ year olds one sheet per rank
#
compositMask=mask_Weapons & mask_Age18Plus
writeWeaponsDivision5ToFile( "WeaponsDivision5.xlsx", compositMask )

###############################################################################
#  WeaponsDivision6 18+ year olds one sheet per rank
#
compositMask=mask_Weapons & mask_Age13Plus
writeWeaponsDivision6ToFile( "WeaponsDivision6.xlsx", compositMask )

localtime = time.asctime( time.localtime(time.time()) )
print  time.strftime("%X") + " Done!"
