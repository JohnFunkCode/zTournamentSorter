#to run this test go to the main directory and run
# nosetests --with-coverage

import pandas as pd
import numpy as np
import unittest

import participants as parts


class TestParticipants(unittest.TestCase):

    def setUp(self):
        return

    def test_participants_has_correct_number_of_entries(self):
        p = parts.Participants()
        #print p._participant_list
        shape=p._participant_list.shape
        #print shape[0]
        self.assertEquals(3, shape[0])

    def test_participants_from_mask_returns_correct_results(self):
        p = parts.Participants()
        df = p.participants_from_mask(p.yellow_belt_mask)
        x = df.shape
        self.assertEquals(2, x[0])

if __name__ == '__main__':
    unittest.main()
