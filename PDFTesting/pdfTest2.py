# importing required classes
import os
from pypdf import PdfReader

indir = 'Files/JobApps'
# # creating a pdf reader object
reader = PdfReader(f'{indir}/swolfeResume.pdf')

reader

pages = ''
for p in range(len(reader.pages)):
    pages = pages+reader.pages[p].extract_text(extraction_mode='layout')
segmented = pages.split('\n')
#print(segmented)

import pandas as pd

# create example DataFrame
df = pd.DataFrame({'lines': segmented})

# apply regular expression to remove white space from all strings in DataFrame
df = df.replace(r'\s+', ' ', regex=True)
df2 = []
for x in df.index:
    print(df.lines[x])
    l = str(df.lines[x])
    if len(l) < 1:
        df2.append(l)
        continue
    first = l[0]
    if first == ' ':
        l2 = l[1:]
        df2.append(l2)
    if first == '•':
        l2 = l[2:]
        df2.append(l2)

df2 = pd.DataFrame({'lines':df2})

for r in df2.index:
    print(df2.lines[r])