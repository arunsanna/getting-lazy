import boto3
import sys
from datetime import datetime, timedelta

#Need to iterate over regions
def get_regions():
    client = boto3.client('ec2')
    region_response = client.describe_regions()
    #print region_response
    regions = [region['RegionName'] for region in region_response['Regions']]
    #print regions
    return regions

#def read_tags():
    tagkey = "Environement"
    tagvalues = []
    #tagkey = raw_input("What is the keyvalue you want to scan:")
    num_array = list()
    #num = raw_input("How many owners you want to scan:")
    #for i in range(int(num)):
    #    n = raw_input("Owner Name :")
    #    tagvalues.append(str(n))
    #print 'Scanning the owners: ',tagvalues
    #return (tagvalues,tagkey)

#calcualte the new expiration date


def tag_extract(tags):
    name = 'No-Name'
    project = 'No-Project'
    environment = 'No-Environment'
    expiration = 'No-Expiration'
    for tag in tags:
        tag_name = str.lower(tag['Key'])
        if tag_name == 'name':
            name = str.lower(tag['Value'])
        if tag_name == 'project':
            project = str.lower(tag['Value'])
        if tag_name == 'environment':
            environment = str.lower(tag['Value'])
        if tag_name == 'expirationdate':
            expiration = str.lower(tag['Value'])
    return(name,expiration,project,environment)

def decision(question,id,name):
    while "the answer is invalid":
        reply = str(raw_input(question+'with id: '+id+' with name: '+name+'  (y/n): ')).lower().strip()
        if reply[0] == 'y':
            return True
        if reply[0] == 'n':
            return False

def get_my_instances():
    for region in get_regions():
        client = boto3.client('ec2', region_name= region)
        #resp = client.describe_instances(Filters=[{'Name': 'tag:'+tag_key, 'Values': [tagvalue]}])
        resp = client.describe_instances()
        for m in resp['Reservations']:
            for n in m['Instances']:
                launch_time = n['LaunchTime']
                launch_time = launch_time.replace(tzinfo=None)
                time_now = datetime.now() + timedelta(days=10)
                time_now = time_now.replace(tzinfo=None)
                delta = time_now-launch_time
                delta = str(delta)
                try:
                    tags = n['Tags']
                    name,expiration,project,environment = tag_extract(tags)
                    print environment
                    print name+' '+n['InstanceId']+' Running from:'+delta+' With Expiration: '+expiration
                except:
                    name = 'No Name'
                    tags = None
                    environment = 'undefined'
                    project = 'undefined'
                    print name+' '+n['InstanceId']+' Running from '+delta+' without tags'

                if tags is None or (n['State']['Name'] == 'running'):
                    #and not (environment == 'production')
                    print 'No tags'
                if n['State']['Name'] == "running":
                    if decision('Do you want to stop the Instance ',n['InstanceId'],name):
                        print "Stoping "+n['InstanceId']
                        client.stop_instances(InstanceIds=[str(n['InstanceId'])])
                    else:
                        print "Leaving "+n['InstanceId']
                #    else:
                #        if decision('Do you want to Start the Instance '+name+' under project '+project+' with instance-id',n['InstanceId'],name,project,expiration):
                #            print "Starting "+n['InstanceId']
                #            client.start_instances(InstanceIds=[str(n['InstanceId'])])
                #        else:
                #            print "Leaving "+n['InstanceId']

get_my_instances()
#get_regions()