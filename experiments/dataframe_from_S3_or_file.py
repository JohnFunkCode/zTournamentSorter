#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Experiment that shows reading a dataframe from either an AWS S3 bucket or a file

Created on Sun November 26 2017
@author: John Funk
"""

import os
import pandas as pd
from s3fs.core import S3FileSystem

#s3=S3FileSystem(anon=False,key='YourAccessKey',secret='YourSecretKey')
s3=S3FileSystem(anon=False)   #uses creds from environment
filename='CleanerTournamentParticipantsNOTTHEFINALLIST-10-15-17.csv'
bucket='jpf-python-datastore'

f=s3.open('{}/{}'.format(bucket,filename),mode='rb')
s3df=pd.read_csv(f)
print(s3df)

# or using simplified url handling - don't know how permissions work here yet
#file='S3://{}/{}'.format(bucket,filename)
#s3df=pd.read_csv(file)
#print s3df


filename = "/users/johnfunk/CloudStation/TournamentProject/CleanerTournamentParticipantsNOTTHEFINALLIST-10-15-17.csv"
f=open(filename,mode='rb')
fsdf=pd.read_csv(f)
print(fsdf)

# or using simplified url handling
#file='file://{}'.format(filename)
#fsdf=pd.read_csv(file)
#print fsdf
