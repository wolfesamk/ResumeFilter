#File System script
import os
import re
import shutil
import pandas as pd

from SafetyScripts.HandyFunctions import clear, wait


def BaseCheckForCreate():
    # this function checks for and creates the Files and JobApps folders.
    clear()
    print('Checking for required base File System Structure.')
    wait(2)

    # list of required folders for initial startup.
    requiredFiles = ['Files','Files\\JobApps']

    # for loop that iterates through requiredFiles list. If folder is not found, creates dir
    for outdir in requiredFiles:
        if not os.path.exists(outdir):
            os.mkdir(outdir)
            creation = os.getcwd() + '\\'+outdir
            print('Created ', creation)
            wait(2)
    print('File System Structure Check Completed')
    wait(2)
    outdir = '*\\'+outdir
    print('You may now move required job post files into', outdir)
    wait(4)
    clear()

def CreateJobPost():
    # this function creates individual job post based on files within sub folder JobApps per jobID

    # calling basecheck just in case end user is using out of order. This is superfluous I think...
    BaseCheckForCreate()

    clear()

    print('Creating Job Post File System Structure')
    wait(2)

    # creating base directory reference
    basedir = 'Files\\JobApps'
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
        print('No new job posts, returning to main menu.')
        wait(3)
        clear()
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
        if keyWords not in files:
            print('Keywords file missing for jobID',jobID,'. Returning to main menu.')
            wait(3)
            clear()
            return
        if resumes not in files:
            print('Resumes file missing for jobID',jobID,'. Returning to main menu.')
            wait(3)
            clear()
            return

        # moving critical files for this jobID to JobID subfolder
        shutil.move(path+'\\'+basedir+'\\'+jobPost,outdir+'\\'+jobPost)
        shutil.move(path+'\\'+basedir+'\\'+keyWords,outdir+'\\'+keyWords)
        shutil.move(path+'\\'+basedir+'\\'+resumes,outdir+'\\'+resumes)

        print('The jobID',jobID,'has been processed.')
        wait(2)
    print('All new Job Posts have been processed. Returning to main menu.')
    wait(3)

def ImportFiles(file,baseDir):
    # this function is for importing critical files as dataframes.

    # combining baseDir and file to locate correct csv.
    f = baseDir+'\\'+file

    # creating dataframe from file location and name
    df = pd.read_csv(f, index_col=False, header=0)

    #returns dataframe.
    return df
