from sklearn.base import TransformerMixin, BaseEstimator
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd

class ColorTransformer(TransformerMixin, BaseEstimator):

    def __init__(self):
        self.vectorizer = CountVectorizer()

    def fit(self, X, y=None):
        X = X['color'].map(lambda x: " ".join(x.split("/")))
        self.vectorizer.fit(X)
        return self

    def transform(self, X, y=None):
        X = X['color'].map(lambda x: " ".join(x.split("/")))
        transformed = self.vectorizer.transform(X)
        columns = self.vectorizer.get_feature_names_out()
        return pd.DataFrame(transformed.toarray(), columns=columns)
