#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Sept 10 13:11:00 2017

@author: John Funk
"""

#
import pandas as pd
import numpy as np
import unittest

class Participants(object):

    def __new__(cls):
        return super(Participants, cls).__new__(cls)

    def __init__(self):
        super(Participants, self).__init__()

        ###############################################################################
        #  Setup some test data - tbd: move this to the participants_test.py
        columns = ['index', 'First Name', 'Last Name', 'Gender', 'Dojo', 'Age', 'Rank', 'Feet', 'Inches', 'Height',
                   'Weight', 'BMI', 'Events', 'Weapons','hitcount']
        data = [(255, 'Lucas', 'May', 'Male', 'CO- Parker', 10, 'Yellow', 4, 3, '4 ft. 3 in.', 52, 154,
                 '2 Events - Forms & Sparring ($75)', 'None',0),
                (194, 'jake', 'coleson', 'Male', 'CO- Cheyenne Mountain', 10, 'Yellow', 4, 0, '4', 60, 156,
                 '2 Events - Forms & Sparring ($75)', 'Weapons ($35)',0),
                (195, 'katie', 'coleson', 'Female', 'CO- Cheyenne Mountain', 12, 'White', 4, 0, '4', 65.161,
                 '2 Events - Forms & Sparring ($75)', 'Weapons ($35)',0)]
        self._participant_list = pd.DataFrame(data, columns=columns)

        ###############################################################################
        #  Define all the atomic masks

        # Atomic masks for Belts
        self.white_belt_mask        = self._participant_list['Rank'] == 'White'
        self.yellow_belt_mask       = self._participant_list['Rank'] == 'Yellow'
        self.orage_belt_mask        = self._participant_list['Rank'] == 'Orange'
        self.purple_belt_mask       = self._participant_list['Rank'] == 'Purple'
        self.blue_belt_mask         = self._participant_list['Rank'] == 'Blue'
        self.blue_stripe_belt_mask  = self._participant_list['Rank'] == 'Blue w/Stripe'
        self.all_blue_belt_mask     = self.blue_belt_mask | self.blue_stripe_belt_mask  # all blue and blue stripe
        self.green_belt_mask        = self._participant_list['Rank'] == 'Green'
        self.green_stripe_belt_mask = self._participant_list['Rank'] == 'Green w/Stripe'
        self.all_green_belt_mask    = self.green_belt_mask | self.green_stripe_belt_mask  # all green and green stripe
        self.third_brown_belt_mask  = self._participant_list['Rank'] == 'Brown 3rd Degree'
        self.second_brown_belt_mask = self._participant_list['Rank'] == 'Brown 2nd Degree'
        self.first_brown_belt_mask  = self._participant_list['Rank'] == 'Brown 1st Degree'
        self.all_brown_belt_mask    = self.first_brown_belt_mask | self.second_brown_belt_mask | self.third_brown_belt_mask # all brown belts
        self.first_black_belt_mask  = self._participant_list['Rank'] == 'Black 1st Degree'
        self.second_black_belt_mask = self._participant_list['Rank'] == 'Black 2nd Degree'
        self.third_black_belt_mask  = self._participant_list['Rank'] == 'Black 3rd Degree'
        self.forth_black_belt_mask  = self._participant_list['Rank'] == 'Black 4th Degree'
        self.fifth_black_belt_mask  = self._participant_list['Rank'] == 'Black 5th Degree'
        self.jr_black_belt_mask     = self._participant_list['Rank'] == 'Black Junior'
        self.all_black_belt_mask    = self.first_black_belt_mask | self.second_black_belt_mask | self.third_black_belt_mask | self.forth_black_belt_mask | self.fifth_black_belt_mask | self.jr_black_belt_mask # # all Jr, 1st, 2nd, and 3rd degree black

        # Atomic mask for Gender
        self.male_mask = self._participant_list['Gender'] == 'Male'
        self.female_mask = self._participant_list['Gender'] == 'Female'

        # Atomic and composit mask for which event Sparring, Kata, Weapons
        self.sparring_and_forms_mask = self._participant_list['Events'] == '2 Events - Forms & Sparring ($75)'
        self.forms_only_mask = self._participant_list['Events'] == '1 Event - Forms ($75)'
        self.sparring_only_mask = self._participant_list['Events'] == '1 Event - Sparring ($75)'
        # Mask for Weapons
        self.weapons_mask = self._participant_list['Events'] == 'Weapons ($35)'

        # Composit Masks for Sparring or Forms
        self.sparring_mask = self.sparring_and_forms_mask | self.sparring_only_mask
        self.forms_mask = self.sparring_and_forms_mask | self.forms_only_mask

        # Atomic mask for age groups found in the tournament guide
        # 4-6 used for kids kata, kids sparring,
        low_age_mask = self._participant_list["Age"] >= 4
        high_age_mask = self._participant_list["Age"] <= 6
        age_4to6_mask = low_age_mask | high_age_mask




    # # Atomic mask for age groups found in the tournament guide
    # # 4-6 used for kids kata, kids sparring,
    # maskLowAge = clean_df["Competitor\'s Age?"] >= 4
    # maskHighAge = clean_df["Competitor\'s Age?"] <= 6
    # mask_Age4to6 = maskLowAge & maskHighAge
    # # testdf=cdf[['First Name','Last Name', 'Gender','Current Belt Rank?','Competitor\'s Age?','Competitor\'s Weight (in lbs.)?','Competitor\'s Height (in feet and inches)?','Choose Forms, Sparring or Both.','Choose Weapons.']][mask_Age4to6]
    #
    # # 7-9 used in Youth Kata, Young Girls Sparring, Youth Boys Sparring
    # maskLowAge = clean_df["Competitor\'s Age?"] >= 7
    # maskHighAge = clean_df["Competitor\'s Age?"] <= 9
    # mask_Age7to9 = maskLowAge & maskHighAge
    # # testdf=cdf[['First Name','Last Name', 'Gender','Current Belt Rank?','Competitor\'s Age?','Competitor\'s Weight (in lbs.)?','Competitor\'s Height (in feet and inches)?','Choose Forms, Sparring or Both.','Choose Weapons.']][mask_Age7to9]
    #
    # # 10-12 used in Boys Sparring, Boys & Girls Kata, Girls Sparring
    # maskLowAge = clean_df["Competitor\'s Age?"] >= 10
    # maskHighAge = clean_df["Competitor\'s Age?"] <= 12
    # mask_Age10to12 = maskLowAge & maskHighAge
    # # testdf=cdf[['First Name','Last Name', 'Gender','Current Belt Rank?','Competitor\'s Age?','Competitor\'s Weight (in lbs.)?','Competitor\'s Height (in feet and inches)?','Choose Forms, Sparring or Both.','Choose Weapons.']][mask_Age10to12]
    #
    # # 13-15 used in Teen Girls Sparring, Teen Kata, Teen Boys Sparring,
    # maskLowAge = clean_df["Competitor\'s Age?"] >= 13
    # maskHighAge = clean_df["Competitor\'s Age?"] <= 15
    # mask_Age13to15 = maskLowAge & maskHighAge
    # # testdf=cdf[['First Name','Last Name', 'Gender','Current Belt Rank?','Competitor\'s Age?','Competitor\'s Weight (in lbs.)?','Competitor\'s Height (in feet and inches)?','Choose Forms, Sparring or Both.','Choose Weapons.']][mask_Age13to15]
    #
    # # 4-9 used in Weapons Division 1
    # maskLowAge = clean_df["Competitor\'s Age?"] >= 4
    # maskHighAge = clean_df["Competitor\'s Age?"] <= 9
    # mask_Age4to9 = maskLowAge & maskHighAge
    # # testdf=cdf[['First Name','Last Name', 'Gender','Current Belt Rank?','Competitor\'s Age?','Competitor\'s Weight (in lbs.)?','Competitor\'s Height (in feet and inches)?','Choose Forms, Sparring or Both.','Choose Weapons.']][mask_Age4to9]
    #
    # # 18-39 used in Womans Sprring, Men and Womens Kata
    # maskLowAge = clean_df["Competitor\'s Age?"] >= 18
    # maskHighAge = clean_df["Competitor\'s Age?"] <= 39
    # mask_Age18to39 = maskLowAge & maskHighAge
    # # testdf=cdf[['First Name','Last Name', 'Gender','Current Belt Rank?','Competitor\'s Age?','Competitor\'s Weight (in lbs.)?','Competitor\'s Height (in feet and inches)?','Choose Forms, Sparring or Both.','Choose Weapons.']][mask_Age18to39]
    #
    # # 40 plus used in Senior Mens Sparring, Senior Womens Sparring, Senior Kata
    # mask_Age40Plus = clean_df["Competitor\'s Age?"] >= 40
    # # testdf=cdf[['First Name','Last Name', 'Gender','Current Belt Rank?','Competitor\'s Age?','Competitor\'s Weight (in lbs.)?','Competitor\'s Height (in feet and inches)?','Choose Forms, Sparring or Both.','Choose Weapons.']][mask_Age40Plus]
    #
    # # 16-17 used in Young Adult Kata, Young Mens Sparring, Young Adult Womens Sparring
    # maskLowAge = clean_df["Competitor\'s Age?"] >= 16
    # maskHighAge = clean_df["Competitor\'s Age?"] <= 17
    # mask_Age16to17 = maskLowAge & maskHighAge
    # # testdf=cdf[['First Name','Last Name', 'Gender','Current Belt Rank?','Competitor\'s Age?','Competitor\'s Weight (in lbs.)?','Competitor\'s Height (in feet and inches)?','Choose Forms, Sparring or Both.','Choose Weapons.']][mask_Age16to17]
    #
    # # 13-17 used in Weapons Division 3
    # maskLowAge = clean_df["Competitor\'s Age?"] >= 13
    # maskHighAge = clean_df["Competitor\'s Age?"] <= 17
    # mask_Age13to17 = maskLowAge & maskHighAge
    # # testdf=cdf[['First Name','Last Name', 'Gender','Current Belt Rank?','Competitor\'s Age?','Competitor\'s Weight (in lbs.)?','Competitor\'s Height (in feet and inches)?','Choose Forms, Sparring or Both.','Choose Weapons.']][mask_Age13to17]
    #
    # # 18 plus used in Weapons Division 4 and 5
    # mask_Age18Plus = clean_df["Competitor\'s Age?"] >= 18
    # # testdf=cdf[['First Name','Last Name', 'Gender','Current Belt Rank?','Competitor\'s Age?','Competitor\'s Weight (in lbs.)?','Competitor\'s Height (in feet and inches)?','Choose Forms, Sparring or Both.','Choose Weapons.']][mask_Age18Plus]
    #
    # # 13 plus used in Weapons Division 6
    # mask_Age13Plus = clean_df["Competitor\'s Age?"] >= 13
    #
    # # testdf=cdf[['First Name','Last Name', 'Gender','Current Belt Rank?','Competitor\'s Age?','Competitor\'s Weight (in lbs.)?','Competitor\'s Height (in feet and inches)?','Choose Forms, Sparring or Both.','Choose Weapons.']][mask_Age13Plus]




    def print_participants(self):
        """Print the participant list to standard out."""
        print self._participant_list

    def participants_from_mask( self, mask ):
      """Gets participants from a mask
      :param self: 
      :param mask: 
      :return:new data frame with the participants
      """
      x=2
      participant_subset = self._participant_list[["First Name", "Last Name", "Gender", "Dojo", "Age", "Rank", "Feet", "Inches", "Height", "Weight", "BMI", "Events", "Weapons"]][mask].sort_values("Age")
      participant_subset.sort_values('BMI',inplace=True)
      #    newdf.rename(columns={'Select Your Z Ultimate Studio':'Dojo','Out of State Studio Name':'Out of State Dojo Name','Competitor\'s Age?':'Age','Current Belt Rank?':'Rank','Competitor\'s Height (e.g. 4 ft. 2 in. )?':'Height','Competitor\'s Weight (eg. 73lbs.)?':'Weight','Choose Forms, Sparring or Both.':'Events','Choose Weapons.':'Weapons'},inplace=True)
      #    newdf.rename(columns={'Select Your Z Ultimate Studio':'Dojo','Competitor\'s Age?':'Age','Current Belt Rank?':'Rank','Competitor\'s Height (e.g. 4 ft. 2 in. )?':'Height','Competitor\'s Weight (eg. 73lbs.)?':'Weight','Choose Forms, Sparring or Both.':'Events','Choose Weapons.':'Weapons'},inplace=True)

      ## update the hitcount every time we touch someone
      for index, row in self._participant_list[mask].iterrows():
           name=row['First Name'] + " " + row['Last Name']
           hc=row['hitcount']
           newhc=hc+1
       #    print name + " has a row count of " + str(newhc)
           self._participant_list.at[index, 'hitcount']=newhc

      return participant_subset

