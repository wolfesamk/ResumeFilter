#File System script
import os
import re
import shutil
import pandas as pd


def BaseCheckForCreate():
    # this function checks for and creates the Files and JobApps folders.
    # list of required folders for initial startup.
    requiredFiles = ['Files','Files\JobApps']
    
    # for loop that iterates through requiredFiles list. If folder is not found, creates dir
    for outdir in requiredFiles:
        if not os.path.exists(outdir):
            os.mkdir(outdir)

def CreateJobPost():
    # this function creates individual job post based on files within sub folder JobApps per jobID
    
    # calling basecheck just in case end user is using out of order. This is superfluous I think...
    BaseCheckForCreate()
    
    # creating base directory reference
    basedir = 'Files\JobApps'
    # finding local path
    path = os.getcwd()
    # combining basedir and path for local base dir
    files = os.listdir(path+'\\'+basedir)
    
    # list for jobID's
    jobIDList = []
    
    # for loop to scan for all jobPostings needing to be imported.
    for f in files:
        #checking that file is jobPost to avoid issues
        if 'jobPost' in f:
            # using regex to only keep the id portion
            jobID = re.sub("[^0-9]","",f)
            # adding jobID to list
            jobIDList.append(jobID)
    
    # if there are no jobs to import end function early.
    if len(jobIDList) < 1:
        return
    
    # for loop to create jobID and move files associated with jobPost
    for jobID in jobIDList:
        # creating local directory for this jobID
        outdir = path+'\\'+basedir+'\\'+jobID
        
        # checking if dir already exists, if not creates it
        if not os.path.exists(outdir):
            os.mkdir(outdir)
            
        # Setting up critical files for this jobID
        jobPost = 'jobPost_'+jobID+'.csv'
        keyWords = 'keywords_'+jobID+'.csv'
        resumes = 'resumes_'+jobID+'.csv'
        
        # moving critical files for this jobID to JobID subfolder
        shutil.move(path+'\\'+basedir+'\\'+jobPost,outdir+'\\'+jobPost)
        shutil.move(path+'\\'+basedir+'\\'+keyWords,outdir+'\\'+keyWords)
        shutil.move(path+'\\'+basedir+'\\'+resumes,outdir+'\\'+resumes)

def ImportFiles(file,baseDir):
    # this function is for importing critical files as dataframes.
    
    # combining baseDir and file to locate correct csv.
    f = baseDir+'\\'+file
    
    # creating dataframe from file location and name
    df = pd.read_csv(f, index_col=False, header=0)
    
    #returns dataframe.
    return df