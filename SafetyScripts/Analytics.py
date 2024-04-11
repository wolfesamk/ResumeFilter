# This object will perform the primary analytics functions.
# 1. Import critical files for job_post, keywords, and resumes.
# 2. Count keyword frequency for each applicant. preferred gets x2 score
# 3. Run each applicant through Content Analysis, Entity Analysis, and Sentiment Analysis
# 4. Run Applicants through scoring system
# 5. Output one report with all details, one report with just candidates names, total score, and keyword score.

import os
import pandas as pd
import math
import SafetyScripts.GoogleAPI as GAPI
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
    dfScoreKeeper = pd.DataFrame(columns=['jobPost'])
    # filling out dataframe with all applicants
    dfScoreKeeper['candidate_id'] = dfApplicants['candidate_id']
    # adding jobID for easier reference later if I decide to merge ScoreKeeper into one file.
    dfScoreKeeper['jobPost'] = jobID
    # returns scorekeeper dataframe
    return dfScoreKeeper

def KeywordCounter(dfApplicants, dfKeywords, dfScoreKeeper):
    # Function creates and populates new column, score_keyword.

    # The known ATS columns for use with Raw Text.
    raw_text_cols = ['personal_1','personal_2','personal_3','technical','job_1',
                     'job_2','job_3','job_4','education','skills']

    # creating local defaults
    mini_count_total = 0
    maxi_count_total = 0

    #creating empty list to save each candidate
    totals =[]
    # for loop to iterate through each candidate
    for r in dfApplicants.index:
        # setting defaults for each candidate
        mini_count_total = 0
        maxi_count_total = 0
        count_total = 0

        # for loop to iterate through the raw text columns.
        for t in raw_text_cols:
            # setting a local raw text variable to save on mistakes.
            raw_text = dfApplicants[t][r]

            # try except to catch empty cells. as I am importing missing cells as 'nan'/null.
            try:
                # the try is to see if the value is null via math, if it is, it skips this column.
                if math.isnan(raw_text) is True:
                    continue
            except TypeError:
                # the except runs the part of the loop we want to process.

                # for loop iterates through the keywords
                for q in dfKeywords.index:

                    # first up is the minimum requirements keywords
                    # creating variable
                    mini = dfKeywords.minimum[q]
                    # try/except to again catch if the cell is null.
                    # if true then the count is 0 for this part.

                    try:
                        if math.isnan(mini) is True:
                            mini_count = 0

                    # if the try fails then we get to the part we want to run.
                    except TypeError:
                        # this uses the function CountOccurences to count the number
                        # of times a given word appears in a given text string.
                        mini_count = CountOccurrences(raw_text,mini)

                    # adding all of the counts together.
                    mini_count_total = mini_count_total + mini_count

                    # the below code odes the same as above but for preferred.
                    # It also applies more weight to preferred qualifications.
                    maxi = dfKeywords.preferred[q]
                    try:
                        if math.isnan(maxi) is True:
                            maxi_count = 0
                    except TypeError:
                        maxi_count = CountOccurrences(raw_text,maxi) * 2
                    maxi_count_total = maxi_count_total + maxi_count
        # adding maxi and mini count totals for applicant
        count_total = mini_count_total + maxi_count_total
        # appending new count to totals list
        totals.append(count_total)

    # creating new column in dfScoreKeeper with totals for keywords.
    dfScoreKeeper['score_keyword'] = totals

    # returning new dfScoreKeeper
    return dfScoreKeeper

def GoogleJob(dfJobpost):
    # this function will generate my base desired values for the job post with the google API... if any.
    # reads for RRS current path
    path = os.getcwd()
    # creates jobID directory location
    rawDir = path + '\\Files\JobApps' + '\\' + str(dfJobpost['jobID'][0])
    # these are the key columns for the job post file
    key_text_cols = ['job_summary', 'work_environment', 'required', 'preferred']
    
    # creating file name to save on Google API calls later
    file_name = rawDir+'\\job_post_'+str(dfJobpost['jobID'][0])+'.csv'
    
    # creating empty dataframe to store the text classification values for the whole job post.
    df_classification = pd.DataFrame(columns=['category','confidence'])
    
    # for loop to iterate through each column. to do this with three distinct types of analysis and
    # to formulate my concept this is going to be tricky. Starting with Classification as it will be
    # the easiest out the gate.
    
    # these two lines are for importing the practice df_classification only
    practice1 = rawDir+'\\practice1_dataframe.csv'
    df_classification = pd.read_csv(practice1)
    practice2 = rawDir+'\\practice2_dataframe.csv'
    # df_entity = pd.read_csv(practice2)
    practice3 = rawDir+'\\practice3_dataframe.csv'
    # df_sentiment = pd.read_csv(practice3)
    
    # this for loop iterates through the columns generating the classification results.
    # classification has a free limit of 30k 1000 character units. It is likely best to run
    # each column by itself for this match system.
    # TODO: I am considering making people who match the generated columns get x2 points.
    #       I need to consider how I am going to score this. Will it be a simple pass fail?
    #       If they match its +1 point. Then of those who match distribute more points to the closest
    #       value?
    for t in key_text_cols:
        break
        # creating simple variable to reduce errors
        raw_text = dfJobpost[t][0]
        # calling Google API for text classification
        df = GAPI.text_classification(raw_text=raw_text)
        # merging the fresh raw text api call with other calls
        df_classification = pd.concat([df_classification,df],ignore_index=True)

    # grouping by category and taking mean of confidence to reduce overall values.
    df_classification = df_classification.groupby('category', as_index=False,sort=False)['confidence'].mean()
    df_classification.to_csv(practice1, index=False)

# TODO: get this working. Once I have this working for the job Post I can probably simplify it into 
#       its own functions for use with both jobpost and with applicants.
    # entity and sentiment analysis have 5k 1000 character limits each month.
    # at scale this will become an issue, but I am going to start with mimicking
    # the classification method.

    # entity analysis
    for t in key_text_cols:
        # creating simple variable to reduce errors
        raw_text = dfJobpost[t][0]

        # calling Google API for text classification
        df = GAPI.entity_analysis(raw_text=raw_text)

        # merging the fresh raw text api call with other calls
        df_entity = pd.concat([df_classification,df],ignore_index=True)
    df_entity.to_csv(practice2, index=False)
    # c = t+'_entity'
    # dfJobpost[c] = GAPI.entity_analysis(raw_text=raw_text)
    # c = t+'_sentiment'
    # dfJobpost[c] = GAPI.entity_analysis(raw_text=raw_text)
    return dfJobpost

def GoogleNER(dfApplicants, dfScoreKeeper):
    # this function will run applicants through all of the NER analytics
    # available through the Google Language API.

    # setting up Google API ADC connection
    # GAPI.authenticate_implicit_with_adc('resumefilter')

    # The known ATS columns for use with Raw Text.
    raw_text_cols = ['personal_1','personal_2','personal_3','technical','job_1',
                     'job_2','job_3','job_4','education','skills']
    # for loop to iterate through each candidate
    for r in dfApplicants.index:

        # for loop to iterate through the raw text columns.
        for t in raw_text_cols:
            # setting a local raw text variable to save on mistakes.
            raw_text = dfApplicants[t][r]

            # try except to catch empty cells. as I am importing missing cells as 'nan'/null.
            try:
                # the try is to see if the value is null via math, if it is, it skips this column.
                if math.isnan(raw_text) is True:
                    continue
            except TypeError:
                print(raw_text)
                response = GAPI.classify_text(raw_text)
                dfRawTextClassification = GAPI.show_text_classification(raw_text,response)
                print(dfRawTextClassification)
                break
        break
    return dfScoreKeeper
