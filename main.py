#this is a test
import pandas as pd
from KeywordExtractor.BaseKeywords import keywords
from SafetyScripts.HandyFunctions import clear,wait,findPath
from SafetyScripts.PDFResumeSplitter import readThisPDF
# from GoogleAPITesting.ContentClass import classify_text,show_text_classification
clear()
resume = readThisPDF('swolfeResume.pdf')
# dict = {'category':[],'confidence':[],'paragraph':[]}
# df_resume = pd.DataFrame(dict)
# for x in resume:
#     x_response = classify_text(x)
#     temp_df = show_text_classification(x,x_response)
#     temp_df['paragraph'] = x
#     df_resume = pd.concat([df_resume,temp_df],ignore_index=True)
# print(df_resume)

for x in resume:
    print('--------')
    print(x)
    print('')
    keywords(x)
    print('--------')