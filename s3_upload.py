import boto3
import botocore

BUCKET_NAME = ''
KEY = 'read.py'

s3 = boto3.resource('s3')

try:
    s3.Bucket(BUCKET_NAME).upload_file(KEY, 'read.py', ExtraArgs={'ACL': 'bucket-owner-full-control'})
except botocore.exceptions.ClientError as e:
    if e.response['Error']['Code'] == "404":
        print("The object does not exist.")
    else:
        raise