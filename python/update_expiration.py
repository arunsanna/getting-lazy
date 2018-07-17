import boto3
from datetime import datetime, timedelta

#Need to iterate over regions
def get_regions():
    client = boto3.client('ec2')
    region_response = client.describe_regions()
    regions = [region['RegionName'] for region in region_response['Regions']]
    return regions

#calcualte the new expiration date
date_after = datetime.now() + timedelta(days=10)
date = date_after.strftime('%Y-%m-%d')

#print get_regions()
tagkey = "Owner"
tagvalue = ['arun.sanna', 'andy.boutte', 'potluri']

for region in get_regions():
    client = boto3.client('ec2', region_name= region)
    resp = client.describe_instances(Filters=[
        {'Name': 'tag:'+tagkey, 'Values': tagvalue}
    ])
    for m in resp['Reservations']:
        inst = m['Instances']
        for n in inst:
            instance = n['InstanceId']
            print instance
            cresp = client.create_tags(
                Resources=[
                    instance
                ],
                Tags=[
                    {
                        'Key': 'ExpirationDate',
                        'Value': date
                    },
                ]
            )

#update the damm tag now
#  resp = client.describe_instances()
 # instancelist = []
 # for reservation in (response["Reservations"]):
 #     for instance in reservation["Instances"]:
 #         instancelist.append(instance["InstanceId"])
 # print(instancelist)
