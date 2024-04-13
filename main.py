#this is a test
from SafetyScripts.HandyFunctions import clear
from SafetyScripts.FileSystemActions import BaseCheckForCreate,CreateJobPost
from SafetyScripts.Analytics import PrepImport, ScoreKeeper, KeywordCounter, NERScoring, GoogleJob, SubScoring
from SafetyScripts.Match import Game
import os
import pandas as pd
clear()

BaseCheckForCreate()
CreateJobPost()
jobID = '1002'
dfJobpost,dfKeywords,dfApplicants = PrepImport(jobID)
dfScoreKeeper = ScoreKeeper(dfApplicants,jobID)
dfScoreKeeper = KeywordCounter(dfApplicants, dfKeywords,dfScoreKeeper)

# commented out to save on API calls
# GoogleJob(dfJobpost)

# dfScoreKeeper = NERScoring(jobID, dfApplicants, dfScoreKeeper)
# clear()
# the following 3 lines are temporary during testing
# reads for RRS current path
path = os.getcwd()
# creates jobID directory location
rawDir = path + '\\Files\\JobApps' + '\\' + str(jobID)
dfScoreKeeper = pd.read_csv(rawDir+'\\dfScoreKeeper_'+jobID+'.csv')

clear()
dfScoreKeeper, dfScoreKeeper_Scaled = SubScoring(jobID, dfJobpost, dfApplicants, dfScoreKeeper)
clear()
dfScoreKeeper_Scaled = Game(dfScoreKeeper_Scaled)
print(dfScoreKeeper_Scaled)
