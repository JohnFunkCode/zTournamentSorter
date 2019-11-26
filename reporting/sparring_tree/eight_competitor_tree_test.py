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
        test_file_name = "8PersonTree_Create_File.pdf"
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
        test_file_name = "8PersonTree_Two_Trees.pdf"
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

    def test_initialize_text_coordinates(self):
        ''' test to make sure the text coordinates are initialized '''
        test_file_name = "8PersonTree_Init_Text_Coords.pdf"
        test_canvas = canvas.Canvas(test_file_name)
        tree = EightCompetitorTree(test_canvas)
        self.assertTrue(len(tree._first_column_text_coordinates) == 8)
        self.assertTrue(len(tree._second_column_text_coordinates) == 4)

        # draw the tree just for the heck of it
        tree.draw_static_template()
        tree.close()
        test_canvas.save()
        # test to see if the PDF file was created
        self.assertTrue(os.path.exists(test_file_name))
        if REMOVE_TEST_FILES:
            os.remove(test_file_name)

    def test_draw_8_names_on_tree(self):
        ''' tests to make sure the names in an 8 person tree get put in the right place'''

        # setup an 8 person tree
        test_file_name = "8PersonTree.pdf"
        test_canvas = canvas.Canvas(test_file_name)
        tree = EightCompetitorTree(test_canvas)
        tree.draw_static_template()

        names = ["One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight"]
        #            ,"Nine","Ten","Eleven","Twelve"]
        competitor_count = len(names)
        i = 0
        for i in range(competitor_count):
            # print('\n' + names[i])
            px, py = tree.calculate_canvas_coordinates_from_competitor_index(competitor_count, i)
            test_canvas.drawString(px, py, names[i])

        # draw the tree just for the heck of it
        tree.draw_static_template()
        tree.close()
        test_canvas.save()
        # test to see if the PDF file was created
        self.assertTrue(os.path.exists(test_file_name))
        if REMOVE_TEST_FILES:
            os.remove(test_file_name)

    def test_draw_7_names_on_tree(self):
        ''' tests to make sure the names in an 8 person tree get put in the right place'''

        # setup an 7 person tree
        test_file_name = "7PersonTree.pdf"
        test_canvas = canvas.Canvas(test_file_name)
        tree = EightCompetitorTree(test_canvas)
        tree.draw_static_template()

        names = ["One", "Two", "Three", "Four", "Five", "Six", "Seven"]
        competitor_count = len(names)
        i = 0
        for i in range(competitor_count):
            # print('\n' + names[i])
            px, py = tree.calculate_canvas_coordinates_from_competitor_index(competitor_count, i)
            test_canvas.drawString(px, py, names[i])

        # draw the tree just for the heck of it
        tree.draw_static_template()
        tree.close()
        test_canvas.save()
        # test to see if the PDF file was created
        self.assertTrue(os.path.exists(test_file_name))
        if REMOVE_TEST_FILES:
            os.remove(test_file_name)

    def test_draw_6_names_on_tree(self):
        ''' tests to make sure the names in an 8 person tree get put in the right place'''

        # setup 6 person tree
        test_file_name = "6PersonTree.pdf"
        test_canvas = canvas.Canvas(test_file_name)
        tree = EightCompetitorTree(test_canvas)
        tree.draw_static_template()

        names = ["One", "Two", "Three", "Four", "Five", "Six"]
        competitor_count = len(names)
        i = 0
        for i in range(competitor_count):
            # print('\n' + names[i])
            px, py = tree.calculate_canvas_coordinates_from_competitor_index(competitor_count, i)
            test_canvas.drawString(px, py, names[i])

        # draw the tree just for the heck of it
        tree.draw_static_template()
        tree.close()
        test_canvas.save()
        # test to see if the PDF file was created
        self.assertTrue(os.path.exists(test_file_name))
        if REMOVE_TEST_FILES:
            os.remove(test_file_name)

    def test_draw_5_names_on_tree(self):
        ''' tests to make sure the names in an 8 person tree get put in the right place'''

        # setup 5 person tree
        test_file_name = "5PersonTree.pdf"
        test_canvas = canvas.Canvas(test_file_name)
        tree = EightCompetitorTree(test_canvas)
        tree.draw_static_template()

        names = ["One", "Two", "Three", "Four", "Five"]
        competitor_count = len(names)
        i = 0
        for i in range(competitor_count):
            # print('\n' + names[i])
            px, py = tree.calculate_canvas_coordinates_from_competitor_index(competitor_count, i)
            test_canvas.drawString(px, py, names[i])

        # draw the tree just for the heck of it
        tree.draw_static_template()
        tree.close()
        test_canvas.save()
        # test to see if the PDF file was created
        self.assertTrue(os.path.exists(test_file_name))
        if REMOVE_TEST_FILES:
            os.remove(test_file_name)

    def test_draw_4_names_on_tree(self):
        ''' tests to make sure the names in an 8 person tree get put in the right place'''

        # setup 4 person tree
        test_file_name = "4PersonTree.pdf"
        test_canvas = canvas.Canvas(test_file_name)
        tree = EightCompetitorTree(test_canvas)
        tree.draw_static_template()

        names = ["One", "Two", "Three", "Four"]
        competitor_count = len(names)
        i = 0
        for i in range(competitor_count):
            # print('\n' + names[i])
            px, py = tree.calculate_canvas_coordinates_from_competitor_index(competitor_count, i)
            test_canvas.drawString(px, py, names[i])

        # draw the tree just for the heck of it
        tree.draw_static_template()
        tree.close()
        test_canvas.save()
        # test to see if the PDF file was created
        self.assertTrue(os.path.exists(test_file_name))
        if REMOVE_TEST_FILES:
            os.remove(test_file_name)

    def test_draw_3_names_on_tree(self):
        ''' tests to make sure the names in an 8 person tree get put in the right place'''

        # setup 3 person tree
        test_file_name = "3PersonTree.pdf"
        test_canvas = canvas.Canvas(test_file_name)
        tree = EightCompetitorTree(test_canvas)
        tree.draw_static_template()

        names = ["One", "Two", "Three"]
        competitor_count = len(names)
        i = 0
        for i in range(competitor_count):
            # print('\n' + names[i])
            px, py = tree.calculate_canvas_coordinates_from_competitor_index(competitor_count, i)
            test_canvas.drawString(px, py, names[i])

        # draw the tree just for the heck of it
        tree.draw_static_template()
        tree.close()
        test_canvas.save()
        # test to see if the PDF file was created
        self.assertTrue(os.path.exists(test_file_name))
        if REMOVE_TEST_FILES:
            os.remove(test_file_name)

    def test_draw_2_names_on_tree(self):
        ''' tests to make sure the names in an 8 person tree get put in the right place'''

        # setup 2 person tree
        test_file_name = "2PersonTree.pdf"
        test_canvas = canvas.Canvas(test_file_name)
        tree = EightCompetitorTree(test_canvas)
        tree.draw_static_template()

        names = ["One", "Two"]
        competitor_count = len(names)
        i = 0
        for i in range(competitor_count):
            # print('\n' + names[i])
            px, py = tree.calculate_canvas_coordinates_from_competitor_index(competitor_count, i)
            test_canvas.drawString(px, py, names[i])

        # draw the tree just for the heck of it
        tree.draw_static_template()
        tree.close()
        test_canvas.save()
        # test to see if the PDF file was created
        self.assertTrue(os.path.exists(test_file_name))
        if REMOVE_TEST_FILES:
            os.remove(test_file_name)

    def test_draw_1_names_on_tree(self):
        ''' tests to make sure the names in an 8 person tree get put in the right place'''

        # setup 1 person tree
        test_file_name = "1PersonTree.pdf"
        test_canvas = canvas.Canvas(test_file_name)
        tree = EightCompetitorTree(test_canvas)
        tree.draw_static_template()

        names = ["One"]
        competitor_count = len(names)
        i = 0
        for i in range(competitor_count):
            # print('\n' + names[i])
            px, py = tree.calculate_canvas_coordinates_from_competitor_index(competitor_count, i)
            test_canvas.drawString(px, py, names[i])

        # draw the tree just for the heck of it
        tree.draw_static_template()
        tree.close()
        test_canvas.save()
        # test to see if the PDF file was created
        self.assertTrue(os.path.exists(test_file_name))
        if REMOVE_TEST_FILES:
            os.remove(test_file_name)

if __name__ == '__main__':
    unittest.main()