from __future__ import print_function
import boto3
import os
import zipfile

s3 = boto3.client('s3')
bucket = ''
key = ''
s3_path = os.path.dirname(key)
try:
    down_dir = '/tmp/test/target.zip'
    s3.download_file(bucket, key, down_dir)
    zip_ref = zipfile.ZipFile(down_dir, 'r')
    zip_ref.extractall('/tmp/test')
    zip_ref.close()
    os.remove(down_dir)
except Exception as e:
    print(e)
    raise e