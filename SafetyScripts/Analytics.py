# This object will perform the primary analytics functions.
# 1. Import critical files for job_post, keywords, and resumes.
# 2. Count keyword frequency for each applicant. preferred gets x2 score
# 3. Run each applicant through Content Analysis, Entity Analysis, and Sentiment Analysis
# 4. Run Applicants through scoring system
# 5. Output one report with all details, one report with just candidates names, total score, and keyword score.

import os
import warnings
import pandas as pd
import math
from sklearn.preprocessing import MinMaxScaler
import SafetyScripts.GoogleAPI as GAPI
from SafetyScripts.HandyFunctions import CountOccurrences
from SafetyScripts.FileSystemActions import ImportFiles
from tqdm import tqdm

#This function is part of element #1
def PrepImport(jobID):
    # reads for RRS current path
    path = os.getcwd()
    # creates jobID directory location
    rawDir = path + '\\Files\\JobApps' + '\\' + jobID
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
    # this function will generate my base desired values for the job post with the google API.

    # concat on empty df causes furture warning, suppressing these.
    warnings.simplefilter(action='ignore', category=FutureWarning)

    # reads for RRS current path
    path = os.getcwd()
    # creates jobID directory location
    rawDir = path + '\\Files\\JobApps' + '\\' + str(dfJobpost['jobID'][0])
    # these are the key columns for the job post file
    key_text_cols = ['job_summary', 'work_environment', 'required', 'preferred']
    jobID = str(dfJobpost['jobID'][0])
    # for loop to iterate through each column. to do this with three distinct types of analysis and
    # to formulate my concept this is going to be tricky. Starting with Classification as it will be
    # the easiest out the gate.

    # creating empty dataframe to store the text classification values for the whole job post.
    df_classification = pd.DataFrame(columns=['category','confidence'])

    # these lines are for importing the practice df_* only
    practice1 = rawDir+'\\df_classification_'+jobID+'.csv'
    # df_classification = pd.read_csv(practice1)

    # this for loop iterates through the columns generating the classification results.
    # classification has a free limit of 30k 1000 character units.

    for t in key_text_cols:
        # creating simple variable to reduce errors
        raw_text = dfJobpost[t][0]
        # calling Google API for text classification
        df = GAPI.text_classification(raw_text=raw_text)
        # merging the fresh raw text api call with other calls
        df_classification = pd.concat([df_classification,df],ignore_index=True)

    # grouping by category and taking mean of confidence to reduce overall values.
    df_classification = df_classification.groupby('category',
                                                  as_index=False,
                                                  sort=False)['confidence'].mean()
    # saving file to save on google API calls
    df_classification.to_csv(practice1, index=False)

    # entity and sentiment analysis have 5k 1000 character limits each month.

    # creating empty dataframe to store the entity classification values for the whole job post.
    df_entity = pd.DataFrame(columns=['name','type','salience','wikipedia_url'])

    # these lines are for importing the practice df_* only
    practice2 = rawDir+'\\df_entity_'+jobID+'.csv'
    # df_entity = pd.read_csv(practice2)

    # entity analysis
    for t in key_text_cols:
        # creating simple variable to reduce errors
        raw_text = dfJobpost[t][0]

        # calling Google API for text classification
        df = GAPI.entity_analysis(raw_text=raw_text)

        # merging the fresh raw text api call with other calls
        df_entity = pd.concat([df_entity,df],ignore_index=True)

    # saving file to save on google API calls
    df_entity.to_csv(practice2, index=False)

    # creating empty dataframe to store the text classification values for the whole job post.
    df_sentiment = pd.DataFrame(columns=['score','magnitude'])

    # these lines are for importing the practice df_* only
    practice3 = rawDir+'\\df_sentiment_'+jobID+'.csv'
    # df_sentiment = pd.read_csv(practice3)

    # entity analysis
    raw_text = ''
    for t in key_text_cols:
        # creating simple variable to reduce errors
        t = dfJobpost[t][0]

        # Sentiment is an average accross the whole document, submitting as one text str
        raw_text = t +'. '+ raw_text        
    # calling Google API for text classification
    df_sentiment = GAPI.sentiment_analysis(raw_text=raw_text)

    # saving file to save on google API calls later
    df_sentiment.to_csv(practice3, index=False)

    return

def NERScoring(jobID, dfApplicants, dfScoreKeeper):
    # concat on empty df causes furture warning, suppressing these.
    warnings.simplefilter(action='ignore', category=FutureWarning)
    # this function will run applicants through all of the NER analytics
    # available through the Google Language API.

    # setting up Google API ADC connection
    # GAPI.authenticate_implicit_with_adc('resumefilter')

    # The known ATS columns for use with Raw Text.
    raw_text_cols = ['personal_1','personal_2','personal_3','technical','job_1',
                     'job_2','job_3','job_4','education','skills']
    
    # reads for RRS current path
    path = os.getcwd()
    # creates jobID directory location
    rawDir = path + '\\Files\\JobApps' + '\\' + str(jobID)
    
    # loading saved jobPost elements
    practice1 = rawDir+'\\df_classification_'+jobID+'.csv'
    df_classification_job = pd.read_csv(practice1)
    score_classification = []
    
    practice2 = rawDir+'\\df_entity_'+jobID+'.csv'
    df_entity_job = pd.read_csv(practice2)
    score_entity = []
    
    practice3 = rawDir+'\\df_sentiment_'+jobID+'.csv'
    df_sentiment_job = pd.read_csv(practice3)
    score_sentiment = []

    # for loop to iterate through each candidate
    for r in tqdm(dfApplicants.index, desc='Candidate Scoring'):
        # creating empty dataframe to store the text classification values for the whole job post.
        df_classification_applicant = pd.DataFrame(columns=['category','confidence'])
        
        # creating empty dataframe to store the entity classification values for the whole job post.
        df_entity_applicant = pd.DataFrame(columns=['name','type','salience','wikipedia_url'])
        
        # creating empty dataframe to store the text classification values for the whole job post.
        df_sentiment_applicant = pd.DataFrame(columns=['score','magnitude'])
        
        full_raw_text = ''
        # for loop to iterate through the raw text columns for the classification element.
        for t in raw_text_cols:
            # setting a local raw text variable to save on mistakes.
            raw_text = dfApplicants[t][r]
            
            # creating full str for sentiment analysis
            if full_raw_text == '':
                full_raw_text = str(raw_text)
            else:
                full_raw_text = full_raw_text + '. ' +str(raw_text)
                
            # try except to catch empty cells. as I am importing missing cells as 'nan'/null.
            try:
                # the try is to see if the value is null via math, if it is, it skips this column.
                if math.isnan(raw_text) is True:
                    continue
            except TypeError:
                # creating full str for sentiment analysis
                if full_raw_text == '':
                    full_raw_text = raw_text
                else:
                    full_raw_text = full_raw_text + '. ' +raw_text
                
                # calling Google API for text classification
                df = GAPI.text_classification(raw_text=raw_text)
                # merging the fresh raw text api call with other calls
                df_classification_applicant = pd.concat([df_classification_applicant,df],ignore_index=True)
                
                # calling Google API for entity classification
                df = GAPI.entity_analysis(raw_text=raw_text)
                # merging the fresh raw text api call with other calls
                df_entity_applicant = pd.concat([df_entity_applicant,df],ignore_index=True)
        # calling Google API for text classification
        df_sentiment_applicant = GAPI.sentiment_analysis(raw_text=raw_text)

        # grouping by category and taking mean of confidence to reduce overall values.
        df_classification_applicant = df_classification_applicant.groupby('category',
                                                                          as_index=False,
                                                                          sort=False)['confidence'].mean()
        
        # creating quick reference lists for text classification scoring
        classification_job_cat_list = df_classification_job['category'].to_list()
        classification_job_con_list = df_classification_job['confidence'].to_list()
        classification_app_cat_list = df_classification_applicant['category'].to_list()
        classification_app_con_list = df_classification_applicant['confidence'].to_list()
        
        # setting base score to the length of the applicant category list.
        temp_score = len(classification_app_cat_list)
        # For loop that iterates through the applicants classification words
        # and scores them according to the following rules.
        # +1 for every NER found element, done above when initializing temp_score
        # +1 for every matching word between job and applicant
        # +difference between applicants confidence score and jobs confidence score
        for c in classification_app_cat_list:
            if c in classification_job_cat_list:
                temp_score = temp_score +1
                place_job = classification_job_cat_list.index(c)
                place_app = classification_app_cat_list.index(c)
                diff = classification_app_con_list[place_app] - classification_job_con_list[place_job]
                temp_score = round(temp_score + diff,6)
        score_classification.append(temp_score)

        # creating quick reference lists for entity classification scoring
        entity_job_name_list = df_entity_job['name'].to_list()
        entity_job_sali_list = df_entity_job['salience'].to_list()
        entity_app_name_list = df_entity_applicant['name'].to_list()
        entity_app_sali_list = df_entity_applicant['salience'].to_list()

        # setting base score to the length of the applicant name list.
        temp_score = len(entity_app_name_list)
        # For loop that iterates through the applicants entity names
        # and scores them according to the following rules.
        # +1 for every NER found element, done above when initializing temp_score
        # +1 for every matching name between job and applicant
        # +difference between applicants salience and jobs salience
        for c in entity_app_name_list:
            if c in entity_job_name_list:
                temp_score = temp_score +1
                place_job = entity_job_name_list.index(c)
                place_app = entity_app_name_list.index(c)
                diff = entity_app_sali_list[place_app] - entity_job_sali_list[place_job]
                temp_score = round(temp_score + diff,6)
        score_entity.append(temp_score)

        # sentiment will be the sentiment score raw + magnitude difference
        # print(dfApplicants.candidate_first_name[r])
        # print(df_sentiment_applicant.score[0])
        # print(df_sentiment_applicant.magnitude[0])
        temp_score = df_sentiment_applicant.score[0] - df_sentiment_job.score[0]
        diff = df_sentiment_applicant.magnitude[0] - df_sentiment_job.magnitude[0]
        temp_score = temp_score + diff
        score_sentiment.append(temp_score)

    dfScoreKeeper['score_classification'] = score_classification
    dfScoreKeeper['score_entity'] = score_entity
    dfScoreKeeper['score_sentiment'] = score_sentiment
    dfScoreKeeper.to_csv(rawDir+'\\dfScoreKeeper_'+jobID+'.csv', index = False)
    return dfScoreKeeper

def SubScoring(jobID, dfJobpost, dfApplicants, dfScoreKeeper):
    # This function will focus on scoring candidates base on other values

    # concat on empty df causes furture warning, suppressing these.
    warnings.simplefilter(action='ignore', category=FutureWarning)

    # reads for RRS current path
    path = os.getcwd()
    # creates jobID directory location
    rawDir = path + '\\Files\\JobApps' + '\\' + str(jobID)

    # creating score lists
    score_months = []
    score_relocation = []
    score_pay = []


    # this for loop will iterate through candidates
    for a in tqdm(dfApplicants.index, desc='Candidate Scoring Part 2'):
        # setting temp score to 0
        temp_score = 0

        #setting applicant months to 0
        applicant_months = 0

        # calculating applicant total months working
        applicant_months = dfApplicants['job_1_months'][a] + dfApplicants['job_2_months'][a] + dfApplicants['job_3_months'][a] + dfApplicants['job_4_months'][a]

        # if statement to check if applicant has work history greater than or 
        # equal to minimum
        if applicant_months >= dfJobpost['required_months'][0]:
            temp_score = temp_score + 1

        # if statement to check if applicant has work history greater than or 
        # equal to preferred
        if applicant_months >= dfJobpost['preferred_months'][0]:
            temp_score = temp_score + 2

        # adding applicants month score to list.
        score_months.append(temp_score)

        # setting temp score to 0
        temp_score = 0
        
        # scoring for relocation
        # if applicant matches relocation and relocation is 1 for company
        # give applicant 1 point.
        if dfApplicants['relocation'][a] == dfJobpost['relocation'][0] and dfJobpost['relocation'][0] == 1:
            temp_score = temp_score + 1

        # if applicant relocation 1 and company relocation 0 give applicant point
        if dfApplicants['relocation'][a] == 1 and dfJobpost['relocation'][0] == 0:
            temp_score = temp_score + 1
        score_relocation.append(temp_score)

        # setting temp score to 0
        temp_score = 0

        # if applicants pay between min and max, use following logic
        # max - applicant - min, rewards cheaper applicants
        if dfApplicants['pay_desired'][a] >= dfJobpost['pay_min'][0] and dfApplicants['pay_desired'][a] <= dfJobpost['pay_max'][0]:
            diff1 = dfJobpost['pay_max'][0] - dfApplicants['pay_desired'][a]
            diff2 = dfApplicants['pay_desired'][a] - dfJobpost['pay_min'][0]
            temp_score = diff1 - diff2
        score_pay.append(temp_score)
    # adding new columns to scorekeeper
    dfScoreKeeper['score_months'] = score_months
    dfScoreKeeper['score_relocation'] = score_relocation
    # dfScoreKeeper['score_pay'] = score_pay
    dfScoreKeeper['score_pay'] = dfApplicants['pay_desired']
    dfScoreKeeper['score_education'] = dfApplicants['education_highest']
    
    # normalizing score columns
    
    # separating columns that need to be normalized vs those that do not
    scorings = ['score_keyword', 'score_classification', 'score_entity', 'score_sentiment', 'score_months', 'score_pay','score_education']
    labels = ['jobPost','candidate_id', 'score_relocation']
    x = dfScoreKeeper[scorings]
    y = dfScoreKeeper[labels]
    
    # creating scaler using sklearn MinMaxScaler
    scaler = MinMaxScaler()
    
    # fitting data to the scaler
    data = scaler.fit_transform(x)
    
    # Creating and merging dataframe
    dfScoreKeeper_Scaled = pd.DataFrame(data,columns=x.columns)
    dfScoreKeeper_Scaled = pd.merge(y, dfScoreKeeper_Scaled,left_index=True, right_index=True)
    
    # saving dataframes for reference later just in case.
    dfScoreKeeper_Scaled.to_csv(rawDir+'\\dfScoreKeeper_Scaled_'+jobID+'.csv', index = False)
    dfScoreKeeper.to_csv(rawDir+'\\dfScoreKeeper_'+jobID+'.csv', index = False)
    return dfScoreKeeper,dfScoreKeeper_Scaled
