'''
This module tests the ring_split module
to run this test go to the main directory and run
nosetests --with-coverage
'''''

import unittest
from domain_model import ring_split as ring_split

class TestEvent(unittest.TestCase):
    ''' class to test the Event module '''

    def setUp(self) -> None:
        ''' setup code for these tests '''

    def test_constructor(self):
        r = ring_split.RingSplit(9)
        self.assertTrue(r.ring_number == 9)

if __name__ == '__main__':
    unittest.main()
