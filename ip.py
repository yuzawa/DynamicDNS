#! /usr/bin/python
# coding: UTF8

import os
import sys

ip = ""

if os.environ.has_key('REMOTE_ADDR'):
    ip = os.environ['REMOTE_ADDR']

print 'Content-Type: text/text\n'
sys.stdout.write(ip)
