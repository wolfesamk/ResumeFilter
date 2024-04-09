# This object will perform the primary analytics functions.
# 1. Import critical files for job_post, keywords, and resumes.
# 2. Count keyword frequency for each applicant. preferred gets x2 score
# 3. Run each applicant through Content Analysis, Entity Analysis, and Sentiment Analysis
# 4. Run Applicants through scoring system
# 5. Output one report with all details, one report with just candidates names, total score, and keyword score.

import os
import pandas as pd
import math
from SafetyScripts.HandyFunctions import CountOccurrences
from SafetyScripts.FileSystemActions import ImportFiles
#This function is part of element #1
def PrepImport(jobID):
    # reads for RRS current path
    path = os.getcwd()
    # creates jobID directory location
    rawDir = path + '\\Files\JobApps' + '\\' + jobID
    # looks for all files in dir
    files = os.listdir(rawDir)
    # looks for critical files
    for f in files:
        if 'job_post' in f:
            dfJobpost = ImportFiles(f, rawDir)
        if 'keywords' in f:
            dfKeywords = ImportFiles(f, rawDir)
        if 'resumes' in f:
            dfApplicants = ImportFiles(f, rawDir)
    # returns dataframes of critical info
    return dfJobpost,dfKeywords,dfApplicants

def ScoreKeeper(dfApplicants,jobID):
    # creates scorekeeper dataframe. Separate for now for ease of scoring.
    dfScoreKeeper = pd.DataFrame()
    # filling out dataframe with all applicants
    dfScoreKeeper['candidate_id'] = dfApplicants['candidate_id']
    # adding jobID for easier reference later if I decide to merge ScoreKeeper into one file.
    dfScoreKeeper['jobPost'] = jobID
    # returns scorekeeper dataframe
    return dfScoreKeeper

def KeywordCounter(dfApplicants, dfKeywords, dfScoreKeeper):
    # Function creates and populates new column, score_keyword.
    
    # The known ATS columns for use with Raw Text.
    raw_text_cols = ['personal_1','personal_2','personal_3','technical','job_1','job_2','job_3','job_4','education','skills']
    
    # creating local defaults
    mini_count_total = 0
    maxi_count_total = 0
    
    #creating empty list to save each candidate
    totals =[]
    for r in dfApplicants.index:
        mini_count_total = 0
        maxi_count_total = 0
        count_total = 0
        for t in raw_text_cols:
            raw_text = dfApplicants[t][r]
            try:
                if math.isnan(raw_text) is True:
                    continue
            except:
                for q in dfKeywords.index:
                    mini = dfKeywords.minimum[q]
                    try:
                        if math.isnan(mini) is True:
                            mini_count = 0
                    except:
                        mini_count = CountOccurrences(raw_text,mini)
                    mini_count_total = mini_count_total + mini_count
                    
                    maxi = dfKeywords.preferred[q]
                    try:
                        if math.isnan(maxi) is True:
                            maxi_count = 0
                    except:
                        maxi_count = CountOccurrences(raw_text,maxi) * 2
                    maxi_count_total = maxi_count_total + maxi_count
        count_total = mini_count_total + maxi_count_total
        print(count_total)
        totals.append(count_total)
    dfScoreKeeper['score_keyword'] = totals
    return dfScoreKeeper