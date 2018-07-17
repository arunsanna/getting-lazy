#challeges
## Note: yes we can pass the array to filter directly but I want to keep it so i can go user by user not everything at all
## 1.  adding functionality to updated tags
## 2.  function that will list all the AMIs will expire tomorrow and then ask to update the expiration date
## 3.  function that will list all instances that will expire tomorrow and update the tags
## 4.  support for multiple profiles
## 5.  check buckets with you name and tagged with your name
## 6.  get instances without tags and stop them
## 7.  How Many VPC's region by region
## 8.  How many subnet for each vpc
## 9.  How many IGW's
## 10. How many NAT Gateways
## 11. How many Security groups and inbound IP Addresses
## 12. Get sizes of S3 Buckets
## 13. ALL numbers
## 14. Git API


import boto3
import sys
from datetime import datetime, timedelta

#Need to iterate over regions
def get_regions():
    client = boto3.client('ec2')
    region_response = client.describe_regions()
    regions = [region['RegionName'] for region in region_response['Regions']]
    return regions

# this loop is if you want to read the array form the user stdin and pass it to the program
def read_tags():
    tagkey = "Owner"
    tagvalues = []
    #tagkey = raw_input("What is the keyvalue you want to scan:")
    num_array = list()
    num = raw_input("How many owners you want to scan:")
    for i in range(int(num)):
        n = raw_input("Owner Name :")
        tagvalues.append(str(n))
    print 'Scanning the owners: ',tagvalues
    return (tagvalues,tagkey)

def tag_extract(tags):
    name = 'No-Name'
    project = 'No-Project'
    environment = 'No-Environment'
    expiration = 'No-Expiration'
    for tag in tags:
        tag_name = str.lower(tag['Key'])
        if tag_name == 'name':
            name = tag['Value']
        if tag_name == 'project':
            project = tag['Value']
        if tag_name == 'environment':
            environment = tag['Value']
        if tag_name == 'expirationdate':
            expiration = tag['Value']
    return(name,expiration,project,environment)

def s_decision(question):
    while "the answer is invalid":
        reply = str(raw_input(question+' (y/n): ')).lower().strip()
        if reply[0] == 'y':
            return True
        if reply[0] == 'n':
            return False

def decision(question,id,name,project,expiration):
    while "the answer is invalid":
        reply = str(raw_input(question+'with id: '+id+' with name: '+name+' under project: '+project+' which expiration: '+expiration+' (y/n): ')).lower().strip()
        if reply[0] == 'y':
            return True
        if reply[0] == 'n':
            return False

def get_my_amis():
    tag_values,tag_key = read_tags()
    for tagvalue in tag_values():
        print 'scanning the AMI under owner '+tagvalue
        for region in get_regions():
            print 'scanning region: '+region
            client = boto3.client('ec2', region_name= region)
            resp = client.describe_images(Filters=[{'Name': 'tag:'+tag_key, 'Values': [tagvalue]}])
            for m in resp['Images']:
                tags =  m['Tags']
                name,expiration,project,environment = tag_extract(tags)
                print name+' '+expiration+' '+project+' '+environment
                if decision('Do you want to deregister AMI ',m['ImageId'],name,project,expiration):
                    print "Deregistring "+m['ImageId']
                    client.deregister_image(ImageId=m['ImageId'])
                else:
                    print "Leaving "+m['ImageId']

# this is for the snap-shots
def get_my_snapshots():
    tag_values,tag_key = read_tags()
    for tagvalue in tag_values:
        print 'scanning the snapshots under owner '+tagvalue
        for region in get_regions():
            print 'scanning the region '+region
            client = boto3.client('ec2', region_name= region)
            resp = client.describe_snapshots(Filters=[{'Name': 'tag:'+tag_key, 'Values': [tagvalue]}])
            for m in resp['Snapshots']:
                tags =  m['Tags']
                name,expiration,project,environment = tag_extract(tags)
                print name+' '+expiration+' '+project+' '+environment


#calculate the new expiration date
def get_date():
    # Need to update using user input
    print 'calculating date after next ten days'
    print datetime.now()
    #date_after = datetime.now() + timedelta(days=10)
    #date = date_after.strftime('%Y-%m-%d')
    #return(date)
    #print date

def get_my_instances():
    tag_values,tag_key = read_tags()
    for tagvalue in tag_values:
        print 'scanning the Instances under owner '+tagvalue
        for region in get_regions():
            print 'scanning region: '+region
            client = boto3.client('ec2', region_name= region)
            resp = client.describe_instances(Filters=[{'Name': 'tag:'+tag_key, 'Values': [tagvalue]}])
            for m in resp['Reservations']:
                for n in m['Instances']:
                    tags =  n['Tags']
                    name,expiration,project,environment = tag_extract(tags)
                    print name+' '+expiration+' '+project+' '+environment

                    if n['State']['Name'] == "running":
                        if decision('Do you want to stop the Instance ',n['InstanceId'],name,project,expiration):
                            print "Stoping "+n['InstanceId']
                            client.stop_instances(InstanceIds=[str(n['InstanceId'])])
                        else:
                            print "Leaving "+n['InstanceId']
                    else:
                        if decision('Do you want to Start the Instance '+name+' under project '+project+' with instance-id',n['InstanceId'],name,project,expiration):
                            print "Starting "+n['InstanceId']
                            client.start_instances(InstanceIds=[str(n['InstanceId'])])
                        else:
                            print "Leaving "+n['InstanceId']

def get_all_instances():
    print 'scanning the Instances'
    for region in get_regions():
        print 'scanning region: '+region
        client = boto3.client('ec2', region_name= region)
        resp = client.describe_instances()
        for m in resp['Reservations']:
            for n in m['Instances']:
                tags =  n['Tags']
                name,expiration,project,environment = tag_extract(tags)
                print name+' '+expiration+' '+project+' '+environment
                if n['State']['Name'] == "running":
                #    if decision('Do you want to stop the Instance ',n['InstanceId'],name,project,expiration):
                #        print "Stoping "+n['InstanceId']
                #        client.stop_instances(InstanceIds=[str(n['InstanceId'])])
                #    else:
                    print "Leaving "+n['InstanceId']
                #else:
                #    if decision('Do you want to Start the Instance '+name+' under project '+project+' with instance-id',n['InstanceId'],name,project,expiration):
                #        print "Starting "+n['InstanceId']
                #        client.start_instances(InstanceIds=[str(n['InstanceId'])])
                #    else:
                #        print "Leaving "+n['InstanceId']

#def create_ami():
    # Need to select the instance and then you need
    # Stop the Instance
    # intiate the AMI baking process
    # wait for sucessfull creation of AMI
    # start the machine back
    # Note: copy the tags compulsary
    # write the 30 day expiration period

# calling the funtions
#get_my_snapshots()
#get_my_amis()
#get_my_instances()
get_all_instances()
#get_date()
