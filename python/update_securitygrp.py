from urllib2 import urlopen
import boto3

#generating the security group
def get_cidr():
  my_ip = urlopen('http://ip.42.pl/raw').read()
  cidr = "".join((my_ip,'/32'))
  return cidr

#regions to iterate through
def get_regions():
    client = boto3.client('ec2')
    region_response = client.describe_regions()
    regions = [region['RegionName'] for region in region_response['Regions']]
    return regions

#my details
tagkey = "Owner"
tagvalue = ['arun.sanna']

#get the security instaces under my name
for region in get_regions():
    client = boto3.client('ec2', region_name= region)
    resp = client.describe_instances(Filters=[
        {'Name': 'tag:'+tagkey, 'Values': tagvalue}
    ])
    for m in resp['Reservations']:
        inst = m['Instances']
        for n in inst:
            security_group = n['SecurityGroups']
            for sg in security_group:
                #we need to use try and catch function here
                sgid = sg['GroupId']
                print sgid
                response = client.describe_security_groups(GroupIds=['string'])
                #client.revoke_security_group_ingress(GroupId=sgid,IpProtocol="tcp",CidrIp=get_cidr(),FromPort=100,ToPort=100)
                #client.authorize_security_group_ingress(GroupId=sgid,IpProtocol="tcp",CidrIp=get_cidr(),FromPort=100,ToPort=100)