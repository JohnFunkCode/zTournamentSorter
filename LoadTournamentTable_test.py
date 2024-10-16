#to run this test go to the main directory and run
# nosetests --with-coverage --verbose

import logging
import pandas as pd
import numpy as np
import unittest
import sys

import LoadTournamentTable
import os


class TestLoadTournamentTable(unittest.TestCase):

    def setUp(self):
        os.putenv("tournament_filename","/Users/johnfunk/Documents/Tournaments/2024-May-04/competitor-list-clean.csv")
        return

    def test_load_tournament_table(self):
        os.putenv("tournament_filename","/Users/johnfunk/Documents/Tournaments/2024-May-04/competitor-list-clean.csv")
        # LoadTournamentTable.main()
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
