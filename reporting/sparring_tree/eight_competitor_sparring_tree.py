""" this module contains code to create an 8 person sparring tree"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import cm

from reportlab.pdfgen import canvas

from reporting.sparring_tree import bracket_position_map as BPM
from reporting.sparring_tree.competitors import Competitors
from reporting.sparring_tree.base_sparring_tree import SparringTree

class EightCompetitorTree(SparringTree):
    """ Creates an 8 compettitor sparring tree"""

    # setup a couple of constants for this tree
    _OFFSET_BETWEEN_BRANCHES_ON_TREE = 4.8
    _SPACE_BELOW_TEXT = 0.1

    _c = None
    _path = None

    _first_column_text_coordinates = None
    _second_column_text_coordinates = None

    def __init__(self, the_canvas):
        """ sets up instance variables for this tree """
        SparringTree.__init__(self, the_canvas)
        self._c.setPageSize(letter)  # defaults to 72 pointer per inch
        self.initialize_text_coordinates()

    def initialize_text_coordinates(self):
        '''initialize the text coordinates, two columns of x,y coordinate of where names gets drawn'''

        # calculate first column text coordinates top of the page to the bottom
        self._first_column_text_coordinates = []
        initial_first_column_text_coords = [[.9, 20.4 + self._SPACE_BELOW_TEXT],
                                            [.9, 18.2 + self._SPACE_BELOW_TEXT]]
        for i in range(4):
            offset = self.truncate(i * self._OFFSET_BETWEEN_BRANCHES_ON_TREE, 1)
            self._first_column_text_coordinates.append([initial_first_column_text_coords[0][0],
                                                        self.truncate(initial_first_column_text_coords[0][1] - offset,
                                                                      1)])
            self._first_column_text_coordinates.append([initial_first_column_text_coords[1][0],
                                                        self.truncate(initial_first_column_text_coords[1][1] - offset,
                                                                      1)])

        self._second_column_text_coordinates = []
        initial_second_column_text_coords = [7.2, 19.4 + self._SPACE_BELOW_TEXT]
        for i in range(4):
            offset = self.truncate(i * self._OFFSET_BETWEEN_BRANCHES_ON_TREE, 1)
            self._second_column_text_coordinates.append(
                [initial_second_column_text_coords[0], self.truncate(initial_second_column_text_coords[1] - offset, 1)])
        i = 0

    def draw_box(self, left, top):
        ''' draw a single checkbox at the coordinates provided '''
        self._path.moveTo(left * cm, top * cm)
        self._path.lineTo((left - .3) * cm, (top * cm))
        self._path.lineTo((left - .3) * cm, (top - .3) * cm)
        self._path.lineTo(left * cm, (top - .3) * cm)
        self._path.lineTo(left * cm, top * cm)

    def draw_boxes(self, left, top):
        ''' draw checkboxes at the coordinates provides to keep track of scores '''
        self.draw_box(left, top)
        self.draw_box(left + .8, top)
        self.draw_box(left + 1.6, top)

    def draw_static_template(self):
        """ Draws the static template portion of the tree"""
        # First bracket
        for i in range(4):
            offset = i * self._OFFSET_BETWEEN_BRANCHES_ON_TREE
            self._path.moveTo(.8 * cm, (3.8 + offset) * cm)  # 3/4 inch to the right, 1.5 inches up
            self._path.lineTo(6 * cm, (3.8 + offset) * cm)
            self._path.lineTo(7.2 * cm, (5 + offset) * cm)
            self._path.lineTo(6 * cm, (6 + offset) * cm)
            self._path.lineTo(.8 * cm, (6 + offset) * cm)
            self.draw_boxes(1.5, 5.3 + offset)  # 9/16 inches to the right and 2.125 inches up
            self.draw_boxes(1.5, 7.5 + offset)  # 9/16 inches to the right and 4 inches up

        # Second bracket
        for i in range(2):
            offset = i * (self._OFFSET_BETWEEN_BRANCHES_ON_TREE * 2)
            self._path.moveTo(7.2 * cm, (5 + offset) * cm)  # 2.75 inch to the right, 2 inches up
            self._path.lineTo(12.4 * cm, (5 + offset) * cm)
            self._path.lineTo(15.2 * cm, (7.5 + offset) * cm)
            self._path.lineTo(12.4 * cm, (9.8 + offset) * cm)
            self._path.lineTo(7.2 * cm, (9.8 + offset) * cm)
            self.draw_boxes(7.5, 6.4 + offset)  # 9/16 inches to the right and 4 inches up
            self.draw_boxes(7.5, 11.3 + offset)  # 9/16 inches to the right and 4 inches up

        # third bracket
        self._path.moveTo(15.2 * cm, 7.5 * cm)  # 2.9375 inch to the right, 6 inches up
        self._path.lineTo(20.4 * cm, 7.5 * cm)
        self._path.moveTo(15.2 * cm, 17.1 * cm)
        self._path.lineTo(20.4 * cm, 17.1 * cm)

        self.draw_boxes(15.5, 9)  # 9/16 inches to the right and 4 inches up
        self.draw_boxes(15.5, 18.7)  # 9/16 inches to the right and 4 inches up

    def draw_header_info_on_tree(self, ring: int, event_time: str, event_title: str, ranks: str):
        ''' draw the header text onto the tree '''
        self._c.drawString(13 * cm, 26.5 * cm, "Time:")
        self._c.drawString(14.5 * cm, 26.5 * cm, event_time)
        self._c.drawString(13 * cm, 25.75 * cm, "Event:")
        self._c.drawString(14.5 * cm, 25.75 * cm, event_title)
        self._c.drawString(13 * cm, 25 * cm, "Rank:")
        self._c.drawString(14.5 * cm, 25 * cm, ranks)
        self._c.drawString(13 * cm, 24.25 * cm, "Ring#:")
        self._c.drawString(14.5 * cm, 24.25 * cm, str(ring))

    def draw_competitors_on_tree(self, competitors: Competitors) -> object:
        ''' draw the competitors on the tree '''
        # print(competitors)

        competitor_count = competitors.get_number_of_competitors()
        if competitor_count > 8:
            print("*** Something is wrong! we have {} competitors for an 8 person tree".format(competitor_count))
            competitor_count = 8
        i = 0
        for index, competitor in competitors.iterrows():
            name = competitor['First_Name'] + ' ' + competitor['Last_Name']
            # print('\n' + name)
            px, py = self.calculate_canvas_coordinates_from_competitor_index(competitor_count, i)
            self._c.drawString(px, py, name)
            i = i + 1
            assert i < 9,  "Should be no more than 8 competitors on an 8 person tree"

if __name__ == '__main__':
    ''' Very simple test try to create a tree and check that the file exists '''
    c = canvas.Canvas("8PersonTree.pdf", pagesize=letter)  # defaults to 72 pointer per inch
    tree = EightCompetitorTree(c)
    tree.draw_static_template()
    tree.close()
    c.save()
    import os

    if os.path.exists("8PersonTree.pdf"):
        print("It worked")
