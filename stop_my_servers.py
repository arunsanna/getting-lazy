import boto3

#Need to iterate over regions
def get_regions():
    client = boto3.client('ec2')
    region_response = client.describe_regions()
    regions = [region['RegionName'] for region in region_response['Regions']]
    return regions

#print get_regions()
#tagkey = "Owner"
#tagvalue = ['arun.sanna']

for region in get_regions():
    client = boto3.client('ec2', region_name= region)
    resp = client.describe_instances(Filters=[
        {'Name': 'tag:'+tagkey, 'Values': tagvalue}
    ])
    for m in resp['Reservations']:
        inst = m['Instances']
        for n in inst:
            instance = n['InstanceId']
            #stop the instance
            print 'stopping the instace '+instance
            client.stop_instances(
                InstanceIds=[instance],
                Force=True
            )