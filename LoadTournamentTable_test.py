#to run this test go to the main directory and run
# nosetests --with-coverage --verbose

import logging
import pandas as pd
import numpy as np
import unittest
import sys
from mock import patch

import LoadTournamentTable
import os


class TestLoadTournamentTable(unittest.TestCase):

    def setUp(self):
        # filename = "/users/johnfunk/CloudStation/TournamentProject/Clean_RegistrantExport_EM0393_20160411140713.csv"  # For Testing on John's machine
#        os.putenv("tournament_filename","/users/johnfunk/CloudStation/TournamentProject/Clean_RegistrantExport_EM0393_20160411140713.csv")
        os.putenv("tournament_filename","/users/johnfunk/CloudStation/TournamentProject/CleanerTournamentParticipantsNOTTHEFINALLIST-10-15-17.csv")
        return

    def test_Age7to8_mask_returns_only_7_and_8_year_olds(self):
        testdf = LoadTournamentTable.clean_df[
            ["First_Name", "Last_Name", "Gender", "Dojo", "Age", "Rank", "Feet", "Inches", "Height", "Weight", "BMI",
             "Events", "Weapons"]][LoadTournamentTable.mask_Age7to8]
        for index, row in testdf.iterrows():
            #name = row['First Name'] + " " + row['Last Name']
            age = row['Age']
            self.assertTrue( (age >=7) & (age <=8))

    def test_Age9to11_mask_returns_only_9_to_11_year_olds(self):
        testdf = LoadTournamentTable.clean_df[
            ["First_Name", "Last_Name", "Gender", "Dojo", "Age", "Rank", "Feet", "Inches", "Height", "Weight", "BMI",
             "Events", "Weapons"]][LoadTournamentTable.mask_Age9to11]
        for index, row in testdf.iterrows():
            # name = row['First Name'] + " " + row['Last Name']
            age = row['Age']
            self.assertTrue( (age >=9) & (age <=11))

    def test_Age12to14_mask_returns_only_12_to_14_year_olds(self):
        testdf = LoadTournamentTable.clean_df[
            ["First_Name", "Last_Name", "Gender", "Dojo", "Age", "Rank", "Feet", "Inches", "Height", "Weight", "BMI",
             "Events", "Weapons"]][LoadTournamentTable.mask_Age12to14]

        for index, row in testdf.iterrows():
            age = row['Age']
            self.assertTrue((age >= 12) & (age <= 14))

    def test_Age15to17_mask_returns_only_15_to_17_year_olds(self):
        testdf = LoadTournamentTable.clean_df[
            ["First_Name", "Last_Name", "Gender", "Dojo", "Age", "Rank", "Feet", "Inches", "Height", "Weight", "BMI",
             "Events", "Weapons"]][LoadTournamentTable.mask_Age15to17]
        for index, row in testdf.iterrows():
            # name = row['First Name'] + " " + row['Last Name']
            age = row['Age']
            self.assertTrue((age >= 15) & (age <= 17))



    # def test_participants_has_correct_number_of_entries(self):
    #     p = parts.Participants()
    #     #print p._participant_list
    #     shape=p._participant_list.shape
    #     #print shape[0]
    #     self.assertEquals(3, shape[0])

    # def test_participants_from_mask_returns_correct_results(self):
    #     p = parts.Participants()
    #     df = p.participants_from_mask(p.yellow_belt_mask)
    #     x = df.shape
    #     self.assertEquals(2, x[0])







if __name__ == '__main__':
    unittest.main()
