def keywords(text):
    stopwords = ['https', '://','www','com' ]
    from rake_nltk import Rake
    #requires python -c "import nltk; nltk.download('stopwords')"
    print(text)
    text = text.replace(')', '')
    text = text.replace('(', '')
    print(text)
    rake_nltk_var = Rake(stopwords=stopwords,min_length=2,max_length=5,include_repeated_phrases=False)
    rake_nltk_var.extract_keywords_from_text(text)
    keyword_extracted = rake_nltk_var.get_ranked_phrases_with_scores()
    print(keyword_extracted)
    
def count_keywords(jobID):
    score = 0
    return score