#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Sept 10 13:11:00 2017

Experiment to rename columns in a dataframe

@author: John Funk
"""

import os
import logging
import sys

import pandas as pd
from tkinter import Tk
from tkinter.filedialog import askopenfilename

class RenameColumns:
    #def __new__(cls):
    #    return super(RenameColumns, cls).__new__(cls)

    def __init__(self, filename):
        #super(RenameColumns, self).__init__()
        self.raw_df = pd.read_csv(filename, keep_default_na=False)

    def get_dataframe_copy(self):
        return self.raw_df

    def dump_raw_df(self):
        logging.info((self.raw_df))

    def print_column_names(self):
        headers = list(self.raw_df.columns)
        for header in headers:
            logging.info(header)

    def is_YourSudio_a_column_name(self):
        import re
        searchstring = ".*State.*Studio.*"

        compiled_regx=re.compile(searchstring)

        headers = list(self.raw_df.columns)

        #m=[x for x in headers if compiled_regx.match(x)]

        newlist = list(filter(compiled_regx.match,headers))
        logging.info(newlist[0])
        logging.info(len(newlist))

    def get_column_name_containing(self,reg_ex_seach_string):
        import re
        compiled_regx=re.compile(reg_ex_seach_string)

        headers = list(self.raw_df.columns)
        newlist = list(filter(compiled_regx.match,headers))
        if(len(newlist)>0):   #Note if multiple column names match the regex, only the first is selected.   Be careful this could cause a problem.
            return newlist[0]
        else:
            return None

    def replace_column_name_containing(self,reg_ex_seach_string, new_column_name,verbose=False):
        old_column_name=self.get_column_name_containing(reg_ex_seach_string)
        if(old_column_name is not None):
            if(verbose):
                logging.info("Replacing "+old_column_name+" with "+ new_column_name)
            self.raw_df.rename( columns={old_column_name:new_column_name},inplace=True)
        else:
            logging.info("Column not found: {}".format(reg_ex_seach_string))

    def rename_all_columns(self):
        logging.info("The Column Headers must contain the following:")
        logging.info("  Event Date")
        logging.info("  Registrant ID")
        logging.info("  First Name")
        logging.info("  Last Name")
        logging.info("  Gender")
        logging.info("  Select Your Studio")
        logging.info("  Out of State Studio")
        logging.info("  Age")
        logging.info("  Weight")
        logging.info("  Height")
        logging.info("  Division")
        logging.info("  Rank")
        logging.info("  Forms or Sparring")
        logging.info("  Techniques")
        logging.info("  Weapons")
        logging.info("  Tickets")

        self.replace_column_name_containing(".*Event.*Date.*", "Event_Date")
        self.replace_column_name_containing(".*Registrant.*", "Registrant_ID")
#        self.replace_column_name_containing(".*First.*Name.*", "First_Name")
        self.replace_column_name_containing(".*First.*", "First_Name")
#        self.replace_column_name_containing(".*Last.*Name.*", "Last_Name")
        self.replace_column_name_containing(".*Last.*", "Last_Name")
#        self.replace_column_name_containing(".*Competitor.*Age.*", "Age")
        self.replace_column_name_containing(".*Age.*", "Age")
        self.replace_column_name_containing('.*Select.*Your.*Studio.*', 'Dojo')
        self.replace_column_name_containing('.*Out.*State.*Studio.*', 'Out_of_State_Dojo')
#        self.replace_column_name_containing(".*Competitor.*Weight.*", "Weight")
        self.replace_column_name_containing(".*Weight.*", "Weight")
#        self.replace_column_name_containing(".*Competitor.*Height.*", "Height")
        self.replace_column_name_containing(".*Height.*", "Height")
        self.replace_column_name_containing(".*Rank.*", "Rank")
#        self.replace_column_name_containing(".*Division.*Based.*Age.*", "Division")
        self.replace_column_name_containing(".*Division.*", "Division")

        # October 2024 - we replaced events and techniques columns with a single column called Events
        # self.replace_column_name_containing(".*Forms.*Sparring.*", "Events")
        # self.replace_column_name_containing(".*Technique.*", "Techniques")
        self.replace_column_name_containing(".*category.*", "Events")

        self.replace_column_name_containing(".*Weapons.*", "Weapons")
#        self.replace_column_name_containing(".*Spectator.*Tickets.*", "Spectator_Tickets")
        self.replace_column_name_containing(".*Tickets.*", "Spectator_Tickets")

        self.re_order_columns()
        return
#good guide to Regex in Python: https://docs.python.org/2/howto/regex.html

    def re_order_columns(self):
        self.re_ordered_df=self.raw_df[['Registrant_ID','First_Name','Last_Name','Gender','Age','Weight','Height','Rank','Division','Dojo','Out_of_State_Dojo','Events','Weapons']]
        self.raw_df=self.re_ordered_df

if __name__ == '__main__':
    #get the filename from the environment var named  tourname_filename
    filename=os.getenv("tournament_filename")

    if filename is None :
        #Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
        root = Tk()
        root.withdraw() # we don't want a full GUI, so keep the root window from appearing
        root.update() # Prevent the askfilename() window doesn't stay open
        filename = askopenfilename()
        root.update() # Prevent the askfilename() window doesn't stay open
    else:
        logging.info("Using the file " + filename + "from the environment")

    errorLogFileName = filename[0:len(filename) - 4] + "-Error.txt"

    logger = logging.getLogger('')
    logger.setLevel(logging.INFO)
    fh = logging.FileHandler(errorLogFileName)
    sh = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s %(message)s', datefmt='%H:%M:%S')
    fh.setFormatter(formatter)
    sh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(sh)

    r=RenameColumns(filename)
    #r.dump_raw_df()
    logging.info("1-----")
    r.print_column_names()
    logging.info("2-----")
    r.rename_all_columns()
    logging.info("3-----")
    r.print_column_names()
    logging.info("4-----")
    r.re_order_columns()
    r.print_column_names()
    logging.info("5-----")

    #r.is_YourSudio_a_column_name()
    logging.info("r.get_column_name_containing('.*Age.*')")
    logging.info(r.get_column_name_containing(".*Age.*"))
    logging.info("6-----")

    r.rename_all_columns()

    # r.replace_column_name_containing(".*Event.*Date.*","Event_Date")
    # r.replace_column_name_containing(".*Registrant.*","Registrant_ID")
    # r.replace_column_name_containing(".*First.*Name.*","First_Name")
    # r.replace_column_name_containing(".*Last.*Name.*","Last_Name")
    # r.replace_column_name_containing(".*Competitor.*Age.*","Age")
    # r.replace_column_name_containing('.*Select.*Your.*Studio.*','Dojo')
    # r.replace_column_name_containing('.*Out.*State.*Studio.*','Out_of_State_Studio')
    # r.replace_column_name_containing(".*Competitor.*Weight.*","Weight")
    # r.replace_column_name_containing(".*Competitor.*Height.*","Height")
    # r.replace_column_name_containing(".*Rank.*","Rank")
    # r.replace_column_name_containing(".*Division.*Based.*Age.*","Division")
    # r.replace_column_name_containing(".*Forms.*Sparring.*", "Events")
    # r.replace_column_name_containing(".*Weapons.*", "Weapons")
    # r.replace_column_name_containing(".*Spectator.*Tickets.*","Spectator_Tickets")


    logging.info("-----")
    r.print_column_names()

    newdf = r.get_dataframe_copy()
    logging.info(newdf)


# newdf.rename(
#     columns={'Select Your Z Ultimate Studio': 'Dojo', 'Competitor\'s Age?': 'Age', 'Current Belt Rank?': 'Rank',
#              'Competitor\'s Height (e.g. 4 ft. 2 in. )?': 'Height',
#              'Competitor\'s Weight (eg. 73lbs.)?': 'Weight', 'Choose Forms, Sparring or Both.': 'Events',
#              'Choose Weapons.': 'Weapons'}, inplace=True)
