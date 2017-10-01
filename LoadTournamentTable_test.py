#to run this test go to the main directory and run
# nosetests --with-coverage

import pandas as pd
import numpy as np
import unittest
import sys
from mock import patch

import LoadTournamentTable


class TestLoadTournamentTable(unittest.TestCase):

    def setUp(self):
        return

    def test_Age7to8_mask_returns_7_and_8_year_olds(self):
        testdf=LoadTournamentTable.clean_df[['First Name','Last Name', 'Gender','Current Belt Rank?','Competitor\'s Age?','Competitor\'s Weight (eg. 73lbs.)?','Competitor\'s Height (e.g. 4 ft. 2 in. )?','Choose Forms, Sparring or Both.','Choose Weapons.']][LoadTournamentTable.mask_Age7to8]
        print "Here are the ages"
        for index, row in testdf.iterrows():
            #name = row['First Name'] + " " + row['Last Name']
            age = row['Competitor\'s Age?']
            self.assertTrue( age >=7 & age <=8)

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
