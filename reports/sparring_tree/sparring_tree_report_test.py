'''
This module tests the sparring tree report
to run this test go to the main directory and run
nosetests --with-coverage
'''''

import logging
import unittest
import pandas as pd

from domain_model import competitors
from reports.sparring_tree.sparring_tree_report import SparringTreeReportPDF

REMOVE_TEST_FILES = False

TEST_DATA_COLUMNS = ['index', 'First_Name', 'Last_Name', 'Gender', 'Dojo', 'Age', 'Rank', 'Feet', 'Inches', 'Height',
                     'Weight', 'BMI', 'Events', 'Weapons', 'hitcount']
TEST_DATA = [(1, 'Katie', 'Coleson', 'Female', 'CO- Parker', 12, 'White', 4, 0, '4', 65, 161,
              '2 Events - Forms & Sparring ($75)', 'Weapons ($35)', 0),
             (2, 'Lucas', 'May', 'Male', 'CO- Cheyenne Mountain', 10, 'Yellow', 4, 3, '4 ft. 3 in.', 52, 154,
              '2 Events - Forms & Sparring ($75)', 'None', 0),
             (3, 'Jake', 'Coleson', 'Male', 'CO- Cheyenne Mountain', 10, 'Yellow', 4, 0, '4', 60, 156,
              '2 Events - Forms & Sparring ($75)', 'Weapons ($35)', 0),
             (4, 'Allen', 'Whitaker', 'Male', 'CO- Arvada', 10, 'Yellow', 4, 0, '4', 55, 151,
              '2 Events - Forms & Sparring ($75)', 'Weapons ($35)', 0),
             (5, 'Bill', 'Kable', 'Male', 'CO- Cheyenne Mountain', 10, 'Yellow', 4, 1, '4', 63, 161,
              '2 Events - Forms & Sparring ($75)', 'Weapons ($35)', 0),
             (6, 'Maddi', 'Stele', 'Female', 'CO- Arvada', 10, 'Purple', 4, 1, '4', 63, 161,
              '2 Events - Forms & Sparring ($75)', 'Weapons ($35)', 0)]


class TestSparringTreeReport(unittest.TestCase):
    ''' class to test the SparringTreeReport code'''

    def setUp(self):
        ''' setup data for the tests'''

    def test_write_event_to_sparring_report_using_pattern_1(self):
        ''' test that we can write a sparring report using pattern 1'''
        df= pd.DataFrame(TEST_DATA, columns=TEST_DATA_COLUMNS)
        the_competitors = competitors.Competitors(df)
        # the_competitors = competitors.Competitors(TEST_DATA,
        #                                           columns=TEST_DATA_COLUMNS)  # create a list of competitors from the test data above

        sparring_tree_report = SparringTreeReportPDF()

        # sparring_tree_report.write_event_to_sparring_report_using_pattern_1([1, 2, 3, 4, 5], "9:00am", "Kids Kata", the_competitors)
        sparring_tree_report.add_page_with_competitors_on_tree([1, 2, 3, 4, 5], "9:00am", "Kids Kata", "10-12", ['White','Yellow','Orange','Purple'], the_competitors)
        sparring_tree_report.close()


if __name__ == '__main__':
    unittest.main()
