""" this module contains code to create a 16 person sparring tree"""

from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.units import cm

from reportlab.pdfgen import canvas

from reporting.sparring_tree import bracket_position_map as BPM
from reporting.sparring_tree.competitors import Competitors
from reporting.sparring_tree.base_sparring_tree import SparringTree

class SixteenCompetitorTree(SparringTree):
    """ Creates a 16 compettitor sparring tree"""

    # setup a couple of constants for this tree
    _OFFSET_BETWEEN_BRANCHES_ON_TREE = 2.4
    _SPACE_BELOW_TEXT = 0.1  # centimeters

    def __init__(self, the_canvas):
        """ sets up instance variables for this tree """
        SparringTree.__init__(self, the_canvas)

        self._c.setPageSize(landscape(letter))  # defaults to 72 pointer per inch
        self.initialize_text_coordinates()

    def initialize_text_coordinates(self):
        '''initialize the text coordinates, two columns of x,y coordinate of where names gets drawn'''

        # calculate first column text coordinates top of the page to the bottom
        self._first_column_text_coordinates = []
        initial_first_column_text_coords = [[.8, 19.4 + self._SPACE_BELOW_TEXT],
                                            [.8, 18.2 + self._SPACE_BELOW_TEXT]]
        for i in range(8):
            offset = self.truncate(i * self._OFFSET_BETWEEN_BRANCHES_ON_TREE, 1)
            # removed truncation because it caused problems with the numbers on a 16 person tree
            # for some reason rounding caused the 15th person ended up 1 pixel off
            # self._first_column_text_coordinates.append([initial_first_column_text_coords[0][0],
            #                                             self.truncate(initial_first_column_text_coords[0][1] - offset,
            #                                                           1)])
            # self._first_column_text_coordinates.append([initial_first_column_text_coords[1][0],
            #                                             self.truncate(initial_first_column_text_coords[1][1] - offset,
            #                                                           1)])
            self._first_column_text_coordinates.append([initial_first_column_text_coords[0][0],
                                                        initial_first_column_text_coords[0][1] - offset])
            self._first_column_text_coordinates.append([initial_first_column_text_coords[1][0],
                                                        initial_first_column_text_coords[1][1] - offset])

            #print("0,{},{}, {}".format(initial_first_column_text_coords[0][1],offset,initial_first_column_text_coords[0][1] - offset))
            #print("1,{},{}, {}".format(initial_first_column_text_coords[1][1],offset,initial_first_column_text_coords[1][1] - offset))


        self._second_column_text_coordinates = []
        initial_second_column_text_coords = [7.2, 18.8 + self._SPACE_BELOW_TEXT]
        for i in range(8):
            offset = self.truncate(i * self._OFFSET_BETWEEN_BRANCHES_ON_TREE, 1)
            self._second_column_text_coordinates.append(
                [initial_second_column_text_coords[0], self.truncate(initial_second_column_text_coords[1] - offset, 1)])
        i = 0

    def draw_box(self, left, top):
        ''' draw a single checkbox at the coordinates provided '''
        top = top + 1
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
        for i in range(8):
            offset = i * self._OFFSET_BETWEEN_BRANCHES_ON_TREE
            self._path.moveTo(.8 * cm, (1.4 + offset) * cm)  # .8 centimeters to the right, (1 + offset) centimeters up
            self._path.lineTo(6.2 * cm, (1.4 + offset) * cm)
            self._path.lineTo(7.1 * cm, (2 + offset) * cm)
            self._path.lineTo(6.2 * cm, (2.6 + offset) * cm)
            self._path.lineTo(.8 * cm, (2.6 + offset) * cm)
            self.draw_boxes(1.5, 1.4 + offset)
            self.draw_boxes(1.5, 2.6 + offset)

        # second bracket
        for i in range(4):
            offset = i * self._OFFSET_BETWEEN_BRANCHES_ON_TREE * 2
            self._path.moveTo(7.1 * cm, (2 + offset) * cm)  # 7.2 centimeters to the right, (2 + offset) centimeters up
            self._path.lineTo(12.6 * cm, (2 + offset) * cm)
            self._path.lineTo(13.3 * cm, (3.2 + offset) * cm)
            self._path.lineTo(12.6 * cm, (4.4 + offset) * cm)
            self._path.lineTo(7.1 * cm, (4.4 + offset) * cm)
            self.draw_boxes(7.5, 2 + offset)
            self.draw_boxes(7.5, 4.4 + offset)

        # third bracket
        for i in range(2):
            offset = i * self._OFFSET_BETWEEN_BRANCHES_ON_TREE * 4
            self._path.moveTo(13.3 * cm, (3.2 + offset) * cm)  # 13.3 centimeters to the right, (3.2 + offset) centimeters up
            self._path.lineTo(18.7 * cm, (3.2 + offset) * cm)
            self._path.lineTo(20.1 * cm, (5.6 + offset) * cm)
            self._path.lineTo(18.7 * cm, (8 + offset) * cm)
            self._path.lineTo(13.3 * cm, (8 + offset) * cm)
            self.draw_boxes(14, 3.2 + offset)
            self.draw_boxes(14, 8 + offset)

        # fourth bracket
        self._path.moveTo(20.1 * cm, 5.6 * cm)  # 20.1 centimeters to the right, 5.6 centimeters up
        self._path.lineTo(25.5 * cm, 5.6 * cm)
        self._path.lineTo(27 * cm, 10.4 * cm)
        self._path.lineTo(25.5 * cm, 15.2 * cm)
        self._path.lineTo(20.1 * cm, 15.2 * cm)
        self.draw_boxes(21, 5.6)
        self.draw_boxes(21, 15.2)

        # winner line
        self._path.moveTo(20.1 * cm, 10.4 * cm)  # 20.1 centimeters to the right, 10.4 centimeters up
        self._path.lineTo(27 * cm, 10.4 * cm)

    def draw_header_info_on_tree(self, ring: int, event_time: str, event_title: str, ranks: str):
        ''' draw the header text onto the tree '''
        self._c.drawString(20 * cm, 20.5 * cm, "Time:")
        self._c.drawString(21.5 * cm, 20.5 * cm, event_time)
        self._c.drawString(20 * cm, 19.75 * cm, "Event:")
        self._c.drawString(21.5 * cm, 19.75 * cm, event_title)
        self._c.drawString(20 * cm, 19 * cm, "Rank:")
        self._c.drawString(21.5 * cm, 19 * cm, ranks)
        self._c.drawString(20 * cm, 18.25 * cm, "Ring#:")
        self._c.drawString(21.5 * cm, 18.25 * cm, str(ring))

    def draw_competitors_on_tree(self, competitors: Competitors) -> object:
        ''' draw the competitors on the tree '''
        # print(competitors)

        competitor_count = competitors.get_number_of_competitors()
        if competitor_count > 16:
            print("*** Something is wrong! we have {} competitors for an 16 person tree".format(competitor_count))
            competitor_count = 16
        i = 0
        for index, competitor in competitors.iterrows():
            name = competitor['First_Name'] + ' ' + competitor['Last_Name']
            # print('\n' + name)
            px, py = self.calculate_canvas_coordinates_from_competitor_index(competitor_count, i)
            self._c.drawString(px, py, name)
            self._c.setFont("Courier", 7)
            dojo = competitor['Dojo']
            if dojo.startswith('CO- '):
                dojo = dojo[4:]
            dojo_weight_height = "{} {}\' {}\" {} lbs".format(dojo, competitor['Feet'], competitor['Inches'],
                                                              competitor['Weight'])
            self._c.drawString(px + (0.0 * cm), py + (.4 * cm), dojo_weight_height)
            self._c.setFont("Helvetica", 12)
            i = i + 1
            assert i < 17, "Should be no more than 16 competitors on an 16 person tree"


if __name__ == '__main__':
    ''' Very simple test try to create a tree and check that the file exists '''
    c = canvas.Canvas("16PersonTree.pdf", pagesize=letter)  # defaults to 72 pointer per inch
    tree = SixteenCompetitorTree(c)
    tree.draw_static_template()
    tree.close()
    c.save()
    import os

    if os.path.exists("16PersonTree.pdf"):
        print("It worked")
