import sys
from datetime import datetime
from pathlib import Path
import json
import time
import timeit
from dateutil import parser
import boto3

import Utils
import Extract

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel


# Dataset directory and particular driver license name
DL_DATASET_DIR = Path(__file__).parents[2].joinpath('Dataset/Driver-License')
# DOC_NAME = DL_DATASET_DIR.joinpath("qin_DL.png")
# DOC_NAME = DL_DATASET_DIR.joinpath("Keri_Front_DL.jpg")  # Alberta
# DOC_NAME = DL_DATASET_DIR.joinpath("Adhe_Front.png")  # G2 CLASS3
# DOC_NAME = DL_DATASET_DIR.joinpath("Vipin_Front_DL.png")
# DOC_NAME = DL_DATASET_DIR.joinpath("Amanda_Front_DL.png")
# DOC_NAME = DL_DATASET_DIR.joinpath("Chowd_Front_DL.png")
# DOC_NAME = DL_DATASET_DIR.joinpath("Fahmi_Front_DL.png")
# DOC_NAME = DL_DATASET_DIR.joinpath("Hossain_Front_DL.png")
# DOC_NAME = DL_DATASET_DIR.joinpath("Kamaliny_Front_DL.png")
# DOC_NAME = DL_DATASET_DIR.joinpath("Kevin_Front_DL.jpg")
# DOC_NAME = DL_DATASET_DIR.joinpath("Killah_Front_DL.png")  # Exception
# DOC_NAME = DL_DATASET_DIR.joinpath("Marjan_Front_DL.png")
# DOC_NAME = DL_DATASET_DIR.joinpath("Michael_Front_DL.png")
# DOC_NAME = DL_DATASET_DIR.joinpath("Nichani_Front_DL.png")
# =============================================================
# Directory to store the raw data in TXT file
RAW_DATA = Path(__file__).parents[1].joinpath('Raw-data')
RAW_DATA_TXT = RAW_DATA.joinpath("raw_data.txt")
# =============================================================
# Directory to store the  key-value format of the data in TXT and JSON files
DL_DATA_DIR = Path(__file__).parents[1].joinpath('Parsed_DL_data')
DL_DATA_TXT = DL_DATA_DIR.joinpath("driver-license.txt")
DL_DATA_JSON = DL_DATA_DIR.joinpath("driver-license.json")
# =============================================================


def check_type_of_license(raw_data):
    with open(raw_data, encoding='utf8') as file:
        contents = file.read()
        search_word = "Ontario" and "ON"
    file.close()
    if search_word in contents:
        return True
    return False


def write_raw_data_in_txt(res):
    with open(RAW_DATA_TXT, 'w', encoding='utf8') as file:
        for item in res:
            if item["BlockType"] == "LINE":
                file.write(item["Text"] + "\n")
    file.close()


def write_kv_pair_in_txt(res):
    with open(DL_DATA_TXT, 'w', encoding='utf8') as file:
        for item in res:
            if item["BlockType"] == "LINE":
                line = item
                # Call the function to pair the data
                Extract.restructData(item["Text"], item['Confidence'],  file)

        Utils.find_name(Extract.list_item, line['Confidence'], file)
    file.close()
    txt_to_json(DL_DATA_TXT)


def txt_to_json(txt_file):
    dict1 = {}
    with open(txt_file, encoding='utf8') as file:
        for line in file:
            # reads each line and trims of extra the spaces
            # and gives only the valid words
            command, description = line.strip().split(None, 1)
            dict1[command] = description.strip()
        file.close()
    # creating json file
    json_out_file = open(DL_DATA_JSON, "w", encoding='utf8')
    json.dump(dict1, json_out_file, indent=4, sort_keys=False)
    json_out_file.close()


def is_dates_legal():
    # Check if the driver is above 21 years old
    print("\nChecking Date of Birth...")
    # time.sleep(.5)
    date = datetime.now().date()
    is_eligible = True
    current_year = date.strftime("%Y")
    with open(DL_DATA_JSON, encoding='utf8') as file:
        json_data = json.load(file)
        # get dob from json
        date_of_birth = json_data["DOB"]
        # parse the dob date to get year only
        dob_year = parser.parse(date_of_birth).year
        # calculate the age
        age = int(current_year) - int(dob_year)
        if age < 21:
            print("Driver is below 21 years old")
            is_eligible = False
        else:  # Check if the expiry date is greater than current date
            print("Checking Expiration date...")
            # time.sleep(.5)
            exp_date = json_data["Expiration_Date"]
            exp_year = parser.parse(exp_date).year
            if int(exp_year) < int(current_year):
                print("Driver's license is expired")
                is_eligible = False
    return is_eligible


# if __name__ == "__main__":
#     while True:
#         Utils.date_count = 0
#         Extract.list_item = []
#         doc_id = input('DOC: ')
#         DOC_NAME = DL_DATASET_DIR.joinpath(doc_id)
#         start = timeit.default_timer()
#         # Read document content
#         with open(DOC_NAME, 'rb') as document:
#             imageBytes = bytearray(document.read())
#         # Amazon Textract client
#         textract = boto3.client('textract', 'us-east-1')
#         # Call Amazon Textract
#         response = textract.detect_document_text(Document={'Bytes': imageBytes})

#         # 1. Write the Raw Data in a text file
#         write_raw_data_in_txt(response["Blocks"])
#         # 2. Check if the type of license is Ontario
#         if check_type_of_license(RAW_DATA_TXT):
#             print("Ontario License\n=> Proceeding to extract...")
#             time.sleep(.5)
#             # 3. Following function will first create txt file
#             # then turn it into json
#             write_kv_pair_in_txt(response["Blocks"])
#             # 4. Check if the age is greater than 21
#             if is_dates_legal():
#                 print("=> Eligible to drive")
#             else:
#                 print("=> Not eligible to drive")
#         else:
#             sys.exit("Not an Ontario License. Please contact w/ RideAlike team")
#         stop = timeit.default_timer()
#         print('Time taken to run the program: ', stop - start)


################### API ####################

# Response Model
class DLInfo(BaseModel):
    Street: str | None
    Address: str | None
    DL_Number: str | None
    Issue_Date: str | None
    Expiration_Date: str | None
    DOB: str | None
    First_name: str | None
    Last_name: str | None
    is_valid: bool | None = False


# app __init__
app = FastAPI()


# validation API
@app.get('/validate/{doc_id}', response_model=DLInfo, status_code=200)
def validate(doc_id: str):
    DOC_NAME = DL_DATASET_DIR.joinpath(doc_id)

    # reset prevoius cache
    Utils.date_count = 0
    Extract.list_item = []

    start = timeit.default_timer()
    # Read document content
    try:
        with open(DOC_NAME, 'rb') as document:
            imageBytes = bytearray(document.read())
    except FileNotFoundError as fe:
        raise HTTPException(
            status_code=400, detail=f'Message: {fe}'
        )
    # Amazon Textract client
    textract = boto3.client('textract', 'us-east-1')
    # Call Amazon Textract
    response = textract.detect_document_text(Document={'Bytes': imageBytes})
    stop = timeit.default_timer()
    print('Time taken to Extract : ', stop - start)
    # 1. Write the Raw Data in a text file
    write_raw_data_in_txt(response["Blocks"])
    # 2. Check if the type of license is Ontario
    if check_type_of_license(RAW_DATA_TXT):
        print("Ontario License\n=> Proceeding to extract...")
        # 3. Following function will first create txt file
        # then turn it into json
        write_kv_pair_in_txt(response["Blocks"])
        json_data = None
        with open(DL_DATA_JSON, encoding='utf8') as file:
            json_data: DLInfo = json.load(file)

        # 4. Check if the age is greater than 21
        try:
            if is_dates_legal():
                print("=> Eligible to drive")
                json_data['is_valid'] = True
                return json_data
            else:
                print("=> Not eligible to drive")
                json_data['is_valid'] = False
                return json_data
        except KeyError as ke:
            raise HTTPException(
                status_code=400, detail=f'Message: {ke} not found!'
            )
    else:
        raise HTTPException(
            status_code=400, detail=f'Not an Ontario License. Please contact w/ RideAlike team'
        )
