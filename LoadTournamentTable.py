#   Feautres to add:
# Better error handling - loop through each record looking for bogus stuff and print an error message telling what's wrong with it
# Summary Stats - how many people of each belt, how many sparring, how may forms, how many weaponds
# Event Stats - how many people in each event as per the event guide
#
#
#


import pandas as pd
import numpy as np
from Tkinter import Tk
from tkFileDialog import askopenfilename
import os
import sys
from pandas import ExcelWriter
import time

#import sys
#matplotlib inline


###############################################################################
# checkInput
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

   # if there are errors exit
    if( errorCount > 0):
        errorLogFile.write( str(errorCount)+" "+"errors found" )
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
#    newdf = cdf[["First Name", "Last Name", "Gender","Select Your Z Ultimate Studio","Out of State Studio Name", "Competitor's Age?", "Current Belt Rank?", "Competitor's Weight (in lbs.)?", "Competitor's Height (in feet and inches)?", "Choose Forms, Sparring or Both.", "Choose Weapons.","Parent or Guardian Name (if competitor is under 18)?","Phone","Mobile Phone"]][mask].sort("Competitor's Age?")
    newdf = cdf[["First Name", "Last Name", "Gender","Select Your Z Ultimate Studio","Out of State Studio Name", "Competitor's Age?", "Current Belt Rank?", "Competitor's Weight (in lbs.)?", "Competitor's Height (in feet and inches)?", "Choose Forms, Sparring or Both.", "Choose Weapons."]][mask].sort("Competitor's Age?")
    return newdf

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
    writer=ExcelWriter(fullpath)
    print "Generating " + fullpath

    mask= mask_WhiteBelt & compositMask
    wmk=newDataFrameFromMask( mask )
    wmk.to_excel(writer,'White')

    mask= mask_YellowBelt & compositMask
    wmk=newDataFrameFromMask( mask )
    wmk.to_excel(writer,'Yellow')

    mask= mask_OrangeBelt & compositMask
    wmk=newDataFrameFromMask( mask )
    wmk.to_excel(writer,'Orange')

    mask= mask_PurpleBelt & compositMask
    wmk=newDataFrameFromMask( mask )
    wmk.to_excel(writer,'Purple')

    mask= mask_AllBlueBelt & compositMask
    wmk=newDataFrameFromMask( mask )
    wmk.to_excel(writer,'Blue')

    mask= mask_AllGreenBelt & compositMask
    wmk=newDataFrameFromMask( mask )
    wmk.to_excel(writer,'Green')

    mask= mask_AllBrownBelt & compositMask
    wmk=newDataFrameFromMask( mask )
    wmk.to_excel(writer,'Brown')

    mask= mask_AllBlackBelt & compositMask
    wmk=newDataFrameFromMask( mask )
    wmk.to_excel(writer,'Black')

    writer.save()
    time.sleep(1)

###############################################################################
# writeWeaponsDivision3ToFile
#  arguments:
#  filename - the filename without path to write
#  compsitMask - a mask made up of everything but the belts that you want
#
def writeWeaponsDivision3ToFile( filename, compositMask ):
#    fullpath = os.getcwd() + "\\Sorted\\" + filename  #Windows
#    fullpath = os.getcwd() + "/Sorted/" + filename  #Mac
    fullpath = os.getcwd() + pathDelimiter() + "Sorted" + pathDelimiter() + filename
    writer=ExcelWriter(fullpath)
    print "Generating " + fullpath

    mask1= mask_WhiteBelt & compositMask
    mask2= mask_YellowBelt & compositMask
    mask3= mask_OrangeBelt & compositMask
    mask4= mask_PurpleBelt & compositMask
    mask5= mask_AllBlueBelt & compositMask
    mask6= mask_AllGreenBelt & compositMask

    mask = mask1 | mask2 | mask3 | mask4 | mask5 | mask6

    wmk=newDataFrameFromMask( mask )
    wmk.to_excel(writer,'Division3')

#    mask= mask_AllBrownBelt & compositMask
#    wmk=newDataFrameFromMask( mask )
#    wmk.to_excel(writer,'Brown')

#    mask= mask_AllBlackBelt & compositMask
#    wmk=newDataFrameFromMask( mask )
#    wmk.to_excel(writer,'Black')


    writer.save()
    time.sleep(1)

###############################################################################
# writeWeaponsDivision4ToFile
#  arguments:
#  filename - the filename without path to write
#  compsitMask - a mask made up of everything but the belts that you want
#
def writeWeaponsDivision4ToFile( filename, compositMask ):
#    fullpath = os.getcwd() + "\\Sorted\\" + filename  #Windows
#    fullpath = os.getcwd() + "/Sorted/" + filename  #Mac
    fullpath = os.getcwd() + pathDelimiter() + "Sorted" + pathDelimiter() + filename
    writer=ExcelWriter(fullpath)
    print "Generating " + fullpath

    mask1= mask_WhiteBelt & compositMask
    mask2= mask_YellowBelt & compositMask
    mask3= mask_OrangeBelt & compositMask
    mask4= mask_PurpleBelt & compositMask

    mask = mask1 | mask2 | mask3 | mask4

    wmk=newDataFrameFromMask( mask )
    wmk.to_excel(writer,'Division4')

    writer.save()
    time.sleep(1)

###############################################################################
#  writeWeaponsDivision5ToFile  18+ year Blue and Green
#  arguments:
#  filename - the filename without path to write
#  compsitMask - a mask made up of everything but the belts that you want
#
def writeWeaponsDivision5ToFile( filename, compositMask ):
#    fullpath = os.getcwd() + "\\Sorted\\" + filename  #Windows
#    fullpath = os.getcwd() + "/Sorted/" + filename  #Mac
    fullpath = os.getcwd() + pathDelimiter() + "Sorted" + pathDelimiter() + filename
    print "Generating " + fullpath
    writer=ExcelWriter(fullpath)

    mask1 = mask_AllBlueBelt & compositMask
    mask2= mask_AllGreenBelt & compositMask
    mask = mask1 | mask2
    wmk=newDataFrameFromMask( mask )
    wmk.to_excel(writer,'Division5')

    writer.save()
    time.sleep(1)

###############################################################################
#  writeWeaponsDivision6ToFile
#  arguments:
#  filename - the filename without path to write
#  compsitMask - a mask made up of everything but the belts that you want
#
def writeWeaponsDivision6ToFile( filename, compositMask ):
#    fullpath = os.getcwd() + "\\Sorted\\" + filename  #Windows
#    fullpath = os.getcwd() + "/Sorted/" + filename  #Mac
    fullpath = os.getcwd() + pathDelimiter() + "Sorted" + pathDelimiter() + filename
    writer=ExcelWriter(fullpath)
    print "Generating " + fullpath

    mask1= mask_AllBrownBelt & compositMask

    mask2= mask_AllBlackBelt & compositMask
    mask = mask1 | mask2
    wmk=newDataFrameFromMask( mask )
    wmk.to_excel(writer,'Division6')

    writer.save()
    time.sleep(1)



Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
filename = askopenfilename()
#filename="/Volumes/1TB/Dropbox/TournamentProject/CleanRegistrantExport.csv" #For John Debugging
#filename = "C:\\Users\\Maria\\Downloads\\tournamentprojectmaterial\\RegistrantExport.csv"
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
testdf=cdf[['First Name','Last Name', 'Gender','Current Belt Rank?','Competitor\'s Age?','Competitor\'s Weight (in lbs.)?','Competitor\'s Height (in feet and inches)?','Choose Forms, Sparring or Both.','Choose Weapons.']][mask_Weapons]


# Composit Masks for Sparring or Forms
mask_Sparring= mask_SparringAndForms | mask_SparringOnly
mask_Forms= mask_SparringAndForms | mask_FormsOnly
#testdf=cdf[['First Name','Last Name', 'Gender','Current Belt Rank?','Competitor\'s Age?','Competitor\'s Weight (in lbs.)?','Competitor\'s Height (in feet and inches)?','Choose Forms, Sparring or Both.','Choose Weapons.']][mask_Forms]

# Atomic mask for age groups found in the tournament guide
# 4-6 used for kids kata, kids sparring,
maskLowAge=cdf["Competitor's Age?"]>=4
maskHighAge=cdf["Competitor's Age?"]<=6
mask_Age4to6 = maskLowAge & maskHighAge
#testdf=cdf[['First Name','Last Name', 'Gender','Current Belt Rank?','Competitor\'s Age?','Competitor\'s Weight (in lbs.)?','Competitor\'s Height (in feet and inches)?','Choose Forms, Sparring or Both.','Choose Weapons.']][mask_Age4to6]

# 7-9 used in Youth Kata, Young Girls Sparring, Youth Boys Sparring
maskLowAge=cdf["Competitor's Age?"]>=7
maskHighAge=cdf["Competitor's Age?"]<=9
mask_Age7to9 = maskLowAge & maskHighAge
#testdf=cdf[['First Name','Last Name', 'Gender','Current Belt Rank?','Competitor\'s Age?','Competitor\'s Weight (in lbs.)?','Competitor\'s Height (in feet and inches)?','Choose Forms, Sparring or Both.','Choose Weapons.']][mask_Age7to9]

# 10-12 used in Boys Sparring, Boys & Girls Kata, Girls Sparring
maskLowAge=cdf["Competitor's Age?"]>=10
maskHighAge=cdf["Competitor's Age?"]<=12
mask_Age10to12 = maskLowAge & maskHighAge
#testdf=cdf[['First Name','Last Name', 'Gender','Current Belt Rank?','Competitor\'s Age?','Competitor\'s Weight (in lbs.)?','Competitor\'s Height (in feet and inches)?','Choose Forms, Sparring or Both.','Choose Weapons.']][mask_Age10to12]

# 13-15 used in Teen Girls Sparring, Teen Kata, Teen Boys Sparring,
maskLowAge=cdf["Competitor's Age?"]>=13
maskHighAge=cdf["Competitor's Age?"]<=15
mask_Age13to15 = maskLowAge & maskHighAge
#testdf=cdf[['First Name','Last Name', 'Gender','Current Belt Rank?','Competitor\'s Age?','Competitor\'s Weight (in lbs.)?','Competitor\'s Height (in feet and inches)?','Choose Forms, Sparring or Both.','Choose Weapons.']][mask_Age13to15]

# 4-9 used in Weapons Division 1
maskLowAge=cdf["Competitor's Age?"]>=4
maskHighAge=cdf["Competitor's Age?"]<=9
mask_Age4to9 = maskLowAge & maskHighAge
#testdf=cdf[['First Name','Last Name', 'Gender','Current Belt Rank?','Competitor\'s Age?','Competitor\'s Weight (in lbs.)?','Competitor\'s Height (in feet and inches)?','Choose Forms, Sparring or Both.','Choose Weapons.']][mask_Age4to9]

# 18-39 used in Womans Sprring, Men and Womens Kata
maskLowAge=cdf["Competitor's Age?"]>=18
maskHighAge=cdf["Competitor's Age?"]<=39
mask_Age18to39 = maskLowAge & maskHighAge
#testdf=cdf[['First Name','Last Name', 'Gender','Current Belt Rank?','Competitor\'s Age?','Competitor\'s Weight (in lbs.)?','Competitor\'s Height (in feet and inches)?','Choose Forms, Sparring or Both.','Choose Weapons.']][mask_Age18to39]

# 40 plus used in Senior Mens Sparring, Senior Womens Sparring, Senior Kata
mask_Age40Plus=cdf["Competitor's Age?"]>=40
#testdf=cdf[['First Name','Last Name', 'Gender','Current Belt Rank?','Competitor\'s Age?','Competitor\'s Weight (in lbs.)?','Competitor\'s Height (in feet and inches)?','Choose Forms, Sparring or Both.','Choose Weapons.']][mask_Age40Plus]

# 16-17 used in Young Adult Kata, Young Mens Sparring, Young Adult Womens Sparring
maskLowAge=cdf["Competitor's Age?"]>=16
maskHighAge=cdf["Competitor's Age?"]<=17
mask_Age16to17 = maskLowAge & maskHighAge
#testdf=cdf[['First Name','Last Name', 'Gender','Current Belt Rank?','Competitor\'s Age?','Competitor\'s Weight (in lbs.)?','Competitor\'s Height (in feet and inches)?','Choose Forms, Sparring or Both.','Choose Weapons.']][mask_Age16to17]

# 13-17 used in Weapons Division 3
maskLowAge=cdf["Competitor's Age?"]>=13
maskHighAge=cdf["Competitor's Age?"]<=17
mask_Age13to17 = maskLowAge & maskHighAge
#testdf=cdf[['First Name','Last Name', 'Gender','Current Belt Rank?','Competitor\'s Age?','Competitor\'s Weight (in lbs.)?','Competitor\'s Height (in feet and inches)?','Choose Forms, Sparring or Both.','Choose Weapons.']][mask_Age13to17]

# 18 plus used in Weapons Division 4 and 5
mask_Age18Plus=cdf["Competitor's Age?"]>=18
#testdf=cdf[['First Name','Last Name', 'Gender','Current Belt Rank?','Competitor\'s Age?','Competitor\'s Weight (in lbs.)?','Competitor\'s Height (in feet and inches)?','Choose Forms, Sparring or Both.','Choose Weapons.']][mask_Age18Plus]

# 13 plus used in Weapons Division 6
mask_Age13Plus=cdf["Competitor's Age?"]>=13
#testdf=cdf[['First Name','Last Name', 'Gender','Current Belt Rank?','Competitor\'s Age?','Competitor\'s Weight (in lbs.)?','Competitor\'s Height (in feet and inches)?','Choose Forms, Sparring or Both.','Choose Weapons.']][mask_Age13Plus]

###############################################################################
# Kids Kata Spreadsheet - 4-6 year olds one sheet per rank
#
compositMask=mask_Forms & mask_Age4to6
#wmk=newDataFrameFromMask( compositMask )
writeEventToFile( "KidsKata.xlsx", compositMask )

###############################################################################
# Youth Kata Spreadsheet - 7-9 year olds one sheet per rank
#
compositMask=mask_Forms & mask_Age7to9
#wmk=newDataFrameFromMask( compositMask )
writeEventToFile( "YouthKata.xlsx", compositMask )

###############################################################################
# Boy's Sparring Spreadsheet - 10-12 year olds one sheet per rank
#
compositMask=mask_Sparring & mask_Age10to12 & mask_Male
#wmk=newDataFrameFromMask( compositMask )
writeEventToFile( "BoysSparring.xlsx", compositMask )

###############################################################################
# Kids Sparring Spreadsheet - 4-6 year olds one sheet per rank
#
compositMask=mask_Sparring & mask_Age4to6
writeEventToFile( "KidsSparring.xlsx", compositMask )

###############################################################################
# Boys & Girls Kata Spreadsheet - 10-12 year olds one sheet per rank
#
compositMask=mask_Forms & mask_Age10to12
writeEventToFile( "BoysGilrsKata.xlsx", compositMask )

###############################################################################
# Youth Girls Sparring Spreadsheet - 7-9 year olds one sheet per rank
#
compositMask=mask_Sparring & mask_Female & mask_Age7to9
writeEventToFile( "YouthGirlSparring.xlsx", compositMask )

###############################################################################
# Youth Boys Sparring Spreadsheet - 7-9 year olds one sheet per rank
#
compositMask=mask_Sparring & mask_Male & mask_Age7to9
writeEventToFile( "YouthBoysSparring.xlsx", compositMask )

###############################################################################
# Girl's Sparring Spreadsheet - 10-12 year olds one sheet per rank
#
compositMask=mask_Sparring & mask_Age10to12 & mask_Female
#wmk=newDataFrameFromMask( compositMask )
writeEventToFile( "GirlsSparring.xlsx", compositMask )


###############################################################################
# Teen Girls Sparring Spreadsheet - 13-15 year olds one sheet per rank
#
compositMask=mask_Sparring & mask_Female & mask_Age13to15
#wmk=newDataFrameFromMask( compositMask )
writeEventToFile( "TeenGirlSparring.xlsx", compositMask )

###############################################################################
# Womans Sparring Spreadsheet - 18-39 year olds one sheet per rank
#
compositMask=mask_Sparring & mask_Female & mask_Age18to39
#wmk=newDataFrameFromMask( compositMask )
writeEventToFile( "WomensSparring.xlsx", compositMask )

###############################################################################
# Weapons Division 1 - 13-15 year olds one sheet per rank
#
compositMask=mask_Weapons & mask_Age4to9
#wmk=newDataFrameFromMask( compositMask )
writeEventToFile( "WeaponsDivision1.xlsx", compositMask )

###############################################################################
# Weapons Division 1 - 10-12 year olds one sheet per rank
#
compositMask=mask_Weapons & mask_Age10to12
#wmk=newDataFrameFromMask( compositMask )
writeEventToFile( "WeaponsDivision2.xlsx", compositMask )

###############################################################################
# Men And Womens Kata - 18-39 year olds one sheet per rank
#
compositMask=mask_Forms & mask_Age18to39
#wmk=newDataFrameFromMask( compositMask )
writeEventToFile( "MenAndWomensKata.xlsx", compositMask )

###############################################################################
# Teen Kata - 13-15 year olds one sheet per rank
#
compositMask=mask_Forms & mask_Age13to15
#wmk=newDataFrameFromMask( compositMask )
writeEventToFile( "TeenKata.xlsx", compositMask )

###############################################################################
# Senior Mens Sparring - 40+ year olds one sheet per rank
#
compositMask=mask_Sparring & mask_Male & mask_Age40Plus
#wmk=newDataFrameFromMask( compositMask )
writeEventToFile( "SeniorMensSparring.xlsx", compositMask )

###############################################################################
# Senior Womens Sparring - 40+ year olds one sheet per rank
#
compositMask=mask_Sparring & mask_Female & mask_Age40Plus
#wmk=newDataFrameFromMask( compositMask )
writeEventToFile( "SeniorWomensSparring.xlsx", compositMask )

###############################################################################
# Young Adult Kata - 16-17 year olds one sheet per rank
#
compositMask=mask_Forms & mask_Age16to17
#wmk=newDataFrameFromMask( compositMask )
writeEventToFile( "YoungAdultKata.xlsx", compositMask )

###############################################################################
#  Mens Sparring - 18-39 year olds one sheet per rank
#
compositMask=mask_Sparring & mask_Male & mask_Age18to39
#wmk=newDataFrameFromMask( compositMask )
writeEventToFile( "MensSparring.xlsx", compositMask )

###############################################################################
#  Teen Boys Sparring - 13-15 year olds one sheet per rank
#
compositMask=mask_Sparring & mask_Male & mask_Age13to15
#wmk=newDataFrameFromMask( compositMask )
writeEventToFile( "TeenBoysSparring.xlsx", compositMask )

###############################################################################
# Senior Kata - 40+ year olds one sheet per rank
#
compositMask=mask_Forms & mask_Age40Plus
#wmk=newDataFrameFromMask( compositMask )
writeEventToFile( "SeniorKata.xlsx", compositMask )

###############################################################################
#  Young Adult Mens Sparring - 16-17 year olds one sheet per rank
#
compositMask=mask_Sparring & mask_Male & mask_Age16to17
#wmk=newDataFrameFromMask( compositMask )
writeEventToFile( "YoungAdultMensSparring.xlsx", compositMask )

###############################################################################
#  Young Adult Womens Sparring - 16-17 year olds one sheet per rank
#
compositMask=mask_Sparring & mask_Female & mask_Age16to17
#wmk=newDataFrameFromMask( compositMask )
writeEventToFile( "YoungAdultWomensSparring.xlsx", compositMask )

###############################################################################
#  WeaponsDivision3 13-17 year olds one sheet per rank
#
compositMask=mask_Weapons & mask_Age13to17
#wmk=newDataFrameFromMask( compositMask )
writeWeaponsDivision3ToFile( "WeaponsDivision3.xlsx", compositMask )

###############################################################################
#  WeaponsDivision4 18+ year olds one sheet per rank
#
compositMask=mask_Weapons & mask_Age18Plus
wmk=newDataFrameFromMask( compositMask )
writeWeaponsDivision4ToFile( "WeaponsDivision4.xlsx", compositMask )


###############################################################################
#  WeaponsDivision5 18+ year olds one sheet per rank
#
compositMask=mask_Weapons & mask_Age18Plus
wmk=newDataFrameFromMask( compositMask )
writeWeaponsDivision5ToFile( "WeaponsDivision5.xlsx", compositMask )

###############################################################################
#  WeaponsDivision6 18+ year olds one sheet per rank
#
compositMask=mask_Weapons & mask_Age13Plus
#wmk=newDataFrameFromMask( compositMask )
writeWeaponsDivision6ToFile( "WeaponsDivision6.xlsx", compositMask )

print "Done!"
