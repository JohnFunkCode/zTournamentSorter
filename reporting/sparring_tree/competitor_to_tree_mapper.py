""" this module contains code to map competitors into sparring trees"""

from reporting.sparring_tree import competitors as competitors


class CompetitorsToTreeMapper():
    ''' class to map competitors into sparring trees'''
    _competitors = None

    def __init__(self):
        '''setup instance variables'''

    def set_competitors(self,competitors):
        self._competitors = competitors
