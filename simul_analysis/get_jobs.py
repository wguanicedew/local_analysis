#!/usr/bin/env python

import json
import requests
import pickle
import re
import datetime,time


days_ago = 10

bot = datetime.datetime(1970,1,1)
enddt = datetime.datetime.utcnow()
startdt = enddt - datetime.timedelta(days=days_ago)
enddtstr = str(enddt.year) + '-' + str(enddt.month).zfill(2) + '-' + str(enddt.day).zfill(2)
startdtstr = str(startdt.year) + '-' + str(startdt.month).zfill(2) + '-' + str(startdt.day).zfill(2)
#r = requests.get('https://bigpanda.cern.ch/jobs/?jobtype=eventservice&json=1&date_from=2017-01-08&date_to=2017-01-09', verify=False)
#r = requests.get('https://bigpanda.cern.ch/jobs/?jobtype=eventservice&json=1&date_from=2017-01-08&date_to=2017-01-09&limit=10&fields=pandaid,jobsetid,creationtime,starttime,jobstatus,endtime,computingsite', verify=False)
#url = 'https://bigpanda.cern.ch/jobs/?jobtype=eventservice&json=1&date_from=%s&date_to=%s&fields=pandaid,jobsetid,creationtime,starttime,jobstatus,endtime,computingsite' % (startdtstr, enddtstr)
url = 'https://bigpanda.cern.ch/jobs/?processingtype=simul&json=1&date_from=%s&date_to=%s' %  (startdtstr, enddtstr)

print url
try:
    r = requests.get(url, verify=False)
except:
   print r.text

try:
    ret = r.json()
    #print ret
except:
   print r.text

filename = open("simul_jobs_%s_days" % days_ago, 'wb')
json.dump(ret, filename)
filename.close()


