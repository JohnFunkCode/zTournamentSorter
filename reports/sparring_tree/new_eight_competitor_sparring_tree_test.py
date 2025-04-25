'''
This module tests the eight_compettitor_tree module
to run this test go to the main directory and run 
nosetests --with-coverage
'''''

import unittest
import os
import logging
from pathlib import Path

from reportlab.pdfgen import canvas
from reports.sparring_tree.new_eight_competitor_sparring_tree import NewEightCompetitorTree
from domain_model.competitors import Competitors


REMOVE_TEST_FILES = False


# from eight_competitor_tree import NewEightCompetitorTree
# import eight_competitor_tree

# data for the tests
TEST_DATA_COLUMNS = ['Registrant_ID', 'First_Name', 'Last_Name', 'Gender', 'Dojo', 'Age', 'Rank', 'Feet', 'Inches', 'Height',
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
               '2 Events - Forms & Sparring ($75)', 'Weapons ($35)', 0)]


class TestNewNewEightCompetitorTree(unittest.TestCase):
    ''' class to test the EightCompettitorTree code'''

    def setUp(self):
        ''' create a directory for all the test reports'''
        try:
            os.mkdir("testoutput")
        except:
            logging.info("expected error")
        return

    def test_creating_a_file(self):
        # set the cwd to the project root
        # path = os.getcwd()
        new_path = Path(__file__).resolve().parents[2]
        os.chdir(new_path)

        ''' simple test to make sure we can create a file with the template code in it'''
        test_file_name = "reports//sparring_tree//testoutput//8PersonTree_Create_File.pdf"
        test_canvas = canvas.Canvas(test_file_name)
        tree = NewEightCompetitorTree(test_canvas,test_file_name)
        tree.draw_static_template()
        tree.close()
        test_canvas.save()

        # test to see if the PDF file was created
        self.assertTrue(os.path.exists(test_file_name))
        if REMOVE_TEST_FILES:
            os.remove(test_file_name)

    def test_creating_a_file_with_two_tree(self):
        ''' tests that we can create a PDF with multiple sparring trees in it'''
        # set the cwd to the project root
        # path = os.getcwd()
        new_path = Path(__file__).resolve().parents[2]
        os.chdir(new_path)

        test_file_name = "reports//sparring_tree//testoutput//8PersonTree_Two_Trees.pdf"
        test_canvas = canvas.Canvas(test_file_name)
        tree = NewEightCompetitorTree(test_canvas, test_file_name)

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
        # set the cwd to the project root
        # path = os.getcwd()
        new_path = Path(__file__).resolve().parents[2]
        os.chdir(new_path)

        test_file_name = "reports//sparring_tree//testoutput//8PersonTree_Init_Text_Coords.pdf"
        test_canvas = canvas.Canvas(test_file_name)
        tree = NewEightCompetitorTree(test_canvas, test_file_name)
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
        # set the cwd to the project root
        # path = os.getcwd()
        new_path = Path(__file__).resolve().parents[2]
        os.chdir(new_path)

        # setup an 8 person tree
        test_file_name = "reports//sparring_tree//testoutput//8PersonTree.pdf"
        test_canvas = canvas.Canvas(test_file_name)
        tree = NewEightCompetitorTree(test_canvas, test_file_name)
        tree.draw_static_template()

        names = ["One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight"]
        #            ,"Nine","Ten","Eleven","Twelve"]
        competitor_count = len(names)
        i = 0
        for i in range(competitor_count):
            # logging.info('\n' + names[i])
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
        # set the cwd to the project root
        # path = os.getcwd()
        new_path = Path(__file__).resolve().parents[2]
        os.chdir(new_path)

        # setup an 7 person tree
        test_file_name = "reports//sparring_tree//testoutput//7PersonTree.pdf"
        test_canvas = canvas.Canvas(test_file_name)
        tree = NewEightCompetitorTree(test_canvas, test_file_name)
        tree.draw_static_template()

        names = ["One", "Two", "Three", "Four", "Five", "Six", "Seven"]
        competitor_count = len(names)
        i = 0
        for i in range(competitor_count):
            # logging.info('\n' + names[i])
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
        # set the cwd to the project root
        # path = os.getcwd()
        new_path = Path(__file__).resolve().parents[2]
        os.chdir(new_path)

        # setup 6 person tree
        test_file_name = "reports//sparring_tree//testoutput//6PersonTree.pdf"
        test_canvas = canvas.Canvas(test_file_name)
        tree = NewEightCompetitorTree(test_canvas, test_file_name)
        tree.draw_static_template()

        names = ["One", "Two", "Three", "Four", "Five", "Six"]
        competitor_count = len(names)
        i = 0
        for i in range(competitor_count):
            # logging.info('\n' + names[i])
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
        # set the cwd to the project root
        # path = os.getcwd()
        new_path = Path(__file__).resolve().parents[2]
        os.chdir(new_path)

        # setup 5 person tree
        test_file_name = "reports//sparring_tree//testoutput//5PersonTree.pdf"
        test_canvas = canvas.Canvas(test_file_name)
        tree = NewEightCompetitorTree(test_canvas, test_file_name)
        tree.draw_static_template()

        names = ["One", "Two", "Three", "Four", "Five"]
        competitor_count = len(names)
        i = 0
        for i in range(competitor_count):
            # logging.info('\n' + names[i])
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
        # set the cwd to the project root
        # path = os.getcwd()
        new_path = Path(__file__).resolve().parents[2]
        os.chdir(new_path)

        # setup 4 person tree
        test_file_name = "reports//sparring_tree//testoutput//4PersonTree.pdf"
        test_canvas = canvas.Canvas(test_file_name)
        tree = NewEightCompetitorTree(test_canvas, test_file_name)
        tree.draw_static_template()

        names = ["One", "Two", "Three", "Four"]
        competitor_count = len(names)
        i = 0
        for i in range(competitor_count):
            # logging.info('\n' + names[i])
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
        # set the cwd to the project root
        # path = os.getcwd()
        new_path = Path(__file__).resolve().parents[2]
        os.chdir(new_path)

        # setup 3 person tree
        test_file_name = "reports//sparring_tree//testoutput//3PersonTree_full_page.pdf"
        test_canvas = canvas.Canvas(test_file_name)
        tree = NewEightCompetitorTree(test_canvas, test_file_name)
        tree.draw_static_template()

        names = ["One", "Two", "Three"]
        competitor_count = len(names)
        i = 0
        for i in range(competitor_count):
            # logging.info('\n' + names[i])
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

        # set the cwd to the project root
        # path = os.getcwd()
        new_path = Path(__file__).resolve().parents[2]
        os.chdir(new_path)

        # setup 2 person tree
        test_file_name = "reports//sparring_tree//testoutput//2PersonTree_full_page.pdf"
        test_canvas = canvas.Canvas(test_file_name)
        tree = NewEightCompetitorTree(test_canvas, test_file_name)
        tree.draw_static_template()

        names = ["One", "Two"]
        competitor_count = len(names)
        i = 0
        for i in range(competitor_count):
            # logging.info('\n' + names[i])
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
        # set the cwd to the project root
        # path = os.getcwd()
        new_path = Path(__file__).resolve().parents[2]
        os.chdir(new_path)

        # setup 1 person tree
        test_file_name = "reports//sparring_tree//testoutput//1PersonTree_full_page.pdf"
        test_canvas = canvas.Canvas(test_file_name)
        tree = NewEightCompetitorTree(test_canvas, test_file_name)
        tree.draw_static_template()

        names = ["One"]
        competitor_count = len(names)
        i = 0
        for i in range(competitor_count):
            # logging.info('\n' + names[i])
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

    def test_draw_competitors_on_tree(self):
        ''' tests that we each compettitor gets assigned physical coordinates '''
        #create competitors from our test data
        #get the first and second column test coordinates from the tree
        #run the algorythm to map competitors into the tree
        # description of how to add a new column to an existing dataframe https://www.geeksforgeeks.org/adding-new-column-to-existing-dataframe-in-pandas/

        # set the cwd to the project root
        # path = os.getcwd()
        new_path = Path(__file__).resolve().parents[2]
        os.chdir(new_path)

        the_competitors = Competitors(TEST_DATA, columns=TEST_DATA_COLUMNS)  # create a list of competitors from the test data above

        # setup an 8 person tree
        test_file_name = "reports//sparring_tree//testoutput//8PersonTree_full_page.pdf"
        test_canvas = canvas.Canvas(test_file_name)
        tree = NewEightCompetitorTree(test_canvas, test_file_name)
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

    def test_add_page_with_competitors_on_tree(self):
        ''' tests that we each compettitor gets assigned physical coordinates '''
        #create competitors from our test data
        #get the first and second column test coordinates from the tree
        #run the algorythm to map competitors into the tree
        # description of how to add a new column to an existing dataframe https://www.geeksforgeeks.org/adding-new-column-to-existing-dataframe-in-pandas/


        # set the cwd to the project root
        # path = os.getcwd()
        new_path = Path(__file__).resolve().parents[2]
        os.chdir(new_path)

        the_competitors = Competitors(TEST_DATA, columns=TEST_DATA_COLUMNS)  # create a list of competitors from the test data above

        # setup an 8 person tree
        test_file_name = "reports//sparring_tree//testoutput//8PersonTree_full_page.pdf"
        test_canvas = canvas.Canvas(test_file_name)
        tree = NewEightCompetitorTree(test_canvas, test_file_name)

        # draw the competitors onto the tree
        tree.add_page_with_competitors_on_tree(1, "2:00", "Boys Sparring",  "10-12","White - Yellow", "A-Z", the_competitors)

        # save the file
        test_canvas.save()

        # test to see if the PDF file was created
        self.assertTrue(os.path.exists(test_file_name))
        if REMOVE_TEST_FILES:
            os.remove(test_file_name)


if __name__ == '__main__':
    unittest.main()
