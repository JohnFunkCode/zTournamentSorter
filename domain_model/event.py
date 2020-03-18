''' this module contains code for an event '''

class Event():
    ''' class to represent an event '''

    name = None
    time = None
    age_range_filter = None
    rings = None


    def __init__(self, name,time, age_range):
        self.name=name
        self.time =time
        self. age_range_filter=age_range


if __name__ == '__main__':
    ''' Very simple test try to create an event '''
    e=Event('Kids Kata', '9:00', ['White'])
    print(e.name,e.time,e.age_range_filter)
