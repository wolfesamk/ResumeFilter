#this is a test
import pandas as pd
from SafetyScripts.BaseKeywords import keywords
from SafetyScripts.HandyFunctions import clear,wait,findPath
from SafetyScripts.PDFResumeSplitter import readThisApp, readThisJob
from SafetyScripts.FileSystemSetup import BaseCheckForCreate,CreateJobPost,MoveApplicant
# from GoogleAPITesting.ContentClass import classify_text,show_text_classification
clear()
#resume = readThisApp('swolfeResume.pdf')
#jobpost = readThisJob('jobPost_01002.pdf')
# dict = {'category':[],'confidence':[],'paragraph':[]}
# df_resume = pd.DataFrame(dict)
# for x in resume:
#     x_response = classify_text(x)
#     temp_df = show_text_classification(x,x_response)
#     temp_df['paragraph'] = x
#     df_resume = pd.concat([df_resume,temp_df],ignore_index=True)
# print(df_resume)

BaseCheckForCreate()
CreateJobPost()
MoveApplicant('01002','resume_Wolfe_Samuel.pdf')