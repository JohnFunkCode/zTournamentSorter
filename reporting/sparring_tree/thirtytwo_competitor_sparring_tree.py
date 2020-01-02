""" this module contains code to create a 32 person sparring tree"""

from reportlab.lib.pagesizes import legal
from reportlab.lib.units import cm

from reportlab.pdfgen import canvas

from reporting.sparring_tree.competitors import Competitors
from reporting.sparring_tree.base_sparring_tree import SparringTree


class ThirtyTwoCompetitorTree(SparringTree):
    """ Creates a 32 compettitor sparring tree"""

    # setup a couple of constants for this tree
    _OFFSET_BETWEEN_BRANCHES_ON_TREE = 2
    _SPACE_BELOW_TEXT = 0.1  # centimeters

    def __init__(self, the_canvas):
        SparringTree.__init__(self, the_canvas)

        """ sets up instance variables for this tree """
        self._c.setPageSize(legal)  # defaults to 72 pointer per inch
        self.initialize_text_coordinates()

    def initialize_text_coordinates(self):
        '''initialize the text coordinates, two columns of x,y coordinate of where names gets drawn'''

        # calculate first column text coordinates top of the page to the bottom
        self._first_column_text_coordinates = []
        initial_first_column_text_coords = [[.5, 32.5 + self._SPACE_BELOW_TEXT],
                                            [.5, 31.5 + self._SPACE_BELOW_TEXT]]
        for i in range(16):
            offset = self.truncate(i * self._OFFSET_BETWEEN_BRANCHES_ON_TREE, 1)
            self._first_column_text_coordinates.append([initial_first_column_text_coords[0][0],
                                                        self.truncate(initial_first_column_text_coords[0][1] - offset,
                                                                      1)])
            self._first_column_text_coordinates.append([initial_first_column_text_coords[1][0],
                                                        self.truncate(initial_first_column_text_coords[1][1] - offset,
                                                                      1)])

        self._second_column_text_coordinates = []
        initial_second_column_text_coords = [5.1, 32 + self._SPACE_BELOW_TEXT]
        for i in range(16):
            offset = self.truncate(i * self._OFFSET_BETWEEN_BRANCHES_ON_TREE, 1)
            self._second_column_text_coordinates.append(
                [initial_second_column_text_coords[0], self.truncate(initial_second_column_text_coords[1] - offset, 1)])
        i = 0

    def draw_box(self, left, top):
        ''' draw a single checkbox at the coordinates provided '''
        top = top + .8
        self._path.moveTo(left * cm, top * cm)
        self._path.lineTo((left - .2) * cm, (top * cm))
        self._path.lineTo((left - .2) * cm, (top - .2) * cm)
        self._path.lineTo(left * cm, (top - .2) * cm)
        self._path.lineTo(left * cm, top * cm)

    def draw_boxes(self, left, top):
        ''' draw checkboxes at the coordinates provides to keep track of scores '''
        self.draw_box(left, top)
        self.draw_box(left + .3, top)
        self.draw_box(left + .6, top)

    def draw_static_template(self):  # TBD - paused here!!!!
        """ Draws the static template portion of the tree"""

        # first bracket
        for i in range(16):
            offset = i * 2
            self._path.moveTo(.5 * cm, (1.5 + offset) * cm)  # .5 centimeters right, (1.6 + offset) centimeters up
            self._path.lineTo(4.5 * cm, (1.5 + offset) * cm)
            self._path.lineTo(5.1 * cm, (2 + offset) * cm)
            self._path.lineTo(4.5 * cm, (2.5 + offset) * cm)
            self._path.lineTo(.5 * cm, (2.5 + offset) * cm)
            self.draw_boxes(1.5, 1.5 + offset)
            self.draw_boxes(1.5, 2.5 + offset)

        # second bracket
        for i in range(8):
            offset = i * 4
            self._path.moveTo(5.1 * cm, (2 + offset) * cm)  # 5.1 centimeters right, (2 + offset) centimeters up
            self._path.lineTo(9 * cm, (2 + offset) * cm)
            self._path.lineTo(10.1 * cm, (3 + offset) * cm)
            self._path.lineTo(9 * cm, (4 + offset) * cm)
            self._path.lineTo(5.1 * cm, (4 + offset) * cm)
            self.draw_boxes(6, 2 + offset)
            self.draw_boxes(6, 4 + offset)

        # third bracket
        for i in range(4):
            offset = i * 8
            self._path.moveTo(10.1 * cm, (3 + offset) * cm)  # 13.3 centimeters right, (3 + offset) centimeters up
            self._path.lineTo(14.1 * cm, (3 + offset) * cm)
            self._path.lineTo(15.5 * cm, (5 + offset) * cm)
            self._path.lineTo(14.1 * cm, (7 + offset) * cm)
            self._path.lineTo(10.1 * cm, (7 + offset) * cm)
            self.draw_boxes(11, 3 + offset)
            self.draw_boxes(11, 7 + offset)

        # forth bracket
        for i in range(2):
            offset = i * 16
            self._path.moveTo(15.5 * cm, (5 + offset) * cm)  # 15.5 centimeters right, (5 + offset) centimeters up
            self._path.lineTo(19.3 * cm, (5 + offset) * cm)
            self._path.lineTo(20.5 * cm, (9 + offset) * cm)
            self._path.lineTo(19.3 * cm, (13 + offset) * cm)
            self._path.lineTo(15.5 * cm, (13 + offset) * cm)
            self.draw_boxes(16, 5 + offset)
            self.draw_boxes(16, 13 + offset)

        # fifth bracket
        offset = 0
        self._path.moveTo(15.5 * cm, 9 * cm)  # 20.1 centimeters right, 5.2 centimeters up
        self._path.lineTo(20.5 * cm, 9 * cm)
        self._path.moveTo(15.5 * cm, 25 * cm)  # 20.1 centimeters right, 5.2 centimeters up
        self._path.lineTo(20.5 * cm, 25 * cm)
        self.draw_boxes(16, 9)
        self.draw_boxes(16, 25)

        # winner line
        # self._path.moveTo(20.1 * cm, 9.4 * cm)  # 20.1 centimeters to the right, 9.4 centimeters up
        # self._path.lineTo(27 * cm, 9.4 * cm)

    def draw_header_info_on_tree(self, ring: int, event_time: str, event_title: str, ranks: str):
        ''' draw the header text onto the tree '''
        self._c.drawString(16 * cm, 34.5 * cm, "Time:")
        self._c.drawString(17.5 * cm, 34.5 * cm, event_time)
        self._c.drawString(16 * cm, 33.75 * cm, "Event:")
        self._c.drawString(17.5 * cm, 33.75 * cm, event_title)
        self._c.drawString(16 * cm, 33 * cm, "Rank:")
        self._c.drawString(17.5 * cm, 33 * cm, ranks)
        self._c.drawString(16 * cm, 32.25 * cm, "Ring#:")
        self._c.drawString(17.5 * cm, 32.25 * cm, str(ring))

    def draw_competitors_on_tree(self, competitors: Competitors) -> object:
        ''' draw the competitors on the tree '''
        # print(competitors)

        competitor_count = competitors.get_number_of_competitors()
        if competitor_count > 32:
            print("*** Something is wrong! we have {} competitors for an 32 person tree".format(competitor_count))
            competitor_count = 32
        i = 0
        for index, competitor in competitors.iterrows():
            name = competitor['First_Name'] + ' ' + competitor['Last_Name']
            # print('\n' + name)
            px, py = self.calculate_canvas_coordinates_from_competitor_index(competitor_count, i)
            self._c.drawString(px, py, name)
            i = i + 1
            assert i < 33, "Should be no more than 16 competitors on an 16 person tree"


if __name__ == '__main__':
    ''' Very simple test try to create a tree and check that the file exists '''
    c = canvas.Canvas("16PersonTree.pdf", pagesize=legal)  # defaults to 72 pointer per inch
    tree = ThirtyTwoCompetitorTree(c)
    tree.draw_static_template()
    tree.close()
    c.save()
    import os

    if os.path.exists("16PersonTree.pdf"):
        print("It worked")
