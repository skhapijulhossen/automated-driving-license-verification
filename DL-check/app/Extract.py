from datetime import datetime
import re
import Utils

# REGEXP written - to get the desired data - refer to the https://regex101.com/
DL_NO_RE = r"^([A-Z](?:\d[- ]*){14})\-*$"
DATE_RE = r"(\d{4})\/(\d{1,2})\/(\d{1,2})"
CLASS_RE = r"^[G][1-3]?$"
OWNER_RE = r"^[A-Z,.\s]{3,20}$"
ADDRESS_RE = r"[ABCEGHJKLMNPRSTVXY][0-9][ABCEGHJKLMNPRSTVWXYZ] ?[0-9][ABCEGHJKLMNPRSTVWXYZ][0-9]"
ST_RE = r"\d+\s+\w+\s+(?:st(?:\.|reet)?|ave(?:\.|nue)?|lane|dr(?:\.|ive)?)|(-[0-9]+)?\d{4}(\s{1}\w{1,})(\s{1}?\w{1,})+"


# An global empty list to store the data , this is useful to identify NAME index for the function find_name
list_item = []


def restructData(item, confidence_lvl, parsed_data_txt):

    match_address = re.search(ADDRESS_RE, item, re.IGNORECASE | re.DOTALL)
    match_street = re.search(ST_RE, item, re.IGNORECASE | re.DOTALL)

    if match_street:
        print('\033[94m' + "Street ", match_street.group(),
              '\033[0m''Confidence: ' + "{:.2f}".format(confidence_lvl) + "%")
        parsed_data_txt.write("Street " + match_street.group() + "\n")

    if match_address:
        print('\033[94m' + "Address ", match_address.group(),
              '\033[0m''Confidence: ' + "{:.2f}".format(confidence_lvl) + "%")
        parsed_data_txt.write("Address " + match_address.group() + "\n")

    match_dlnumber = re.search(DL_NO_RE, item)
    if match_dlnumber and re.search(r"\s", match_dlnumber.group()):
        result = match_dlnumber.group().replace(" ", "")
        # checkDL function is used to check if the dl number is of 17 digits if not it eliminates the - from the dl number
        print('\033[94m' + 'DL_Number ', Utils.checkDL(result),
              '\033[0m' 'Confidence: ' + "{:.2f}".format(confidence_lvl) + "%")
        parsed_data_txt.write("DL_Number " + Utils.checkDL(result) + "\n")

    match_dates = re.search(DATE_RE, item)
    if match_dates and Utils.date_count < 3:
        Utils.date_count += 1
        # converting the date to date format
        date = datetime.strptime(match_dates.group(), '%Y/%m/%d').date()
        # The date in the format of YYYY/MM/DD depending on which order we have the date
        datetype = Utils.printTypeOfDate(Utils.date_count)
        result = datetype + " " + date.strftime('%Y/%m/%d')
        # For example 1st date is issue date and 2nd date is expiration date 3rd date is date of birth
        print('\033[94m' + result + '\033[0m' ' Confidence: ' +
              "{:.2f}".format(confidence_lvl) + "%")
        parsed_data_txt.write(result + "\n")

    match_class = re.search(CLASS_RE, item)
    if match_class:
        print('\033[94m' + "Class ", match_class.group(),
              '\033[0m' 'Confidence: ' + "{:.2f}".format(confidence_lvl) + "%")
        parsed_data_txt.write("Class " + match_class.group() + "\n")

    list_item.append(item)
