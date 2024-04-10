## need to have gcloud CLI installed to run
## must pip install tabulate
# importing required classes
from google.cloud import language_v2 as language
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

def show_text_classification(text: str, response: language.ClassifyTextResponse):
    columns = ["category", "confidence"]
    data = ((category.name, category.confidence) for category in response.categories)
    df = pd.DataFrame(columns=columns, data=data)

    #print(f"Text analyzed:\n{text}")
    #print(df.to_markdown(index=False, tablefmt="presto", floatfmt=".0%"))
    return df

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
    # print(df.to_markdown(index=False, tablefmt="presto", floatfmt=".0%"))