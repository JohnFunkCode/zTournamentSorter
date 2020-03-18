'''
This module tests the ring module
to run this test go to the main directory and run
nosetests --with-coverage
'''''

import unittest
from domain_model import ring as ring

class TestRing(unittest.TestCase):
    ''' class to test the Event module '''

    def setUp(self) -> None:
        ''' setup code for these tests '''

    def test_constructor(self):
        r = ring.Ring(None, 9, 'A-Z', ['White', 'Yellow'])
        self.assertTrue(r.ring_number == 9)

if __name__ == '__main__':
    unittest.main()
