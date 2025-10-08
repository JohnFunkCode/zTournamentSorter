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
        searchstring = ".*State.*Dojo.*"

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
        # logging.info("  Event Date")  # No longer requiring event date column
        logging.info("  Registrant_ID")
        logging.info("  First_Name")
        logging.info("  Last_Name")
        logging.info("  Gender")
        logging.info("  Dojo")
        logging.info("  Out_of_State_Dojo")
        logging.info("  Age")
        logging.info("  Weight")
        logging.info("  Height")
        logging.info("  Division")
        logging.info("  Rank")
        logging.info("  Events")
        logging.info("  Weapons")
        logging.info("  Spectator_Tickets")

        # self.replace_column_name_containing(".*Event.*Date.*", "Event_Date") # no longer requiring event date column
        self.replace_column_name_containing(".*Registrant.*", "Registrant_ID")
        self.replace_column_name_containing(".*First.*", "First_Name")
        self.replace_column_name_containing(".*Last.*", "Last_Name")
        self.replace_column_name_containing(".*Age.*", "Age")
        # self.replace_column_name_containing('.*Select.*Your.*Dojo.*', 'Dojo')  #Note we're not fixing the Dojo column because of 'Out_of_State_Dojo'
        self.replace_column_name_containing('Dojo', 'Dojo')
        self.replace_column_name_containing('.*Out.*State.*Dojo.*', 'Out_of_State_Dojo')
        self.replace_column_name_containing(".*Weight.*", "Weight")
        self.replace_column_name_containing(".*Height.*", "Height")
        self.replace_column_name_containing(".*Rank.*", "Rank")
        self.replace_column_name_containing(".*Division.*", "Division")
        self.replace_column_name_containing(".*Events.*", "Events")
        self.replace_column_name_containing(".*Weapons.*", "Weapons")
        self.replace_column_name_containing(".*Tickets.*", "Spectator_Tickets")

        self.re_order_columns()
        return
#good guide to Regex in Python: https://docs.python.org/2/howto/regex.html

    def re_order_columns(self):
        self.re_ordered_df=self.raw_df[['Registrant_ID','First_Name','Last_Name','Gender','Age','Weight','Height','Rank','Division','Dojo','Out_of_State_Dojo','Events','Weapons','Spectator_Tickets']]
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

    logging.info("-----")
    r.print_column_names()

    newdf = r.get_dataframe_copy()
    logging.info(newdf)


