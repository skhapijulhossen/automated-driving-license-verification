import re
import Extract


""" The Raw data we get as the response follows always the same pattern. (Verify this by looking at the response in white lines)
    Thus,  find_name function reads the array that contains all the data we got as response from AWS
    and then checks if the data contains the word "NAME" or "NOM" if so, the index that comes right after
    "NAME" word will be considered as the name of the person and 2 indexes after that will be considered as the last name of the person ""
"""


def find_name(data_arr, confidence_lvl, parsed_data_txt):
    for i in range(len(data_arr)):
        if ("NAME" and "NOM") in data_arr[i]:
            check_owner(data_arr[i + 1], data_arr[i + 2],
                        confidence_lvl, parsed_data_txt)
            break


""" Following function matches the regex written for fname and lname
    if it matches then it uses the replace method to replace the comma with space
    this is done to avoid the comma in the name """


def check_owner(username, lastname, confidence_lvl, parsed_data_txt):
    match_username_re = re.search(Extract.OWNER_RE, username)
    match_lastname_re = re.search(Extract.OWNER_RE, lastname)
    # with open(Extract.DRIVER_LICENSE_DATA_TXT, 'w') as the_file:
    if match_username_re:
        fname = match_username_re.string.replace(",", " ")
        print('\033[94m' + "First_name ", fname,
              '\033[0m' 'Confidence: ' + "{:.2f}".format(confidence_lvl) + "%")
        parsed_data_txt.write("First_name " + fname + "\n")
    if match_lastname_re:
        lname = match_lastname_re.string.replace(",", " ")
        print('\033[94m' + "Last_name ", lname,
              '\033[0m' 'Confidence: ' + "{:.2f}".format(confidence_lvl) + "%")
        parsed_data_txt.write("Last_name " + lname + "\n")


def rreplace(s, old, new, occurrence):
    line = s.rsplit(old, occurrence)
    return new.join(line)


def checkDL(dl_number):
    if len(dl_number) == 15:
        return dl_number
    elif len(dl_number) < 15:
        # X here means that Textract didn't recognize the number
        dl_number = dl_number + "X" * (15 - len(dl_number))
        return dl_number
    else:
        while len(dl_number) != 15:
            dl_number = rreplace(dl_number, '-', '', 1)
        return dl_number


# count variable is used to identify respective date type with switch statement for the function printTypeOfDate
date_count = 0


def printTypeOfDate(n):
    switcher = {
        1: 'Issue_Date',
        2: 'Expiration_Date',
        3: 'DOB'
    }
    return switcher.get(n, "None")
