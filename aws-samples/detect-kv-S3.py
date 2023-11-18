import json
import boto3
import re
from urllib.parse import unquote_plus

boto3.set_stream_logger('')
mySession = boto3.session.Session()
awsRegion = "us-east-2"

# Document
s3BucketName = "textract-driver-licenses"
documentName = "Kevin_Front_DL.jpg"
version = "tun57W8x6cEra7SnvfybjgjqCS9voODF"

# Amazon Textract client
textract = boto3.client('textract', region_name=awsRegion)

# Call Amazon Textract
response = textract.detect_document_text(
    Document={
        'S3Object': {
            'Bucket': s3BucketName,
            'Name': documentName,
            'Version': version
        },
    },
)


# Print text
print("\nText\n========")
text = ""
for item in response["Blocks"]:
    if item["BlockType"] == "LINE":
        print('\033[94m' + item["Text"] + '\033[0m')
        text = text + " " + item["Text"]
print(text)
# match = re.search(r"[A-Z][0-9]{4}\s*-\s*[0-9]{5}\s*-\s*[0-9]{5}",text) #[A-Z][0-9]{4}\s*-\s*[0-9]{5}\s*-\s*[0-9]{5}
# if match:
#     print('Drivers License :' + match.string[match.pos:match.endpos].replace(" ",""))
# [A-Z][0-9]{4}\s*-\s*[0-9]{5}\s*-\s*[0-9]{5}
match = re.findall(r"([A-Z][0-9]{4}\s*-\s*[0-9]{5}\s*-\s*[0-9]{5})", text)
if match:
    for item in match:
        print('Drivers License :' + item)

# Amazon Comprehend client
comprehend = boto3.client('comprehend')

# Detect sentiment
sentiment = comprehend.detect_sentiment(LanguageCode="en", Text=text)
print("\nSentiment\n========\n{}".format(sentiment.get('Sentiment')))

# Detect entities
entities = comprehend.detect_entities(LanguageCode="en", Text=text)
print("\nEntities\n========")
for entity in entities["Entities"]:
    print("{}\t=>\t{}".format(entity["Type"], entity["Text"]))
    # [A-Z][0-9]{4}\s*-\s*[0-9]{5}\s*-\s*[0-9]{5}
    match = re.search(
        "[A-Z][0-9]{4}\s*-\s*[0-9]{5}\s*-\s*[0-9]{5}", entity["Text"])
    if match:
        print('Drivers License found:' +
              match.string[match.pos:match.endpos].replace(" ", ""))
