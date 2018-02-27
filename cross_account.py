#!/usr/bin/env python

# Python script which uses AWS STS to create short term credentials and save them to a .tf file
import os
import sys
import boto3

environmentVarsFilename = "cross_account.sh"
terraformVarsFilename = "cross_account.json"

# Print usage if proper arguments are not passed. Prompt user to provide required arguments
def usage():
  print "Missing arguments"
  print "Usage: python cross-account.py <job_id> <region> <cross_account_role>"

# Print resulting credentials in shell script
def printEnvVarsFile():
  path = os.getcwd() + '/' + environmentVarsFilename
  print path
  f = open(path,'w')
  f.write( "export ")
  f.write( "AWS_ACCESS_KEY_ID=%s " % assumedRoleObject['Credentials']['AccessKeyId'])
  f.write( "AWS_SECRET_ACCESS_KEY=%s " % assumedRoleObject['Credentials']['SecretAccessKey'])
  f.write( "AWS_SESSION_TOKEN=%s " % assumedRoleObject['Credentials']['SessionToken'])
  f.write( "AWS_DEFAULT_REGION=%s" % target_region)
  f.close()

def printJSONVarsFile():
  path = os.getcwd() + '/' + terraformVarsFilename
  print path
  f = open(path,'w')
  f.write( "{ ")
  f.write( "\"aws_access_key\": \"%s\", " % assumedRoleObject['Credentials']['AccessKeyId'])
  f.write( "\"aws_secret_key\": \"%s\", " % assumedRoleObject['Credentials']['SecretAccessKey'])
  f.write("\"aws_session_token\": \"%s\", " % assumedRoleObject['Credentials']['SessionToken'])
  f.write( "\"aws_token\" : \"%s\" " % target_region)
  f.write( "}")
  f.close()


#print len(sys.argv)
if len(sys.argv) != 4:
	usage()
	quit(1)

session_name = sys.argv[1]
target_region = sys.argv[2]
arn = sys.argv[3]

client = boto3.client('sts')
assumedRoleObject = client.assume_role( DurationSeconds=3600,RoleArn=arn,RoleSessionName=session_name,)

printEnvVarsFile()
printJSONVarsFile()
