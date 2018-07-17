import boto3

def get_regions():
    client = boto3.client('ec2')
    region_response = client.describe_regions()
    regions = [region['RegionName'] for region in region_response['Regions']]
    return regions

#tagkey = "Owner"
#tagvalue = ['arun.sanna']

for region in get_regions():
    client = boto3.client('ec2', region_name= region)
    resp = client.describe_instances()
    for m in resp['Reservations']:
        inst = m['Instances']
        for n in inst:
            #print n
            status = n['State']['Name']
            if status == 'stopped':
                tags = n['Tags']
                for tag in tags:
                    tag_name = str.lower(tag['Key'])
                    if tag_name == 'owner':
                        tag_value = str.lower(tag['Value'])
                        print tag['Value'], (n['InstanceId']), n['LaunchTime']
