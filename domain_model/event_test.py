'''
This module tests the event module
to run this test go to the main directory and run
nosetests --with-coverage
'''''

import unittest
from domain_model import event as ev

class TestEvent(unittest.TestCase):
    ''' class to test the Event module '''

    def setUp(self) -> None:
        ''' setup code for these tests '''

    def test_constructor(self):
        e = ev.Event('Kids Kata', '9:00', ['White'])
        self.assertTrue(e.name == 'Kids Kata')


if __name__ == '__main__':
    unittest.main()