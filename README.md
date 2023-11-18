
## Driver's License Eligibility
The directory `DL-check` contains the regexp matching to assign key-value pairs, along with the Renter's eligibility check for being able to rent on the platform based on DL data. This marks the first step before any subsequent steps such as the driver license abstract check happens. 
#### Test
❗ To test the script written for driver license eligibility, first ensure you have installed the dependencies and the modules used in the code by following this [README](https://github.com/batunpc/ridealike-dev/tree/main/DL-check).\
Then open the root directory in IDE  and make sure you have the Dataset folder as subdirectory<br />
```bash
cd DL-check 
python main.py
```
#### Hierarchy 

```txt
📦DL-check 
 ┣ 📂Parsed_DL_data
 ┃ ┣ 📜driver-license.json => storing in key-value pairs in JSON
 ┃ ┗ 📜driver-license.txt => key-value pairs in text format
 ┣ 📂Raw-data
 ┃ ┗ 📜raw_data.txt => storing the raw text
 ┣ 📜Extract.py => Module for regexp matching (Only executes for Ontario Licenses)
 ┣ 📜README.md 
 ┣ 📜Utils.py => Module to include helper functions
 ┗ 📜main.py => main module - checks the type of license initially if Ontario then calls Extract.py to restructure the data
```
## Driver's abstract verification

| Script                                                                    | Description                                                |
| ------------------------------------------------------------------------- | -----------------------------------------------------------
| [abstract-pdf-text.py](./abstract-algorithm/abstract-pdf-text.py)         | Same PDF processing used for reading **_Driver abstract_** |  
| [search.py](./abstract-algorithm/search.py).                              | Printing document in reading order.                        |

## Table of aws-samples
The table below demonstrates code snippets showing how Amazon Textract can be used to get insights from documents. Throughout the research, we found the following scripts that extracts text from given documents in different ways. For example the script called `detect-kv-S3.py` is used to extract data from a document in S3 bucket. To learn more about S3 buckets and how the script is used you can scroll to S3 Bucket section below, also you can refer to the [AWS S3 documentation](https://boto3.readthedocs.io/en/latest/reference/services/s3.html). However processing document using local machine was the most applicable for our use case within our time frame. Feel free to experiment with the other scripts shown below.

| Script                                                          | Description                                                     |
| ----------------------------------------------------------------| ----------------------------------------------------------------|
| [detect-kv-S3.py](./aws-samples/detect-kv-S3.py)                | Example showing processing a document in Amazon S3 bucket.      |
| [reading-order.py](./aws-samples/reading-order.py)              | Example of printing document in reading order.                  |
| [entity-comprehend.py](./aws-samples/entity-comprehend.py)      | Detecting entities and sentiment.                               |
| [pdf-text.py](./aws-samples/pdf-text.py)                        | PDF document processing.                                        |



## S3 Bucket documentation
To [create S3 Bucket](https://docs.aws.amazon.com/AmazonS3/latest/userguide/creating-bucket.html) you must have an AWS account. 

After the bucket is created, you can upload files to the bucket. Below is the code to manage the documents uploaded from S3 bucket. The API call is same as what we have done locally.



Here we are using the S3 bucket to store the documents. The bucket is created in the AWS account and the access is granted with respected permission. I have created this bucket with the following values, however you can write your own bucket/document and version name.
```python
# Document
s3BucketName = "textract-driver-licenses"
documentName = "Kevin_Front_DL.jpg"
version = "tun57W8x6cEra7SnvfybjgjqCS9voODF"

# To create Amazon Textract client
textract = boto3.client('textract', region_name=awsRegion)

```
After specifying the bucket name, document name and version, we can call the API to extract the text from the document.

```python
# API call
response = textract.detect_document_text(
    Document={
        'S3Object': {
            'Bucket': s3BucketName,
            'Name': documentName,
            'Version': version
        },
    },
)
```

❗ If you choose to use S3 buckets for storage, it is important for admins to note that S3 buckets should never be left open publicly as it poses a serious threat from scripting attacks. S3 buckets should always be made private to avoid data leaks. However, all the Textract related can be done without the use of S3 and on a local machine as well.

## Overview
The module `Extract.py` is where the detect_document_text API call and regex resides. There are several different ways of doing this API call such as using the S3 bucket (_AWS Cloud Storage Provider_) to store the documents. However our implementation uses the local machine to process the documents and does the API call with the existing `Dataset directory` in the codebase. However, the exact implementation can be used with S3 bucket as well. 
<br/>

## Requirements
Install the following:
- Python 
- [Anaconda](https://www.anaconda.com/) -> For Python environment and dependencies
- [AWS cli](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) with [AWS account](https://signin.aws.amazon.com/signin?redirect_uri=https%3A%2F%2Fconsole.aws.amazon.com%2Fconsole%2Fhome%3FhashArgs%3D%2523%26isauthcode%3Dtrue%26state%3DhashArgsFromTB_us-east-2_74612e27751b17c8&client_id=arn%3Aaws%3Asignin%3A%3A%3Aconsole%2Fcanvas&forceMobileApp=0&code_challenge=2HqpiKJXxi8LW56ddweOZqjcxXFTF4--LjUyX8_WP3A&code_challenge_method=SHA-256) -> To use AWS services
    - 1. For this step please follow the documentation [here](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-prereqs.html). This documentation will walk you through the steps to install AWS cli. Make sure you have set up the AWS cli environment providing ACCESS ID, SECRET KEY, region and output type, as it instructed in the docs.
- [Boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html#installation) -> Standard library for AWS services.  Install this library by `pip install boto3` After installation of Boto3, 
verify with the command  `boto3 --version` 

## After installation
We are using the following Python modules 
```python
import re  # This module provides regular expression matching operations
import boto3 # AWS service interface
from datetime import datetime # To get the dates from the driver-license wit the format YYYY-MM-DD
from pathlib import Path # To get the path of the file regardless of the OS
```

To specify the pathway of the corresponding directories and make it consistent in every OS, we use the `Path` module and initialize it into constants. <br />
### _Paths used in the code_
🛑 __Extract.py__
```python
# Constant that targets the Dataset directory 
DL_DATASET_FOLDER = Path(__file__).parents[1].joinpath('Dataset/Driver-License')
# Specify the particular license using the constant initialized above
DOC_NAME = DL_DATASET_FOLDER.joinpath("Amanda_Front_DL.png")

# This directory is the directory where we store end-result with key-value pairing
DRIVER_LICENSE_DATA_DIR = Path(__file__).parents[0].joinpath('Parsed_DL_data')
# Path to specify where the output key-value TXT file is stored,
DRIVER_LICENSE_DATA_TXT = DRIVER_LICENSE_DATA_DIR.joinpath("driver-license.txt")
```

🛑 __main.py__
```python
# Path to the directory where RAW TEXT stored
# This step is to check type of the license by reading from RAW TEXT file
RAW_DATA = Path(__file__).parents[0].joinpath('Raw-data')
RAW_DATA_TXT = RAW_DATA.joinpath("raw_data.txt")

file1 = open(RAW_DATA_TXT, "w")
# Writes `Raw Text` that got extracted from the document specified in Extract.py module.
for item in Extract.response["Blocks"]:
    if item["BlockType"] == "LINE":
        file1.write(item["Text"] + "\n")
file1.close()

# Check if type of DL is from Ontario
# ====================================
# if the `Ontario` is not present on the license then we will skip the KV Pair
with open(RAW_DATA_TXT) as file:
    contents = file.read()
    search_word = "Ontario"
    if search_word in contents:
        print('Ontario License found')
        Extract.restructData() # Proper key-value format for Ontario DL
    else:
        print('Not from Ontario, please contact w/ RideAlike team')

```




