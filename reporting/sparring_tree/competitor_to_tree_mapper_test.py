'''
This module tests the competitor_to_tree_mapper module
to run this test go to the main directory and run
nosetests --with-coverage
'''''

import unittest
from reporting.sparring_tree import competitors as competitors
from reporting.sparring_tree import competitor_to_tree_mapper as ctm

class CompetitorToTreeMapper(unittest.TestCase):
    ''' class to test the CompetitorToTreeMapper code'''

    def setUp(self):
        ''' setup code for the tests'''
        return

    def test_set_competitors(self):
        '''test arraning compettitor for sparring so they are arranged by BMI,
        then ordered to avoid people from the same dojo sparring each other '''

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

        competitor_mapper=ctm.CompetitorsToTreeMapper()
        competitor_mapper.set_competitors(c)



if __name__ == '__main__':
    unittest.main()
