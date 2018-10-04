#!/usr/bin/python3

import boto
from boto.route53.record import ResourceRecordSets
from boto.route53.connection import Route53Connection
import urllib.request, urllib.parse, urllib.error
from syslog import syslog

import configparser

def r53_ip_change(config):

    GET_IP_URL = config.get("settings","GET_IP_URL")
    AWS_ACCESS_KEY_ID = config.get("settings","AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = config.get("settings","AWS_SECRET_ACCESS_KEY")
    AWS_R53_ADDR = config.get("settings","AWS_R53_ADDR")
    AWS_R53_ZONE = config.get("settings","AWS_R53_ZONE")

#    print (GET_IP_URL)
    ip = urllib.request.urlopen(GET_IP_URL).read().strip().decode('utf-8')

#    print( type(ip) )
#    print (ip)

    r53 = Route53Connection(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)

    records = r53.get_all_rrsets(AWS_R53_ZONE,'A',AWS_R53_ADDR,maxitems=1)[0]

#    print (records)

    oldip = records.resource_records[0]

#    print (oldip)

    if ip not in oldip:
        print("{0} does Not exist in {1}".format(ip, AWS_R53_ADDR))
        print("Current value is {0}.",format(oldip))
        print("Updating records.")
        r53rr = ResourceRecordSets(r53, AWS_R53_ZONE)
        print("Deleting old record.")
        d_record = r53rr.add_change("DELETE", AWS_R53_ADDR, "A", 300)
        d_record.add_value(oldip)
        print("Creating updated record.")
        c_record = r53rr.add_change("CREATE", AWS_R53_ADDR,"A", 300)
        c_record.add_value(ip)
        print("Committing changes.")
        r53rr.commit()
        print("Records updated with new IP at {0}.".format(ip))
#    else:
#        print("{0} exists for {1}".format(ip, AWS_R53_ADDR))

if __name__ == "__main__":

    config = configparser.SafeConfigParser()

    try:
        config.read("/usr/local/lib/getmyip/config")

        r53_ip_change(config)

    except configparser.Error as e:
        print("type:{0}".format(type(e)))
        print("args:{0}".format(e.args))
        print("message:{0}".format(e.message))
        print("{0}".format(e))
