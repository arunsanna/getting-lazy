import boto3

#Need to iterate over regions
def get_regions():
    client = boto3.client('ec2')
    region_response = client.describe_regions()
    regions = [region['RegionName'] for region in region_response['Regions']]
    return regions

#print get_regions()
tagkey = "Owner"
tagvalue = ['arun.sanna']

def get_my_amis():
    for region in get_regions():
        client = boto3.client('ec2', region_name= region)
        resp = client.describe_images(Filters=[{'Name': 'tag:'+tagkey, 'Values': tagvalue}])
        for m in resp['Images']:
            tags =  m['Tags']
            for tag in tags:
                if tag['Key'] == 'Name':
                    print tag['Value']
                if tag['Key'] == 'ExpirationDate':
                    print tag['Value']
                if tag['Key'] == 'Project':
                    print tag['Value']

# calling the funtions
get_my_amis()