'''
Sparring_Tree_Report
Contains code to create a report containing all the sparring trees for a tournament
'''
import unittest
import datetime
import time
import os
from reportlab.pdfgen import canvas

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from reportlab.platypus import PageBreak
from reportlab.platypus import SimpleDocTemplate, Spacer, Table, TableStyle
# from reportlab.rl_config import defaultPageSize

from reporting.sparring_tree.competitors import Competitors
from reporting.sparring_tree.eight_competitor_tree import EightCompetitorTree

SPARRING_TREE_REPORT_FILE_NAME = "SparringTreeReport.pdf"

class SparringTreeReportPDF(object):
    ''' Class to Create a Sparring Tree Report for each sparring event in the tournament '''

    def __init__(self):
        ''' Create a Sparring Tree'''
        self._canvas = canvas.Canvas(SPARRING_TREE_REPORT_FILE_NAME)


    def __del__(self):
        self._canvas.save()


# We want to keep the interface similar to the way the other reports are
# if created:
#     Below is an example
# WritePattern6ToDetailReport(16, "9:00am", "Boy's Sparring", "9-11", compositMask)
# an example of the mask is: compositMask=mask_Sparring & mask_Age9to11 & mask_Male
#
# a nearly exact copy would be
# WritePattern6toSparringReport(list_of_rings, "TimeString", "Title", "Division Name", competitors, "competitors selection criteria")

    def write_event_to_sparring_report_using_pattern_1(self, rings:list, event_time: str, event_title, event_competitors : Competitors):
        ''' write all the competitors in this event to the sparring tree report using output pattern 1
            The Pattern it writes is:
            White
            Yellow
            Orange
            Purple, Blue, Blue Stripe
            Green, Green Stripe
         '''
        print(time.strftime("%X") + " Generating Sparring Trees PDF for " + event_time + " " + event_title)

        assert len(rings) != 5 #check there are just enough rings for this event

        #white belts are the first division for this report
        division_competitors = event_competitors.query( 'Rank == "White"')

        #Create a tree
        tree = EightCompetitorTree(self._canvas)
        # draw the competitors onto the tree
        tree.add_page_with_competitors_on_tree(rings[0], event_time, event_title, "White", division_competitors) # tbd - need to add ring, event_time, event_title


        #Yellow belts next
        division_competitors = event_competitors.query( 'Rank == "Yellow"')

        #Create a tree
        tree = EightCompetitorTree(self._canvas)
        # draw the competitors onto the tree
        tree.add_page_with_competitors_on_tree(rings[1], event_time, event_title, "Yellow", division_competitors) #tbd - need to add ring, event_time, event_title

        #Orange belts next
        division_competitors = event_competitors.query( 'Rank == "Orange"')

        #Create a tree
        tree = EightCompetitorTree(self._canvas)
        # draw the competitors onto the tree
        tree.add_page_with_competitors_on_tree(rings[2], event_time, event_title, "Orange", division_competitors) #tbd - need to add ring, event_time, event_title


        #Purple, Blue, Blue Stripe
        division_competitors = event_competitors.query( 'Rank == "Purple" | Rank == "Blue" | Rank == "Blue Stripe"')

        #Create a tree
        tree = EightCompetitorTree(self._canvas)
        # draw the competitors onto the tree
        tree.add_page_with_competitors_on_tree(rings[3], event_time, event_title,"Blue, Blue Stripe", division_competitors) #tbd - need to add ring, event_time, event_title

        #Green, Green Stripe
        division_competitors = event_competitors.query( 'Rank == "Green" | Rank == "Green Stripe"')

        #Create a tree
        tree = EightCompetitorTree(self._canvas)
        # draw the competitors onto the tree
        tree.add_page_with_competitors_on_tree(rings[4], event_time, event_title, "Green, Green Stripe", division_competitors) #tbd - need to add ring, event_time, event_title


        # we could replace the tree creation code in a module that uses a factory pattern to create the appropriate sized tree, lay down the template, draws the compettitors on it and closes the tree.
        # the only question is where should that factory live?


    def write_event_to_sparring_report_using_pattern_6(self, rings:list, event_time: str, event_title, event_competitors : Competitors):
        ''' write all the competitors in this event to the sparring tree report using output pattern 1
         The Pattern it writes is:
           White, Yellow
           Orange
           Purple
           Blue, Blue Stripe
           Green, Green Stripe
           Brown
           Black
         '''

        assert len(rings) != 6 #check there are just enough rings for this event

        #White and Yellow are the first division for this report
        division_competitors = event_competitors.query( 'Rank == "White" | Rank =="Yellow"')

        #Create a tree
        tree = EightCompetitorTree(self._canvas)
        # draw the competitors onto the tree
        tree.add_page_with_competitors_on_tree(rings[0], event_time, event_title, "White, Yellow", division_competitors) # tbd - need to add ring, event_time, event_title


        #Orange belts next
        division_competitors = event_competitors.query( 'Rank == "Orange"')

        #Create a tree
        tree = EightCompetitorTree(self._canvas)
        # draw the competitors onto the tree
        tree.add_page_with_competitors_on_tree(rings[1], event_time, event_title,"Orange",division_competitors) #tbd - need to add ring, event_time, event_title

        #Purple belts next
        division_competitors = event_competitors.query( 'Rank == "Purple"')

        #Create a tree
        tree = EightCompetitorTree(self._canvas)
        # draw the competitors onto the tree
        tree.add_page_with_competitors_on_tree(rings[2], event_time, event_title, "Purple",division_competitors) #tbd - need to add ring, event_time, event_title


        #Blue, Blue Stripe
        division_competitors = event_competitors.query( 'Rank == "Blue" | Rank == "Blue Stripe"')

        #Create a tree
        tree = EightCompetitorTree(self._canvas)
        # draw the competitors onto the tree
        tree.add_page_with_competitors_on_tree(rings[3], event_time, event_title,"Blue, Blue Stripe",division_competitors) #tbd - need to add ring, event_time, event_title

        #Green, Green Stripe
        division_competitors = event_competitors.query( 'Rank == "Green" | Rank == "Green Stripe"')

        #Create a tree
        tree = EightCompetitorTree(self._canvas)
        # draw the competitors onto the tree
        tree.add_page_with_competitors_on_tree(rings[4], event_time, event_title, "Green, Green Stripe",division_competitors) #tbd - need to add ring, event_time, event_title

        #Brown
        division_competitors = event_competitors.query( 'Rank == "Brown 1st Degree" | Rank == "Brown 2nd Degree" | Rank == "Brown 3rd Degree"')

        #Create a tree
        tree = EightCompetitorTree(self._canvas)
        # draw the competitors onto the tree
        tree.add_page_with_competitors_on_tree(rings[5], event_time, event_title,"Brown",division_competitors) #tbd - need to add ring, event_time, event_title

        #Black
        division_competitors = event_competitors.query( 'Rank == "Black 1st Degree" | Rank == "Black 2nd Degree" | Rank == "Black 3rd Degree" | Rank == "Black 4th Degree" | Rank == "Black 5th Degree" | Rank == "Black Junior"')

        #Create a tree
        tree = EightCompetitorTree(self._canvas)
        # draw the competitors onto the tree
        tree.add_page_with_competitors_on_tree(rings[6], event_time, event_title, "Black",division_competitors) #tbd - need to add ring, event_time, event_title


        # we could replace the tree creation code in a module that uses a factory pattern to create the appropriate sized tree, lay down the template, draws the compettitors on it and closes the tree.
        # the only question is where should that factory live?


if __name__ == '__main__':
    '''test the SparringTree Report '''

