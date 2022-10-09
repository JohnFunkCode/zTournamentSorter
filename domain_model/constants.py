#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sunday May 1, 2022

@author: john funk

query_paramater_constants.py
Contains the constants needed for consistant querying data frames
"""

#Belts
WHITE_BELT='White'
YELLOW_BELT='Yellow'
ORANGE_BELT='Orange'
PURPLE_BELT='Purple'
BLUE_BELT='Blue'
BLUE_STRIPE_BELT='Blue w/Stripe'
GREEN_BELT='Green'
GREEN_STRIPE_BELT='Green w/Stripe'
THIRD_DEGREE_BROWN_BELT='Brown 3rd Degree'
SECOND_DEGREE_BROWN_BELT='Brown 2nd Degree'
FIRST_DEGREE_BROWN_BELT='Brown 1st Degree'
FIRST_DEGREE_BLACK_BELT='Black 1st Degree'
SECOND_DEGREE_BLACK_BELT='Black 2nd Degree'
THIRD_DEGREE_BLACK_BELT='Black 3rd Degree'
FOURTH_DEGREE_BLACK_BELT='Black 4th Degree'
FIFTH_DEGREE_BLACK_BELT='Black 5th Degree'
JUNIOR_BLACK_BELT='Black Junior'

#Alphabetic Splits
FIRST_ALPHABETIC_SPLIT_REGEX=r'^[a-lA-L]'  # means letters in the set a-l
FIRST_ALPHABETIC_SPLIT_LABEL='A - L'
SECOND_ALPHABETIC_SPLIT_REGEX=r'^[m-zM-Z]'  # means letters in the set m-z
SECOND_ALPHABETIC_SPLIT_LABEL='M - Z'

#Sleep time after writing a file
SLEEP_TIME=.0001

#Number of competitors in a division to raise an alert
TOO_MANY_COMPETITORS = 20