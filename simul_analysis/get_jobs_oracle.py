#!/usr/bin/env python

import cx_Oracle
from datetime import datetime
import json

file = open("/afs/cern.ch/user/w/wguan/private/panda_connect.txt")
conStr = file.readline()
file.close()

days = 1
def get_jobs():
        jobs = []
        conn=cx_Oracle.connect(conStr)
        cursor=conn.cursor()
        sql = """
                select pandaid, eventservice, computingsite, attemptnr, jobstatus, jobsubstatus, starttime, endtime, corecount, actualcorecount, piloterrorcode, piloterrordiag, transexitcode, exeerrorcode, exeerrordiag, taskbuffererrorcode, taskbuffererrordiag from atlas_panda.jobsarchived4
                where processingtype='simul' and modificationtime>current_date-%s
            union
                select pandaid, eventservice, computingsite, attemptnr, jobstatus, jobsubstatus, starttime, endtime, corecount, actualcorecount, piloterrorcode, piloterrordiag, transexitcode, exeerrorcode, exeerrordiag, taskbuffererrorcode, taskbuffererrordiag from atlas_pandaarch.jobsarchived
                where processingtype='simul' and modificationtime>current_date-%s
        """ % (days, days)
        #print sql

        cursor.execute(sql)
        rows = cursor.fetchall()
        columns = [column[0].lower() for column in cursor.description]
        for row in rows:
            job = dict(zip(columns, row))
            if job['eventservice'] == None:
                job['eventservice'] = 'ordinary'
            if job['eventservice'] == 1:
                job['eventservice'] = 'ES'
            if job['eventservice'] == 2:
                job['eventservice'] = 'ESMerge'

            job['durationsec'] = 0
            if job['starttime'] and job['endtime']:
                duration = job['endtime'] - job['starttime']
                job['durationsec'] = duration.total_seconds()
            if job['starttime']:
                job['starttime'] = job['starttime'].strftime('%Y-%m-%d %H:%M:%S')
            if job['endtime']:
                job['endtime'] = job['endtime'].strftime('%Y-%m-%d %H:%M:%S')
            #print job
            #break
            jobs.append(job)
        return jobs


if __name__ == "__main__":
    jobs = get_jobs()
    filename = open("oracle_simul_jobs_%s_days" % days, 'wb')
    json.dump({'jobs': jobs}, filename)
    filename.close()
