# importing required classes
import os
from pypdf import PdfReader
indir = 'Files/JobApps'
# creating a pdf reader object
reader = PdfReader(f'{indir}/swolfeResume.pdf')

# printing number of pages in pdf file
print(len(reader.pages))

# creating a page object
page1 = reader.pages[0].extract_text()

# creating a page object
page2 = reader.pages[1].extract_text()

swolfeResume = page1+page2

with open(f'{indir}/swolfeResume.txt','w') as file:
    file.write(swolfeResume)