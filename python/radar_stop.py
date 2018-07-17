import boto3
region = 'us-east-1'
instance = 'i-3bc651ab'
client = boto3.client('ec2', region_name=region)
client.stop_instances(InstanceIds=[instance])