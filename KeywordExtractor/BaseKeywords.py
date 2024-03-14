def keywords(text):
    import yake
    from rake_nltk import Rake
    #requires python -c "import nltk; nltk.download('stopwords')"
    rake_nltk_var = Rake()
    rake_nltk_var.extract_keywords_from_text(text)
    keyword_extracted = rake_nltk_var.get_ranked_phrases_with_scores()
    print(keyword_extracted)