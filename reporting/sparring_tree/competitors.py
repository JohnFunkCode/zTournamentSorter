""" this module contains code to manage a collection of competitors """

import pandas as pd


class Competitors(pd.DataFrame):
    ''' class to manage a list of competitor'''

    def __init__(self, data=None, index=None, columns=None, dtype=None, copy=False):
        '''setup instance variables'''
        super().__init__(data, index, columns, dtype, copy)

    def get_number_of_competitors(self):
        '''convenience  method to get the number of competitors'''
        return self.shape[0]

    def sort_by_body_mass_index_and_dojo(self):
        ''' sort the competitors by ascending BMI and Dojo'''
        self.sort_values(by=['BMI', 'Dojo'], inplace=True)


if __name__ == '__main__':
    '''test getting the number of compettitors '''
    cols = ['index', 'First Name', 'Last Name', 'Gender', 'Dojo', 'Age', 'Rank', 'Feet', 'Inches', 'Height',
            'Weight', 'BMI', 'Events', 'Weapons', 'hitcount']
    data = [(255, 'Lucas', 'May', 'Male', 'CO- Parker', 10, 'Yellow', 4, 3, '4 ft. 3 in.', 52, 154,
             '2 Events - Forms & Sparring ($75)', 'None', 0),
            (194, 'jake', 'coleson', 'Male', 'CO- Cheyenne Mountain', 10, 'Yellow', 4, 0, '4', 60, 156,
             '2 Events - Forms & Sparring ($75)', 'Weapons ($35)', 0),
            (195, 'katie', 'coleson', 'Female', 'CO- Cheyenne Mountain', 12, 'White', 4, 0, '4', 65.161,
             '2 Events - Forms & Sparring ($75)', 'Weapons ($35)', 0)]
    df = pd.DataFrame(data, columns=cols)
    #      c = competitors.Competitors(df)
    # c = Competitors()
    c = Competitors(data, columns=cols)
    s = c.get_number_of_competitors()
    print(s)
