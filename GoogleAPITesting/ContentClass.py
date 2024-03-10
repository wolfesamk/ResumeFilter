## need to have gcloud CLI installed to run
## must pip install tabulate
# importing required classes
from google.cloud import language_v2 as language
import pandas as pd

def classify_text(text: str) -> language.ClassifyTextResponse:
    client = language.LanguageServiceClient()
    document = language.Document(
        content=text,
        type_=language.Document.Type.PLAIN_TEXT,
    )
    return client.classify_text(document=document)

def show_text_classification(text: str, response: language.ClassifyTextResponse):
    columns = ["category", "confidence"]
    data = ((category.name, category.confidence) for category in response.categories)
    df = pd.DataFrame(columns=columns, data=data)

    #print(f"Text analyzed:\n{text}")
    #print(df.to_markdown(index=False, tablefmt="presto", floatfmt=".0%"))
    return df