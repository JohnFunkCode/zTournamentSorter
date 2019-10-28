#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Sept 10 13:11:00 2017

Experiment to rename columns in a dataframe

@author: John Funk
"""

import os
import pandas as pd
from tkinter import Tk
from tkinter.filedialog import askopenfilename

class RenameColumns:
    #def __new__(cls):
    #    return super(RenameColumns, cls).__new__(cls)

    def __init__(self, filename):
        #super(RenameColumns, self).__init__()
        self.raw_df = pd.read_csv(filename)

    def get_dataframe_copy(self):
        return self.raw_df

    def dump_raw_df(self):
        print((self.raw_df))

    def print_column_names(self):
        headers = list(self.raw_df.columns)
        for header in headers:
            print(header)

    def is_YourSudio_a_column_name(self):
        import re
        searchstring = ".*State.*Studio.*"

        compiled_regx=re.compile(searchstring)

        headers = list(self.raw_df.columns)

        #m=[x for x in headers if compiled_regx.match(x)]

        newlist = list(filter(compiled_regx.match,headers))
        print(newlist[0])
        print(len(newlist))

    def get_column_name_containing(self,reg_ex_seach_string):
        import re
        compiled_regx=re.compile(reg_ex_seach_string)

        headers = list(self.raw_df.columns)
        newlist = list(filter(compiled_regx.match,headers))
        if(len(newlist)==1):
            return newlist[0]
        else:
            return None

    def replace_column_name_containing(self,reg_ex_seach_string, new_column_name,verbose=False):
        old_column_name=self.get_column_name_containing(reg_ex_seach_string)
        if(old_column_name is not None):
            if(verbose):
                print("Replacing "+old_column_name+" with "+ new_column_name)
            self.raw_df.rename( columns={old_column_name:new_column_name},inplace=True)
        else:
            print("Column not found: {}".format(reg_ex_seach_string))

    def rename_all_columns(self):
        self.replace_column_name_containing(".*Event.*Date.*", "Event_Date")
        self.replace_column_name_containing(".*Registrant.*", "Registrant_ID")
        self.replace_column_name_containing(".*First.*Name.*", "First_Name")
        self.replace_column_name_containing(".*Last.*Name.*", "Last_Name")
        self.replace_column_name_containing(".*Competitor.*Age.*", "Age")
        self.replace_column_name_containing('.*Select.*Your.*Studio.*', 'Dojo')
        self.replace_column_name_containing('.*Out.*State.*Studio.*', 'Out_of_State_Dojo')
        self.replace_column_name_containing(".*Competitor.*Weight.*", "Weight")
        self.replace_column_name_containing(".*Competitor.*Height.*", "Height")
        self.replace_column_name_containing(".*Rank.*", "Rank")
        self.replace_column_name_containing(".*Division.*Based.*Age.*", "Division")
        self.replace_column_name_containing(".*Forms.*Sparring.*", "Events")
        self.replace_column_name_containing(".*Weapons.*", "Weapons")
        self.replace_column_name_containing(".*Spectator.*Tickets.*", "Spectator_Tickets")
        return

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
        print("Using the file " + filename + "from the environment")

    r=RenameColumns(filename)
    #r.dump_raw_df()
    r.print_column_names()
    print("-----")
    #r.is_YourSudio_a_column_name()
    print("r.get_column_name_containing('.*Competitor.*Age.*')")
    print(r.get_column_name_containing(".*Competitor.*Age.*"))
    print("-----")

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


    print("-----")
    r.print_column_names()

    newdf = r.get_dataframe_copy()
    print(newdf)


# newdf.rename(
#     columns={'Select Your Z Ultimate Studio': 'Dojo', 'Competitor\'s Age?': 'Age', 'Current Belt Rank?': 'Rank',
#              'Competitor\'s Height (e.g. 4 ft. 2 in. )?': 'Height',
#              'Competitor\'s Weight (eg. 73lbs.)?': 'Weight', 'Choose Forms, Sparring or Both.': 'Events',
#              'Choose Weapons.': 'Weapons'}, inplace=True)
