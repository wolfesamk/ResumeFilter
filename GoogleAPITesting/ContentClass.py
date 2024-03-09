## need to have gcloud CLI installed to run

from google.cloud import language

# importing required classes
import os
from pypdf import PdfReader
indir = 'Files/JobApps'
# creating a pdf reader object
reader = PdfReader(f'{indir}/swolfeResume.pdf')

# creating a page object
page1 = reader.pages[0].extract_text()

# creating a page object
page2 = reader.pages[1].extract_text()

swolfeResume = page1+page2

with open(f'{indir}/swolfeResume.txt','w') as file:
    file.write(swolfeResume)

from google.cloud import language

def classify_text(text: str) -> language.ClassifyTextResponse:
    client = language.LanguageServiceClient()
    document = language.Document(
        content=text,
        type_=language.Document.Type.PLAIN_TEXT,
    )
    return client.classify_text(document=document)

def show_text_classification(text: str, response: language.ClassifyTextResponse):
    import pandas as pd

    columns = ["category", "confidence"]
    data = ((category.name, category.confidence) for category in response.categories)
    df = pd.DataFrame(columns=columns, data=data)

    print(f"Text analyzed:\n{text}")
    print(df.to_markdown(index=False, tablefmt="presto", floatfmt=".0%"))

# Send a request to the API
classify_text_response = classify_text(swolfeResume)

# Show the results
show_text_classification(swolfeResume, classify_text_response)