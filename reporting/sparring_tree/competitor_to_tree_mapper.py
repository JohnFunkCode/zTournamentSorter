""" this module contains code to map competitors into sparring trees"""

from reporting.sparring_tree import competitors
#from reporting.sparring_tree import eight_competitor_tree

# braket position map
# each bracket coordinate contains
# [the number of people in ring, the number of people in 1st round, second round starting position]
# None is used as a placeholder if there is no people to put in the second round
# it doesn't make sense to have a 0, or 1 person bracket but we include them to make the array indexing work nicely
BRAKET_POSITION_MAP = [[0, 0, None],  # placeholder to make array indexing work
                       [1, 1, None],  # placeholder to make array indexing work
                       [2, 2, None],
                       [3, 2, 1],
                       [4, 4, None],
                       [5, 2, 1],
                       [6, 4, 2],
                       [7, 6, 3],
                       [8, 8, None],
                       [9, 2, 1],
                       [10, 4, 2],
                       [11, 6, 3],
                       [12, 8, 4],
                       [13, 10, 5],
                       [14, 12, 6],
                       [15, 14, 7],
                       [16, 15, None]]


class CompetitorsToTreeMapper():
    ''' class to map competitors into sparring trees'''

    def __init__(self):
        '''setup instance variables'''
        self._competitors = None

    def set_competitors(self, comps: competitors.Competitors) -> object:
        """ set the list of competitors for this instance """
        self._competitors = self.arrange_competitors_for_sparring(comps)

    def get_competitors(self) -> competitors.Competitors:
        ''' get the competitors '''
        return self._competitors

    def get_number_of_competitors(self) -> int:
        ''' convenience method to return the number of competitors '''
        # return self._competitors.get_number_of_competitors()
        return self._competitors.shape[0]

    def arrange_competitors_for_sparring(self, comps: competitors.Competitors) -> competitors.Competitors:
        ''' arrange competitors by BMI and so ajacent competitors are from different dojos (if possible) '''
        result_list = []

        comps.sort_by_body_mass_index_and_dojo()

        while comps.shape[0] > 1:
            name1 = comps.iloc[0]['First Name']
            dojo1 = comps.iloc[0]['Dojo']
            name2 = ''
            # dojo2 = ''
            for i in range(1, len(comps)):
                if comps.iloc[i].Dojo != dojo1:
                    # print(i,"Different Dojo")
                    name2 = comps.iloc[i]['First Name']
                    # dojo2 = comps.iloc[i]['Dojo']
                    break
                # else:
                # print(i,"Same Dojo")

            if name2 == '':
                name2 = comps.iloc[1]['First Name']
                # dojo2 = comps.iloc[1]['Dojo']

            # print(name1, dojo1, '|', name2, dojo2)
            result_list.append(comps.iloc[0])
            result_list.append(comps.iloc[i])

            # remove the two names from the data frame
            df1 = comps[comps['First Name'] != name1]
            comps = df1[df1['First Name'] != name2]

        # if there is an odd number process the last one now0
        if (comps.shape[0] % 2) != 0:
            name1 = comps.iloc[0]['First Name']
            dojo1 = comps.iloc[0]['Dojo']
            # print(name1, dojo1)
            result_list.append(comps.iloc[0])

        # print(result_list)
        column_names = comps.columns.values.tolist()
        # print(column_names)
        # print(result_list)
        result_df = competitors.Competitors(data=result_list, columns=column_names)
        return result_df

    # def calculate_bracket_position_from_competitor_index(self, competitor_index: int) -> Tuple[int, int]:
    #     ''' calculates which spot in the bracket this competitor will occupy
    #         for example the 2rd person in a match with 3 competitors will end up in the second position of the first round
    #     '''
    #     compettitors_in_column1 = BRAKET_POSITION_MAP[self.get_number_of_competitors()][1]
    #     # print('competitors in column 1:',compettitors_in_column1)
    #     second_column_starting_index = BRAKET_POSITION_MAP[self.get_number_of_competitors()][2]
    #     # print('starting index for column 2:',second_column_starting_index)
    #     if competitor_index < compettitors_in_column1:
    #         column = competitor_index + 1
    #         row = 1
    #     else:
    #         column = second_column_starting_index + (competitor_index - compettitors_in_column1) + 1
    #         row = 2
    #     # print(column,row)
    #     return column, row

    # def calculate_canvas_coordinates_from_competitor_index(self, tree: eight_competitor_tree, competitor_index: int):
    #     x, y = self.calculate_bracket_position_from_competitor_index(competitor_index)
    #     print('backet coordinate: ', x, y)
    #     if x == 1:
    #         x_coordinate, y_coordinate = tree.get_canvas_coord_for_nth_competitor_in_column1(competitor_index)
    #     else:
    #         x_coordinate, y_coordinate = tree.get_canvas_coord_for_nth_competitor_in_column1(competitor_index)
    #     print('canvas coordinate: ', x_coordinate, y_coordinate)
    #     return x_coordinate, y_coordinate


if __name__ == '__main__':
    cols = ['index', 'First Name', 'Last Name', 'Gender', 'Dojo', 'Age', 'Rank', 'Feet', 'Inches', 'Height',
            'Weight', 'BMI', 'Events', 'Weapons', 'hitcount']
    data = [(1, 'Katie', 'coleson', 'Female', 'CO- Parker', 12, 'White', 4, 0, '4', 65, 161,
             '2 Events - Forms & Sparring ($75)', 'Weapons ($35)', 0),
            (2, 'Lucas', 'May', 'Male', 'CO- Cheyenne Mountain', 10, 'Yellow', 4, 3, '4 ft. 3 in.', 52, 154,
             '2 Events - Forms & Sparring ($75)', 'None', 0),
            (3, 'Jake', 'Coleson', 'Male', 'CO- Cheyenne Mountain', 10, 'Yellow', 4, 0, '4', 60, 156,
             '2 Events - Forms & Sparring ($75)', 'Weapons ($35)', 0),
            (4, 'Allen', 'Whitaker', 'Male', 'CO- Arvada', 10, 'Yellow', 4, 0, '4', 55, 151,
             '2 Events - Forms & Sparring ($75)', 'Weapons ($35)', 0),
            (5, 'Bill', 'Kable', 'Male', 'CO- Cheyenne Mountain', 10, 'Yellow', 4, 1, '4', 63, 161,
             '2 Events - Forms & Sparring ($75)', 'Weapons ($35)', 0)]

    c = competitors.Competitors(data, columns=cols)  # create a list of competitors from the test data above
    competitor_mapper = CompetitorsToTreeMapper()
    competitor_mapper.set_competitors(c)
    n = competitor_mapper.get_number_of_competitors()
    print('Number of competitors:', n)
