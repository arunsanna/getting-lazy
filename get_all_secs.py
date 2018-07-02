import boto3
import sys
import os

macid = os.popen("curl -s curl http://169.254.169.254/latest/meta-data/network/interfaces/macs/").read()
url = "curl -s http://169.254.169.254/latest/meta-data/network/interfaces/macs/"+macid+"security-group-ids"
sg_id = os.popen(url).read()

#read the security group
#sg_id = str(sys.argv[1])

#Need to iterate over regions
#def get_regions():
#    client = boto3.client('ec2')
#    region_response = client.describe_regions()
#    regions = [region['RegionName'] for region in region_response['Regions']]
#    return regions
region = "us-east-1"
#iterate over regions and print
#for region in get_regions():
# client = boto3.client('ec2', region_name=region)
    #grp = client.describe_security_groups()
    #for m in grp['SecurityGroups']:
        #print m['GroupId'], region
        #if m['GroupId'] == sg_id:
            #print 'we found your SecurityGroup'
            client.revoke_security_group_ingress(
                GroupId=sg_id,
                IpPermissions=[
                    {
                        'IpProtocol': "tcp",
                        'FromPort': 22,
                        'ToPort': 22,
                        'IpRanges': [
                            {
                                'CidrIp': ''
                            }
                       ]
                    }
                ]
            )

