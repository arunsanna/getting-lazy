
import boto3
import urllib

s3 = boto3.resource('s3')

def lambda_handler():
    url = 'https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/index.json'
    urllib.urlretrieve( url, filename="./index.json")
    data = open('index.json', 'rb')
    try:
        s3.Bucket('arun-cloudfront-logs').put_object(Key='test.json', Body=data)
    except Exception as e:
        print e

def s3_upload(event, context):
    copy_source = {
        'Bucket': 'arun-cloudfront-logs',
        'Key': 'billing-tags-testing.csv.zip'
    }
    s3.meta.client.copy(copy_source, 'arun-sanna-s3', 'billing-tags-testing.csv.zip')
    #url = 'https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/index.json'
    #urllib.urlretrieve( url, filename='/tmp/index.json')
    #
    #data = open('/tmp/index.json', 'rb')
    #try:
    #    s3.Bucket('arun-sanna-s3').put_object(Key='test.json', Body=data)
    #except Exception as e:
    #    print e