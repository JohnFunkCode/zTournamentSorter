#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Sept 10 13:11:00 2017

@author: John Funk
"""

import pandas as pd
import numpy as np
import os

class RenameColumns:
    def __new__(cls):
        return super(RenameColumns, cls).__new__(cls)

    def __init__(self, filename):
        #super(RenameColumns, self).__init__()
        self.raw_df = pd.read_csv(filename)

    def dump_raw_df(self):
        print(self.raw_df)

    def print_index(self):
        self.l = list(self.raw_df.index)
        print self.l

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
        print "Using the file " + filename + "from the environment"

    r=RenameColumns(filename)
    #r.dump_raw_df()
    r.print_index()