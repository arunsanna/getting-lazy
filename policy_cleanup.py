import boto3
import sys
from datetime import datetime, timedelta

client = boto3.client('iam')

def decision(policy):
    while "the answer is invalid":
        reply = str(raw_input('clean policy '+policy+': ')).lower().strip()
        if reply[0] == 'y':
            return True
        if reply[0] == 'n':
            return False

#list all policies
response = client.list_policies(
    Scope='Local',
    OnlyAttached=False
)

for n in response['Policies']:
    policy = n['PolicyName']
    arn = n['Arn']
    if decision(policy):
        print "removing "+policy
        resp_del = client.delete_policy(PolicyArn=arn)
    else:
        print "Leaving "+policy
