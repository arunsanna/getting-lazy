import boto3
from urllib2 import urlopen

def get_regions():
    client = boto3.client('ec2')
    region_response = client.describe_regions()
    regions = [region['RegionName'] for region in region_response['Regions']]
    return regions

def decision(question,name):
    while "the answer is invalid":
        reply = str(raw_input(question+' with name: '+name+'(y/n): ')).lower().strip() 
        if reply[0] == 'y':
            return True
        if reply[0] == 'n':
            return False

def check_sg(sg_id,region):
    client = boto3.client('ec2', region_name=region)
    resp = client.describe_security_groups(GroupIds=[sg_id],)
    for m in resp['SecurityGroups']:
        for n in m['IpPermissions']:
            for cidr in n['IpRanges']:   
                print cidr['CidrIp']
                if cidr['CidrIp'] == get_ip():
                    # give a count for match
                    # if the match is 0 call the update security group else not
                    # match the damm protocol also 
                


def get_ip():
    my_ip = urlopen('http://ip.42.pl/raw').read()
    cidr = "".join((my_ip,'/32'))
    return cidr

#for region in get_regions():
#    client = boto3.client('elb', region_name=region)
#    resp = client.describe_load_balancers()
#    for m in resp['LoadBalancerDescriptions']:
#        print 'Avalible Elastic load balancers'
#        if decision('Do you want to update sg with your IP ',m['CanonicalHostedZoneName']):
#            print "Geeting all Security Groups"
#            print "Your IP address is "+get_ip()
#            print "Updating only one Security Group"
#            
#            m['SecurityGroups'][0]

check_sg('sg-0de633af9dfcf3a03','us-east-1')