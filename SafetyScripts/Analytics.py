# This object will perform the primary analytics functions.
# 1. Import Resume's and Cover Letters into dataframe
# 2. Import keywords csv and count frequency for each applicant
# 3. Run each applicant through Content Analysis, Entity Analysis, and Sentiment Analysis
# 4. Run Applicants through scoring system
# 5. Output one report with all details, one report with just candidates names, total score, and keyword score.

import os
import pandas as pd
from SafetyScripts.PDFSplitter import readThisApp
from SafetyScripts.FileSystemActions import MoveApplicant
from SafetyScripts.HandyFunctions import CountOccurrences
import re
#This function is part of element #1
def ApplicantImport(jobID):
    path = os.getcwd()
    rawDir = path + '\\Files\JobApps' + '\\' + jobID + '\\' + 'Raw'
    processedDir = path + '\\Files\JobApps' + '\\' + jobID + '\\' + 'Processed'
    files = os.listdir(rawDir)
    df_applicants = pd.DataFrame(columns=['Name_First','Name_Last','Resume_Raw','Resume_Raw_Seg'])
    temp_names_first = []
    temp_names_last = []
    temp_resume_raw_seg = []
    temp_resume_raw = ''
    for f in files:
        names = f.split('.')[0].split('_')[1:]
        temp_names_last.append(names[0])
        temp_names_first.append(names[1])
        temp_resume_raw_seg.append(readThisApp(f,jobID))
        for seg in temp_resume_raw_seg[0]:
            if temp_resume_raw == '':
                temp_resume_raw = seg
            else:
                temp_resume_raw = temp_resume_raw + ' '+ seg
        ####MoveApplicant(jobID,f)
    df_applicants['Name_First'] = temp_names_first
    df_applicants['Name_Last'] = temp_names_last
    df_applicants['Resume_Raw'] = temp_resume_raw
    df_applicants['Resume_Raw_Seg'] = temp_resume_raw_seg
    return df_applicants

# This is element 2
def KeywordImport(jobID,df_applicants):
    path = os.getcwd()
    path = path  + '\\Files\JobApps' + '\\' + jobID
    files = os.listdir(path)
    for f in files:
        if 'keywords' in f:
            files = f
        else:
            continue
    df_keywords = pd.read_csv(path+'\\'+files)
    keywords_min = df_keywords['minimum'].to_list()
    keywords_max = df_keywords['preferred'].dropna().to_list()
    for i in df_applicants.index:
        text = df_applicants['Resume_Raw'].loc[i]
        text = re.sub(r'\W', ' ', text)
        pattern = re.compile(r'\s+')
        text = re.sub(pattern,' ',text)
        text = text.lower()
        # print(text)#

        count_total = 0
        count_min = 0
        count_max = 0
        for word in keywords_min:
            word = word.lower()
            count_min = count_min+CountOccurrences(text,word)
        for word in keywords_max:
            word = word.lower()
            count_max = count_max+CountOccurrences(text, word)
        count_total = count_min + count_max
        print(count_min)
        print(count_max)
        print(count_total)