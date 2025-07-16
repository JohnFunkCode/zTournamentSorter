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

#BELT Translations
BELT_EXPANSION_TABLE = {
    'White': WHITE_BELT,
    'Yellow': YELLOW_BELT,
    'Orange': ORANGE_BELT,
    'Purple': PURPLE_BELT,
    'Blue': BLUE_BELT,
    'Blue w/Stripe': BLUE_STRIPE_BELT,
    'Green': GREEN_BELT,
    'Green w/Stripe': GREEN_STRIPE_BELT,
    'Brown': [THIRD_DEGREE_BROWN_BELT, SECOND_DEGREE_BROWN_BELT,FIRST_DEGREE_BROWN_BELT],
    'Black': [FIRST_DEGREE_BLACK_BELT, SECOND_DEGREE_BLACK_BELT, THIRD_DEGREE_BLACK_BELT, FOURTH_DEGREE_BLACK_BELT,FIFTH_DEGREE_BLACK_BELT, JUNIOR_BLACK_BELT],
    # special case
    'Jr. Black' : [JUNIOR_BLACK_BELT, FIRST_DEGREE_BLACK_BELT],  # special case to help parents who register their Jr. Black Belts in Black Belt divisions
    'Jr. Black & Black': [JUNIOR_BLACK_BELT, FIRST_DEGREE_BLACK_BELT, SECOND_DEGREE_BLACK_BELT, THIRD_DEGREE_BLACK_BELT, FOURTH_DEGREE_BLACK_BELT,FIFTH_DEGREE_BLACK_BELT],  # special case for young adult divisions
    # special case for weapons divisions
    'White - Jr. Black': [WHITE_BELT, YELLOW_BELT, ORANGE_BELT, PURPLE_BELT, BLUE_BELT, BLUE_STRIPE_BELT, GREEN_BELT, GREEN_STRIPE_BELT, THIRD_DEGREE_BROWN_BELT, SECOND_DEGREE_BROWN_BELT,FIRST_DEGREE_BROWN_BELT, JUNIOR_BLACK_BELT, FIRST_DEGREE_BLACK_BELT],  # special case for weapons divisions
    'White - Blue w/Green Stripe' : [WHITE_BELT, YELLOW_BELT, ORANGE_BELT, PURPLE_BELT, BLUE_BELT, BLUE_STRIPE_BELT],  # special case for weapons divisions
    'Green - Jr. Black' : [GREEN_BELT, GREEN_STRIPE_BELT, THIRD_DEGREE_BROWN_BELT, SECOND_DEGREE_BROWN_BELT,FIRST_DEGREE_BROWN_BELT, JUNIOR_BLACK_BELT, FIRST_DEGREE_BLACK_BELT],  # special case for weapons divisions
    #special cases for old style belts
    'Blue/Stripe' : BLUE_STRIPE_BELT,  # special case for old style which used Blue/Stripe instead of Blue w/Stripe
    'Green/Stripe': GREEN_STRIPE_BELT  # special case for old style which used Green/Stripe instead of Green w/Stripe
}


#Alphabetic Splits
FIRST_ALPHABETIC_SPLIT_REGEX=r'^[a-lA-L]'  # means letters in the set a-l
FIRST_ALPHABETIC_SPLIT_LABEL='A - L'
SECOND_ALPHABETIC_SPLIT_REGEX=r'^[m-zM-Z]'  # means letters in the set m-z
SECOND_ALPHABETIC_SPLIT_LABEL='M - Z'

#Sleep time after writing a file
SLEEP_TIME=.01

#Number of competitors in a division to raise an alert
TOO_MANY_COMPETITORS = 16

#Ageless - we replace this with + (e.g. 18-100 gets expressed as 18+)
AGELESS = 100