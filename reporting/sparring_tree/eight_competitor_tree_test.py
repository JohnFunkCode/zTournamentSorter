'''
This module tests the eight_compettitor_tree module
to run this test go to the main directory and run
nosetests --with-coverage
'''''

import unittest
import os
from reportlab.pdfgen import canvas
from reporting.sparring_tree.eight_competitor_tree import EightCompetitorTree

REMOVE_TEST_FILES = False


# from eight_competitor_tree import EightCompetitorTree
# import eight_competitor_tree

class TestEightCompetitorTree(unittest.TestCase):
    ''' class to test the EightCompettitorTree code'''
    def setUp(self):
        ''' setup code for the tests'''
        return

    def test_creating_a_file(self):
        ''' simple test to make sure we can create a file with the template code in it'''
        test_file_name = "8PersonTree.pdf"
        test_canvas = canvas.Canvas(test_file_name)
        tree = EightCompetitorTree(test_canvas)
        tree.draw_static_template()
        tree.close()
        test_canvas.save()

        # test to see if the PDF file was created
        self.assertTrue(os.path.exists(test_file_name))
        if REMOVE_TEST_FILES:
            os.remove(test_file_name)

    def test_creating_a_file_with_two_tree(self):
        ''' tests that we can create a PDF with multiple sparring trees in it'''
        test_file_name = "8PersonTree.pdf"
        test_canvas = canvas.Canvas(test_file_name)
        tree = EightCompetitorTree(test_canvas)

        # draw first tree
        tree.draw_static_template()
        tree.close()

        # draw second tree
        tree.draw_static_template()
        tree.close()

        self.assertTrue(test_canvas.__dict__['_pageNumber'] == 3)  # Make sure we have 2 pages
        test_canvas.save()
        if REMOVE_TEST_FILES:
            os.remove(test_file_name)


if __name__ == '__main__':
    unittest.main()
