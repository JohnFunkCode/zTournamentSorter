'''  this module contains code to represent a ring'''
import logging

from domain_model import event
from domain_model import competitors

class Ring():
    ''' class to represent a ring'''
    ring_number = None  # example 1
    rank_lable = None  # example "White", "White, Yellow"
    last_name_filter = None
    rank_filter = None
    competitors = None

    def __init__(self, event, ring_number, last_name_filter, rank_filter):
        self.ring_number=ring_number
        self.event=event
        self.last_name_filter=last_name_filter
        self.rank_filter=rank_filter

if __name__ == '__main__':
    ''' Very simple test try to create an event '''
    r=Ring(None, 9, 'A-Z', ['White', 'Yellow'])
    logging.info(r.event, r.last_name_filter, r.rank_filter)