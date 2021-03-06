import sys
import time
import math

import numpy as np
import pandas as pd

#from LoadTournamentTable import df

###############################################################################
# clean_unicode_from_file
#  This function removes unicode characters from the input file and writes a warning to the error file
def clean_unicode_from_file(inputFileName, errorLogFile):
    import io
    with io.open(inputFileName, 'r+b') as f:
        while True:
            b = f.read(1)
            if not b:
                break
            if (b > b'\x7f'):
                errorString="Warning:  Replaced garbage character {} with # character".format(ord(b))
                print(errorString)
                errorLogFile.write(errorString + "\r\f")
                b = b'\x23'
                f.seek(-1, 1)
                f.write(b)



###############################################################################
# clean_all_input_errors
#  This function scans indiviual rows looking for input errors
def clean_all_input_errors(inputDataFrame, errorLogFile):
    errorCount = 0
    print(time.strftime("%X") + " Checking for errors in the data....")

    # first use Ria's technique to remove bogus lines from the data frame
    print("  " + time.strftime("%X") + " Cleaning out garbage rows")
    cleanDataFrame = inputDataFrame[np.isfinite(inputDataFrame['Registrant_ID'])]

    #next check for non-numeric data in the age field
    print("  " + time.strftime("%X") + " Checking the age field")
    for index, row in cleanDataFrame.iterrows():
        try:
            age=int(row['Age'])
            if (age < 4):
                errorCount += 1
                errorString = "Error: The row: " + str(row["Registrant_ID"]) + " " + str(row["First_Name"]) + " " + str(
                    row["Last_Name"]) + " has an age field of "+str(age)+" which is less than the age in our youngest division"
                errorLogFile.write(errorString + "\r\f")
                print(errorString)

        except ValueError:
            errorCount+=1
            errorString="Error: The row: "+str(row["Registrant_ID"])+" "+str(row["First_Name"])+" "+str(row["Last_Name"])+ " has something other than a number in Age field"
            errorLogFile.write(errorString+"\r\f")
            print(errorString)


    #Test Rank - looking for 'Please Select'
    print("  " + time.strftime("%X") + " Looking for invalid Rank data")
    mask_NoBelt=(cleanDataFrame['Rank']=='Please Select')
    #df_NoBelt=cleanDataFrame[['Registrant_ID','First_Name','Last_Name','Dojo','Email','Phone','Mobile Phone']][mask_NoBelt]
    df_NoBelt=cleanDataFrame[['Registrant_ID','First_Name','Last_Name','Dojo']][mask_NoBelt]
    beltErrorCount = df_NoBelt.shape[0]
    if beltErrorCount > 0:
      errorCount+=beltErrorCount
      errorLogFile.write( "The Following People did not select a valid rank:\r\n" )
      print("The Following People did not select a valid rank:")
      for index, row in df_NoBelt.iterrows():
            errorString="Error: The row: "+str(row["Registrant_ID"])+" "+str(row["First_Name"])+" "+str(row["Last_Name"])+ " has something other than a number in Age field"
            errorLogFile.write(errorString+"\r\f")
            print(errorString)


#        errorLogFile.write( "Error: The row: "+str(row["Registrant_ID"])+" "+str(row["First_Name"])+" "+str(row["Last_Name"]) + " did not contain a valid rank " )

    print("  " + time.strftime("%X") + " Looking for invalid weight")
    #Convert weight to digits with regex and generate an error if not valid
    import re
    compiledRegex=re.compile('\d+')
    for index, row in cleanDataFrame.iterrows():
        rawWeightString=row['Weight']
        if pd.isnull(rawWeightString):
            errorCount += 1
            errorString = "Error: The row: " + str(row["Registrant_ID"]) + " " + str(row["First_Name"]) + " " + str(
                row["Last_Name"]) + " has an empty Weight field"
            errorLogFile.write(errorString + "\r\f")
            print(errorString)
        else:
            matchList=compiledRegex.match(rawWeightString)
            if matchList is None:
                cleanWeightString='0'
            else:
                cleanWeightString=matchList.group()
    #        cleanDataFrame.loc[index,'Competitor\'s Weight (in lbs.)?']=cleanWeightString #try .at instead http://pandas.pydata.org/pandas-docs/stable/indexing.html#fast-scalar-value-getting-and-setting
            cleanDataFrame.at[index,'Weight']=cleanWeightString #try .at instead http://pandas.pydata.org/pandas-docs/stable/indexing.html#fast-scalar-value-getting-and-setting

            #print cleanWeightString
            cleanWeight=int(cleanWeightString)
            if (0==cleanWeight) or (350 < cleanWeight):
                errorCount+=1
                errorString="Error: The row: "+str(row["Registrant_ID"])+" "+str(row["First_Name"])+" "+str(row["Last_Name"])+ " has an invalid Weight field:" + rawWeightString
                errorLogFile.write(errorString+"\r\f")
                print(errorString)


#    #Check for non-numeric data in the Weight Field
#    for index, row in cleanDataFrame.iterrows():
#        try:
#            int(row['Weight'])
#        except ValueError:
#            errorCount+=1
#            errorString="Error: The row: "+str(row["Registrant_ID"])+" "+str(row["First_Name"])+" "+str(row["Last_Name"])+ " has something other than a number in Weight field"
#            errorLogFile.write(errorString+"\r\f")
#            print errorString

#good guide to Regex in Python: https://docs.python.org/2/howto/regex.html
#import re
#wString="98 lbs"
#p=re.compile('\d+')
#s=p.match(wString)
#print s.group()

#Height
    print("  " + time.strftime("%X") + " Looking for invalid height")
#    import re
    compiledRegex=re.compile('\d+')
    for index, row in cleanDataFrame.iterrows():
        splitString=row['Height']
        if pd.isnull(splitString):
            errorCount += 1
            errorString = "Error: The row: " + str(row["Registrant_ID"]) + " " + str(row["First_Name"]) + " " + str(
                row["Last_Name"]) + " has an empty Height field"
            errorLogFile.write(errorString + "\r\f")
            print(errorString)
        else:
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
                    if int(inches)>12:
                        feet=math.floor(int(inches)/12)
                        inches=int(inches)%12
            if l==0:
                feet=0
                inches=0

            #resonability test
            if (int(feet) < 2) or (int(feet) > 7):
               #print splitString, "|", feet, "|", inches, "is not reasonable"
               errorCount+=1
               errorString="Error: The row: "+str(row["Registrant_ID"])+" "+str(row["First_Name"])+" "+str(row["Last_Name"])+ " has bad data in the height field: " + splitString
               errorLogFile.write(errorString+"\r\f")
               print(errorString)

            #Write it to new columns in the data frame
            cleanDataFrame.loc[index,'Feet']=feet
            cleanDataFrame.loc[index,'Inches']=inches
            heightInInches = (int(feet)*12)+int(inches)
            cleanDataFrame.loc[index,'HeightInInches']=heightInInches
            bodyMassIndex=(heightInInches*2)+int(cleanDataFrame.loc[index,'Weight'])
            cleanDataFrame.loc[index,'BMI']=bodyMassIndex
            #print splitString, "|", feet, "|", inches

            cleanDataFrame.at[index,'Feet']=feet
            cleanDataFrame.at[index,'Inches']=inches
            heightInInches = (int(feet)*12)+int(inches)
            cleanDataFrame.at[index,'HeightInInches']=heightInInches
            bodyMassIndex=(heightInInches*2)+int(cleanDataFrame.loc[index,'Weight'])
            cleanDataFrame.at[index,'BMI']=bodyMassIndex
            #print splitString, "|", feet, "|", inches

# Rank - this is the field that has caused us the most problem in the 2017 tournaments
    print("  " + time.strftime("%X") + " Looking for invalid Ranks")
    valid_ranks=['Black 1st Degree','Black 2nd Degree','Black 3rd Degree',
                 'Black 4th Degree','Black 5th Degree',
                 'Black Junior',
                 'Brown 3rd Degree','Brown 2nd Degree','Brown 1st Degree',
                 'Green','Green w/Stripe',
                 'Blue', 'Blue w/Stripe',
                 'Purple',
                 'Orange',
                 'Yellow',
                 'White']
    print("Valid Ranks at this time are:")
    for index in valid_ranks[:]:
        print(" " + index)


    for index, row in cleanDataFrame.iterrows():
        rank = row["Rank"]
        if pd.isnull(rank):
            errorCount += 1
            errorString = "Error: The row: " + str(row["Registrant_ID"]) + " " + str(row["First_Name"]) + " " + str(
                row["Last_Name"]) + " has an empty Current Belt Rank field"
            errorLogFile.write(errorString + "\r\f")
            print(errorString)
        if rank not in valid_ranks:
            errorCount += 1
            errorString = "Error: The row: " + str(row["Registrant_ID"]) + " " + str(row["First_Name"]) + " " + str(
                row["Last_Name"]) + " has an invalid  Belt Rank field: "+rank
            errorLogFile.write(errorString + "\r\f")
            print(errorString)

    #Look for out of state dojos and move them into the 'Dojo' column
    print("  " + time.strftime("%X") + " Looking for out of state dojos")
    for index, row in cleanDataFrame.iterrows():
        theString=row['Dojo']
        if( theString=="Out of State" ):
            outofstateString=row['Out_of_State_Dojo']
            if(pd.isnull(outofstateString)):
                errorCount+=1
                errorString="Error: The row: "+str(row["Registrant_ID"])+" "+str(row["First_Name"])+" "+str(row["Last_Name"])+ " says the student is from Out of State, but there is no out of State Studio provided"
                errorLogFile.write(errorString+"\r\f")
                #print errorString
            else:
                #print outofstateString
                cleanDataFrame.at[index,'Dojo']="** "+outofstateString




   # if there are errors exit
    if( errorCount > 0):
        errorLogFile.write( str(errorCount)+" "+"errors found" )
        errorLogFile.close()
        print(str(errorCount)+" "+"errors found")
        sys.exit("Exiting - The input must be fixed manually")
    else:
         errorLogFile.write( "No errors found" )


    return cleanDataFrame
