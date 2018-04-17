#!/usr/bin/env python

import json
import matplotlib.pyplot as plt
from matplotlib import colors as mcolors

def draw_pie(labels, sizes, colors, title):
    plt.pie(sizes, labels=labels, colors=colors,
            autopct='%1.1f%%', shadow=True)
 
    plt.axis('equal')
    plt.title(title)
    plt.show()


days = 20
#file = open("simul_jobs_%s_days" % days, 'r')
file = open("oracle_simul_jobs_%s_days" % days, 'r')
jobs_file = json.load(file)
file.close()

jobs = jobs_file['jobs']
#report = {'ES': {'jobs': 0, 'walltime': 0}, 'ESMerge': {'jobs': 0, 'walltime': 0}, 'NotES': {'jobs': 0, 'walltime': 0}}
report = {}

for job in jobs:
    #print job
    es = job["eventservice"]
    computingsite = job["computingsite"]
    #if computingsite in ['LRZ-LMU_MUC_MCORE1']:
    #    break
    attemptnr = job["attemptnr"]
    jobstatus = job["jobstatus"]
    jobsubstatus = job["jobsubstatus"]
    if jobsubstatus == "": jobsubstatus = 'None'
    walltime = job['durationsec']

    ##if attemptnr > 30 and es == 'ordinary':
    ##    print job['pandaid']
    ##if es == 4:
    ##      print job['pandaid']

    if not walltime or walltime == "":
        walltime = 0

    if jobstatus in ['closed', 'cancelled'] and walltime < 30:
        walltime = 0
    ##
    ## if jobstatus in ['closed', 'cancelled'] and walltime > 10:
    ##    print job['pandaid']
    ##


    if job["starttime"] and job['actualcorecount']:
        corecount = job['actualcorecount']
    else:
        corecount = job['corecount']
    if not corecount:
        corecount = 0
    if es not in report:
        report[es] = {'jobs': 0, 'walltime': 0, 'walltime_time_core': 0}

    if 'sites' not in report[es]:
        report[es]['sites'] = {}
    if computingsite not in report[es]['sites']:
        report[es]['sites'][computingsite] = {'jobs': 0, 'walltime': 0, 'walltime_time_core': 0}

    if 'jobstatus' not in report[es]:
        report[es]['jobstatus'] = {}
    if jobstatus not in report[es]['jobstatus']:
        report[es]['jobstatus'][jobstatus] = {'jobs': 0, 'walltime': 0, 'walltime_time_core': 0}

    if 'attemptnr' not in report[es]:
        report[es]['attemptnr'] = {}
    if attemptnr not in report[es]['attemptnr']:
        report[es]['attemptnr'][attemptnr] = {'jobs': 0, 'walltime': 0, 'walltime_time_core': 0}

    if 'jobstatus' not in report[es]['attemptnr'][attemptnr]:
        report[es]['attemptnr'][attemptnr]['jobstatus'] = {}
    if jobstatus not in report[es]['attemptnr'][attemptnr]['jobstatus']:
        report[es]['attemptnr'][attemptnr]['jobstatus'][jobstatus] = {'jobs': 0, 'walltime': 0, 'walltime_time_core': 0}

    report[es]['jobs'] += 1
    report[es]['walltime'] += walltime
    report[es]['walltime_time_core'] += walltime * corecount

    report[es]['sites'][computingsite]['jobs'] += 1
    report[es]['sites'][computingsite]['walltime'] += walltime
    report[es]['sites'][computingsite]['walltime_time_core'] += walltime * corecount

    report[es]['jobstatus'][jobstatus]['jobs'] += 1
    report[es]['jobstatus'][jobstatus]['walltime'] += walltime
    report[es]['jobstatus'][jobstatus]['walltime_time_core'] += walltime * corecount

    report[es]['attemptnr'][attemptnr]['jobs'] += 1
    report[es]['attemptnr'][attemptnr]['walltime'] += walltime
    report[es]['attemptnr'][attemptnr]['walltime_time_core'] += walltime * corecount

    report[es]['attemptnr'][attemptnr]['jobstatus'][jobstatus]['jobs'] += 1
    report[es]['attemptnr'][attemptnr]['jobstatus'][jobstatus]['walltime'] += walltime
    report[es]['attemptnr'][attemptnr]['jobstatus'][jobstatus]['walltime_time_core'] += walltime * corecount

#print report

defined_colors = mcolors.cnames.values()


##### group by simul job types
labels = []
sizes = []
for es in report:
    labels.append(es)
    sizes.append(report[es]['jobs'])
colors = defined_colors[:len(sizes)]
title = "Simul Jobs count"
draw_pie(labels, sizes, colors, title)


labels = []
sizes = []
for es in report:
    labels.append(es)
    sizes.append(report[es]['walltime_time_core'])
colors = defined_colors[:len(sizes)]
title = "Simul Jobs walltime_time_core"
draw_pie(labels, sizes, colors, title)


##### group by job status
for es in report:
    labels = []
    sizes = []
    for jobstatus in report[es]['jobstatus']:
        labels.append(jobstatus)
        sizes.append(report[es]['jobstatus'][jobstatus]['jobs'])
    colors = defined_colors[:len(sizes)]
    title = "%s simul Jobs count, by jobstatus" % es
    draw_pie(labels, sizes, colors, title)


for es in report:
    labels = []
    sizes = []
    for jobstatus in report[es]['jobstatus']:
        labels.append(jobstatus)
        sizes.append(report[es]['jobstatus'][jobstatus]['walltime_time_core'])
    colors = defined_colors[:len(sizes)]
    title = "%s simul Jobs walltime_time_core, by jobstatus" % es
    draw_pie(labels, sizes, colors, title)


##### group by attemptnr
for es in report:
    labels = []
    sizes = []
    for attemptnr in report[es]['attemptnr']:
        labels.append(attemptnr)
        sizes.append(report[es]['attemptnr'][attemptnr]['jobs'])
    colors = defined_colors[:len(sizes)]
    title = "%s simul Jobs count, by attemptnr" % es
    draw_pie(labels, sizes, colors, title)

for es in report:
    labels = []
    sizes = []
    for attemptnr in report[es]['attemptnr']:
        labels.append(attemptnr)
        sizes.append(report[es]['attemptnr'][attemptnr]['walltime_time_core'])
    colors = defined_colors[:len(sizes)]
    title = "%s simul Jobs walltime_time_core, by attemptnr" % es
    draw_pie(labels, sizes, colors, title)


##### group by attemptnr, jobstatus
def cal_jobs_walltime(attemptList, jobsList):
    jobs = {}
    walltime_time_core = {}
    for attemptnr in attemptList:
        for jobstatus in jobsList[attemptnr]['jobstatus']:
            if jobstatus not in jobs:
                jobs[jobstatus] = jobsList[attemptnr]['jobstatus'][jobstatus]['jobs']
                walltime_time_core[jobstatus] = jobsList[attemptnr]['jobstatus'][jobstatus]['walltime_time_core']
            else:
                jobs[jobstatus] += jobsList[attemptnr]['jobstatus'][jobstatus]['jobs']
                walltime_time_core[jobstatus] += jobsList[attemptnr]['jobstatus'][jobstatus]['walltime_time_core']
            
    return jobs, walltime_time_core



for es in report:
    attemptnrs = report[es]['attemptnr'].keys()
    attemptnrs.sort()
    attempts = {'attemptnr~1': [], 'attemptnr2~5': [], 'attemptnr6~10': [], 'attemptnr11~50': [], 'attemptnr51~': []}
    for attemptnr in attemptnrs:
        if attemptnr <= 1: attempts['attemptnr~1'].append(attemptnr)
        elif attemptnr >= 2 and attemptnr <=5: attempts['attemptnr2~5'].append(attemptnr)
        elif attemptnr >= 6 and attemptnr <=10: attempts['attemptnr6~10'].append(attemptnr)
        elif attemptnr >= 11 and attemptnr <=50: attempts['attemptnr11~50'].append(attemptnr)
        elif attemptnr >= 51: attempts['attemptnr51~'].append(attemptnr)
    for key in attempts:
        value = attempts[key]
        if value:
            jobs, walltime_time_core = cal_jobs_walltime(value, report[es]['attemptnr'])
            labels = []
            sizes = []
            for kjobs in jobs:
                labels.append(kjobs)
                sizes.append(jobs[kjobs])
            colors = defined_colors[:len(sizes)]
            title = "%s simul Jobs %s count, by jobstatus" % (es, key)
            draw_pie(labels, sizes, colors, title)

            labels = []
            sizes = []
            for kjobs in walltime_time_core:
                labels.append(kjobs)
                sizes.append(walltime_time_core[kjobs])
            colors = defined_colors[:len(sizes)]
            title = "%s simul Jobs %s walltime_time_core, by jobstatus" % (es, key)
            draw_pie(labels, sizes, colors, title)



"""
for es in report:
    for attemptnr in report[es]['attemptnr']:
        labels = []
        sizes = []
        for jobstatus in report[es]['attemptnr'][attemptnr]['jobstatus']:
            labels.append(jobstatus)
            sizes.append(report[es]['attemptnr'][attemptnr]['jobstatus'][jobstatus]['jobs'])
        colors = defined_colors[:len(sizes)]
        title = "%s simul Jobs attemptnr %s count, by jobstatus" % (es, attemptnr)
        draw_pie(labels, sizes, colors, title)


for es in report:
    for attemptnr in report[es]['attemptnr']:
        labels = []
        sizes = []
        for jobstatus in report[es]['attemptnr'][attemptnr]['jobstatus']:
            labels.append(jobstatus)
            sizes.append(report[es]['attemptnr'][attemptnr]['jobstatus'][jobstatus]['walltime_time_core'])
        colors = defined_colors[:len(sizes)]
        title = "%s simul Jobs attemptnr %s walltime_time_core, by jobstatus" % (es, attemptnr)
        draw_pie(labels, sizes, colors, title)
"""
