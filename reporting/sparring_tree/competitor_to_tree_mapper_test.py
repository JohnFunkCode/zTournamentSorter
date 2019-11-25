'''
This module tests the competitor_to_tree_mapper module
to run this test go to the main directory and run
nosetests --with-coverage
'''''

import os
import unittest
from reportlab.pdfgen import canvas

from reporting.sparring_tree import competitors
from reporting.sparring_tree import competitor_to_tree_mapper as ctm
from reporting.sparring_tree.eight_competitor_tree import EightCompetitorTree

REMOVE_TEST_FILES = False

class CompetitorToTreeMapper(unittest.TestCase):
    ''' class to test the CompetitorToTreeMapper code'''

    def setUp(self):
        ''' setup data for the tests'''
        self._cols = ['index', 'First Name', 'Last Name', 'Gender', 'Dojo', 'Age', 'Rank', 'Feet', 'Inches', 'Height',
                      'Weight', 'BMI', 'Events', 'Weapons', 'hitcount']
        self._data = [(1, 'Katie', 'Coleson', 'Female', 'CO- Parker', 12, 'White', 4, 0, '4', 65, 161,
                       '2 Events - Forms & Sparring ($75)', 'Weapons ($35)', 0),
                      (2, 'Lucas', 'May', 'Male', 'CO- Cheyenne Mountain', 10, 'Yellow', 4, 3, '4 ft. 3 in.', 52, 154,
                       '2 Events - Forms & Sparring ($75)', 'None', 0),
                      (3, 'Jake', 'Coleson', 'Male', 'CO- Cheyenne Mountain', 10, 'Yellow', 4, 0, '4', 60, 156,
                       '2 Events - Forms & Sparring ($75)', 'Weapons ($35)', 0),
                      (4, 'Allen', 'Whitaker', 'Male', 'CO- Arvada', 10, 'Yellow', 4, 0, '4', 55, 151,
                       '2 Events - Forms & Sparring ($75)', 'Weapons ($35)', 0),
                      (5, 'Bill', 'Kable', 'Male', 'CO- Cheyenne Mountain', 10, 'Yellow', 4, 1, '4', 63, 161,
                       '2 Events - Forms & Sparring ($75)', 'Weapons ($35)', 0)]

    def test_set_competitors(self):
        '''test arraning compettitor for sparring so they are arranged by BMI,
        then ordered to avoid people from the same dojo sparring each other '''

        c = competitors.Competitors(self._data, columns=self._cols) # create a list of competitors from the test data above
        competitor_mapper = ctm.CompetitorsToTreeMapper()
        competitor_mapper.set_competitors(c)
        n = competitor_mapper.get_number_of_competitors()
        self.assertTrue(n == 5)

    def test_get_competitors_arranged_for_sparring(self):
        ''' test getting a competitor list arraged for sparring trees by ....'''

        c = competitors.Competitors(self._data, columns=self._cols) # create a list of competitors from the test data above
        competitor_mapper = ctm.CompetitorsToTreeMapper()
        competitor_mapper.set_competitors(c)
        # competitors_arranged_for_sparring=competitor_mapper.get_competitors_arranged_for_sparring(c)
        print(competitor_mapper.get_competitors())
        n = competitor_mapper.get_number_of_competitors()

        for i in range(0, n - 1, 2):
            comps = competitor_mapper.get_competitors()
            dojo_1 = comps.iloc[i]['Dojo']
            bmi_1 = comps.iloc[i]['BMI']
            dojo_2 = comps.iloc[i + 1]['Dojo']
            bmi_2 = comps.iloc[i + 1]['BMI']
            self.assertTrue(dojo_1 != dojo_2)
            self.assertTrue(bmi_1 < bmi_2)

#TBD add additional tests for odd and even number of compettitors,
#TBD also add a test for > 8 competttitors or 0 compettitors


    def test_map_competitors_to_tree_coordinates(self):
        ''' tests that we each compettitor gets assigned physical coordinates '''
        #create compettitors from our test data
        #get the first and second column test coordinates from the tree
        #run the algorythm to map compettitors into the tree
        # description of how to add a new column to an existing dataframe https://www.geeksforgeeks.org/adding-new-column-to-existing-dataframe-in-pandas/
        c = competitors.Competitors(self._data, columns=self._cols)  # create a list of competitors from the test data above

        # setup an 8 person tree
        test_file_name = "8PersonTree.pdf"
        test_canvas = canvas.Canvas(test_file_name)
        tree = EightCompetitorTree(test_canvas)
        tree.draw_static_template()

        # Setup the competitor_mapper
        competitor_mapper = ctm.CompetitorsToTreeMapper()
        competitor_mapper.set_competitors(c)

        # draw the competitors onto the tree
        tree.draw_competitors_on_tree(competitor_mapper)

        # close out the 8 person tree
        tree.close()
        test_canvas.save()

        # test to see if the PDF file was created
        self.assertTrue(os.path.exists(test_file_name))
        if REMOVE_TEST_FILES:
            os.remove(test_file_name)



if __name__ == '__main__':
    unittest.main()
