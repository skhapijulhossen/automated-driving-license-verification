from pathlib import Path
import sys

CONVICTIONS_DIR = Path(__file__).parents[1].joinpath('convictions')


def nonblank_lines(f):
    # helper function to ignore white spaces in file
    for ispace in f:
        fixedline = ispace.rstrip()
        if fixedline:
            yield fixedline


# Read in the list of minor convictions
minor_convictions_lines = []
with open(CONVICTIONS_DIR.joinpath("minor-tickets.txt"), encoding='utf8') as f_in:
    for line in nonblank_lines(f_in):
        minor_convictions_lines = minor_convictions_lines + [line]
# Read in the list of major convictions
major_convictions_lines = []
with open(CONVICTIONS_DIR.joinpath("major-tickets.txt"), encoding='utf8') as f_in:
    for line in nonblank_lines(f_in):
        major_convictions_lines = major_convictions_lines + [line]
# Read in the list of serious convictions
serious_convictions_lines = []
with open(CONVICTIONS_DIR.joinpath("serious-tickets.txt"), encoding='utf8') as f_in:
    for line in nonblank_lines(f_in):
        serious_convictions_lines = serious_convictions_lines + [line]


def count_flags(driver_abstract_filename):
    # Count the number of flags based on the conviction list If serious conviction is present,
    # reject without moving on to the next list.
    flag = 0
    index = 0
    with open(driver_abstract_filename,  encoding='utf8') as file:
        for line in nonblank_lines(file):
            index += 1
            for serious_conv in serious_convictions_lines:
                if serious_conv.upper() in line.upper():
                    print("Serious conviction:  " + str(index) +
                          ": " + line + "\nApplication rejected")
                    sys.exit(1)
            for minor_conv in minor_convictions_lines:
                if minor_conv.upper() in line.upper():
                    flag += 1
                    print("Offense at line " + str(index) + ": " + line)
            for major_conv in major_convictions_lines:
                if major_conv.upper() in line.upper():
                    flag += 2
                    print("Offense at line " + str(index) + ": " + line)
            if flag >= 6:
                print("Application rejected \nDriver flags: ", flag)
                break
    file.close()
    return flag
