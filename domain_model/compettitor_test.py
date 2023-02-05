'''
This module tests the competitor module
to run this test go to the main directory and run
nosetests --with-coverage
'''''

import unittest
import logging

from domain_model import competitors as competitors


class TestCompetitors(unittest.TestCase):
    ''' class to test the Competitor code'''

    def setUp(self):
        ''' setup code for the tests'''
        import pandas as pd
        pd.set_option('display.max_rows', 500)
        pd.set_option('display.max_columns', 500)
        pd.set_option('display.width', 1000)
        return

    def test_competttitors_has_correct_number_of_entries(self):
        '''test getting the number of compettitors '''
        cols = ['index', 'First_Name', 'Last_Name', 'Gender', 'Dojo', 'Age', 'Rank', 'Feet', 'Inches', 'Height',
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
        '''test getting the number of compettitors '''
        cols = ['index', 'First_Name', 'Last_Name', 'Gender', 'Dojo', 'Age', 'Rank', 'Feet', 'Inches', 'Height',
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
        cols = ['index', 'First_Name', 'Last_Name', 'Gender', 'Dojo', 'Age', 'Rank', 'Feet', 'Inches', 'Height',
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

if __name__ == '__main__':
    unittest.main()
