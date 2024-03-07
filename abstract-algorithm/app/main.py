from pathlib import Path
import time
import timeit
import boto3
import search

RECORD_DIR = Path(__file__).parents[1].joinpath('record')
DRIVER_ABSTRACT_TXT = RECORD_DIR.joinpath("driver-abstract.txt")


# API helper functions
def start_job(client, s3_bucket_name, object_name):
    response = None
    response = client.start_document_text_detection(
        DocumentLocation={
            'S3Object': {
                'Bucket': s3_bucket_name,
                'Name': object_name
            }})

    return response["JobId"]


def is_job_complete(client, job_id):
    time.sleep(1)
    response = client.get_document_text_detection(JobId=job_id)
    status = response["JobStatus"]
    print(f"Job status: {status}")

    while status == "IN_PROGRESS":
        time.sleep(1)
        response = client.get_document_text_detection(JobId=job_id)
        status = response["JobStatus"]
        print(f"Job status: {status}")

    return status


def get_job_results(client, job_id):
    pages = []
    time.sleep(1)
    response = client.get_document_text_detection(JobId=job_id)
    pages.append(response)
    print(f"Resultset page received: {len(pages)}")
    next_token = None
    if 'NextToken' in response:
        next_token = response['NextToken']

    while next_token:
        time.sleep(1)
        response = client.\
            get_document_text_detection(JobId=job_id, NextToken=next_token)
        pages.append(response)
        print(f"Resultset page received: {len(pages)}")
        next_token = None
        if 'NextToken' in response:
            next_token = response['NextToken']
    return pages


def get_raw_data():
    # This function uses S3 Bucket
    # Document
    s3_bucket_name = "ridealike-dev"  # replace with your s3 bucket name
    # replace with your object key
    document_name = "Patre Vipin_driver_abstract_(uncertified).pdf"
    region = "us-east-1"  # replace with your region
    client = boto3.client('textract', region_name=region)

    job_id = start_job(client, s3_bucket_name, document_name)
    print(f"Started job with id: {job_id}")
    if is_job_complete(client, job_id):
        response = get_job_results(client, job_id)

    # Print detected text
    with open(DRIVER_ABSTRACT_TXT, 'w', encoding='utf8') as the_file:
        for result_page in response:
            for item in result_page["Blocks"]:
                if item["BlockType"] == "LINE":
                    the_file.write(item["Text"] + "\n")


def check_user(driver_abstract_filename):
    if search.count_flags(driver_abstract_filename) < 6:
        print("Application accepted")


if __name__ == "__main__":
    start = timeit.default_timer()
    try:
        get_raw_data()
    except Exception as e:
        print(e)
    check_user(DRIVER_ABSTRACT_TXT)
    stop = timeit.default_timer()
    print('Time taken to run the program: ', stop - start)
