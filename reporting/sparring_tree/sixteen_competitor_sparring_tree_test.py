'''
This module tests the sixteen_compettitor_tree module
to run this test go to the main directory and run
nosetests --with-coverage
'''''

import unittest
import os
from reportlab.pdfgen import canvas
from reporting.sparring_tree.sixteen_competitor_sparring_tree import SixteenCompetitorTree
from reporting.sparring_tree.competitors import Competitors

REMOVE_TEST_FILES = False

# from eight_competitor_tree import SixteenCompetitorTree
# import eight_competitor_tree

# data for the tests
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
              '2 Events - Forms & Sparring ($75)', 'Weapons ($35)', 0)]

SIXTEEN_NAMES = ["One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight",
                 "Nine", "Ten", "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen"]


class TestSixteenCompetitorTree(unittest.TestCase):
    ''' class to test the SixteenCompettitorTree code'''

    def setUp(self):
        ''' create a directory for all the test reports'''
        try:
            os.mkdir("testoutput")
        except:
            print("exptedted error")
        return

    def test_creating_a_file(self):
        ''' simple test to make sure we can create a file with the template code in it'''
        test_file_name = "testoutput//16PersonTree_Create_File.pdf"
        test_canvas = canvas.Canvas(test_file_name)
        tree = SixteenCompetitorTree(test_canvas)
        tree.draw_static_template()
        tree.close()
        test_canvas.save()

        # test to see if the PDF file was created
        self.assertTrue(os.path.exists(test_file_name))
        if REMOVE_TEST_FILES:
            os.remove(test_file_name)

    def test_creating_a_file_with_two_tree(self):
        ''' tests that we can create a PDF with multiple sparring trees in it'''
        test_file_name = "testoutput//16PersonTree_Two_Trees.pdf"
        test_canvas = canvas.Canvas(test_file_name)
        tree = SixteenCompetitorTree(test_canvas)

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
        test_file_name = "testoutput//16PersonTree_Init_Text_Coords.pdf"
        test_canvas = canvas.Canvas(test_file_name)
        tree = SixteenCompetitorTree(test_canvas)
        self.assertTrue(len(tree._first_column_text_coordinates) == 16)
        self.assertTrue(len(tree._second_column_text_coordinates) == 8)

        # draw the tree just for the heck of it
        tree.draw_static_template()
        tree.close()
        test_canvas.save()
        # test to see if the PDF file was created
        self.assertTrue(os.path.exists(test_file_name))
        if REMOVE_TEST_FILES:
            os.remove(test_file_name)

    def draw_n_names_on_tree(self, names: list, test_file_name: str):
        ''' tests to make sure the names in a 16 person tree get put in the right place'''
        print("\nDrawing {} ".format(test_file_name))
        # setup a 16 person tree
        test_canvas = canvas.Canvas(test_file_name)
        tree = SixteenCompetitorTree(test_canvas)
        tree.draw_static_template()

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

    def test_draw_16_names_on_tree(self):
        ''' tests to make sure the names in a 16 person tree get put in the right place'''
        names = SIXTEEN_NAMES
        self.draw_n_names_on_tree(names, "testoutput//16PeopleOn16PersonTree.pdf")

    def test_draw_15_names_on_tree(self):
        ''' tests to make sure the names in a 16 person tree get put in the right place'''
        names = SIXTEEN_NAMES[0:15]
        self.draw_n_names_on_tree(names, "testoutput//15PeopleOn16PersonTree.pdf")

    def test_draw_14_names_on_tree(self):
        ''' tests to make sure the names in a 16 person tree get put in the right place'''
        names = SIXTEEN_NAMES[0:14]
        self.draw_n_names_on_tree(names, "testoutput//14PeopleOn16PersonTree.pdf")

    def test_draw_13_names_on_tree(self):
        ''' tests to make sure the names in a 16 person tree get put in the right place'''
        names = SIXTEEN_NAMES[0:13]
        self.draw_n_names_on_tree(names, "testoutput//13PeopleOn16PersonTree.pdf")

    def test_draw_12_names_on_tree(self):
        ''' tests to make sure the names in a 16 person tree get put in the right place'''
        names = SIXTEEN_NAMES[0:12]
        self.draw_n_names_on_tree(names, "testoutput//12PeopleOn16PersonTree.pdf")

    def test_draw_11_names_on_tree(self):
        ''' tests to make sure the names in a 16 person tree get put in the right place'''
        names = SIXTEEN_NAMES[0:11]
        self.draw_n_names_on_tree(names, "testoutput//11PeopleOn16PersonTree.pdf")

    def test_draw_10_names_on_tree(self):
        ''' tests to make sure the names in a 16 person tree get put in the right place'''
        names = SIXTEEN_NAMES[0:10]
        self.draw_n_names_on_tree(names, "testoutput//10PeopleOn16PersonTree.pdf")

    def test_draw_9_names_on_tree(self):
        ''' tests to make sure the names in a 16 person tree get put in the right place'''
        names = SIXTEEN_NAMES[0:9]
        self.draw_n_names_on_tree(names, "testoutput//9PeopleOn16PersonTree.pdf")

    def test_draw_8_names_on_tree(self):
        ''' tests to make sure the names in a 16 person tree get put in the right place'''
        names = SIXTEEN_NAMES[0:8]
        self.draw_n_names_on_tree(names, "testoutput//8PeopleOn16PersonTree.pdf")

    def test_draw_7_names_on_tree(self):
        ''' tests to make sure the names in a 16 person tree get put in the right place'''
        names = SIXTEEN_NAMES[0:7]
        self.draw_n_names_on_tree(names, "testoutput//7PeopleOn16PersonTree.pdf")

    def test_draw_6_names_on_tree(self):
        ''' tests to make sure the names in a 16 person tree get put in the right place'''
        names = SIXTEEN_NAMES[0:6]
        self.draw_n_names_on_tree(names, "testoutput//6PeopleOn16PersonTree.pdf")

    def test_draw_5_names_on_tree(self):
        names = SIXTEEN_NAMES[0:5]
        self.draw_n_names_on_tree(names, "testoutput//5PeopleOn16PersonTree.pdf")

    def test_draw_4_names_on_tree(self):
        ''' tests to make sure the names in a 16 person tree get put in the right place'''
        names = SIXTEEN_NAMES[0:4]
        self.draw_n_names_on_tree(names, "testoutput//4PeopleOn16PersonTree.pdf")

    def test_draw_3_names_on_tree(self):
        ''' tests to make sure the names in a 16 person tree get put in the right place'''
        names = SIXTEEN_NAMES[0:3]
        self.draw_n_names_on_tree(names, "testoutput//3PeopleOn16PersonTree.pdf")

    def test_draw_2_names_on_tree(self):
        ''' tests to make sure the names in a 16 person tree get put in the right place'''
        names = SIXTEEN_NAMES[0:2]
        self.draw_n_names_on_tree(names, "testoutput//2PeopleOn16PersonTree.pdf")

    def test_draw_1_names_on_tree(self):
        ''' tests to make sure the names in a 16 person tree get put in the right place'''
        names = SIXTEEN_NAMES[0:1]
        self.draw_n_names_on_tree(names, "testoutput//1PeopleOn16PersonTree.pdf")

    def test_draw_competitors_on_tree(self):
        ''' tests that we each compettitor gets assigned physical coordinates '''
        # create compettitors from our test data
        # get the first and second column test coordinates from the tree
        # run the algorythm to map compettitors into the tree
        # description of how to add a new column to an existing dataframe https://www.geeksforgeeks.org/adding-new-column-to-existing-dataframe-in-pandas/
        the_competitors = Competitors(TEST_DATA,
                                      columns=TEST_DATA_COLUMNS)  # create a list of competitors from the test data above

        # setup a 16 person tree
        test_file_name = "testoutput//16PersonTree_from_competitors.pdf"
        test_canvas = canvas.Canvas(test_file_name)
        tree = SixteenCompetitorTree(test_canvas)
        tree.draw_static_template()

        # draw the competitors onto the tree
        tree.draw_competitors_on_tree(the_competitors)

        # close out the 16 person tree
        tree.close()
        test_canvas.save()

        # test to see if the PDF file was created
        self.assertTrue(os.path.exists(test_file_name))
        if REMOVE_TEST_FILES:
            os.remove(test_file_name)

    def test_add_page_with_competitors_on_tree(self):
        ''' tests that we each compettitor gets assigned physical coordinates '''
        # create compettitors from our test data
        # get the first and second column test coordinates from the tree
        # run the algorythm to map compettitors into the tree
        # description of how to add a new column to an existing dataframe https://www.geeksforgeeks.org/adding-new-column-to-existing-dataframe-in-pandas/
        the_competitors = Competitors(TEST_DATA,
                                      columns=TEST_DATA_COLUMNS)  # create a list of competitors from the test data above

        # setup a 16 person tree
        test_file_name = "testoutput//16PersonTree_full_page.pdf"
        test_canvas = canvas.Canvas(test_file_name)
        tree = SixteenCompetitorTree(test_canvas)

        # draw the competitors onto the tree
        tree.add_page_with_competitors_on_tree(1, "2:00", "Sr. Mens Sparring", "Black", the_competitors)

        # save the file
        test_canvas.save()

        # test to see if the PDF file was created
        self.assertTrue(os.path.exists(test_file_name))
        if REMOVE_TEST_FILES:
            os.remove(test_file_name)


if __name__ == '__main__':
    unittest.main()
