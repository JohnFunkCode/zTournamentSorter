import sys

number_of_args=len(sys.argv)
print number_of_args

if(number_of_args) >1 :
    filename = sys.argv[1]
else:
    filename = "hardcoded.txt"

print filename
