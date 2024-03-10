# Attempting to create custom NLP model
# importing required classes
from pypdf import PdfReader
import spacy
from spacy import displacy
import en_core_web_trf

# needs to have python -m spacy download en_core_web_lg installed - speed
# python -m spacy download en_core_web_trf - accuracy
nlp = en_core_web_trf.load()

indir = 'Files/JobApps'
# creating a pdf reader object
reader = PdfReader(f'{indir}/swolfeResume.pdf')

pages = ''
for p in range(len(reader.pages)):
    pages = reader.pages[p].extract_text() + pages

doc = nlp(pages)
for w in doc:
    print(w.text,w.pos_)
    
    #I am not happy with this NLP. 