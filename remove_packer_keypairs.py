import boto3

def get_regions():
    client = boto3.client('ec2')
    region_response = client.describe_regions()
    regions = [region['RegionName'] for region in region_response['Regions']]
    return regions

for region in get_regions():
    print region
    client = boto3.client('ec2', region_name= region)
    resp = client.describe_key_pairs() 
    print resp
    for keypair in resp['KeyPairs']:
       print keypair['KeyName']
       