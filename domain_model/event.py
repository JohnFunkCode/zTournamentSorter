''' this module contains code for an event '''

class Event():
    ''' class to represent an event '''

    name = None
    time = None
    age_range_filter = None
    ring_numbers = None
    rings = None


    def __init__(self, name,time, age_range, ring_numbers):
        self.name=name
        self.time =time
        self. age_range_filter=age_range
        self.ring_numbers=ring_numbers

    def add_ring(self,ranks,):

if __name__ == '__main__':
    ''' Very simple test try to create an event '''
    e=Event('Kids Kata', '9:00', ['4-6'],[1,2,3,4,5,6,7,8])
    print(e.name,e.time,e.age_range_filter,e.ring_numbers)
