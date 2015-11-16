#!/usr/bin/python
# -*- coding: utf-8 -*-

import boto
from boto.route53.record import ResourceRecordSets
from boto.route53.connection import Route53Connection
import urllib2
from syslog import syslog

import ConfigParser

if __name__ == "__main__":

    config = ConfigParser.SafeConfigParser()
    config.read("./config")

    GET_IP_URL = config.get("settings","GET_IP_URL")
    AWS_ACCESS_KEY_ID = config.get("settings","AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = config.get("settings","AWS_SECRET_ACCESS_KEY")
    AWS_R53_ADDR = config.get("settings","AWS_R53_ADDR")
    AWS_R53_ZONE = config.get("settings","AWS_R53_ZONE")

    print GET_IP_URL
    ip = urllib2.urlopen(GET_IP_URL).read().strip()

    print ip

    r53 = Route53Connection(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)

    records = r53.get_all_rrsets(AWS_R53_ZONE,'A',AWS_R53_ADDR,maxitems=1)[0]

    print records

    oldip = records.resource_records[0]

    print oldip

    if ip in oldip:
        print "%s exists for %s." % (ip, AWS_R53_ADDR)
    else:
        print "%s does NOT exist in %s." % (ip, AWS_R53_ADDR)
        print "Current value is %s." % (oldip)
        print "Updating records."
        r53rr = ResourceRecordSets(r53, AWS_R53_ZONE)
        print "Deleting old record."
        d_record = r53rr.add_change("DELETE", AWS_R53_ADDR, "A", 300)
        d_record.add_value(oldip)
        print "Creating updated record."
        c_record = r53rr.add_change("CREATE", AWS_R53_ADDR,"A", 300)
        c_record.add_value(ip)
        print "Committing changes."
        r53rr.commit()
        print "Records updated with new IP at %s." % (ip)
