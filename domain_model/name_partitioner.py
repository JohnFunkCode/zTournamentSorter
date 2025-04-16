# done - record the scores in a collection in the class.
# done - the winner is the one with the lowest score, and the lowest spread_score
# done - calculate the number of buckets, and only test that number and that number +1 to account for the edge cases.
# done - connect this back up to the test harness
# tbd - test this all with a few of the edge cases we've cooked up
# tbd - run tests with the big test data set
# tbd - think about refactoring the return values to make it easier to call from the tournament code - probably return a list with the partition boundaries.
# tbd - see if a recursive version is still understandable enough that you could debug it in a year.
# tbd - clean up comments and logging for production use

import logging
import os
import sys
from datetime import datetime
import math

import pandas
import pandas as pd

class NamePartionioner:
    ''' class to manage split a list of competitor's into even groups based on last name'''

    def __init__(self):
        '''setup instance variables'''
        super().__init__()
        self.list_of_scores = []
        # logging = self.initialize_logger()

    def split_into_two_partitions(self, max_entries_per_partition: int, the_data: pd.DataFrame) -> list:
        '''split the data into two partitions'''
        logging.info("split_into_two_partitions")

        i = 0
        for boundry1 in range(1, 26):
            # logging.info(f'A-{chr(64 + boundry1)}, {chr(64 + boundry1 + 1)}-{chr(64 + boundry2)}, {chr(64 + boundry2+1)}-Z')
            query_string1 = f'LastNameFirstLetter >= "A" and LastNameFirstLetter <= "{chr(64 + boundry1)}"'
            bucket1 = the_data.query(query_string1)
            sizeofbucket1 = len(bucket1)

            query_string2 = f'LastNameFirstLetter >= "{chr(64 + boundry1 + 1)}" and LastNameFirstLetter <= "Z"'
            bucket2 = the_data.query(query_string2)
            sizeofbucket2 = len(bucket2)

            bucket_variance_score = (max_entries_per_partition - sizeofbucket1) ** 2 + (
                    max_entries_per_partition - sizeofbucket2) ** 2

            spread_score = ((boundry1 - 0) ** 2 +
                            (26 - boundry1) ** 2)

            # spread_score = ((boundry1 - ord('A')) ** 2 +
            #           (ord('Z') - boundry1) ** 2)

            if (max_entries_per_partition < sizeofbucket1) or (max_entries_per_partition < sizeofbucket2):
                bucket_variance_score = 65535

            if (bucket_variance_score < 65535):
                logging.info(f'A-{chr(64 + boundry1)}:{sizeofbucket1}:{boundry1 - 0}, '
                             f'{chr(64 + boundry1 + 1)}-Z::{sizeofbucket2}:{26 - boundry1} '
                             f'- bucket_variance_score={bucket_variance_score} spread_score={spread_score}')
                self.list_of_scores.append({'bucket_variance_score': bucket_variance_score,
                                            'spread_score': spread_score,
                                            'boundaries': (['A', chr(64 + boundry1)],
                                                           [chr(64 + boundry1 + 1), 'Z'])})

            i = i + 1
        logging.info(f'evaluated {i} two partition combinations. {len(self.list_of_scores)} solutions found')

    def split_into_three_partitions(self, max_entries_per_partition: int, the_data: pd.DataFrame) -> list:
        logging.info("split_into_three_partitions")
        i = 0
        for boundry1 in range(1, 26):
            # logging.info(f'A-{chr(64+boundry1)}')
            for boundry2 in range(boundry1 + 1, 26):
                # logging.info(f'A-{chr(64 + boundry1)}, {chr(64 + boundry1 + 1)}-{chr(64 + boundry2)}, {chr(64 + boundry2+1)}-Z')
                query_string1 = f'LastNameFirstLetter >= "A" and LastNameFirstLetter <= "{chr(64 + boundry1)}"'
                bucket1 = the_data.query(query_string1)
                sizeofbucket1 = len(bucket1)

                query_string2 = f'LastNameFirstLetter >= "{chr(64 + boundry1 + 1)}" and LastNameFirstLetter <= "{chr(64 + boundry2)}"'
                bucket2 = the_data.query(query_string2)
                sizeofbucket2 = len(bucket2)

                query_string3 = f'LastNameFirstLetter >= "{chr(64 + boundry2 + 1)}" and LastNameFirstLetter <= "Z"'
                bucket3 = the_data.query(query_string3)
                sizeofbucket3 = len(bucket3)

                bucket_variance_score = (max_entries_per_partition - sizeofbucket1) ** 2 + (
                        max_entries_per_partition - sizeofbucket2) ** 2 + (
                                                max_entries_per_partition - sizeofbucket3) ** 2

                spread_score = ((boundry1 - 0) ** 2 +
                                (boundry2 - boundry1) ** 2 +
                                (26 - boundry2) ** 2)

                # spread_score = ( (boundry1 - ord('A')) ** 2 +
                #            (boundry2 - boundry1) ** 2 +
                #            (ord('Z') - boundry2) ** 2)

                if (max_entries_per_partition < sizeofbucket1) or (max_entries_per_partition < sizeofbucket2) or (
                        max_entries_per_partition < sizeofbucket3):
                    bucket_variance_score = 65535

                if (bucket_variance_score < 65535):
                    logging.info(f'A-{chr(64 + boundry1)}:{sizeofbucket1}:{boundry1 - 0}, '
                                 f'{chr(64 + boundry1 + 1)}-{chr(64 + boundry2)}:{sizeofbucket2}:{boundry2 - boundry1}, '
                                 f'{chr(64 + boundry2 + 1)}-Z:{sizeofbucket3}:{26 - boundry2} '
                                 f'- bucket_variance_score={bucket_variance_score} spread_score={spread_score}')
                    self.list_of_scores.append({'bucket_variance_score': bucket_variance_score,
                                                'spread_score': spread_score,
                                                'boundaries': (['A', chr(64 + boundry1)],
                                                               [chr(64 + boundry1 + 1), chr(64 + boundry2)],
                                                               [chr(64 + boundry2 + 1), 'Z'])})

                i = i + 1
        logging.info(f'evaluated {i} three partition combinations. {len(self.list_of_scores)} solutions found')

    def split_into_four_partitions(self, max_entries_per_partition: int, the_data: pd.DataFrame) -> list:
        logging.info("split_into_four_partitions")

        i = 0
        for boundry1 in range(1, 26):
            # logging.info(f'A-{chr(64+boundry1)}')
            for boundry2 in range(boundry1 + 1, 26):
                for boundry3 in range(boundry2 + 1, 26):
                    # logging.info(f'A-{chr(64 + boundry1)}, {chr(64 + boundry1 + 1)}-{chr(64 + boundry2)}, {chr(64 + boundry2 + 1)}-{chr(64 + boundry3)}, {chr(64 + boundry3+1)}-Z')
                    query_string1 = f'LastNameFirstLetter >= "A" and LastNameFirstLetter <= "{chr(64 + boundry1)}"'
                    bucket1 = the_data.query(query_string1)
                    sizeofbucket1 = len(bucket1)

                    query_string2 = f'LastNameFirstLetter >= "{chr(64 + boundry1 + 1)}" and LastNameFirstLetter <= "{chr(64 + boundry2)}"'
                    bucket2 = the_data.query(query_string2)
                    sizeofbucket2 = len(bucket2)

                    query_string3 = f'LastNameFirstLetter >= "{chr(64 + boundry2 + 1)}" and LastNameFirstLetter <= "{chr(64 + boundry3)}"'
                    bucket3 = the_data.query(query_string3)
                    sizeofbucket3 = len(bucket3)

                    query_string4 = f'LastNameFirstLetter >= "{chr(64 + boundry3 + 1)}" and LastNameFirstLetter <= "Z"'
                    bucket4 = the_data.query(query_string4)
                    sizeofbucket4 = len(bucket4)

                    bucket_variance_score = ((max_entries_per_partition - sizeofbucket1) ** 2 +
                                             (max_entries_per_partition - sizeofbucket2) ** 2 +
                                             (max_entries_per_partition - sizeofbucket3) ** 2)

                    spread_score = ((boundry1 - 0) ** 2 +
                                    (boundry2 - boundry1) ** 2 +
                                    (boundry3 - boundry2) ** 2 +
                                    (26 - boundry3) ** 2)

                    # spread_score = ((boundry1 - ord('A')) ** 2 +
                    #           (boundry2 - boundry1) ** 2 +
                    #           (boundry3 - boundry2) ** 2 +
                    #           (ord('Z') - boundry3) ** 2)

                    if (max_entries_per_partition < sizeofbucket1) or (max_entries_per_partition < sizeofbucket2) or (
                            max_entries_per_partition < sizeofbucket3) or (max_entries_per_partition < sizeofbucket4):
                        bucket_variance_score = 65535

                    if (sizeofbucket1 == 0) or (sizeofbucket2 == 0) or (sizeofbucket3 == 0) or (sizeofbucket4 == 0):
                        bucket_variance_score = 65535

                    if (bucket_variance_score < 65535):
                        logging.info(f'A-{chr(64 + boundry1)}:{sizeofbucket1}:{boundry1 - 0}, '
                                     f'{chr(64 + boundry1 + 1)}-{chr(64 + boundry2)}:{sizeofbucket2}:{boundry2 - boundry1}, '
                                     f'{chr(64 + boundry2 + 1)}-{chr(64 + boundry3)}:{sizeofbucket3}:{boundry3 - boundry2}, '
                                     f'{chr(64 + boundry3 + 1)}-Z:{sizeofbucket4}:{26 - boundry3} '
                                     f'- bucket_variance_score={bucket_variance_score} spread_score={spread_score}')
                        self.list_of_scores.append(
                            {'bucket_variance_score': bucket_variance_score, 'spread_score': spread_score,
                             'boundaries': (['A', chr(64 + boundry1)],
                                            [chr(64 + boundry1 + 1), chr(64 + boundry2)],
                                            [chr(64 + boundry2 + 1), chr(64 + boundry3)],
                                            [chr(64 + boundry3 + 1), 'Z'])})

                    i = i + 1
        logging.info(f'evaluated {i} four partition combinations. {len(self.list_of_scores)} solutions found')

    # def get_partition_boundaries(self, the_data:pd.DataFrame, max_entries_per_partition:int) -> list:
    #     logging.info(the_data)
    #
    #     # calculate the number of partitions
    #     number_of_partitions = math.ceil((len(the_data) / max_entries_per_partition))
    #     logging.info(f'number_of_partitions:', number_of_partitions)
    #
    #     return [{'A','F'},{'G','L'},{'M','R'}]
    def get_optimum_partition_boundaries(self, the_data: pandas.DataFrame, min_number_of_partitions: int ,max_entries_per_partition: int) -> list:
        assert min_number_of_partitions >= 0, "min_number_of_partitions must be greater than or equal to 0"
        size_of_dataframe = len(the_data)
        expected_partitions = math.ceil(size_of_dataframe / max_entries_per_partition)
        logging.info(
            f'data size:{size_of_dataframe}, max people per partition: {max_entries_per_partition}, expected_partitions: {expected_partitions} or {expected_partitions + 1}')

        # don't create more than 4 partitions - something is wrong if we get to this point
        if (expected_partitions > 4):
            logging.error(
                f'Too much data to split into maximum of 4 partitions - data size:{size_of_dataframe}, max people per partition: {max_entries_per_partition}, would require: {expected_partitions} or {expected_partitions + 1} partitions')
            raise ValueError(
                f'Too much data to split into the maximum of 4 partitions - data size:{size_of_dataframe}, max people per partition: {max_entries_per_partition}, would require: {expected_partitions} or {expected_partitions + 1} partitions')
            # return [['A', 'Z']]

        # don't create less partitions than specified
        if (expected_partitions < min_number_of_partitions):
            logging.info(f'Data could be put into {expected_partitions} partitions, but specified number {min_number_of_partitions} will be used instead')
            expected_partitions = min_number_of_partitions

        # Add a column to the data with the first letter of the 'Last Name' field
        the_data_with_LastNameFirstLetter = the_data.copy()
        the_data_with_LastNameFirstLetter['LastNameFirstLetter'] = the_data_with_LastNameFirstLetter['Last_Name'].str[0]
        logging.debug(the_data)

        match expected_partitions:
            case 1:
                return [['A', 'Z']]

            case 2:
                self.split_into_two_partitions(max_entries_per_partition, the_data_with_LastNameFirstLetter)
                if (len(self.list_of_scores) == 0):
                    logging.info("no solutions found for two partitions, trying three")
                    self.split_into_three_partitions(max_entries_per_partition, the_data_with_LastNameFirstLetter)

            case 3:
                self.split_into_three_partitions(max_entries_per_partition, the_data_with_LastNameFirstLetter)
                if (len(self.list_of_scores) == 0):
                    logging.info("no solutions found for three partitions, trying four")
                    self.split_into_four_partitions(max_entries_per_partition, the_data_with_LastNameFirstLetter)

        if len(self.list_of_scores) == 0:
            logging.error(
                f'No solutions found to partition the data into partitions of {max_entries_per_partition} entries')
            raise ValueError(
                f'No solutions found to partition the data into partitions of {max_entries_per_partition} entries')
            # return [['A', 'Z']]

        # self.split_into_two_partitions(max_entries_per_partition, the_data)
        # self.split_into_three_partitions(max_entries_per_partition, the_data)
        # self.split_into_four_partitions(max_entries_per_partition, the_data)

        # # Find the index of the element with the lowest bucket_variance_score and highest spread_score
        # min_bucket_variance_score_max_spread_score_index = min(
        #     range(len(self.list_of_scores)),
        #     key=lambda i: (self.list_of_scores[i]['bucket_variance_score'], -self.list_of_scores[i]['spread_score'])
        # )

        # Find the index of the element with the lowest bucket_variance_score and lowest spread_score
        min_bucket_variance_score_min_spread_score_index = min(
            range(len(self.list_of_scores)),
            key=lambda i: (self.list_of_scores[i]['bucket_variance_score'], self.list_of_scores[i]['spread_score'])
        )

        logging.info(
            f'Index of the element with the lowest Score and lowest spread_score: {min_bucket_variance_score_min_spread_score_index}')
        best = self.list_of_scores[min_bucket_variance_score_min_spread_score_index]

        #
        # logging.info(f'Index of the element with the lowest Score and highest spread_score: {min_bucket_variance_score_max_spread_score_index}')
        # best = self.list_of_scores[min_bucket_variance_score_max_spread_score_index]
        logging.info(best)
        logging.info(best['boundaries'])
        return best['boundaries']

    def initialize_logger(self):
        # setup logging to file and to stdout
        if (not os.path.exists("logs")):
            os.makedirs("logs")
        errorLogFileName = "logs/error_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".log"
        logger = logging.getLogger('')
        logger.setLevel(logging.INFO)
        fh = logging.FileHandler(errorLogFileName)
        sh = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter('[%(asctime)s] %(levelname)s %(message)s', datefmt='%H:%M:%S')
        fh.setFormatter(formatter)
        sh.setFormatter(formatter)
        logger.addHandler(fh)
        logger.addHandler(sh)
        return logging


if __name__ == '__main__':
    data = {
        'first_Name': ['Jack', 'Jim', 'John', 'Jane', 'Jenny', 'John'],
        'Last_Name': ['Black', 'Brown', 'Doe', 'Martinez', 'Smith', 'Zawichi']
    }
    the_data = pd.DataFrame(data)

    # # Add a column to the dataframe with the first letter of the 'Last Name' field
    # the_data['LastNameFirstLetter'] = the_data['Last_Name'].str[0]

    max_entries_per_partition = 2

    np = NamePartionioner()
    # logger=np.initialize_logger()

    np.initialize_logger()

    np.get_optimum_partition_boundaries(the_data, max_entries_per_partition)
