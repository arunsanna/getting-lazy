from urllib2 import urlopen
import boto3
my_ip = urlopen('http://ip.42.pl/raw').read()
cidr = "".join((my_ip,'/32'))
print cidr