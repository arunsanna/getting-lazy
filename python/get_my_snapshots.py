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

for region in get_regions():
    client = boto3.client('ec2', region_name= region)
    resp = client.describe_snapshots(Filters=[
        {'Name': 'tag:'+tagkey, 'Values': tagvalue}
    ])
    #print resp
    for m in resp['Snapshots']:
        tags =  m['Tags']
        for tag in tags:
            if tag['Key'] == 'Name':
                print region+' '+tag['Value']
                if tag['Key'] == 'ExpirationDate':
                    print 'Expiration Date '+tag['Value']

