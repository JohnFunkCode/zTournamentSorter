# experiments/ringevelopeparser/ring_envelope_parser.py
import csv
import logging
import re
from collections import defaultdict
from dataclasses import dataclass
from typing import List, Optional, Dict, Any

from domain_model import constants

# --- Helper functions ---

def get_gender_from_event_name(event_name: str) -> str:
    male = 'Men' in event_name or 'Boy' in event_name
    female = 'Women' in event_name or 'Girl' in event_name
    if male and female:
        return '*'
    if not male and not female:
        return '*'
    return 'Male' if male else 'Female'

def get_belt_ranks_from_belts_string(belts_string: str) -> List[str]:
    belts = [belt.strip() for belt in belts_string.split(',')]
    no_empty_belts = [b for b in belts if b]
    belt_ranks: List[str] = []
    for belt_string in no_empty_belts:
        try:
            expanded = constants.BELT_EXPANSION_TABLE[belt_string]
        except KeyError:
            logging.error(f"Invalid Belt specified '{belt_string}' is not found in BELT_EXPANSION_TABLE")
            raise ValueError(f"Invalid Belt specified '{belt_string}' is not found in BELT_EXPANSION_TABLE")
        if isinstance(expanded, list):
            belt_ranks.extend(expanded)
        else:
            belt_ranks.append(expanded)
    return belt_ranks

def get_minimum_maximum_age_from_age_string(age_string: str) -> tuple[int, int]:
    cleaned = age_string.replace(" ", "")
    if '+' in cleaned:
        core = cleaned.strip('()').replace('+', '')
        min_age = int(core)
        return min_age, constants.AGELESS
    # range form
    inner = cleaned.strip('()')
    parts = inner.split('-')
    if len(parts) != 2:
        raise ValueError(f"Invalid age range: {age_string}")
    min_age = int(parts[0])
    max_age = int(parts[1])
    return min_age, max_age

def is_valid_event_time(event_time: str) -> bool:
    pattern = r'^\d{1,2}:\d{2} (a\.m\.|p\.m\.|noon)$'
    return bool(re.match(pattern, event_time))

def is_valid_age(age_str: str) -> bool:
    cleaned = age_str.replace(" ", "")
    # (4-6), (7-8), (18+), (40+), (18-39)
    pattern = r'^\(\d+(?:-\d+|\+)?\)$'
    return bool(re.match(pattern, cleaned))

# --- Data classes ---

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
    ranks: List[str]
    ring_info: List[list[Any, str, str]]  # list of [ring_num, start_letter, end_letter]

# --- Collection class ---

class RingCollection:
    def __init__(self, assignments: Optional[List[RingAssignment]] = None):
        self.assignments = assignments or []

    @classmethod
    def from_csv(cls, path: str) -> "RingCollection":
        logging.info(f"Reading Ring Envelope Database CSV file: {path}")
        assignments: List[RingAssignment] = []
        with open(path, newline="") as f:
            reader = csv.DictReader(f)
            required = {"Time:", "Ring:", "Division:", "Age:", "Belts:"}
            if not required.issubset(set(reader.fieldnames or [])):
                logging.error("The Ring Envelope Database CSV file is missing one or more required columns: 'Time:', 'Ring:', 'Division:', 'Age:', 'Belts:'")
                raise ValueError("The Ring Envelope Database CSV file is missing one or more required columns: 'Time:', 'Ring:', 'Division:', 'Age:', 'Belts:'")

            for row in reader:
                division = row["Division:"]
                if "Instructor" in division or "Demo" in division:
                    continue

                event_time = row["Time:"]
                if not is_valid_event_time(event_time):
                    logging.error("The Ring Envelope Database CSV file contains an invalid event time: " + event_time)
                    raise ValueError("The Ring Envelope Database CSV file contains an invalid event time: " + event_time)

                ring = row["Ring:"]
                if division == "":
                    logging.error("The Ring Envelope Database CSV file contains an empty Division: " + ring)
                    raise ValueError("The Ring Envelope Database CSV file contains an empty Division: " + ring)

                gender = get_gender_from_event_name(division)

                age_str = row["Age:"]
                if not is_valid_age(age_str):
                    logging.error("The Ring Envelope Database CSV file contains an invalid age: " + age_str)
                    raise ValueError("The Ring Envelope Database CSV file contains an invalid age: " + age_str)

                min_age, max_age = get_minimum_maximum_age_from_age_string(age_str)
                rank_label = row["Belts:"]
                ranks = get_belt_ranks_from_belts_string(rank_label)
                letter_range = row.get("A-Z:")

                assignments.append(RingAssignment(
                    event_time=event_time,
                    ring=ring,
                    division=division,
                    gender=gender,
                    min_age=min_age,
                    max_age=max_age,
                    rank_label=rank_label,
                    ranks=ranks,
                    letter_range=letter_range
                ))
        logging.info(f"Done Reading The Ring Envelope Database CSV file: {path}")
        return cls(assignments)

    def get_event(self,
                  time: str,
                  division: str,
                  gender: str,
                  min_age: int,
                  max_age: int,
                  rank_label: str,
                  belt_ranks: List[str]) -> Optional[Event]:
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

        details_map = {a.ring: a.letter_range for a in matches}
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
            rank_label=rank_label,
            ranks=belt_ranks,
            ring_info=ring_details  # type: ignore
        )

    def get_all_events(self) -> List[Event]:
        groups: Dict[tuple, List[RingAssignment]] = defaultdict(list)
        for a in self.assignments:
            key = (a.event_time, a.division, a.gender, a.min_age, a.max_age, a.rank_label, tuple(a.ranks))
            groups[key].append(a)

        events: List[Event] = []
        for (time, division, gender, min_age, max_age, rank_label, belt_ranks_tuple), assigns in groups.items():
            belt_ranks = list(belt_ranks_tuple)
            details_map = {a.ring: a.letter_range for a in assigns}
            ring_info: List[list[Any, str, str]] = []
            for ring in sorted(details_map):
                letter_range = details_map[ring]
                if letter_range:
                    parts = letter_range.split('-')
                    if len(parts) == 2:
                        start_letter, end_letter = parts
                    else:
                        start_letter = end_letter = parts[0]
                else:
                    start_letter = end_letter = ""
                try:
                    ring_num: Any = int(ring)
                except ValueError:
                    ring_num = ring
                ring_info.append([ring_num, start_letter, end_letter])
            events.append(Event(time, division, gender, min_age, max_age, rank_label, belt_ranks, ring_info))
        return events
