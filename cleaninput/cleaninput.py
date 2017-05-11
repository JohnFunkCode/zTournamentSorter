import sys
import time

import numpy as np
import pandas as pd

#from LoadTournamentTable import df

###############################################################################
# clean_all_input_errors
#  This function scans indiviual rows looking for input errors
def clean_all_input_errors(inputDataFrame, errorLogFile):
    errorCount = 0
    print time.strftime("%X") + " Checking for errors in the data...."

    # first use Ria's technique to remove bogus lines from the data frame
    print "  " + time.strftime("%X") + " Cleaning out garbage rows"
    cleanDataFrame = inputDataFrame[np.isfinite(inputDataFrame['Registrant ID'])]

    #next check for non-numeric data in the age field
    print "  " + time.strftime("%X") + " Checking for non-numeric data in numeric fields"
    for index, row in cleanDataFrame.iterrows():
        try:
            int(row['Competitor\'s Age?'])
        except ValueError:
            errorCount+=1
            errorString="Error: The row: "+str(row["Registrant ID"])+" "+str(row["First Name"])+" "+str(row["Last Name"])+ " has something other than a number in Age field"
            errorLogFile.write(errorString+"\r\f")
            print errorString

    #Test Rank - looking for 'Please Select'
    print "  " + time.strftime("%X") + " Looking for invalid Rank data"
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

    print "  " + time.strftime("%X") + " Looking for invalid weight"
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

#Height
    print "  " + time.strftime("%X") + " Looking for invalid height"
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

    #Look for out of state dojos and move them into the 'Select Your Z Ultimate Studio' column
    print "  " + time.strftime("%X") + " Looking for out of state dojos"
    for index, row in cleanDataFrame.iterrows():
        theString=row['Select Your Z Ultimate Studio']
        if( theString=="Out of State" ):
            outofstateString=row['Out of State Studio Name']
            if(pd.isnull(outofstateString)):
                errorCount+=1
                errorString="Error: The row: "+str(row["Registrant ID"])+" "+str(row["First Name"])+" "+str(row["Last Name"])+ " says the student is from Out of State, but there is no out of State Studio provided"
                errorLogFile.write(errorString+"\r\f")
                #print errorString
            else:
                #print outofstateString
                cleanDataFrame.at[index,'Select Your Z Ultimate Studio']="** "+outofstateString




   # if there are errors exit
    if( errorCount > 0):
        errorLogFile.write( str(errorCount)+" "+"errors found" )
        errorLogFile.close()
        print str(errorCount)+" "+"errors found"
        sys.exit("Exiting - The input must be fixed manually")
    else:
         errorLogFile.write( "No errors found" )


    return cleanDataFrame