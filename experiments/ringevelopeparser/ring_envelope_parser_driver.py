from ring_envelope_parser import RingCollection

import os
from pathlib import Path




if __name__ == "__main__":
    # Set cwd to the directory containing this script
    os.chdir(Path(__file__).parent)



    # load your data
    rc = RingCollection.from_csv("Tourn Ring Envelope Data Base_2025_05_03-fixed_rank.csv")

    # get all events
    events = rc.get_all_events()

    # print them out
    for evt in events:
        header = (
            f"event_time: {evt.event_time} \t| "
            f"division_name: {evt.division_name} | "
            f"gender: {evt.gender} |  "
            f"minimum_age: {evt.min_age} | "
            f" maximum_age: {evt.max_age} | "
            f"ranks_label: {evt.rank_label} | "
            f"ranks: {evt.ranks} 7| "
            f"ring_info: {evt.ring_info}"
        )
        print(header)
        # for detail in evt.ring_details:
        #     print(f"  • Ring {detail['ring']}: Letter Range {detail['letter_range'] if detail['letter_range'] else 'blank'}")
        # print()  # blank line between events