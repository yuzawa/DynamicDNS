import boto
from boto.route53.record import ResourceRecordSets
from boto.route53.connection import Route53Connection
import urllib2
from syslog import syslog

# ======= CONFIG ========
AWS_ACCESS_KEY_ID = 'AKIAIYJFCYZ5YGZFBGFQ'
AWS_SECRET_ACCESS_KEY = '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'
AWS_R53_ADDR = "test.manabu-yuzawa.org." # Should end in period
AWS_R53_ZONE  = "Z69OGRXUK53QL"
GET_IP_URL = "http://fedora22.manabu-yuzawa.org/cgi-bin/ip.py"
# ===== END CONFIG ======

ip = urllib2.urlopen(GET_IP_URL).read().strip()
#ip = "192.168.11.2"

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
