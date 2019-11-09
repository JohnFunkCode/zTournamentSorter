'''
This module tests the competitor module
to run this test go to the main directory and run
nosetests --with-coverage
'''''

import unittest
from reporting.sparring_tree import competitors as competitors


class CompetitorToTreeMapper(unittest.TestCase):
    ''' class to test the Competitor code'''

    def setUp(self):
        ''' setup code for the tests'''
        return

    def test_competttitors_has_correct_number_of_entries(self):
        '''test getting the number of compettitors '''
        cols = ['index', 'First Name', 'Last Name', 'Gender', 'Dojo', 'Age', 'Rank', 'Feet', 'Inches', 'Height',
                'Weight', 'BMI', 'Events', 'Weapons', 'hitcount']
        data = [(255, 'Lucas', 'May', 'Male', 'CO- Parker', 10, 'Yellow', 4, 3, '4 ft. 3 in.', 52, 154,
                 '2 Events - Forms & Sparring ($75)', 'None', 0),
                (194, 'jake', 'coleson', 'Male', 'CO- Cheyenne Mountain', 10, 'Yellow', 4, 0, '4', 60, 156,
                 '2 Events - Forms & Sparring ($75)', 'Weapons ($35)', 0),
                (195, 'katie', 'coleson', 'Female', 'CO- Cheyenne Mountain', 12, 'White', 4, 0, '4', 65.161,
                 '2 Events - Forms & Sparring ($75)', 'Weapons ($35)', 0)]
        c = competitors.Competitors(data, columns=cols)
        s = c.get_number_of_competitors()
        self.assertEqual(3, s)

    def test_sort_competitors_by_bmi_and_dojo(self):
        '''test getting the number of compettitors '''
        cols = ['index', 'First Name', 'Last Name', 'Gender', 'Dojo', 'Age', 'Rank', 'Feet', 'Inches', 'Height',
                'Weight', 'BMI', 'Events', 'Weapons', 'hitcount']
        data = [(255, 'Lucas', 'May', 'Male', 'CO- Parker', 10, 'Yellow', 4, 3, '4 ft. 3 in.', 52, 154,
                 '2 Events - Forms & Sparring ($75)', 'None', 0),
                (194, 'jake', 'coleson', 'Male', 'CO- Cheyenne Mountain', 10, 'Yellow', 4, 0, '4', 60, 156,
                 '2 Events - Forms & Sparring ($75)', 'Weapons ($35)', 0),
                (195, 'katie', 'coleson', 'Female', 'CO- Cheyenne Mountain', 12, 'White', 4, 0, '4', 65, 161,
                 '2 Events - Forms & Sparring ($75)', 'Weapons ($35)', 0)]

        c = competitors.Competitors(data, columns=cols)
        c.sort_by_body_mass_index_and_dojo()
        last_bmi = 0
        for index, competitor in c.iterrows():
            # print(index,competitor['First Name'],competitor.BMI)
            self.assertTrue(competitor.BMI >= last_bmi)
            last_bmi = competitor.BMI


if __name__ == '__main__':
    unittest.main()
