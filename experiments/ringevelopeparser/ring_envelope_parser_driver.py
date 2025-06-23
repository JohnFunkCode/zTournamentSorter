from ring_envelope_parser import RingCollection

import os
from pathlib import Path

# Set cwd to the directory containing this script
os.chdir(Path(__file__).parent)

# load your data
rc = RingCollection.from_csv("Tourn Ring Envelope Data Base_2025_05_03.csv")

# get all events
events = rc.get_all_events()

# print them out
for evt in events:
    header = (
        f"Time: {evt.time} | Division: {evt.division} | "
        f"Age: {evt.age} | Belt: {evt.belt_rank}"
    )
    print(header)
    for detail in evt.ring_details:
        print(f"  • Ring {detail['ring']}: Letter Range {detail['letter_range'] if detail['letter_range'] else 'blank'}")
    print()  # blank line between events