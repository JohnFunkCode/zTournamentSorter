'''
Sparring_Tree_Report
Contains code to create a report containing all the sparring trees for a tournament
'''
import unittest
import datetime
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

    def write_event_to_sparring_report_using_pattern_1(self, event_time: str, event_title, event_competitors : Competitors):
        ''' write all the competitors in this event to the sparring tree report using output pattern 1
            The Pattern it writes is:
            White
            Yellow
            Orange
            Purple, Blue, Blue Stripe
            Green, Green Stripe
         '''
        tree = EightCompetitorTree(self._canvas)
        tree.draw_static_template()


        #white belts are the first division for this report
        division_competitors = event_competitors.query( 'Rank == "Yellow"')

        # lay down the template
        tree.draw_static_template()

        # draw the competitors onto the tree
        tree.draw_competitors_on_tree(division_competitors)

        tree.close()


if __name__ == '__main__':
    '''test the SparringTree Report '''

