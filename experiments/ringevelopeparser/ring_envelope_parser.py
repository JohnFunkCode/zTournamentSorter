import csv
from collections import defaultdict
from dataclasses import dataclass
from typing import List, Optional, Dict, Any

@dataclass
class RingAssignment:
    time: str
    ring: str
    division: str
    age: str
    belt_rank: str
    letter_range: str

@dataclass
class Event:
    time: str
    division: str
    age: str
    belt_rank: str
    ring_details: List[Dict[str, Any]]  # each dict has 'ring' and 'letter_range'

class RingCollection:
    def __init__(self, assignments: Optional[List[RingAssignment]] = None):
        self.assignments = assignments or []

    @classmethod
    def from_csv(cls, path: str) -> "RingCollection":
        assignments = []
        with open(path, newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                assignments.append(RingAssignment(
                    time=row["Time:"],
                    ring=row["Ring:"],
                    division=row["Division:"],
                    age=row["Age:"],
                    belt_rank=row["Belts:"],
                    letter_range=row.get("A-Z:")
                ))
        return cls(assignments)

    def get_event(self,
                  time: str,
                  division: str,
                  age: str,
                  belt_rank: str
                  ) -> Optional[Event]:
        # collect all matching assignments
        matches = [
            a for a in self.assignments
            if a.time == time
            and a.division == division
            and a.age == age
            and a.belt_rank == belt_rank
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
            time=time,
            division=division,
            age=age,
            belt_rank=belt_rank,
            ring_details=ring_details
        )

    def get_all_events(self) -> List[Event]:
        # grouping by the four key fields
        groups: Dict[tuple, List[RingAssignment]] = defaultdict(list)
        for a in self.assignments:
            key = (a.time, a.division, a.age, a.belt_rank)
            groups[key].append(a)

        events: List[Event] = []
        for (time, division, age, belt_rank), assigns in groups.items():
            details_map = {a.ring: a.letter_range for a in assigns}
            ring_details = [
                {'ring': ring, 'letter_range': details_map[ring]}
                for ring in sorted(details_map)
            ]
            events.append(Event(time, division, age, belt_rank, ring_details))
        return events