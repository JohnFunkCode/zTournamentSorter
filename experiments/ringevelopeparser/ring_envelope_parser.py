import csv
from collections import defaultdict
from dataclasses import dataclass
from typing import List, Optional, Dict, Any

from domain_model import constants


@dataclass
class RingAssignment:
    event_time: str
    ring: str
    division: str
    gender: str
    min_age: int
    max_age: int
    rank_label: str
    ranks: List[str]
    letter_range: str

@dataclass
class Event:
    event_time: str
    division_name: str
    gender: str
    min_age: int
    max_age: int
    rank_label: str
    ranks: list[str]
    ring_info: List[list[Any,str, str]]  # each dict has 'ring' and 'letter_range'

class RingCollection:
    def __init__(self, assignments: Optional[List[RingAssignment]] = None):
        self.assignments = assignments or []

    @classmethod
    def get_gender_from_event_name(cls,event_name: str) -> str:
        male = False
        female = False
        if 'Men' in event_name or 'Boy' in event_name:
            male = True
        if 'Women' in event_name or 'Girl' in event_name:
            female = True
        elif male and female:
            return '*'
        elif (not male) and (not female):
            return '*'
        elif male:
            return 'Male'
        else:
            return 'Female'

    @classmethod
    def get_belt_ranks_from_belts_string(cls, belts_string: str) -> List[str]:
        # Split the belts string by commas and strip whitespace
        belts = [belt.strip() for belt in belts_string.split(',')]
        # Filter out any empty strings
        no_empty_belts = [belt for belt in belts if belt]

        # Initialize an empty list to hold all belt ranks
        belt_ranks = []

        # For each belt string, get the expanded list and extend our result list
        for belt_string in no_empty_belts:
            expanded_ranks = constants.BELT_EXPANSION_TABLE[belt_string]
            # If expanded_ranks is a list, extend belt_ranks with it
            if isinstance(expanded_ranks, list):
                belt_ranks.extend(expanded_ranks)
            else:
                # If it's a single value, append it
                belt_ranks.append(expanded_ranks)
        return belt_ranks

    @classmethod
    def get_minimum_maximum_age_from_age_string(cls, age_string: str) -> tuple[int, int]:
        # Handle cases like "18+"
        if "+" in age_string:
            age_string = age_string.replace('+', '')  # Remove the plus sign
            age_string = age_string.replace('(', '')  # Remove any opening parenthesis
            age_string = age_string.replace(')', '')
            # Extract the number before the plus sign and convert to int
            min_age = int(age_string)
            max_age = constants.AGELESS
            return min_age, max_age

        # Otherwise split the age string by hyphen and strip whitespace
        parts = [part.strip() for part in age_string.split('-')]
        min_age = int( parts[0].replace('(',''))
        max_age = int(parts[1].replace(')',''))
        return min_age, max_age

    @classmethod
    def from_csv(cls, path: str) -> "RingCollection":
        assignments = []
        with open(path, newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if "Instructor" in row["Division:"]:
                    # Skip instructor rows
                    continue
                if "Demo" in row["Division:"]:
                    # Skip demo rows
                    continue
                assignments.append(RingAssignment(
                    event_time=row["Time:"],
                    ring=row["Ring:"],
                    division=row["Division:"],
                    gender = cls.get_gender_from_event_name(row["Division:"]),
                    min_age=cls.get_minimum_maximum_age_from_age_string(row["Age:"])[0],
                    max_age=cls.get_minimum_maximum_age_from_age_string(row["Age:"])[1],
                    # age=row["Age:"],
                    rank_label=row["Belts:"],
                    ranks=cls.get_belt_ranks_from_belts_string(row["Belts:"]),
                    letter_range=row.get("A-Z:")
                ))
        return cls(assignments)

    def get_event(self,
                  time: str,
                  division: str,
                  gender: str,
                  min_age: int,
                  max_age: int,
                  rank_label: str,
                  belt_ranks: List[str]
                  ) -> Optional[Event]:
        # collect all matching assignments
        matches = [
            a for a in self.assignments
            if a.event_time == time
               and a.division == division
               and a.gender == gender
               and a.min_age == min_age
               and a.max_age == max_age
               and a.rank_label == rank_label
               and a.ranks == belt_ranks
        ]
        if not matches:
            return None

        # build a mapping from ring -> letter_range (deduplicated)
        details_map = {a.ring: a.letter_range for a in matches}

        # produce sorted list of dicts
        ring_details = [
            {'ring': ring, 'letter_range': details_map[ring]}
            for ring in sorted(details_map)
        ]

        return Event(
            event_time=time,
            division_name=division,
            gender=gender,
            min_age=min_age,
            max_age=max_age,
            ranks=belt_ranks,
            ring_info=ring_details
        )
    #

    def get_all_events(self) -> List[Event]:
        # grouping by the key fields
        groups: Dict[tuple, List[RingAssignment]] = defaultdict(list)
        for a in self.assignments:
            # Include belt_ranks in the grouping key
            key = (a.event_time, a.division, a.gender, a.min_age, a.max_age, a.rank_label, tuple(a.ranks))
            groups[key].append(a)

        events: List[Event] = []
        for (time, division, gender, min_age, max_age, rank_label, belt_ranks_tuple), assigns in groups.items():
            # Convert belt_ranks_tuple back to a list
            belt_ranks = list(belt_ranks_tuple)

            # details_map = {a.ring: a.letter_range for a in assigns}
            # ring_details = [
            #     {'ring': ring, 'letter_range': details_map[ring]}
            #     for ring in sorted(details_map)
            # ]
            details_map = {a.ring: a.letter_range for a in assigns}
            ring_info = []

            for ring in sorted(details_map):
                letter_range = details_map[ring]
                if letter_range:
                    # Split the letter range by hyphen
                    parts = letter_range.split('-')
                    # If we have a proper range with start and end letters
                    if len(parts) == 2:
                        start_letter, end_letter = parts
                    # Handle case where there's only one letter or improper format
                    else:
                        start_letter = parts[0]
                        end_letter = parts[0]
                else:
                    # Handle empty letter range
                    start_letter = ""
                    end_letter = ""

                # Convert ring to int if possible, otherwise keep as string
                try:
                    ring_num = int(ring)
                except ValueError:
                    ring_num = ring

                ring_info.append([ring_num, start_letter, end_letter])

            events.append(Event(time, division, gender, min_age, max_age, rank_label, belt_ranks, ring_info))

        return events