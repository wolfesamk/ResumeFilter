#File System script
import sys
import subprocess
import os
from os import system, name
from time import sleep
from datetime import datetime
import pandas as pd

def BaseCheckForCreate():
    requiredFiles = ['Files','Files\JobApps']
    for outdir in requiredFiles:
        if not os.path.exists(outdir):
            os.mkdir(outdir)
    # path = os.getcwd()
    # files = os.listdir(path+'\\'+outdir)
    # lib_files = []
    # for f in files:
    #     if 'lib' in f:
    #         lib_files.append(f)
    # if len(lib_files) < 1:
    #     return False
    # lib_files.sort(reverse=True)
    # hist_libs = lib_files[0]

def CreateJobPost():
    import re
    import shutil
    BaseCheckForCreate()
    basedir = 'Files\JobApps'
    path = os.getcwd()
    files = os.listdir(path+'\\'+basedir)
    jobIDList = []
    for f in files:
        if 'jobPost' in f:
            #need to remove jobPost_ to create pure id
            id = re.sub("[^0-9]","",f)
            jobIDList.append(id)
    if len(jobIDList) < 1:
        return
    for id in jobIDList:
        outdir = path+'\\'+basedir+'\\'+id
        if not os.path.exists(outdir):
            os.mkdir(outdir)
        outdir2 = outdir +'\\'+ 'Raw'
        if not os.path.exists(outdir2):
            os.mkdir(outdir2)
        outdir3 = outdir +'\\'+ 'Processed'
        if not os.path.exists(outdir3):
            os.mkdir(outdir3)
        jobPost = 'jobPost_'+id+'.pdf'
        keyWords = 'keywords_'+id+'.csv'
        shutil.move(path+'\\'+basedir+'\\'+jobPost,outdir+'\\'+jobPost)
        shutil.move(path+'\\'+basedir+'\\'+keyWords,outdir+'\\'+keyWords)

def MoveApplicant(jobID,fileName):
    import shutil
    basedir = os.getcwd()+'\Files\JobApps\\'+ jobID
    raw = basedir+'\\'+'Raw'
    processed = basedir+'\\'+'Processed'
    shutil.move(raw+'\\'+fileName,processed+'\\'+fileName)