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

def analyze_text_entities(text: str) -> language.AnalyzeEntitiesResponse:
    client = language.LanguageServiceClient()
    document = language.Document(
        content=text,
        type_=language.Document.Type.PLAIN_TEXT,
    )
    return client.analyze_entities(document=document)

def show_text_entities(response: language.AnalyzeEntitiesResponse):
    import pandas as pd

    columns = ("name", "type", "salience", "mid", "wikipedia_url")
    data = (
        (
            entity.name,
            entity.type_.name,
            entity.salience,
            entity.metadata.get("mid", ""),
            entity.metadata.get("wikipedia_url", ""),
        )
        for entity in response.entities
    )
    df = pd.DataFrame(columns=columns, data=data)
    print(df.to_markdown(index=False, tablefmt="presto", floatfmt=".0%"))
    
# Send a request to the API
analyze_entities_response = analyze_text_entities(swolfeResume)

# Show the results
show_text_entities(analyze_entities_response)