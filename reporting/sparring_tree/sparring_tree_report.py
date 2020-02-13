'''
Sparring_Tree_Report
Contains code to create a report containing all the sparring trees for a tournament
'''
import time
from reportlab.pdfgen import canvas

from reporting.sparring_tree.competitors import Competitors
from reporting.sparring_tree.eight_competitor_sparring_tree import EightCompetitorTree
from reporting.sparring_tree.sixteen_competitor_sparring_tree import SixteenCompetitorTree
from reporting.sparring_tree.thirtytwo_competitor_sparring_tree import ThirtyTwoCompetitorTree
from reporting.sparring_tree.base_sparring_tree import SparringTree

SPARRING_TREE_REPORT_LETTER_FILE_NAME = "SparringTreeReport-Letter.pdf"
SPARRING_TREE_REPORT_LEGAL_FILE_NAME = "SparringTreeReport-Legal.pdf"


def create_sparring_tree( letter_canvas: canvas, legal_canvas: canvas, number_of_competitors: int, the_source_filename : str) -> SparringTree:
    ''' Factory method to create a sparring tree of the appropriate size based on the number of competitors'''
    # assert number_of_competitors <=0, "Error Less than 1 competitor"
    assert number_of_competitors <= 32, "Coding Error: More than 16 competitors provided"

    the_tree = None

    if number_of_competitors <= 8:
        the_tree = EightCompetitorTree(letter_canvas, the_source_filename)
    elif number_of_competitors <= 16:
        the_tree = SixteenCompetitorTree(letter_canvas, the_source_filename)
    elif number_of_competitors <= 32:
        the_tree = ThirtyTwoCompetitorTree(legal_canvas, the_source_filename)
    return the_tree

class SparringTreeReportPDF():
    ''' Class to Create a Sparring Tree Report for each sparring event in the tournament '''

    def __init__(self):
        ''' Create a Sparring Tree'''
        self._letter_canvas = canvas.Canvas(SPARRING_TREE_REPORT_LETTER_FILE_NAME)
        self._legal_canvas = canvas.Canvas(SPARRING_TREE_REPORT_LEGAL_FILE_NAME)
        self._source_filename = "not initialized"

    #  seems to cause problems for debugging
    #    def __del__(self):
    #        self._canvas.save()

    def close(self):
        ''' close things out by saving the canvas'''
        self._letter_canvas.save()
        self._legal_canvas.save()

    def set_source_file(self, the_source_filename :str):
        ''' setup the source filename so it's available to print in the footer of each tree'''
        self._source_filename = the_source_filename

    def write_event_to_sparring_report_using_pattern_1(self, rings: list, event_time: str, event_title,
                                                       event_competitors: Competitors):
        ''' write all the competitors in this event to the sparring tree report using output pattern 1
            The Pattern it writes is:
            White
            Yellow
            Orange
            Purple, Blue, Blue Stripe
            Green, Green Stripe
         '''
        print(time.strftime("%X") + " Generating Sparring Trees PDF for " + event_time + " " + event_title)

        assert len(
            rings) != 4, "Coding Error: Not enough rings provided for this event"  # check there are just enough rings for this event

        # white belts are the first division for this report
        division_competitors = event_competitors.query('Rank == "White"')

        # Create a tree
        tree = create_sparring_tree(self._letter_canvas, self._legal_canvas, division_competitors.get_number_of_competitors(),self._source_filename)
        # draw the competitors onto the tree
        tree.add_page_with_competitors_on_tree(rings[0], event_time, event_title, "White",
                                               division_competitors)

        # Yellow belts next
        division_competitors = event_competitors.query('Rank == "Yellow"')

        # Create a tree
        tree = create_sparring_tree(self._letter_canvas, self._legal_canvas, division_competitors.get_number_of_competitors(),self._source_filename)
        # draw the competitors onto the tree
        tree.add_page_with_competitors_on_tree(rings[1], event_time, event_title, "Yellow",
                                               division_competitors)

        # Orange belts next
        division_competitors = event_competitors.query('Rank == "Orange"')

        # Create a tree
        tree = create_sparring_tree(self._letter_canvas, self._legal_canvas, division_competitors.get_number_of_competitors(),self._source_filename)
        # draw the competitors onto the tree
        tree.add_page_with_competitors_on_tree(rings[2], event_time, event_title, "Orange",
                                               division_competitors)

        # Purple, Blue, Blue Stripe
        division_competitors = event_competitors.query('Rank == "Purple" | Rank == "Blue" | Rank == "Blue w/Stripe"')

        # Create a tree
        tree = create_sparring_tree(self._letter_canvas, self._legal_canvas, division_competitors.get_number_of_competitors(),self._source_filename)
        # draw the competitors onto the tree
        tree.add_page_with_competitors_on_tree(rings[3], event_time, event_title, "Purple, Blue, Blue Stripe",
                                               division_competitors)

        # Green, Green Stripe
        division_competitors = event_competitors.query('Rank == "Green" | Rank == "Green w/Stripe"')

        # Create a tree
        tree = create_sparring_tree(self._letter_canvas, self._legal_canvas, division_competitors.get_number_of_competitors(),self._source_filename)
        # draw the competitors onto the tree
        tree.add_page_with_competitors_on_tree(rings[4], event_time, event_title, "Green, Green Stripe",
                                               division_competitors)

    def write_event_to_sparring_report_using_pattern_4(self, rings: list, event_time: str, event_title,
                                                       event_competitors: Competitors):
        ''' writes all the competitors in this event to the sparring tree report using output patter 5
          The pattern it writes is: Pattern4
          White, Yellow, Orange
          Purple, Blue, Blue Stripe
          Green, Green Stripe, Brown
          Black
        '''
        assert len(
            rings) != 3, "Coding Error: Not enough rings provided for this event"  # check there are just enough rings for this event

        # White,  Yellow, Orange are the first division for this report
        division_competitors = event_competitors.query('Rank == "White" | Rank =="Yellow" | Rank == "Orange"')

        # Create a tree
        tree = create_sparring_tree(self._letter_canvas, self._legal_canvas, division_competitors.get_number_of_competitors(),self._source_filename)
        # draw the competitors onto the tree
        tree.add_page_with_competitors_on_tree(rings[0], event_time, event_title, "White, Yellow, Orange",
                                               division_competitors)

        # Purple, Blue, Blue Stripe
        division_competitors = event_competitors.query('Rank == "Purple" | Rank == "Blue" | Rank == "Blue w/Stripe"')

        # Create a tree
        tree = create_sparring_tree(self._letter_canvas, self._legal_canvas, division_competitors.get_number_of_competitors(),self._source_filename)
        # draw the competitors onto the tree
        tree.add_page_with_competitors_on_tree(rings[1], event_time, event_title, "Purple, Blue, Blue Stripe",
                                               division_competitors)

        # Green, Green Stripe, Brown
        division_competitors = event_competitors.query('Rank == "Green" | Rank == "Green Blue w/Stripe"'
                                                       '| Rank == "Brown 1st Degree" | Rank == "Brown 2nd Degree"'
                                                       '| Rank == "Brown 3rd Degree"')

        # Create a tree
        tree = create_sparring_tree(self._letter_canvas, self._legal_canvas, division_competitors.get_number_of_competitors(),self._source_filename)
        # draw the competitors onto the tree
        tree.add_page_with_competitors_on_tree(rings[2], event_time, event_title, "Green, Green Stripe, Brown",
                                               division_competitors)

        # Black
        division_competitors = event_competitors.query(
            'Rank == "Black 1st Degree" | Rank == "Black 2nd Degree" | Rank == "Black 3rd Degree" | Rank == "Black 4th Degree" | Rank == "Black 5th Degree" | Rank == "Black Junior"')

        # Create a tree
        tree = create_sparring_tree(self._letter_canvas, self._legal_canvas, division_competitors.get_number_of_competitors(),self._source_filename)
        # draw the competitors onto the tree
        tree.add_page_with_competitors_on_tree(rings[3], event_time, event_title, "Black",
                                               division_competitors)

    def write_event_to_sparring_report_using_pattern_5(self, rings: list, event_time: str, event_title,
                                                       event_competitors: Competitors):
        ''' writes all the competitors in this event to the sparring tree report using output patter 5
          The pattern it writes is: Pattern5
          White, Yellow
          Orange
          Purple
          Blue, Blue Stripe
          Green, Green Stripe, Brown
        '''
        assert len(
            rings) != 4, "Coding Error: Not enough rings provided for this event"  # check there are just enough rings for this event

        # White and Yellow are the first division for this report
        division_competitors = event_competitors.query('Rank == "White" | Rank =="Yellow"')

        # Create a tree
        tree = create_sparring_tree(self._letter_canvas, self._legal_canvas, division_competitors.get_number_of_competitors(),self._source_filename)
        # draw the competitors onto the tree
        tree.add_page_with_competitors_on_tree(rings[0], event_time, event_title, "White, Yellow",
                                               division_competitors)
        # Orange belts next
        division_competitors = event_competitors.query('Rank == "Orange"')

        # Create a tree
        tree = create_sparring_tree(self._letter_canvas, self._legal_canvas, division_competitors.get_number_of_competitors(),self._source_filename)
        # draw the competitors onto the tree
        tree.add_page_with_competitors_on_tree(rings[1], event_time, event_title, "Orange",
                                               division_competitors)

        # Purple belts next
        division_competitors = event_competitors.query('Rank == "Purple"')

        # Create a tree
        tree = create_sparring_tree(self._letter_canvas, self._legal_canvas, division_competitors.get_number_of_competitors(),self._source_filename)
        # draw the competitors onto the tree
        tree.add_page_with_competitors_on_tree(rings[2], event_time, event_title, "Purple",
                                               division_competitors)

        # Blue, Blue Stripe
        division_competitors = event_competitors.query('Rank == "Blue" | Rank == "Blue w/Stripe"')

        # Create a tree
        tree = create_sparring_tree(self._letter_canvas, self._legal_canvas, division_competitors.get_number_of_competitors(),self._source_filename)
        # draw the competitors onto the tree
        tree.add_page_with_competitors_on_tree(rings[3], event_time, event_title, "Blue, Blue Stripe",
                                               division_competitors)

        # Green, Green Stripe, Brown
        division_competitors = event_competitors.query('Rank == "Green" | Rank == "Green w/Stripe"'
                                                       '| Rank == "Brown 1st Degree" | Rank == "Brown 2nd Degree"'
                                                       '| Rank == "Brown 3rd Degree"')

        # Create a tree
        tree = create_sparring_tree(self._letter_canvas, self._legal_canvas, division_competitors.get_number_of_competitors(),self._source_filename)
        # draw the competitors onto the tree
        tree.add_page_with_competitors_on_tree(rings[4], event_time, event_title, "Green, Green Stripe, Brown",
                                               division_competitors)

    def write_event_to_sparring_report_using_pattern_6(self, rings: list, event_time: str, event_title,
                                                       event_competitors: Competitors):
        ''' write all the competitors in this event to the sparring tree report using output pattern 6
         The Pattern it writes is:
           White, Yellow
           Orange
           Purple
           Blue, Blue Stripe
           Green, Green Stripe
           Brown
           Black
         '''

        assert len(
            rings) != 6, "Coding Error: Not enough rings provided for this event"  # check there are just enough rings for this event

        # White and Yellow are the first division for this report
        division_competitors = event_competitors.query('Rank == "White" | Rank =="Yellow"')

        # Create a tree
        tree = create_sparring_tree(self._letter_canvas, self._legal_canvas, division_competitors.get_number_of_competitors(),self._source_filename)
        # draw the competitors onto the tree
        tree.add_page_with_competitors_on_tree(rings[0], event_time, event_title, "White, Yellow",
                                               division_competitors)

        # Orange belts next
        division_competitors = event_competitors.query('Rank == "Orange"')

        # Create a tree
        tree = create_sparring_tree(self._letter_canvas, self._legal_canvas, division_competitors.get_number_of_competitors(),self._source_filename)
        # draw the competitors onto the tree
        tree.add_page_with_competitors_on_tree(rings[1], event_time, event_title, "Orange",
                                               division_competitors)

        # Purple belts next
        division_competitors = event_competitors.query('Rank == "Purple"')

        # Create a tree
        tree = create_sparring_tree(self._letter_canvas, self._legal_canvas, division_competitors.get_number_of_competitors(),self._source_filename)
        # draw the competitors onto the tree
        tree.add_page_with_competitors_on_tree(rings[2], event_time, event_title, "Purple",
                                               division_competitors)

        # Blue, Blue Stripe
        division_competitors = event_competitors.query('Rank == "Blue" | Rank == "Blue w/Stripe"')

        # Create a tree
        tree = create_sparring_tree(self._letter_canvas, self._legal_canvas, division_competitors.get_number_of_competitors(),self._source_filename)
        # draw the competitors onto the tree
        tree.add_page_with_competitors_on_tree(rings[3], event_time, event_title, "Blue, Blue Stripe",
                                               division_competitors)

        # Green, Green Stripe
        division_competitors = event_competitors.query('Rank == "Green" | Rank == "Green w/Stripe"')

        # Create a tree
        tree = create_sparring_tree(self._letter_canvas, self._legal_canvas, division_competitors.get_number_of_competitors(),self._source_filename)
        # draw the competitors onto the tree
        tree.add_page_with_competitors_on_tree(rings[4], event_time, event_title, "Green, Green Stripe",
                                               division_competitors)

        # Brown
        division_competitors = event_competitors.query(
            'Rank == "Brown 1st Degree" | Rank == "Brown 2nd Degree" | Rank == "Brown 3rd Degree"')

        # Create a tree
        tree = create_sparring_tree(self._letter_canvas, self._legal_canvas, division_competitors.get_number_of_competitors(),self._source_filename)
        # draw the competitors onto the tree
        tree.add_page_with_competitors_on_tree(rings[5], event_time, event_title, "Brown",
                                               division_competitors)

        # Black
        division_competitors = event_competitors.query(
            'Rank == "Black 1st Degree" | Rank == "Black 2nd Degree" | Rank == "Black 3rd Degree" | Rank == "Black 4th Degree" | Rank == "Black 5th Degree" | Rank == "Black Junior"')

        # Create a tree
        tree = create_sparring_tree(self._letter_canvas, self._legal_canvas, division_competitors.get_number_of_competitors(),self._source_filename)
        # draw the competitors onto the tree
        tree.add_page_with_competitors_on_tree(rings[6], event_time, event_title, "Black",
                                               division_competitors)

        # we could replace the tree creation code in a module that uses a factory pattern to create the appropriate sized tree, lay down the template, draws the compettitors on it and closes the tree.
        # the only question is where should that factory live?


if __name__ == '__main__':
    '''test the SparringTree Report '''
