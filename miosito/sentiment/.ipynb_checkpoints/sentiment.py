

class SentimentAnalyzer:
    @classmethodclass ItalianSentimentAnalyzer:
    SVM_PICKLE_PATH = '{}/dataset/svm.pickle'.format(BASE_DIR)
    VECTORIZER_PICKLE_PATH = '{}/dataset/tfidf_vect.pickle'.format(BASE_DIR)
    CALIBRATOR_PICKLE_PATH = '{}/dataset/calibrator.pickle'.format(BASE_DIR)

    @classmethod
    def get_dataset(cls):
        documents = TextPattern.objects.filter(~Q(sentiment=None)).all()
        feature_vect = TfidfVectorizer(
            strip_accents='unicode',
            tokenizer=word_tokenize,
            stop_words=stopwords.words('italian'),
            decode_error='ignore',
            analyzer='word',
            norm='l2',
            ngram_range=(1, 3)
        )
        x_data = feature_vect.fit_transform([doc.text for doc in documents])
        y_data = [doc.sentiment for doc in documents]
        pickle.dump(feature_vect, open(cls.VECTORIZER_PICKLE_PATH, "wb"))
        return x_data, y_data
    def get_dataset(cls):
        documents = TextPattern.objects.filter(~Q(sentiment=None)).all()
        feature_vect = TfidfVectorizer(
            strip_accents='unicode',
            tokenizer=word_tokenize,
            stop_words=stopwords.words('italian'),
            decode_error='ignore',
            analyzer='word',
            norm='l2',
            ngram_range=(1, 3)
        )
        x_data = feature_vect.fit_transform([doc.text for doc in documents])
        y_data = [doc.sentiment for doc in documents]
        pickle.dump(feature_vect, open(cls.VECTORIZER_PICKLE_PATH, "wb"))
        return x_data, y_data