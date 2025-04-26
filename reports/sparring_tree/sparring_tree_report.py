'''
Sparring_Tree_Report
Contains code to create a report containing all the sparring trees for a tournament
'''
import logging
import time
import pathlib

import pandas
from reportlab.pdfgen import canvas

import reports
from domain_model.competitors import Competitors
from reports.sparring_tree.new_eight_competitor_sparring_tree import NewEightCompetitorTree
from reports.sparring_tree.new_sixteen_competitor_sparring_tree import NewSixteenCompetitorTree
from reports.sparring_tree.thirtytwo_competitor_sparring_tree import ThirtyTwoCompetitorTree
from reports.sparring_tree.base_sparring_tree import SparringTree

import domain_model.constants as constants

SPARRING_TREE_REPORT_LETTER_FILE_NAME = "SparringTreeReport-Letter.pdf"
SPARRING_TREE_REPORT_LEGAL_FILE_NAME = "SparringTreeReport-Legal.pdf"


def create_sparring_tree( letter_canvas: canvas, legal_canvas: canvas, number_of_competitors: int, the_source_filename : str) -> SparringTree:
    ''' Factory method to create a sparring tree of the appropriate size based on the number of competitors'''
    # assert number_of_competitors <=0, "Error Less than 1 competitor"
    assert number_of_competitors <= 32, "Coding Error: More than 32 competitors provided"

    the_tree = None

    if number_of_competitors <= 8:
        the_tree = NewEightCompetitorTree(letter_canvas, the_source_filename)
    elif number_of_competitors <= 16:
        the_tree = NewSixteenCompetitorTree(letter_canvas, the_source_filename)
    elif number_of_competitors <= 32:
        the_tree = ThirtyTwoCompetitorTree(legal_canvas, the_source_filename)
    return the_tree

class SparringTreeReportPDF():
    ''' Class to Create a Sparring Tree Report for each sparring event in the tournament '''

    def __init__(self,sourcefile:str,output_folder_path:str, isCustomDivision: bool):
        if isCustomDivision:
            p=pathlib.Path(sourcefile)
            name_only = str(p.name)
            output_folder_path_no_extension = name_only[0:len(name_only)-4]
            self._letter_filename_with_path = str(pathlib.Path(output_folder_path + reports.FileHandlingUtilities.pathDelimiter() + output_folder_path_no_extension + '-' + SPARRING_TREE_REPORT_LETTER_FILE_NAME))
            self._legal_filename_with_path = str(pathlib.Path(output_folder_path + reports.FileHandlingUtilities.pathDelimiter() + output_folder_path_no_extension + '-' + SPARRING_TREE_REPORT_LEGAL_FILE_NAME))
        else:
            self._letter_filename_with_path = str(pathlib.Path(output_folder_path + reports.FileHandlingUtilities.pathDelimiter() + SPARRING_TREE_REPORT_LETTER_FILE_NAME))
            self._legal_filename_with_path = str(pathlib.Path(output_folder_path + reports.FileHandlingUtilities.pathDelimiter() + SPARRING_TREE_REPORT_LEGAL_FILE_NAME))

        ''' Create a Sparring Tree'''
        # self._letter_canvas = canvas.Canvas(SPARRING_TREE_REPORT_LETTER_FILE_NAME)
        # self._legal_canvas = canvas.Canvas(SPARRING_TREE_REPORT_LEGAL_FILE_NAME)
        self._letter_canvas = canvas.Canvas(self._letter_filename_with_path)
        self._legal_canvas = canvas.Canvas(self._legal_filename_with_path)
        self._legal_pages = 0
        # self._source_filename = "not initialized"
        self._source_filename = sourcefile

    #  seems to cause problems for debugging
    #    def __del__(self):
    #        self._canvas.save()

    def close(self):
        ''' close things out by saving the canvas'''
        self._letter_canvas.save()

        if self._legal_pages > 0:
            self._legal_canvas.save()

    def set_source_file(self, the_source_filename :str):
        ''' setup the source filename so it's available to print in the footer of each tree'''
        self._source_filename = the_source_filename


    def write_single_sparring_tree(self, event_time: str, division_name, gender: str, rank_label: str, minimum_age: int, maximum_age: int, rings: list, ranks: list, clean_df : pandas.DataFrame ):
        ''' writes a single sparring tree '''

        if (maximum_age == constants.AGELESS):
            age_label = '{0}+'.format(minimum_age)
        else:
            age_label = '{0} - {1}'.format(minimum_age, maximum_age)

        if (maximum_age == 100):
            age_label = '{0}+'.format(minimum_age)
        else:
            age_label = '{0}-{1}'.format(minimum_age, maximum_age)

        # Hack for 3 year olds
        if minimum_age == 4:
            minimum_age = 2

        logging.info("Generating Sparring Trees PDF for " + event_time + " " + division_name + " " + age_label)

        age_query = 'Age >={0} and Age <={1}'.format(minimum_age, maximum_age)

        rank_query = ''
        for r in range(0, len(ranks)):
            rank_query = rank_query + 'Rank =="' + ranks[r] + '"'
            if r < len(ranks) - 1:  # Add ' and ' to everything but the last one
                rank_query = rank_query + ' or '

        if gender != '*':
            gender_query = 'Gender == "' + gender + '"'
            combined_query = '(Events.str.contains("Sparring")) and ({0}) and ({1}) and ({2})'.format(age_query,
                                                                                                   rank_query,
                                                                                                   gender_query)
        else:
            combined_query = '(Events.str.contains("Sparring")) and ({0}) and ({1})'.format(age_query, rank_query)

        division_competitors = Competitors(clean_df.query(combined_query).sort_values("Age").sort_values("BMI"))
        t=division_competitors.get_number_of_competitors()

        ## update the hitcount every time we touch someone
        for index, row in division_competitors.iterrows():
            name = row['First_Name'] + " " + row['Last_Name']
            id = row['Registrant_ID']
            hc = clean_df.at[index, 'hitcount']
            newhc = hc + 1
            # logging.info(f'{id}:{name} has a row count of {newhc}')
            clean_df.at[index, 'hitcount'] = newhc

        #automatic split logic
        number_of_rings = len(rings)
        highest_ring_number_specified = rings[-1][0]

        if( number_of_rings >1 ):  #means we want to use autosplit
            import domain_model.name_partitioner
            np = domain_model.name_partitioner.NamePartionioner()
            partition_boundaries = np.get_optimum_partition_boundaries(the_data=division_competitors, min_number_of_partitions=number_of_rings,max_entries_per_partition=20)
            print(partition_boundaries)
            new_ring_info = []
            ring_number = rings[0][0]
            for partition in partition_boundaries:
                # in case we have more partitions than rings, we need to handle it gracefully
                if (ring_number > highest_ring_number_specified):
                    ring_number_to_display = '*TBA'
                else:
                    ring_number_to_display = str(ring_number)
                new_ring_info.append([ring_number_to_display, partition[0], partition[1]])
                ring_number = ring_number + 1
            print(new_ring_info)
            if(len(new_ring_info) < len(rings)):
                logging.warning(f'Overriding ring configuration in {division_name} Sparring for {event_time} {division_name} {age_label} {rank_label} - original rings: {rings} new rings:{new_ring_info} - results in using less rings than planned!')
            if(len(new_ring_info) > len(rings)):
                logging.warning(f'Overriding ring configuration in {division_name} Sparring for {event_time} {division_name} {age_label} {rank_label} - original rings: {rings} new rings:{new_ring_info}  - results in using MORE rings than planned!')
            if (len(new_ring_info) == len(rings)):
                logging.info(f'Overriding ring configuration in {division_name} Sparring for {event_time} {division_name} {age_label} {rank_label} - original rings: {rings} new rings:{new_ring_info}  - no change in the number of rings used!')

            rings=new_ring_info

        for info in rings:
            starting_letter=info[1]
            ending_letter=info[2]
            # Extract the first letter of the 'Last_Name' column
            division_competitors['First_Letter'] = division_competitors['Last_Name'].str[0]

            # Apply the conditions on the 'First_Letter' column
            filtered_competitors = division_competitors[(division_competitors['First_Letter'] >= starting_letter) & (division_competitors['First_Letter'] <= ending_letter) | (division_competitors['First_Letter'] >= starting_letter.lower()) & (division_competitors['First_Letter'] <= ending_letter.lower())]

            if number_of_rings > 1:  # more than 1 ring means we split
                split_lable = f'({starting_letter}-{ending_letter})'
            else:
                split_lable = ''

            # Create a tree
            tree = create_sparring_tree(self._letter_canvas, self._legal_canvas,
                                        filtered_competitors.get_number_of_competitors(), self._source_filename)
               # draw the competitors onto the tree
            tree.add_page_with_competitors_on_tree(rings[0][0], event_time, division_name, age_label, rank_label, split_lable,
                                                   filtered_competitors)


        # if len(rings) > 1:  # more than 1 ring means we split
        #     # filter to only keep contestants who's last name fall into the first alphabetic split
        #     first_alphabetic_split = division_competitors[division_competitors['Last_Name'].str.contains(constants.FIRST_ALPHABETIC_SPLIT_REGEX)]
        #     t=first_alphabetic_split.get_number_of_competitors()
        #
        #     # filter to only keep contestants who's last name fall into the second alphabetic split
        #     second_alphabetic_split = division_competitors[division_competitors['Last_Name'].str.contains(constants.SECOND_ALPHABETIC_SPLIT_REGEX)]
        #     t=first_alphabetic_split.get_number_of_competitors()
        #
        #     # Create a tree for first split
        #     tree = create_sparring_tree(self._letter_canvas, self._legal_canvas,
        #                                 first_alphabetic_split.get_number_of_competitors(), self._source_filename)
        #     # draw the competitors onto the tree
        #     tree.add_page_with_competitors_on_tree(rings[0], event_time, division_name, age_label,rank_label, split_label=constants.FIRST_ALPHABETIC_SPLIT_LABEL,
        #                                            competitors=first_alphabetic_split)
        #
        #
        #     # Create a tree for second split
        #     tree = create_sparring_tree(self._letter_canvas, self._legal_canvas,
        #                                 second_alphabetic_split.get_number_of_competitors(), self._source_filename)
        #     # draw the competitors onto the tree
        #     tree.add_page_with_competitors_on_tree(rings[1], event_time, division_name, age_label, rank_label, split_label=constants.SECOND_ALPHABETIC_SPLIT_LABEL,
        #                                            competitors=second_alphabetic_split)
        # else:
        #     # Create a tree
        #     tree = create_sparring_tree(self._letter_canvas, self._legal_canvas,
        #                                 division_competitors.get_number_of_competitors(), self._source_filename)
        #        # draw the competitors onto the tree
        #     tree.add_page_with_competitors_on_tree(rings[0], event_time, division_name, age_label, rank_label, '',
        #                                            division_competitors)


    # def write_event_to_sparring_report_using_pattern_1(self, rings: list, event_time: str, event_title,
    #                                                    event_competitors: Competitors):
    #     ''' write all the competitors in this event to the sparring tree report using output pattern 1
    #         The Pattern it writes is:
    #         White
    #         Yellow
    #         Orange
    #         Purple, Blue, Blue Stripe
    #         Green, Green Stripe
    #      '''
    #     logging.info("Generating Sparring Trees PDF for " + event_time + " " + event_title)
    #
    #     assert len(
    #         rings) != 4, "Coding Error: Not enough rings provided for this event"  # check there are just enough rings for this event
    #
    #     # white belts are the first division for this report
    #     division_competitors = event_competitors.query('Rank == @constants.WHITE_BELT')
    #
    #     # Create a tree
    #     tree = create_sparring_tree(self._letter_canvas, self._legal_canvas, division_competitors.get_number_of_competitors(),self._source_filename)
    #     # draw the competitors onto the tree
    #     tree.add_page_with_competitors_on_tree(rings[0], event_time, event_title, "White", split_label='',
    #                                            competitors=division_competitors)
    #
    #     # Yellow belts next
    #     division_competitors = event_competitors.query('Rank == @constants.YELLOW_BELT')
    #
    #     # Create a tree
    #     tree = create_sparring_tree(self._letter_canvas, self._legal_canvas, division_competitors.get_number_of_competitors(),self._source_filename)
    #     # draw the competitors onto the tree
    #     tree.add_page_with_competitors_on_tree(rings[1], event_time, event_title, "Yellow", split_label='',
    #                                            competitors=division_competitors)
    #
    #     # Orange belts next
    #     division_competitors = event_competitors.query('Rank == @constants.ORANGE_BELT')
    #
    #     # Create a tree
    #     tree = create_sparring_tree(self._letter_canvas, self._legal_canvas, division_competitors.get_number_of_competitors(),self._source_filename)
    #     # draw the competitors onto the tree
    #     tree.add_page_with_competitors_on_tree(rings[2], event_time, event_title, "Orange", split_label='',
    #                                            competitors=division_competitors)
    #
    #     # Purple, Blue, Blue Stripe
    #     division_competitors = event_competitors.query('Rank == @constants.PURPLE_BELT | Rank == @constants.BLUE_BELT | Rank == @constants.BLUE_STRIPE_BELT')
    #
    #     # Create a tree
    #     tree = create_sparring_tree(self._letter_canvas, self._legal_canvas, division_competitors.get_number_of_competitors(),self._source_filename)
    #     # draw the competitors onto the tree
    #     tree.add_page_with_competitors_on_tree(rings[3], event_time, event_title, "Purple, Blue, Blue Stripe",split_label='',
    #                                            competitors=division_competitors)
    #
    #     # Green, Green Stripe
    #     division_competitors = event_competitors.query('Rank == @constants.GREEN_BELT | Rank == @constants.GREEN_STRIPE_BELT')
    #
    #     # Create a tree
    #     tree = create_sparring_tree(self._letter_canvas, self._legal_canvas, division_competitors.get_number_of_competitors(),self._source_filename)
    #     # draw the competitors onto the tree
    #     tree.add_page_with_competitors_on_tree(rings[4], event_time, event_title, "Green, Green Stripe",split_label='',
    #                                            competitors=division_competitors)

    # def write_event_to_sparring_report_using_pattern_4(self, rings: list, event_time: str, event_title,
    #                                                    event_competitors: Competitors):
    #     ''' writes all the competitors in this event to the sparring tree report using output patter 5
    #       The pattern it writes is: Pattern4
    #       White, Yellow, Orange
    #       Purple, Blue, Blue Stripe
    #       Green, Green Stripe, Brown
    #       Black
    #     '''
    #     assert len(
    #         rings) != 3, "Coding Error: Not enough rings provided for this event"  # check there are just enough rings for this event
    #
    #     # White,  Yellow, Orange are the first division for this report
    #     division_competitors = event_competitors.query('Rank == @constants.WHITE_BELT | Rank == @constants.YELLOW_BELT | Rank == @constants.ORANGE_BELT')
    #
    #     # Create a tree
    #     tree = create_sparring_tree(self._letter_canvas, self._legal_canvas, division_competitors.get_number_of_competitors(),self._source_filename)
    #     # draw the competitors onto the tree
    #     tree.add_page_with_competitors_on_tree(rings[0], event_time, event_title, "White, Yellow, Orange",split_label='',
    #                                            competitors=division_competitors)
    #
    #     # Purple, Blue, Blue Stripe
    #     division_competitors = event_competitors.query('Rank == @constants.PURPLE_BELT | Rank == @constants.BLUE_BELT | Rank == @constants.BLUE_STRIPE_BELT')
    #
    #     # Create a tree
    #     tree = create_sparring_tree(self._letter_canvas, self._legal_canvas, division_competitors.get_number_of_competitors(),self._source_filename)
    #     # draw the competitors onto the tree
    #     tree.add_page_with_competitors_on_tree(rings[1], event_time, event_title, "Purple, Blue, Blue Stripe",split_label='',
    #                                            competitors=division_competitors)
    #
    #     # Green, Green Stripe, Brown
    #     division_competitors = event_competitors.query('Rank == @constants.GREEN_BELT | Rank == @constants.GREEN_STRIPE_BELT'
    #                                                    '| Rank == @constants.FIRST_DEGREE_BROWN_BELT | Rank == @constants.SECOND_DEGREE_BROWN_BELT'
    #                                                    '| Rank == @constants.THIRD_DEGREE_BROWN_BELT')
    #
    #     # Create a tree
    #     tree = create_sparring_tree(self._letter_canvas, self._legal_canvas, division_competitors.get_number_of_competitors(),self._source_filename)
    #     # draw the competitors onto the tree
    #     tree.add_page_with_competitors_on_tree(rings[2], event_time, event_title, "Green, Green Stripe, Brown",split_label='',
    #                                            competitors=division_competitors)
    #
    #     # Black
    #     division_competitors = event_competitors.query(
    #         'Rank == @constants.FIRST_DEGREE_BLACK_BELT | Rank == @constants.SECOND_DEGREE_BLACK_BELT | Rank == @constants.THIRD_DEGREE_BLACK_BELT | Rank == @constants.FOURTH_DEGREE_BLACK_BELT | Rank == @constants.FIFTH_DEGREE_BLACK_BELT | Rank == @constants.JUNIOR_BLACK_BELT')
    #
    #     # Create a tree
    #     tree = create_sparring_tree(self._letter_canvas, self._legal_canvas, division_competitors.get_number_of_competitors(),self._source_filename)
    #     # draw the competitors onto the tree
    #     tree.add_page_with_competitors_on_tree(rings[3], event_time, event_title, "Black", split_label='',
    #                                            competitors=division_competitors)

    # def write_event_to_sparring_report_using_pattern_5(self, rings: list, event_time: str, event_title,
    #                                                    event_competitors: Competitors):
    #     ''' writes all the competitors in this event to the sparring tree report using output patter 5
    #       The pattern it writes is: Pattern5
    #       White, Yellow
    #       Orange
    #       Purple
    #       Blue, Blue Stripe
    #       Green, Green Stripe, Brown
    #     '''
    #     assert len(
    #         rings) != 4, "Coding Error: Not enough rings provided for this event"  # check there are just enough rings for this event
    #
    #     # White and Yellow are the first division for this report
    #     division_competitors = event_competitors.query('Rank == @constants.WHITE_BELT | Rank == @constants.YELLOW_BELT')
    #
    #     # Create a tree
    #     tree = create_sparring_tree(self._letter_canvas, self._legal_canvas, division_competitors.get_number_of_competitors(),self._source_filename)
    #     # draw the competitors onto the tree
    #     tree.add_page_with_competitors_on_tree(rings[0], event_time, event_title, "White, Yellow", split_label='',
    #                                            competitors=division_competitors)
    #     # Orange belts next
    #     division_competitors = event_competitors.query('Rank == @constants.ORANGE_BELT')
    #
    #     # Create a tree
    #     tree = create_sparring_tree(self._letter_canvas, self._legal_canvas, division_competitors.get_number_of_competitors(),self._source_filename)
    #     # draw the competitors onto the tree
    #     tree.add_page_with_competitors_on_tree(rings[1], event_time, event_title, "Orange", split_label='',
    #                                            competitors=division_competitors)
    #
    #     # Purple belts next
    #     division_competitors = event_competitors.query('Rank == @constants.PURPLE_BELT')
    #
    #     # Create a tree
    #     tree = create_sparring_tree(self._letter_canvas, self._legal_canvas, division_competitors.get_number_of_competitors(),self._source_filename)
    #     # draw the competitors onto the tree
    #     tree.add_page_with_competitors_on_tree(rings[2], event_time, event_title, "Purple",split_label='',
    #                                            competitors=division_competitors)
    #
    #     # Blue, Blue Stripe
    #     division_competitors = event_competitors.query('Rank == @constants.BLUE_BELT | Rank == @constants.BLUE_STRIPE_BELT')
    #
    #     # Create a tree
    #     tree = create_sparring_tree(self._letter_canvas, self._legal_canvas, division_competitors.get_number_of_competitors(),self._source_filename)
    #     # draw the competitors onto the tree
    #     tree.add_page_with_competitors_on_tree(rings[3], event_time, event_title, "Blue, Blue Stripe", split_label='',
    #                                            competitors=division_competitors)
    #
    #     # Green, Green Stripe, Brown
    #     division_competitors = event_competitors.query('Rank == @constants.GREEN_BELT | Rank == @constants.GREEN_STRIPE_BELT'
    #                                                    '| Rank == @constants.FIRST_DEGREE_BROWN_BELT | Rank == @constants.SECOND_DEGREE_BROWN_BELT'
    #                                                    '| Rank == @constants.THIRD_DEGREE_BROWN_BELT')
    #
    #     # Create a tree
    #     tree = create_sparring_tree(self._letter_canvas, self._legal_canvas, division_competitors.get_number_of_competitors(),self._source_filename)
    #     # draw the competitors onto the tree
    #     tree.add_page_with_competitors_on_tree(rings[4], event_time, event_title, "Green, Green Stripe, Brown", split_label='',
    #                                            competitors=division_competitors)

    # def write_event_to_sparring_report_using_pattern_6(self, rings: list, event_time: str, event_title,
    #                                                    event_competitors: Competitors):
    #     ''' write all the competitors in this event to the sparring tree report using output pattern 6
    #      The Pattern it writes is:
    #        White, Yellow
    #        Orange
    #        Purple
    #        Blue, Blue Stripe
    #        Green, Green Stripe
    #        Brown
    #        Black
    #      '''
    #
    #     assert len(
    #         rings) != 6, "Coding Error: Not enough rings provided for this event"  # check there are just enough rings for this event
    #
    #     # White and Yellow are the first division for this report
    #     division_competitors = event_competitors.query('Rank == @constants.WHITE_BELT | Rank == @constants.YELLOW_BELT')
    #
    #     # Create a tree
    #     tree = create_sparring_tree(self._letter_canvas, self._legal_canvas, division_competitors.get_number_of_competitors(),self._source_filename)
    #     # draw the competitors onto the tree
    #     tree.add_page_with_competitors_on_tree(rings[0], event_time, event_title, "White, Yellow", split_label='',
    #                                            competitors=division_competitors)
    #
    #     # Orange belts next
    #     division_competitors = event_competitors.query('Rank == @constants.ORANGE_BELT')
    #
    #     # Create a tree
    #     tree = create_sparring_tree(self._letter_canvas, self._legal_canvas, division_competitors.get_number_of_competitors(),self._source_filename)
    #     # draw the competitors onto the tree
    #     tree.add_page_with_competitors_on_tree(rings[1], event_time, event_title, "Orange", split_label='',
    #                                            competitors=division_competitors)
    #
    #     # Purple belts next
    #     division_competitors = event_competitors.query('Rank == @constants.PURPLE_BELT')
    #
    #     # Create a tree
    #     tree = create_sparring_tree(self._letter_canvas, self._legal_canvas, division_competitors.get_number_of_competitors(),self._source_filename)
    #     # draw the competitors onto the tree
    #     tree.add_page_with_competitors_on_tree(rings[2], event_time, event_title, "Purple", split_label='',
    #                                            competitors=division_competitors)
    #
    #     # Blue, Blue Stripe
    #     division_competitors = event_competitors.query('Rank == @constants.BLUE_BELT | Rank == @constants.BLUE_STRIPE_BELT')
    #
    #     # Create a tree
    #     tree = create_sparring_tree(self._letter_canvas, self._legal_canvas, division_competitors.get_number_of_competitors(),self._source_filename)
    #     # draw the competitors onto the tree
    #     tree.add_page_with_competitors_on_tree(rings[3], event_time, event_title, "Blue, Blue Stripe", split_label='',
    #                                            competitors=division_competitors)
    #
    #     # Green, Green Stripe
    #     division_competitors = event_competitors.query('Rank == @constants.GREEN_BELT | Rank == @constants.GREEN_STRIPE_BELT')
    #
    #     # Create a tree
    #     tree = create_sparring_tree(self._letter_canvas, self._legal_canvas, division_competitors.get_number_of_competitors(),self._source_filename)
    #     # draw the competitors onto the tree
    #     tree.add_page_with_competitors_on_tree(rings[4], event_time, event_title, "Green, Green Stripe", split_label='',
    #                                            competitors=division_competitors)
    #
    #     # Brown
    #     division_competitors = event_competitors.query(
    #         'Rank == @constants.FIRST_DEGREE_BROWN_BELT | Rank == @constants.SECOND_DEGREE_BROWN_BELT | Rank == @constants.THIRD_DEGREE_BROWN_BELT')
    #
    #     # Create a tree
    #     tree = create_sparring_tree(self._letter_canvas, self._legal_canvas, division_competitors.get_number_of_competitors(),self._source_filename)
    #     # draw the competitors onto the tree
    #     tree.add_page_with_competitors_on_tree(rings[5], event_time, event_title, "Brown", split_label='',
    #                                            competitors=division_competitors)
    #
    #     # Black
    #     division_competitors = event_competitors.query(
    #         'Rank == @constants.FIRST_DEGREE_BLACK_BELT | Rank == @constants.SECOND_DEGREE_BLACK_BELT | Rank == @constants.THIRD_DEGREE_BLACK_BELT | Rank == @constants.FOURTH_DEGREE_BLACK_BELT | Rank == @constants.FIFTH_DEGREE_BLACK_BELT | Rank == @constants.JUNIOR_BLACK_BELT')
    #
    #     # Create a tree
    #     tree = create_sparring_tree(self._letter_canvas, self._legal_canvas, division_competitors.get_number_of_competitors(),self._source_filename)
    #     # draw the competitors onto the tree
    #     tree.add_page_with_competitors_on_tree(rings[6], event_time, event_title, "Black", split_label='',
    #                                            competitors=division_competitors)

        # we could replace the tree creation code in a module that uses a factory pattern to create the appropriate sized tree, lay down the template, draws the competitors on it and closes the tree.
        # the only question is where should that factory live?


if __name__ == '__main__':
    '''test the SparringTree Report '''
