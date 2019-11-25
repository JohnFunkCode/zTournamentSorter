""" this module contains code to create an 8 person sparring tree"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import cm

from reportlab.pdfgen import canvas

from reporting.sparring_tree import bracket_position_map as BPM
from reporting.sparring_tree.competitor_to_tree_mapper import CompetitorsToTreeMapper

C_STUFF = CompetitorsToTreeMapper()


class EightCompetitorTree():
    """ Creates an 8 compettitor sparring tree"""

    # setup a couple of constants for this tree
    _OFFSET_BETWEEN_BRANCHES_ON_TREE = 4.8
    _SPACE_BELOW_TEXT = 0.1

    _c = None
    _path = None

    _first_column_text_coordinates = None
    _second_column_text_coordinates = None

    def __init__(self, canvas):
        """ sets up instance variables for this tree """
        self._c = canvas
        self._c.setPageSize(letter)  # defaults to 72 pointer per inch
        self._path = self._c.beginPath()
        # print(self._c.__dict__)
        print('EightCompetitorTree initialized with filename:' + self._c.__dict__['_filename'])
        self.initialize_text_coordinates()

    def close(self):
        """ generate the page"""
        self._c.drawPath(self._path, stroke=1, fill=0)
        self._c.showPage()

    def truncate(self, n, decimals=0):
        multiplier = 10 ** decimals
        return int(n * multiplier) / multiplier

    def initialize_text_coordinates(self):
        '''initialize the text coordinates, two columns of x,y coordinate of where names gets drawn'''

        # calculate first column text coordinates top of the page to the bottom
        self._first_column_text_coordinates = []
        initial_first_column_text_coords = [[.9, 20.4 + self._SPACE_BELOW_TEXT],
                                            [.9, 18.2 + self._SPACE_BELOW_TEXT]]
        for i in range(4):
            offset = self.truncate(i * self._OFFSET_BETWEEN_BRANCHES_ON_TREE, 1)
            self._first_column_text_coordinates.append([initial_first_column_text_coords[0][0],
                                                        self.truncate(initial_first_column_text_coords[0][1] - offset, 1)])
            self._first_column_text_coordinates.append([initial_first_column_text_coords[1][0],
                                                        self.truncate(initial_first_column_text_coords[1][1] - offset, 1)])

        self._second_column_text_coordinates = []
        initial_second_column_text_coords = [7.2, 19.4 + self._SPACE_BELOW_TEXT]
        for i in range(4):
            offset = self.truncate(i * self._OFFSET_BETWEEN_BRANCHES_ON_TREE, 1)
            self._second_column_text_coordinates.append(
                [initial_second_column_text_coords[0], self.truncate(initial_second_column_text_coords[1] - offset, 1)])
        i = 0

    def get_canvas_coord_for_nth_competitor_in_column1(self, competitor_index):
        '''returns the x,y coordinates on the canvas for the given competitor index
        for example the 2nd compettitor in column 1 will be placed at x,y on the canvas '''
        px, py = self._first_column_text_coordinates[competitor_index]
        return self._first_column_text_coordinates[competitor_index]

    def get_canvas_coord_for_nth_competitor_in_column2(self, competitor_index):
        '''returns the x,y coordinates on the canvas for the given competitor index
        for example the 2nd compettitor in column 2 will be placed at x,y on the canvas '''
        return self._second_column_text_coordinates[competitor_index]

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

    def calculate_canvas_coordinates_from_competitor_index(self, competitor_count: int, competitor_index: int):
        print(competitor_index)
        column, row = BPM.calculate_bracket_position_from_competitor_index(competitor_count, competitor_index)
        print('backet coordinate: ', column, row)
        if column == 1:
            x_coordinate, y_coordinate = self.get_canvas_coord_for_nth_competitor_in_column1(row - 1)
        else:
            x_coordinate, y_coordinate = self.get_canvas_coord_for_nth_competitor_in_column2(row - 1)
        x_coordinate = x_coordinate * cm
        y_coordinate = y_coordinate * cm
        print('canvas coordinate: ', x_coordinate, y_coordinate)
        return x_coordinate, y_coordinate

    def draw_competitors_on_tree(self, competitor_to_tree_mapper: CompetitorsToTreeMapper) -> object:
        ''' draw the competitors on the tree
        :type competitor_to_tree_mapper: object
        '''
        comps = competitor_to_tree_mapper.get_competitors()
        print(comps)
        competitor_count = comps.get_number_of_competitors()
        i = 0
        for index, competitor in comps.iterrows():
            name = competitor['First Name'] + ' ' + competitor['Last Name']
            print('\n' + name)
            px, py = self.calculate_canvas_coordinates_from_competitor_index(competitor_count, i)
            self._c.drawString(px, py, name)
            i = i + 1


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
