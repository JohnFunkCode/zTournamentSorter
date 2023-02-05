#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import requests
import json
import csv

# API endpoint for namey
# https://namey.muffinlabs.com/name.json?count=10&type=female&with_surname=true&frequency=common
# https://namey.muffinlabs.com/name.json?count=10&type=male&with_surname=true&frequency=common

fields = ['First Name','Last Name']

bothurl = "https://namey.muffinlabs.com/name.json?count=10&with_surname=true&frequency=common"
maleurl = "https://namey.muffinlabs.com/name.json?count=10&type=male&with_surname=true&frequency=common"
femaleurl = "https://namey.muffinlabs.com/name.json?count=10&type=female&with_surname=true&frequency=common"

urls=[['MaleNames.csv',maleurl],['FemaleNames.csv',femaleurl]]

logging.info('Generating random names.  This will take about 2 minutes.')
for url in urls:

    # Create an empty list to store names
    names = []

    logging.info(f'Writing {url[0]}', end='')

    # Loop to generate 500 names
    for i in range(50):
        # Make a GET request to the API
        logging.info('.', end='')
        time.sleep(1)
        response = requests.get(url[1])
        # Convert the response to a JSON object
        data = json.loads(response.text)
        # logging.info(f'raw data {data}')
        # Append the name to the list
        for name in data:
            s=name.split()
            # logging.info(f'first:{s[0]} last:{s[1]}')
            names.append(s)
            # names.append(name)

    with open(url[0],'w',newline='') as file:
        write=csv.writer(file)
        write.writerow(fields)
        write.writerows(names)
    logging.info()

