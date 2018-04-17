#!/usr/bin/env python

import json

days = 30
file = open("simul_jobs_%s_days" % days, 'r')
jobs_file = json.load(file)
file.close()

jobs = jobs_file['jobs']
#report = {'ES': {'jobs': 0, 'walltime': 0}, 'ESMerge': {'jobs': 0, 'walltime': 0}, 'NotES': {'jobs': 0, 'walltime': 0}}
report = {}

for job in jobs:
    es = job["eventservice"]
    computingsite = job["computingsite"]
    attemptnr = job["attemptnr"]
    jobstatus = job["jobstatus"]
    jobsubstatus = job["jobsubstatus"]
    if jobsubstatus == "": jobsubstatus = 'None'
    walltime = job['durationsec']
    if not walltime or walltime == "":
        walltime = 0
    if job["starttime"]:
        corecount = job['actualcorecount']
    else:
        corecount = job['corecount']
    if es not in report:
        report[es] = {'jobs': 0, 'walltime': 0, 'walltime_time_core': 0}
    if computingsite not in report[es]:
        report[es][computingsite] = {'jobs': 0, 'walltime': 0, 'walltime_time_core': 0}
    if jobstatus not in report[es]:
        report[es][jobstatus] = {'jobs': 0, 'walltime': 0, 'walltime_time_core': 0}
    if attemptnr not in report[es]:
        report[es][attemptnr] = {'jobs': 0, 'walltime': 0, 'walltime_time_core': 0}
    if jobstatus not in report[es][attemptnr]:
        report[es][attemptnr][jobstatus] = {'jobs': 0, 'walltime': 0, 'walltime_time_core': 0}

    report[es]['jobs'] += 1
    report[es]['walltime'] += walltime
    report[es]['walltime_time_core'] += walltime * corecount

    report[es][computingsite]['jobs'] += 1
    report[es][computingsite]['walltime'] += walltime
    report[es][computingsite]['walltime_time_core'] += walltime * corecount

    report[es][jobstatus]['jobs'] += 1
    report[es][jobstatus]['walltime'] += walltime
    report[es][jobstatus]['walltime_time_core'] += walltime * corecount

    report[es][attemptnr]['jobs'] += 1
    report[es][attemptnr]['walltime'] += walltime
    report[es][attemptnr]['walltime_time_core'] += walltime * corecount

    report[es][attemptnr][jobstatus]['jobs'] += 1
    report[es][attemptnr][jobstatus]['walltime'] += walltime
    report[es][attemptnr][jobstatus]['walltime_time_core'] += walltime * corecount

print report

    
