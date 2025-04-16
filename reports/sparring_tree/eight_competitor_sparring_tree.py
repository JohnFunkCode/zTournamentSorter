""" this module contains code to create an 8 person sparring tree"""
import logging
import datetime

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader

from domain_model.competitors import Competitors
from reports.sparring_tree.base_sparring_tree import SparringTree

class EightCompetitorTree(SparringTree):
    """ Creates an 8 compettitor sparring tree"""

    # setup a couple of constants for this tree
    _OFFSET_BETWEEN_BRANCHES_ON_TREE = 4.8
    _SPACE_BELOW_TEXT = 0.1

    _c = None
    _path = None

    _first_column_text_coordinates = None
    _second_column_text_coordinates = None
    _source_filename = "not initialized"
    _creation_timestamp = "not initialized"

    def __init__(self, the_canvas, the_source_filename):
        """ sets up instance variables for this tree """
        SparringTree.__init__(self, the_canvas, the_source_filename)
        self._c.setPageSize(letter)  # defaults to 72 pointer per inch
        self.initialize_text_coordinates()
        self._source_filename = the_source_filename
        now = datetime.datetime.now()
        self._creation_timestamp = now.strftime("%Y-%m-%d %H:%M")


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
        #top += 1.0
        top += 1.2
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
            self._path.moveTo(.8 * cm, (3.8 + offset) * cm)  # .8 cm to the right, 3.8 cm up
            self._path.lineTo(6 * cm, (3.8 + offset) * cm)
            self._path.lineTo(7.2 * cm, (5 + offset) * cm)
            self._path.lineTo(6 * cm, (6 + offset) * cm)
            self._path.lineTo(.8 * cm, (6 + offset) * cm)
            self.draw_boxes(1.5, 3.8 + offset)
            self.draw_boxes(1.5, 6 + offset)

        # Second bracket
        for i in range(2):
            offset = i * (self._OFFSET_BETWEEN_BRANCHES_ON_TREE * 2)
            self._path.moveTo(7.2 * cm, (5 + offset) * cm)  # 7.2 cm to the right, 5 cm up
            self._path.lineTo(12.4 * cm, (5 + offset) * cm)
            # self._path.lineTo(15.2 * cm, (7.5 + offset) * cm) # last minute change for Spring 2023 tournament
            # self._path.lineTo(12.4 * cm, (9.8 + offset) * cm) # last minute change for Spring 2023 tournament
            self._path.moveTo(12.4 * cm, (9.8 + offset) * cm)
            self._path.lineTo(7.2 * cm, (9.8 + offset) * cm)
            self.draw_boxes(7.9, 5 + offset)
            self.draw_boxes(7.9, 9.8 + offset)

        # last minute change for Spring 2023 tournament
        # # third bracket
        # self._path.moveTo(15.2 * cm, 7.5 * cm)  # 15.2 cm to the right, 7.5 cm up
        # self._path.lineTo(20.4 * cm, 7.5 * cm)
        # self._path.moveTo(15.2 * cm, 17.1 * cm)
        # self._path.lineTo(20.4 * cm, 17.1 * cm)
        #
        # self.draw_boxes(16.0, 7.5)  # 16 cm to the right and 7.4 cm up
        # self.draw_boxes(16.0, 17.1)

        # #self._c.drawString(14.25 * cm, 4.6 * cm, "Third:")
        # self._path.moveTo( 15.3 * cm ,4.5 * cm)
        # self._path.lineTo( 21.4 * cm, 4.5 * cm)
        #
        # #self._c.drawString(14 * cm, 2.6 * cm, "Fourth:")
        # self._path.moveTo( 15.3 * cm ,2.5 * cm)
        # self._path.lineTo( 21.4 * cm, 2.5 * cm)

        # logo = ImageReader('Z_LOGO_OneInch.jpg')
        # self._c.drawImage(logo, 10.16 * cm, 23.4 * cm, mask='auto')
        logo = ImageReader('Z Ultimate Logo Rectangle-1Inch-300DPI.png')
        self._c.drawImage(logo, 1 * cm, 24 * cm, 2.5 * cm, 3.5 * cm, mask='auto')


    def draw_header_info_on_tree(self, ring: int, event_time: str, event_title: str, age: str, ranks: str, split_label: str, number_of_competitors: int):
        ''' draw the header text onto the tree '''
        # self._c.drawString(13 * cm, 26.5 * cm, "Time:")
        # self._c.drawString(14.3 * cm, 26.5 * cm, event_time)
        # self._c.drawString(13 * cm, 25.75 * cm, "Event:")
        # self._c.drawString(14.3 * cm, 25.75 * cm, event_title)
        # self._c.drawString(13 * cm, 25 * cm, "Rank:")
        # self._c.drawString(14.3 * cm, 25 * cm, ranks)
        # self._c.drawString(13 * cm, 24.25 * cm, "Ring#:")
        # self._c.drawString(14.3 * cm, 24.25 * cm, str(ring))
        # if split_label != '':
        #     self._c.setFillColorRGB(255,0,0)
        #     self._c.drawString(15 * cm, 24.25 * cm, 'Contestants '+ split_label)
        #     self._c.setFillColorRGB(0, 0, 0)
        # self._c.drawString(13 * cm, 23.5 *cm, "Competitors:")
        # self._c.drawString(15.5 *cm, 23.5 *cm, "{}".format(number_of_competitors))
        self._c.drawString(12.5 * cm, 26.5 * cm, "Ring:")
        self._c.drawString(14.3 * cm, 26.5 * cm, f'{ring}   {event_time}')
        self._c.drawString(12.5 * cm, 25.75 * cm, "Division:")
        self._c.drawString(14.3 * cm, 25.75 * cm, event_title)
        self._c.drawString(12.5 * cm, 25 * cm, "Age:")
        self._c.drawString(14.3 * cm, 25 * cm, age)
        if split_label != '':
            self._c.setFillColorRGB(255,0,0)
            self._c.drawString(15.5 * cm, 25 * cm, 'Contestants '+ split_label)
            self._c.setFillColorRGB(0, 0, 0)

        self._c.drawString(12.5 * cm, 24.25 * cm, "Ranks:")
        self._c.drawString(14.3 * cm, 24.25 * cm, ranks)
        self._c.drawString(12.5 * cm, 23.5 *cm, "Competitors:")
        self._c.drawString(15.5 *cm, 23.5 *cm, "{}".format(number_of_competitors))

        #write the footer as well
        self._c.saveState()
        self._c.setFont('Times-Roman', 9)
        self._c.drawCentredString(10.795 * cm, .5 * cm, "Generated at: {} From File: {}".format(self._creation_timestamp,self._source_filename))
        self._c.restoreState()

    def draw_competitors_on_tree(self, competitors: Competitors) -> object:
        ''' draw the competitors on the tree '''
        # logging.info(competitors)

        competitor_count = competitors.get_number_of_competitors()
        if competitor_count > 8:
            logging.info("*** Something is wrong! we have {} competitors for an 8 person tree".format(competitor_count))
            competitor_count = 8
        i = 0
        for index, competitor in competitors.iterrows():
            name = competitor['First_Name'] + ' ' + competitor['Last_Name']
            # logging.info('\n' + name)
            px, py = self.calculate_canvas_coordinates_from_competitor_index(competitor_count, i)
            self._c.setFont("Helvetica", 12)
            self._c.drawString(px, py, name)

            #self._c.saveState()
            self._c.setFont("Courier", 7)
            dojo= competitor['Dojo']
            #self._c.drawString(px + (2.4 * cm), py + (.6 * cm), dojo)
            #weight_height = "{}\' {}\" {} lbs".format(competitor['Feet'], competitor['Inches'], competitor['Weight'])
            #from reportlab.pdfbase import pdfmetrics
            #self._c.drawString(px + pdfmetrics.stringWidth(name,"Helvetica",12) + 5, py, weight_height)
            if dojo.startswith('CO- '):
                dojo=dojo[4:]
            # dojo_weight_height = "{} {}\' {}\" {}lbs BMI={}".format(dojo,competitor['Feet'], competitor['Inches'], competitor['Weight'], competitor['BMI'])
            dojo_weight_height = f"{competitor['Feet']}\' {competitor['Inches']}\" {competitor['Weight']}lbs BMI={competitor['BMI']}"

            self._c.drawString(px + (0.0 * cm), py + (.45 * cm), dojo_weight_height)
            self._c.setFont("Helvetica", 12)
            #self._c.restoreState()
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
        logging.info("It worked")
