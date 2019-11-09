""" this module contains code to map competitors into sparring trees"""

from reporting.sparring_tree import competitors


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
        #return self._competitors.get_number_of_competitors()
        return self._competitors.shape[0]

    def arrange_competitors_for_sparring(self, comps: competitors.Competitors) -> competitors.Competitors:
        ''' arrange competitors by BMI and so ajacent competitors are from different dojos (if possible) '''
        result_list = []

        comps.sort_by_body_mass_index_and_dojo()

        while comps.shape[0] > 1:
            name1 = comps.iloc[0]['First Name']
            dojo1 = comps.iloc[0]['Dojo']
            name2 = ''
            #dojo2 = ''
            for i in range(1, len(comps)):
                if comps.iloc[i].Dojo != dojo1:
                    # print(i,"Different Dojo")
                    name2 = comps.iloc[i]['First Name']
                    #dojo2 = comps.iloc[i]['Dojo']
                    break
                #else:
                    # print(i,"Same Dojo")

            if name2 == '':
                name2 = comps.iloc[1]['First Name']
                #dojo2 = comps.iloc[1]['Dojo']

            #print(name1, dojo1, '|', name2, dojo2)
            result_list.append(comps.iloc[0])
            result_list.append(comps.iloc[i])

            # remove the two names from the data frame
            df1 = comps[comps['First Name'] != name1]
            comps = df1[df1['First Name'] != name2]

        # if there is an odd number process the last one now0
        if (comps.shape[0] % 2) != 0:
            name1 = comps.iloc[0]['First Name']
            dojo1 = comps.iloc[0]['Dojo']
            #print(name1, dojo1)
            result_list.append(comps.iloc[0])

        # print(result_list)
        column_names = comps.columns.values.tolist()
        # print(column_names)
        # print(result_list)
        result_df = competitors.Competitors(data=result_list, columns=column_names)
        return result_df
