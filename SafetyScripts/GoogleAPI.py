## need to have gcloud CLI installed to run
# https://codelabs.developers.google.com/codelabs/cloud-natural-language-python3#0
## must pip install tabulate
# importing required classes
from google.cloud import language_v2 as language
from google.cloud import storage
import pandas as pd
def authenticate_implicit_with_adc(project_id="resumefilter"):
    """
    When interacting with Google Cloud Client libraries, the library can auto-detect the
    credentials to use.

    // TODO(Developer):
    //  1. Before running this sample,
    //  set up ADC as described in https://cloud.google.com/docs/authentication/external/set-up-adc
    //  2. Replace the project variable.
    //  3. Make sure that the user account or service account that you are using
    //  has the required permissions. For this sample, you must have "storage.buckets.list".
    Args:
        project_id: The project id of your Google Cloud project.
    """
    # pip install --upgrade google-cloud-storage
    # This snippet demonstrates how to list buckets.
    # *NOTE*: Replace the client created below with the client required for your application.
    # Note that the credentials are not specified when constructing the client.
    # Hence, the client library will look for credentials using ADC.
    storage_client = storage.Client(project=project_id)
    buckets = storage_client.list_buckets()
    print("Buckets:")
    for bucket in buckets:
        print(bucket.name)
    print("Listed all storage buckets.")

def classify_text(text: str) -> language.ClassifyTextResponse:
    client = language.LanguageServiceClient()
    document = language.Document(
        content=text,
        type_=language.Document.Type.PLAIN_TEXT,
    )
    return client.classify_text(document=document)

def show_text_classification(response: language.ClassifyTextResponse):
    columns = ["category", "confidence"]
    data = ((category.name, category.confidence) for category in response.categories)
    df = pd.DataFrame(columns=columns, data=data)
    # text: str, 
    #print(f"Text analyzed:\n{text}")
    #print(df.to_markdown(index=False, tablefmt="presto", floatfmt=".0%"))
    return df

def text_classification(raw_text):
    response = classify_text(raw_text)
    return show_text_classification(response)

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
    return df
    # print(df.to_markdown(index=False, tablefmt="presto", floatfmt=".0%"))

def entity_analysis(raw_text):
    response = analyze_text_entities(raw_text)
    return show_text_entities(response)

def analyze_text_sentiment(text: str) -> language.AnalyzeSentimentResponse:
    client = language.LanguageServiceClient()
    document = language.Document(
        content=text,
        type_=language.Document.Type.PLAIN_TEXT,
    )
    return client.analyze_sentiment(document=document)

def show_text_sentiment(response: language.AnalyzeSentimentResponse):
    import pandas as pd

    columns = ["score", "sentence"]
    data = [(s.sentiment.score, s.text.content) for s in response.sentences]
    df_sentence = pd.DataFrame(columns=columns, data=data)

    sentiment = response.document_sentiment
    columns = ["score", "magnitude", "language"]
    data = [(sentiment.score, sentiment.magnitude, response.language)]
    df_document = pd.DataFrame(columns=columns, data=data)
    return df_document

def sentiment_analysis(raw_text):
    response = analyze_text_sentiment(raw_text)
    return show_text_sentiment(response)