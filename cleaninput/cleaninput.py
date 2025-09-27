import os
import time
import math
import logging

import numpy as np
import pandas as pd
import domain_model.constants as constants
from cleaninput import input_errors


#from LoadTournamentTable import df

###############################################################################
#### SET Encoding to UTF-8 added 3/27/2022
def set_utf_encoding():
    if os.name == "nt":
        import _locale
        _locale._gdl_bak = _locale._getdefaultlocale
        _locale._getdefaultlocale = (lambda *args: (_locale._gdl_bak()[0], 'utf8'))

###############################################################################
# clean_unicode_from_file
#  This function removes unicode characters from the input file and writes a warning to the error file
def clean_unicode_from_file(inputFileName):
    import io
    with io.open(inputFileName, 'r+b') as f:
        while True:
            b = f.read(1)
            if not b:
                break
            if (b > b'\x7f'):
                errorString="Replaced garbage character {} with # character".format(ord(b))
                logging.warning(errorString)
                b = b'\x23'
                f.seek(-1, 1)
                f.write(b)



###############################################################################
# clean_all_input_errors
#  This function scans indiviual rows looking for input errors
def clean_all_input_errors(inputDataFrame: str, input_error_list: input_errors.InputErrors):
    errorCount = 0

    logging.info("Checking for errors in the data....")

    # First let's establish a Registrant_ID column in the input dataframe
    number_of_rows = inputDataFrame.shape[0]
    column_list = inputDataFrame.columns.values.tolist()
    if ('Registrant_ID' not in column_list):
        errorString = "Registrant_ID column doesn't exist, creating an empty one"
        logging.warning(errorString)
    else:
        inputDataFrame.drop(columns="Registrant_ID",inplace=True)
    inputDataFrame.insert(0, "Registrant_ID", list(range(0, number_of_rows)))

    # Drop any un-named columns
    for column_name in column_list:
        if('Unnamed' in column_name):
            inputDataFrame.drop(columns=column_name,inplace=True)

    # first use Ria's technique to remove bogus lines from the data frame
    logging.info("   Cleaning out garbage rows")
    #logging.info(np.isfinite(inputDataFrame['Registrant_ID']))
    cleanDataFrame = inputDataFrame[np.isfinite(inputDataFrame['Registrant_ID'])]

    #next check for non-numeric data in the age field
    logging.info("   Checking the age field")
    for index, row in cleanDataFrame.iterrows():
        try:
            age=int(row['Age'])
            if (age < 3):
                errorCount += 1
                errorString = "Error: The row: " + str(row["Registrant_ID"]) + " " + str(row["First_Name"]) + " " + str(
                    row["Last_Name"]) + " has an age field of "+str(age)+" which is less than the age in our youngest division"
                logging.info(errorString)
                input_error_list.append(index, 'Age')

        except ValueError:
            errorCount+=1
            errorString="Error: The row: "+str(row["Registrant_ID"])+" "+str(row["First_Name"])+" "+str(row["Last_Name"])+ " has something other than a number in Age field"
            logging.info(errorString)
            input_error_list.append(index, 'Age')

    #Weight
    logging.info("   Looking for invalid weight")
    #Convert weight to digits with regex and generate an error if not valid
    import re
    compiledRegex=re.compile(r'\d+')
    for index, row in cleanDataFrame.iterrows():
        rawWeightString=str(row['Weight'])
        if pd.isnull(rawWeightString):
            errorCount += 1
            errorString = "Error: The row: " + str(row["Registrant_ID"]) + " " + str(row["First_Name"]) + " " + str(
                row["Last_Name"]) + " has an empty Weight field"
            logging.info(errorString)
            input_error_list.append(index, 'Weight')
        else:
            matchList=compiledRegex.match(rawWeightString)
            if matchList is None:
                cleanWeightString='0'
            else:
                cleanWeightString=matchList.group()
    #        cleanDataFrame.loc[index,'Competitor\'s Weight (in lbs.)?']=cleanWeightString #try .at instead http://pandas.pydata.org/pandas-docs/stable/indexing.html#fast-scalar-value-getting-and-setting
            cleanDataFrame.at[index,'Weight']=int(cleanWeightString) #cast it as an int to match the type stored in the dataframe

            #print cleanWeightString
            cleanWeight=int(cleanWeightString)
            if (0==cleanWeight) or (350 < cleanWeight):
                errorCount+=1
                errorString="Error: The row: "+str(row["Registrant_ID"])+" "+str(row["First_Name"])+" "+str(row["Last_Name"])+ " has an invalid Weight field:" + rawWeightString
                logging.info(errorString)
                input_error_list.append(index, 'Weight')

    #Height
    logging.info("   Looking for invalid height")
#    import re
    compiledRegex=re.compile('\d+')
    for index, row in cleanDataFrame.iterrows():
        splitString=row['Height']
        if pd.isnull(splitString):
            errorCount += 1
            errorString = "Error: The row: " + str(row["Registrant_ID"]) + " " + str(row["First_Name"]) + " " + str(
                row["Last_Name"]) + " has an empty Height field"
            logging.info(errorString)
            input_error_list.append(index, 'Height')
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
               logging.info(errorString)
               input_error_list.append(index, 'Height')

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

    #Look for out of state dojos and move them into the 'Dojo' column
    logging.info("   Looking for out of state studios")

    # First let's establish if the Out_of_State_Dojo column in the input dataframe if there isn't show a warning,
    # then just create one so all the rest of the logic works.
    column_list = cleanDataFrame.columns.values.tolist()
    if ('Out_of_State_Dojo' not in column_list):
        errorString = "Out_of_State_Dojo column doesn't exist in the input file, out of state dojos won't be processed"
        logging.warning(errorString)
        cleanDataFrame.insert(0,'Out_of_State_Dojo','')

    for index, row in cleanDataFrame.iterrows():
        theString=row['Dojo']
        if( theString=="Out of State" ):
            outofstateString=row['Out_of_State_Dojo']
            if(pd.isnull(outofstateString)):
                errorCount+=1
                errorString="Error: The row: "+str(row["Registrant_ID"])+" "+str(row["First_Name"])+" "+str(row["Last_Name"])+ " says the student is from Out of State, but there is no out of State Dojo provided"
                #print errorString
                input_error_list.append(index, 'Height')
            else:
                #print outofstateString
                cleanDataFrame.at[index,'Dojo']="** "+outofstateString

    # # Test Rank - looking for 'Please Select'
    # logging.info("   Looking for unselected Rank")
    # mask_NoBelt = (cleanDataFrame['Rank'] == 'Please Select')
    # # df_NoBelt=cleanDataFrame[['Registrant_ID','First_Name','Last_Name','Dojo','Email','Phone','Mobile Phone']][mask_NoBelt]
    # df_NoBelt = cleanDataFrame[['Registrant_ID', 'First_Name', 'Last_Name', 'Dojo']][mask_NoBelt]
    # beltErrorCount = df_NoBelt.shape[0]
    # if beltErrorCount > 0:
    #     errorCount += beltErrorCount
    #     logging.info("The Following People did not select a valid rank:")
    #     for index, row in df_NoBelt.iterrows():
    #         errorString = "Error: The row: " + str(row["Registrant_ID"]) + " " + str(row["First_Name"]) + " " + str(
    #             row["Last_Name"]) + " did not select a rank."
    #         logging.info(errorString)


    # Rank - this is the field that has caused us the most problem in the 2017 tournaments
    logging.info("   Looking for invalid Ranks")
    # valid_ranks=['Black 1st Degree','Black 2nd Degree','Black 3rd Degree',
    #              'Black 4th Degree','Black 5th Degree',
    #              'Black Junior',
    #              'Brown 3rd Degree','Brown 2nd Degree','Brown 1st Degree',
    #              'Green','Green w/Stripe',
    #              'Blue', 'Blue w/Stripe',
    #              'Purple',
    #              'Orange',
    #              'Yellow',
    #              'White']
    valid_ranks=[constants.FIRST_DEGREE_BLACK_BELT,constants.SECOND_DEGREE_BLACK_BELT,constants.THIRD_DEGREE_BLACK_BELT,
                 constants.FOURTH_DEGREE_BLACK_BELT,constants.FIFTH_DEGREE_BLACK_BELT,
                 constants.JUNIOR_BLACK_BELT,
                 constants.THIRD_DEGREE_BROWN_BELT,constants.SECOND_DEGREE_BROWN_BELT,constants.FIRST_DEGREE_BROWN_BELT,
                 constants.GREEN_BELT,constants.GREEN_STRIPE_BELT,
                 constants.BLUE_BELT,constants.BLUE_STRIPE_BELT,
                 constants.PURPLE_BELT,
                 constants.ORANGE_BELT,
                 constants.YELLOW_BELT,
                 constants.WHITE_BELT]
    logging.info("Valid Ranks at this time are:")
    for index in valid_ranks[:]:
        logging.info("  " + index)

    for index, row in cleanDataFrame.iterrows():
        rank = row["Rank"]
        if pd.isnull(rank):
            errorCount += 1
            errorString = "Error: The row: " + str(row["Registrant_ID"]) + " " + str(row["First_Name"]) + " " + str(
                row["Last_Name"]) + " has an empty Current Belt Rank field"
            logging.info(errorString)
            input_error_list.append(index, 'Rank')
        if rank not in valid_ranks:
            errorCount += 1
            errorString = "Error: The row: " + str(row["Registrant_ID"]) + " " + str(row["First_Name"]) + " " + str(
                row["Last_Name"]) + " has an invalid  Belt Rank field: "+str(rank)
            logging.info(errorString)
            input_error_list.append(index, 'Rank')

    # if there are errors exit
    if( errorCount > 0):
        logging.info(str(errorCount)+" "+"errors found")
        # sys.exit("Exiting - The input must be fixed manually")
    else:
         logging.info( "No errors found" )


    return cleanDataFrame,errorCount
