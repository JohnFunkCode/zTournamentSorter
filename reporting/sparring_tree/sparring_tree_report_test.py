'''
This module tests the sparring tree report
to run this test go to the main directory and run
nosetests --with-coverage
'''''

import os
import unittest
from reportlab.pdfgen import canvas

from reporting.sparring_tree import competitors
from reporting.sparring_tree.eight_competitor_tree import EightCompetitorTree

REMOVE_TEST_FILES = False

class TestSparringTreeReport(unittest.TestCase):
    ''' class to test the SparringTreeReport code'''

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



    def test_draw_competitors_on_tree(self):
        ''' tests that we each compettitor gets assigned physical coordinates '''
        #create compettitors from our test data
        #get the first and second column test coordinates from the tree
        #run the algorythm to map compettitors into the tree
        # description of how to add a new column to an existing dataframe https://www.geeksforgeeks.org/adding-new-column-to-existing-dataframe-in-pandas/
        the_competitors = competitors.Competitors(self._data, columns=self._cols)  # create a list of competitors from the test data above

        # setup an 8 person tree
        test_file_name = "8PersonTree.pdf"
        test_canvas = canvas.Canvas(test_file_name)
        tree = EightCompetitorTree(test_canvas)
        tree.draw_static_template()


        # draw the competitors onto the tree
        tree.draw_competitors_on_tree(the_competitors)

        # close out the 8 person tree
        tree.close()
        test_canvas.save()

        # test to see if the PDF file was created
        self.assertTrue(os.path.exists(test_file_name))
        if REMOVE_TEST_FILES:
            os.remove(test_file_name)



if __name__ == '__main__':
    unittest.main()
