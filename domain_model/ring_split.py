''' this module contains code for an ring_split.  It is used to hold the subset of compettitors when a ring has to be split '''
import logging

class RingSplit():
    ''' class to represent an ring_split '''

    ring_number = None
    competitors = None

    def __init__(self, ring_number):
        self.ring_number = ring_number

if __name__ == '__main__':
    ''' Very simple test try to create an RingSplit '''
    r = RingSplit(9)
    logging.info(r.ring_number)