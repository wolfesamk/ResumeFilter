#this is a test
from SafetyScripts.HandyFunctions import clear
from SafetyScripts.FileSystemActions import BaseCheckForCreate,CreateJobPost,MoveApplicant
from SafetyScripts.Analytics import ApplicantImport, KeywordImport
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
df_applicants = ApplicantImport('01002')
KeywordImport(jobID='01002',df_applicants=df_applicants)