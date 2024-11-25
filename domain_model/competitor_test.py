'''
This module tests the competitor module
to run this test go to the main directory and run
nosetests --with-coverage
'''''

import sys
import unittest
import logging
import pandas as pd

from domain_model import competitors as competitors

logger = logging.getLogger('')
logger.setLevel(logging.INFO)
sh = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('[%(asctime)s] %(levelname)s %(message)s', datefmt='%H:%M:%S')
sh.setFormatter(formatter)
logger.addHandler(sh)

class TestCompetitors(unittest.TestCase):
    ''' class to test the Competitor code'''

    def setUp(self):
        ''' setup code for the tests'''
        pd.set_option('display.max_rows', 500)
        pd.set_option('display.max_columns', 500)
        pd.set_option('display.width', 1000)
        return

    def test_competttitors_has_correct_number_of_entries(self):
        '''test getting the number of Competitors '''
        cols = ['Registrant_ID', 'First_Name', 'Last_Name', 'Gender', 'Dojo', 'Age', 'Rank', 'Feet', 'Inches', 'Height',
                'Weight', 'BMI', 'Events', 'Weapons', 'hitcount']
        data = [(255, 'Lucas', 'May', 'Male', 'CO- Parker', 10, 'Yellow', 4, 3, '4 ft. 3 in.', 52, 154,
                 '2 Events - Forms & Sparring ($75)', 'None', 0),
                (194, 'jake', 'coleson', 'Male', 'CO- Parker', 10, 'Yellow', 4, 0, '4', 60, 156,
                 '2 Events - Forms & Sparring ($75)', 'Weapons ($35)', 0),
                (195, 'katie', 'coleson', 'Female', 'CO- Cheyenne Mountain', 12, 'White', 4, 0, '4', 65.161,
                 '2 Events - Forms & Sparring ($75)', 'Weapons ($35)', 0)]
        c = competitors.Competitors(data, columns=cols)
        s = c.get_number_of_competitors()
        self.assertEqual(3, s)

    def test_sort_competitors_by_bmi_and_dojo(self):
        '''test getting the number of Competitors '''
        cols = ['Registrant_ID', 'First_Name', 'Last_Name', 'Gender', 'Dojo', 'Age', 'Rank', 'Feet', 'Inches', 'Height',
                'Weight', 'BMI', 'Events', 'Weapons', 'hitcount']
        data = [(255, 'Lucas', 'May', 'Male', 'CO- Parker', 10, 'Yellow', 4, 0, '4', 60, 156,
                 '2 Events - Forms & Sparring ($75)', 'None', 0),
                (194, 'jake', 'coleson', 'Male', 'Parker', 10, 'Yellow', 4, 3, '4 ft. 3 in.', 52, 154,
                 '2 Events - Forms & Sparring ($75)', 'Weapons ($35)', 0),
                (195, 'katie', 'coleson', 'Female', 'CO- Cheyenne Mountain', 12, 'White', 4, 0, '4', 65, 161,
                 '2 Events - Forms & Sparring ($75)', 'Weapons ($35)', 0)]

        c = competitors.Competitors(data, columns=cols)
        c= c.sort_by_body_mass_index_and_dojo()
        last_bmi = 0
        for index, competitor in c.iterrows():
            # logging.info(index,competitor['First Name'],competitor.BMI)
            self.assertTrue(competitor.BMI >= last_bmi)
            last_bmi = competitor.BMI

    def test_arrange_competitors_for_sparring(self):
        cols = ['Registrant_ID', 'First_Name', 'Last_Name', 'Gender', 'Dojo', 'Age', 'Rank', 'Feet', 'Inches', 'Height',
                      'Weight', 'BMI', 'Events', 'Weapons', 'hitcount']
        data = [(1, 'Katie', 'Coleson', 'Female', 'CO- Parker', 12, 'White', 4, 0, '4', 65, 161,
                       '2 Events - Forms & Sparring ($75)', 'Weapons ($35)', 0),
                      (2, 'Lucas', 'May', 'Male', 'CO- Cheyenne Mountain', 10, 'Yellow', 4, 3, '4 ft. 3 in.', 52, 154,
                       '2 Events - Forms & Sparring ($75)', 'None', 0),
                      (3, 'Jake', 'Coleson', 'Male', 'CO- Cheyenne Mountain', 10, 'Yellow', 4, 0, '4', 60, 156,
                       '2 Events - Forms & Sparring ($75)', 'Weapons ($35)', 0),
                      (4, 'Allen', 'Whitaker', 'Male', 'CO- Arvada', 10, 'Yellow', 4, 0, '4', 55, 151,
                       '2 Events - Forms & Sparring ($75)', 'Weapons ($35)', 0),
                      (5, 'Bill', 'Kable', 'Male', 'CO- Parker', 10, 'Yellow', 4, 1, '4', 63, 161,
                       '2 Events - Forms & Sparring ($75)', 'Weapons ($35)', 0)]
        some_competitors = competitors.Competitors(data, columns=cols)

        # import pandas as pd
        # pd.set_option('display.max_columns', None)  # or 1000
        # pd.set_option('display.max_rows', None)  # or 1000
        # pd.set_option('display.max_colwidth', -1)  # or 199
        # pd.set_option('display.width',200)
        #

        logging.info( "Initial Competitors:")
        logging.info(some_competitors)

        arranged_competitors = some_competitors.arrange_competitors_for_sparring()
        logging.info( "Sorted Competitors:")
        logging.info(some_competitors)

        self.assertTrue(arranged_competitors.get_number_of_competitors() == 5)

        n = some_competitors.get_number_of_competitors()

        for i in range(0, n - 1, 2):
            dojo_1 = arranged_competitors.iloc[i]['Dojo']
            bmi_1 = arranged_competitors.iloc[i]['BMI']
            dojo_2 = arranged_competitors.iloc[i + 1]['Dojo']
            bmi_2 = arranged_competitors.iloc[i + 1]['BMI']
            self.assertTrue(dojo_1 != dojo_2)
            self.assertTrue(bmi_1 < bmi_2)

    def test_for_Feb2024Bug_arranging_competitors_even_number_of_competitors(self):
        pd.set_option("display.max_columns", None)
        pd.set_option("display.max_rows", None)
        pd.set_option("display.width", 1000)


        data = [(83, 'Bailey', 'Ness',          'Female',12.0,'87', '4 ft 11 in',   'Orange',   'Teens (12-14)','CO- Broomfield',   'Colorado', 'Forms | Sparring | Techniques','','4', '11',   59.0,   205.0, 4,  'N'),
                (24, 'Lana',   'Letlout',       'Female',12.0,'97', '5\'2"',        'Orange',   'Teens (12-14)','CO- Aurora',       '',         'Forms | Sparring | Techniques','','5', '2',    62.0,   221.,   4,  'L'),
                (45, 'Hiyam',  'Alfuraiji',     'Female',13.0,'102',"5'",           'Orange',   'Teens (12-14)','CO- Aurora',       '',         'Forms | Sparring | Techniques','','5', 0,      60.0,   222.0,  4,  'A'),
                (51, 'Aya',    'Letlout',       'Female',14.0,'96', '5\'3"',        'Orange',   'Teens (12-14)','CO- Aurora',       '',         'Forms | Sparring | Techniques','','5', '3',    63.0,   222.0,  4,  'L'),
                (60, 'Roxy',   'Davis',         'Female',13.0,'105','62"',          'Orange',   'Teens (12-14)','CO- Aurora',       'CO',       'Forms | Sparring | Techniques','',5,   2,      62.0,   229.0,  4,  'D'),
                (67, 'Simonne','Galvin',        'Female',13.0,'120','4?9?',         'White',    'Teens (12-14)','CO- Aurora',       'CO',       'Forms | Sparring',             '','4', '9',    57.0,   234.0,  3,  'G'),
                (365,'Lauren', 'Ruffner',       'Female',13.0,'112','5 ft 3 in',    'Orange',   'Teens (12-14)','CO- Parker',       'CO',       'Sparring',                     '','5', '3',    63.0,   238.0,  1,  'R'),
                (455,'Test',   'Test',          'Female',13.0,'112','5 ft 3 in',    'Orange',   'Teens (12-14)','CO- Aurora',       'CO',       'Sparring',                     '','5', '3',    63.0,   238.0,  1,  'T'),
                (49, 'Hala',   'Al Charderchi', 'Female',13.0,'146','58',           'Orange',   'Teens (12-14)','CO- Aurora',       'Colorado', 'Forms | Sparring | Techniques','',4,   10,     58.0,   262.0,  4,  'A'),
                (37, 'Destiny','Benjamin-Dumas','Female',13.0,'160','63',           'Yellow',   'Teens (12-14)','CO- Aurora',       'Colorado', 'Forms | Sparring | Techniques','',5,   3,      63.0,   286.0,  4,  'B')]

        cols = ['Registrant_ID','First_Name', 'Last_Name','Gender','Age','Weight','Height', 'Rank', 'Division', 'Dojo', 'Out State','Events', 'Weapons', 'Feet', 'Inches', 'HeightInInches','BMI', 'hitcount', 'First_Letter']
        original_comps = competitors.Competitors(data, columns=cols)
        logging.info(original_comps)

        comps_in_sparring_order = original_comps.arrange_competitors_for_sparring()
        # comps_in_sparring_order = original_comps.sort_values(by=['Registrant_ID'], ascending=[True])  # test the test
        logging.info("\nSorted Competitors:")
        logging.info(comps_in_sparring_order)

        # Merge the two DataFrames to find the intersection
        intersection = pd.merge(comps_in_sparring_order, original_comps, on=['Registrant_ID', 'First_Name', 'Last_Name'],how='inner')['Registrant_ID'].unique()
        # intersection = pd.merge(comps,comps_in_sparring_order, on='Registrant_ID',how='inner')['Registrant_ID'].unique()

        logging.info("\nIntersection:")
        logging.info(intersection)

        # Validate that every item in original_comps is also in sparring_order
        logging.info(f'\nOriginal Competitors: {len(original_comps)} intersected with Competitors in Sparring Order: {len(intersection)}')
        if len(intersection) == len(original_comps):
            logging.info("Validation successful: All items in original_comps are in comps_in_sparring_order")
        else:
            logging.info("Validation failed: Some items in original_comps are not in comps_in_sparring_order")

        self.assertTrue(len(intersection) == len(original_comps))

    def test_for_Feb2024Bug_arranging_competitors_odd_number_of_competitors(self):
        pd.set_option("display.max_columns", None)
        pd.set_option("display.max_rows", None)
        pd.set_option("display.width", 1000)


        data = [(83, 'Bailey', 'Ness',          'Female',12.0,'87', '4 ft 11 in',   'Orange',   'Teens (12-14)','CO- Broomfield',   'Colorado', 'Forms | Sparring | Techniques','','4', '11',   59.0,   205.0, 4,  'N'),
                (24, 'Lana',   'Letlout',       'Female',12.0,'97', '5\'2"',        'Orange',   'Teens (12-14)','CO- Aurora',       '',         'Forms | Sparring | Techniques','','5', '2',    62.0,   221.,   4,  'L'),
                (45, 'Hiyam',  'Alfuraiji',     'Female',13.0,'102',"5'",           'Orange',   'Teens (12-14)','CO- Aurora',       '',         'Forms | Sparring | Techniques','','5', 0,      60.0,   222.0,  4,  'A'),
                (51, 'Aya',    'Letlout',       'Female',14.0,'96', '5\'3"',        'Orange',   'Teens (12-14)','CO- Aurora',       '',         'Forms | Sparring | Techniques','','5', '3',    63.0,   222.0,  4,  'L'),
                (60, 'Roxy',   'Davis',         'Female',13.0,'105','62"',          'Orange',   'Teens (12-14)','CO- Aurora',       'CO',       'Forms | Sparring | Techniques','',5,   2,      62.0,   229.0,  4,  'D'),
                (67, 'Simonne','Galvin',        'Female',13.0,'120','4?9?',         'White',    'Teens (12-14)','CO- Aurora',       'CO',       'Forms | Sparring',             '','4', '9',    57.0,   234.0,  3,  'G'),
                (365,'Lauren', 'Ruffner',       'Female',13.0,'112','5 ft 3 in',    'Orange',   'Teens (12-14)','CO- Parker',       'CO',       'Sparring',                     '','5', '3',    63.0,   238.0,  1,  'R'),
                (49, 'Hala',   'Al Charderchi', 'Female',13.0,'146','58',           'Orange',   'Teens (12-14)','CO- Aurora',       'Colorado', 'Forms | Sparring | Techniques','',4,   10,     58.0,   262.0,  4,  'A'),
                (37, 'Destiny','Benjamin-Dumas','Female',13.0,'160','63',           'Yellow',   'Teens (12-14)','CO- Aurora',       'Colorado', 'Forms | Sparring | Techniques','',5,   3,      63.0,   286.0,  4,  'B')]

        cols = ['Registrant_ID','First_Name', 'Last_Name','Gender','Age','Weight','Height', 'Rank', 'Division', 'Dojo', 'Out State','Events', 'Weapons', 'Feet', 'Inches', 'HeightInInches','BMI', 'hitcount', 'First_Letter']
        original_comps = competitors.Competitors(data, columns=cols)
        logging.info(original_comps)

        comps_in_sparring_order = original_comps.arrange_competitors_for_sparring()
        # comps_in_sparring_order = original_comps.sort_values(by=['Registrant_ID'], ascending=[True])  # test the test
        logging.info("\nSorted Competitors:")
        logging.info(comps_in_sparring_order)

        # Merge the two DataFrames to find the intersection
        intersection = pd.merge(comps_in_sparring_order, original_comps, on=['Registrant_ID', 'First_Name', 'Last_Name'],how='inner')['Registrant_ID'].unique()
        # intersection = pd.merge(comps,comps_in_sparring_order, on='Registrant_ID',how='inner')['Registrant_ID'].unique()

        logging.info("\nIntersection:")
        logging.info(intersection)

        # Validate that every item in original_comps is also in sparring_order
        logging.info(f'\nOriginal Competitors: {len(original_comps)} intersected with Competitors in Sparring Order: {len(intersection)}')
        if len(intersection) == len(original_comps):
            logging.info("Validation successful: All items in original_comps are in comps_in_sparring_order")
        else:
            logging.info("Validation failed: Some items in original_comps are not in comps_in_sparring_order")

        self.assertTrue(len(intersection) == len(original_comps))


if __name__ == '__main__':
    unittest.main()
