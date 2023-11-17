
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
