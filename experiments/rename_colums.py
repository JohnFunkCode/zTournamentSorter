#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Sept 10 13:11:00 2017

Experiment to rename columns in a dataframe

@author: John Funk
"""

import os
import sys
import pandas as pd
import time
from Tkinter import Tk
from tkFileDialog import askopenfilename

class RenameColumns:
    def __new__(cls):
        return super(RenameColumns, cls).__new__(cls)

    def __init__(self, filename):
        #super(RenameColumns, self).__init__()
        self.raw_df = pd.read_csv(filename)

    def dump_raw_df(self):
        print(self.raw_df)

    def print_column_names(self):
        headers = list(self.raw_df.columns)
        for header in headers:
            print header

    def is_YourSudio_a_column_name(self):
        import re
        searchstring=".*State.*Studio.*"

        compiled_regx=re.compile(searchstring)

        headers = list(self.raw_df.columns)

        #m=[x for x in headers if compiled_regx.match(x)]

        newlist = filter(compiled_regx.match,headers)
        print newlist[0]
        print len(newlist)

    def get_column_name_containing(self,reg_ex_seach_string):
        import re
        compiled_regx=re.compile(reg_ex_seach_string)

        headers = list(self.raw_df.columns)
        newlist = filter(compiled_regx.match,headers)
        if(len(newlist)==1):
            return newlist[0]
        else:
            return None

    def replace_column_name_containing(self,reg_ex_seach_string, new_column_name,verbose=False):
        old_column_name=r.get_column_name_containing(reg_ex_seach_string)
        if(old_column_name != None):
            if(verbose):
                print "Replacing "+old_column_name+" with "+ new_column_name
            self.raw_df.rename( columns={old_column_name:new_column_name},inplace=True)
        else:
            print "Column not found"

    def test(self,string1,string2):
        print string1
        print string2

if __name__ == '__main__':
    #get the filename from the environment var named  tourname_filename
    filename=os.getenv("tournament_filename")

    if filename is None :
        from Tkinter import Tk

        #Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
        root = Tk()
        root.withdraw() # we don't want a full GUI, so keep the root window from appearing
        root.update() # Prevent the askfilename() window doesn't stay open
        filename = askopenfilename()
        root.update() # Prevent the askfilename() window doesn't stay open
    else:
        print "Using the file " + filename + "from the environment"

    r=RenameColumns(filename)
    #r.dump_raw_df()
    r.print_column_names()
    print "-----"
    #r.is_YourSudio_a_column_name()
    print "r.get_column_name_containing('.*Competitor.*Age.*')"
    print r.get_column_name_containing(".*Competitor.*Age.*")
    print "-----"

    r.replace_column_name_containing(".*Competitor.*Age.*","Age")
    r.replace_column_name_containing('.*Select.*Your.*Studio.*','Dojo')
    r.replace_column_name_containing(".*Competitor.*Weight.*","Weight")
    r.replace_column_name_containing(".*Competitor.*Height.*","Height")
    r.replace_column_name_containing(".*Rank.*","Rank")
    r.replace_column_name_containing(".*Division.*Based.*Age.*","Division")
    r.replace_column_name_containing(".*Forms.*Sparring.*", "Events")
    r.replace_column_name_containing(".*Forms.*Sparring.*", "Events")
    r.replace_column_name_containing(".*Weapons.*", "Weapons")
    r.replace_column_name_containing(".*Spectator.*Tickets.*","Spectator Tickets")


    print "-----"
    r.print_column_names()



# newdf.rename(
#     columns={'Select Your Z Ultimate Studio': 'Dojo', 'Competitor\'s Age?': 'Age', 'Current Belt Rank?': 'Rank',
#              'Competitor\'s Height (e.g. 4 ft. 2 in. )?': 'Height',
#              'Competitor\'s Weight (eg. 73lbs.)?': 'Weight', 'Choose Forms, Sparring or Both.': 'Events',
#              'Choose Weapons.': 'Weapons'}, inplace=True)

