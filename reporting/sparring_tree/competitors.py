""" this module contains code to manage a collection of competitors """

import pandas as pd


class Competitors(pd.DataFrame):
    ''' class to manage a list of competitor'''

    @property
    def _constructor(self):
        return Competitors

    # def __init__(self, data=None, index=None, columns=None, dtype=None, copy=False):
    #     '''setup instance variables'''
    #     super().__init__(data, index, columns, dtype, copy)

    def get_number_of_competitors(self):
        '''convenience  method to get the number of competitors'''
        return self.shape[0]

    def sort_by_body_mass_index_and_dojo(self):
        ''' sort the competitors by ascending BMI and Dojo'''
        self.sort_values(by=['BMI', 'Dojo'])

    def arrange_competitors_for_sparring(self):
        ''' arrange competitors by BMI and so ajacent competitors are from different dojos (if possible) '''
        result_list = []

        comps = self

        comps.sort_by_body_mass_index_and_dojo()

        while comps.shape[0] > 1:
            name1 = comps.iloc[0]['First_Name']
            dojo1 = comps.iloc[0]['Dojo']
            name2 = ''
            # dojo2 = ''
            for i in range(1, len(comps)):
                if comps.iloc[i].Dojo != dojo1:
                    # print(i,"Different Dojo")
                    name2 = comps.iloc[i]['First_Name']
                    # dojo2 = comps.iloc[i]['Dojo']
                    break
                # else:
                # print(i,"Same Dojo")

            if name2 == '':
                name2 = comps.iloc[1]['First_Name']
                # dojo2 = comps.iloc[1]['Dojo']

            # print(name1, dojo1, '|', name2, dojo2)
            result_list.append(comps.iloc[0])
            result_list.append(comps.iloc[i])

            # remove the two names from the data frame
            df1 = comps[comps['First_Name'] != name1]
            comps = df1[df1['First_Name'] != name2]

        # if there is an odd number process the last one now0
        if (comps.shape[0] % 2) != 0:
            name1 = comps.iloc[0]['First_Name']
            dojo1 = comps.iloc[0]['Dojo']
            # print(name1, dojo1)
            result_list.append(comps.iloc[0])

        # print(result_list)
        column_names = comps.columns.values.tolist()
        # print(column_names)
        # print(result_list)
        result_df = Competitors(data=result_list, columns=column_names)
        return result_df


if __name__ == '__main__':
    '''test getting the number of compettitors '''
    cols = ['index', 'First_Name', 'Last_Name', 'Gender', 'Dojo', 'Age', 'Rank', 'Feet', 'Inches', 'Height',
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
