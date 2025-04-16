""" this code to calculate the bracket position of competitors in a sparring tree"""
import logging
from typing import Tuple

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
                       [16, 16, None],
                       [17, 2, 1],
                       [18, 4, 2],
                       [19, 6, 3],
                       [20, 8, 4],
                       [21, 10, 5],
                       [22, 12, 6],
                       [23, 14, 7],
                       [24, 16, 8],
                       [25, 18, 9],
                       [26, 20, 10],
                       [27, 22, 11],
                       [28, 24, 12],
                       [29, 26, 13],
                       [30, 28, 14],
                       [31, 30, 15],
                       [32, 32, None]]


def calculate_bracket_position_from_competitor_index(number_of_competitors: int, competitor_index: int) -> Tuple[int, int]:
    ''' calculates which spot in the bracket this competitor will occupy
        for example the 2rd person in a match with 3 competitors will end up in the second position of the first round
    '''
    competitors_in_column1 = BRAKET_POSITION_MAP[number_of_competitors][1]
    second_column_starting_index = BRAKET_POSITION_MAP[number_of_competitors][2]
    # logging.info('competitors in column 1: {} starting index for column 2: {}'.format(competitors_in_column1, second_column_starting_index))
    if competitor_index < competitors_in_column1:
        row = competitor_index + 1
        column = 1
    else:
        row = second_column_starting_index + (competitor_index - competitors_in_column1) + 1
        column = 2
    # logging.info(column,row)
    return column, row


if __name__ == '__main__':
    PEOPLE_IN_RING = 5
    for i in range(PEOPLE_IN_RING):
        x, y = calculate_bracket_position_from_competitor_index(PEOPLE_IN_RING, i)
        logging.info(x, y)
