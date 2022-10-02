""" this module contains code to base sparring tree"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import cm

from reportlab.pdfgen import canvas

from reports.sparring_tree import bracket_position_map as BPM
from domain_model.competitors import Competitors


class SparringTree():
    """ Creates an empty compettitor sparring tree"""

    # setup a couple of constants for this tree
    _OFFSET_BETWEEN_BRANCHES_ON_TREE = 4.8
    _SPACE_BELOW_TEXT = 0.1

    _c = None
    _path = None

    _first_column_text_coordinates = None
    _second_column_text_coordinates = None

    def __init__(self, the_canvas, the_source_filename):
        """ sets up instance variables for this tree """
        self._c = the_canvas
        self._c.setPageSize(letter)  # defaults to 72 pointer per inch
        self._path = self._c.beginPath()
        self.initialize_text_coordinates()
        self.source_filename = the_source_filename

    def close(self):
        """ generate the page"""
        self._c.drawPath(self._path, stroke=1, fill=0)
        self._c.showPage()

    def truncate(self, number, decimal_places=0):
        ''' utility funciton to truncate a number to a given number of decimal places'''
        multiplier = 10 ** decimal_places
        return int(number * multiplier) / multiplier

    def initialize_text_coordinates(self):
        '''initialize the text coordinates, two columns of x,y coordinate of where names gets drawn'''
        # calculate first column text coordinates top of the page to the bottom
        self._first_column_text_coordinates = []
        self._second_column_text_coordinates = []

    def get_canvas_coord_for_nth_competitor_in_column1(self, competitor_index):
        '''returns the x,y coordinates on the canvas for the given competitor index
        for example the 2nd compettitor in column 1 will be placed at x,y on the canvas '''
        px, py = self._first_column_text_coordinates[competitor_index]
        return self._first_column_text_coordinates[competitor_index]

    def get_canvas_coord_for_nth_competitor_in_column2(self, competitor_index):
        '''returns the x,y coordinates on the canvas for the given competitor index
        for example the 2nd compettitor in column 2 will be placed at x,y on the canvas '''
        return self._second_column_text_coordinates[competitor_index]

    def calculate_canvas_coordinates_from_competitor_index(self, competitor_count: int, competitor_index: int):
        ''' calculates the canvas coordinates (physical x,s) for a competitor based on how many competitors there are
         and what this competitor place in at list '''
        # print(competitor_index)
        column, row = BPM.calculate_bracket_position_from_competitor_index(competitor_count, competitor_index)
        #print('backet coordinate: ', column, row)
        if column == 1:
            x_coordinate, y_coordinate = self.get_canvas_coord_for_nth_competitor_in_column1(row - 1)
        else:
            x_coordinate, y_coordinate = self.get_canvas_coord_for_nth_competitor_in_column2(row - 1)
        x_coordinate = x_coordinate * cm
        y_coordinate = y_coordinate * cm
        #print('canvas coordinate, {}, {} '.format(x_coordinate, y_coordinate))
        return x_coordinate, y_coordinate


    def add_page_with_competitors_on_tree(self, ring: int, event_time: str, event_title: str, ranks, split_label:str, competitors: Competitors) -> object:
        ''' adds a compleate page with a tree and the competitors '''

        if competitors.get_number_of_competitors() > 20:
            print("*** Warning: {} {} Ring:{} has too many competitors".format(event_time,event_title,ring))

        # lay down the template
        self.draw_static_template()

        # lay down the header info
        self.draw_header_info_on_tree(ring, event_time, event_title, ranks, split_label, competitors.get_number_of_competitors())

        # arrange the competitors for sparring
        ordered_competitors=competitors.arrange_competitors_for_sparring()

        # draw the competitors onto the tree
        self.draw_competitors_on_tree(ordered_competitors)

        # close the tree - causes the page to be written
        self.close()


if __name__ == '__main__':
    ''' Very simple test try to create a tree and check that the file exists '''
    c = canvas.Canvas("BlankTree.pdf", pagesize=letter)  # defaults to 72 pointer per inch
    tree = SparringTree(c)
    tree.draw_static_template()
    tree.close()
    c.save()
    import os

    if os.path.exists("BlankTree.pdf"):
        print("It worked")
