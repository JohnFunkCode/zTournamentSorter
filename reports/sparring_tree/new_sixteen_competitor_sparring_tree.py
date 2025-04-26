""" this module contains code to create a 16 person sparring tree"""
import os
import logging
import datetime
from pathlib import Path

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.units import cm
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader


from domain_model.competitors import Competitors
from reports.sparring_tree.base_sparring_tree import SparringTree

# tbd - refactor this to a utility module
def pathDelimiter():
    path = os.getcwd()
    if "\\" in path:
        delimiter = "\\"  # Windows
    else:
        delimiter = "/"  # Unix
    return delimiter

class NewSixteenCompetitorTree(SparringTree):
    """ Creates a 16 compettitor sparring tree"""

    # setup a couple of constants for this tree
    _OFFSET_BETWEEN_BRANCHES_ON_TREE = 2.4
    _SPACE_BELOW_TEXT = 0.1  # centimeters
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
        initial_first_column_text_coords = [[.8, 18.5 + self._SPACE_BELOW_TEXT],
                                            [.8, 17.3 + self._SPACE_BELOW_TEXT]]
        for i in range(8):
            offset = self.truncate(i * self._OFFSET_BETWEEN_BRANCHES_ON_TREE, 1)
            self._first_column_text_coordinates.append([initial_first_column_text_coords[0][0],
                                                        initial_first_column_text_coords[0][1] - offset])
            self._first_column_text_coordinates.append([initial_first_column_text_coords[1][0],
                                                        initial_first_column_text_coords[1][1] - offset])

        self._second_column_text_coordinates = []
        initial_second_column_text_coords = [7.2, 17.9 + self._SPACE_BELOW_TEXT]
        for i in range(8):
            offset = self.truncate(i * self._OFFSET_BETWEEN_BRANCHES_ON_TREE, 1)
            self._second_column_text_coordinates.append(
                [initial_second_column_text_coords[0], self.truncate(initial_second_column_text_coords[1] - offset, 1)])

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
        logo = ImageReader('Z Ultimate Logo Rectangle-1Inch-300DPI.png')
        self._c.drawImage(logo, 1 * cm, 25.4 * cm, 1.875 * cm, 2.625 * cm, mask='auto')

        # Draw the static template portion of the tree - Note this template must be less than 3.5 inches tall (currently set for a 2482 x 931 300 dpi image)
        backgroundImageFilename='reports'+pathDelimiter()+'sparring_tree'+pathDelimiter()+'sparring_tree_template-300dpi.png'  #<--comment out for stand-alone testing
        backgroundImage = ImageReader(backgroundImageFilename)
        image_width, image_height = backgroundImage.getSize()
        page_width,page_height=letter
        yposition = page_height - ((image_height / 300) * inch)
        self._c.drawImage(backgroundImage, 0, yposition, (image_width / 300) * inch, (image_height / 300 ) * inch, mask='auto')


        """ Draws the static template portion of the tree"""
        # first bracket
        for i in range(8):
            offset = i * self._OFFSET_BETWEEN_BRANCHES_ON_TREE
            self._path.moveTo(.8 * cm, (0.5 + offset) * cm)  # .8 centimeters to the right, (1 + offset) centimeters up
            self._path.lineTo(6.2 * cm, (0.5 + offset) * cm)
            self._path.lineTo(7.1 * cm, (1.1 + offset) * cm)
            self._path.lineTo(6.2 * cm, (1.7 + offset) * cm)
            self._path.lineTo(.8 * cm, (1.7 + offset) * cm)
            self.draw_boxes(1.5, 0.5 + offset)
            self.draw_boxes(1.5, 1.7 + offset)

        # second bracket
        for i in range(4):
            offset = i * self._OFFSET_BETWEEN_BRANCHES_ON_TREE * 2
            self._path.moveTo(7.1 * cm, (1.1 + offset) * cm)  # 7.2 centimeters to the right, (2 + offset) centimeters up
            self._path.lineTo(12.6 * cm, (1.1 + offset) * cm)
            self._path.lineTo(13.3 * cm, (2.3 + offset) * cm)
            self._path.lineTo(12.6 * cm, (3.5 + offset) * cm)
            self._path.lineTo(7.1 * cm, (3.5 + offset) * cm)
            self.draw_boxes(7.5, 1.1 + offset)
            self.draw_boxes(7.5, 3.5 + offset)

        # third bracket
        round_indicator = ['D', 'C']
        for i in range(2):
            offset = i * self._OFFSET_BETWEEN_BRANCHES_ON_TREE * 4
            self._path.moveTo(13.3 * cm, (2.3 + offset) * cm)  # 13.3 centimeters to the right, (3.2 + offset) centimeters up
            self._path.lineTo(18.7 * cm, (2.3 + offset) * cm)
            self._c.drawString(14.1 * cm, (1.8 + offset) * cm, f"Advance to round {round_indicator[i]}")

            # self._path.lineTo(20.1 * cm, (4.7 + offset) * cm) # last minute change for Spring 2023 tournament
            # self._path.lineTo(18.7 * cm, (7.1 + offset) * cm) # last minute change for Spring 2023 tournament
            self._path.moveTo(18.7 * cm, (7.1 + offset) * cm)
            self._path.lineTo(13.3 * cm, (7.1 + offset) * cm)
            self._c.drawString(14.1 * cm, (6.7 + offset) * cm, f"Advance to round {round_indicator[i]}")

            # self.draw_boxes(14, 2.3 + offset)
            # self.draw_boxes(14, 7.1 + offset)



    def draw_header_info_on_tree(self, ring: int, event_time: str, event_title: str, age: str, ranks: str, split_label: str, number_of_competitors: int):
        ''' draw the header text onto the tree '''
        # Define the starting position and the total height for the header
        top_y = 27.5 * cm  # Starting y-coordinate
        height = .9 * inch  # Total height for the header (3/4 inch)
        line_spacing = height / 5  # Divide the height evenly for 5 fields

        # Draw each field with adjusted vertical spacing
        self._c.drawString(12.5 * cm, top_y, "Ring:")
        self._c.drawString(14.3 * cm, top_y, f'{ring}   {event_time}')

        self._c.drawString(12.5 * cm, top_y - line_spacing, "Division:")
        self._c.drawString(14.3 * cm, top_y - line_spacing, event_title)

        self._c.drawString(12.5 * cm, top_y - 2 * line_spacing, "Age:")
        self._c.drawString(14.3 * cm, top_y - 2 * line_spacing, age)

        if split_label != '':
            self._c.setFillColorRGB(255, 0, 0)
            self._c.drawString(15.5 * cm, top_y - 2 * line_spacing, 'Contestants ' + split_label)
            self._c.setFillColorRGB(0, 0, 0)

        self._c.drawString(12.5 * cm, top_y - 3 * line_spacing, "Ranks:")
        self._c.drawString(14.3 * cm, top_y - 3 * line_spacing, ranks)

        self._c.drawString(12.5 * cm, top_y - 4 * line_spacing, "Competitors:")
        self._c.drawString(15.5 * cm, top_y - 4 * line_spacing, "{}".format(number_of_competitors))

        # write the footer as well
        self._c.saveState()
        self._c.setFont('Times-Roman', 9)
        # self._c.drawCentredString(13.97 * cm, .5 * cm, "Generated at: {} From File: {}".format(self._creation_timestamp, self._source_filename))
        self._c.drawCentredString(10.795 * cm, .1 * cm, "Generated at: {} From File: {}".format(self._creation_timestamp,self._source_filename))

        self._c.restoreState()

    def draw_competitors_on_tree(self, competitors: Competitors) -> object:
        ''' draw the competitors on the tree '''
        # logging.info(competitors)

        competitor_count = competitors.get_number_of_competitors()
        if competitor_count > 16:
            logging.info("*** Something is wrong! we have {} competitors for an 16 person tree".format(competitor_count))
            competitor_count = 16
        i = 0
        for index, competitor in competitors.iterrows():
            name = competitor['First_Name'] + ' ' + competitor['Last_Name']
            # logging.info('\n' + name)
            px, py = self.calculate_canvas_coordinates_from_competitor_index(competitor_count, i)
            self._c.drawString(px, py, name)
            self._c.setFont("Courier", 7)
            dojo = competitor['Dojo']
            if dojo.startswith('CO- '):
                dojo = dojo[4:]
            dojo_weight_height = f"{competitor['Feet']}\' {competitor['Inches']}\" {competitor['Weight']}lbs BMI={competitor['BMI']}"


            self._c.drawString(px + (0.0 * cm), py + (.4 * cm), dojo_weight_height)
            self._c.setFont("Helvetica", 12)
            i = i + 1
            assert i < 17, "Should be no more than 16 competitors on an 16 person tree"


if __name__ == '__main__':
    ''' Very simple test try to create a tree and check that the file exists '''

    # set the cwd to the project root
    new_path = Path(__file__).resolve().parents[2]
    os.chdir(new_path)

    c = canvas.Canvas("reports//sparring_tree//testoutput//16PersonTree.pdf", pagesize=letter)  # defaults to 72 pointer per inch
    tree = NewSixteenCompetitorTree(c, "test_file.csv")
    tree.draw_static_template()
    tree.close()
    c.save()
    import os

    if os.path.exists("16PersonTree.pdf"):
        logging.info("It worked")
