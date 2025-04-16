import logging
import sys

number_of_args=len(sys.argv)
logging.info(number_of_args)

if(number_of_args) >1 :
    filename = sys.argv[1]
else:
    filename = "hardcoded.txt"

logging.info(filename)
