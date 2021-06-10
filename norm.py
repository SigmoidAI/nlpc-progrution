'''
Made with love by Sigmoid.

@author - Păpăluță Vasile (papaluta.vasile@isa.utm.md)
'''

# Importing all needed functions.
from sklearn.base import BaseEstimator, TransformerMixin
import re
from nltk import word_tokenize, MWETokenizer

class TextNormalizer(BaseEstimator, TransformerMixin):
    def __init__(self):
        '''
            Initializes the Text Normalizer.
        '''
        #Isolating words containing letters a through z, along with some other combinations of symbols
        self.what_to_find = "c\+\+|c#|[a-z]+"
    
    def fit(self, X, y=None):
        '''
            This function exists only to make the class compatible with the sklean API.
        :param X: numpy.ndarray
            This parameter is used for reading the dataset to be normalized in the transform function;
        :param y: numpy.ndarray
            Exists only to fit with the sklearn API, is usually ignored;
        '''
        return self
    
    def transform(self, X, y=None):
        '''
            Normalizez the text from a numpy array; \n is replaced by space, all letters become lowercase;
        :param X: numpy.ndarray
            For reading the text which needs to be normalized;
        :param y: numpy.ndarray
            Exists only to fit with the sklearn API, is usually ignored;
        '''
        
        #replacing \n by space, converting all letters to lowercase
        for i in range(len(X)):
            X[i] = X[i].replace('\n', " ")
            X[i] = X[i].lower()
            X[i] = ' '.join(re.findall(self.what_to_find, X[i]))
        return X
            
    def fit_transform(self, X, y=None):
        '''
            Applies the fit and transform functions simultaneously;
        :param X: numpy.ndarray
            For reading the text which needs to be normalized;
        :param y: numpy.ndarray
            Exists only to fit with the sklearn API, is usually ignored;
        '''
        return self.fit(X, y).transform(X)
    

class StopWordsExtractor(BaseEstimator, TransformerMixin):
    def __init__(self, stop_words):
        '''
            Initializes the Stopwords Extractor;
        :param stop_words: list
            A list which contains the stopwords which need to be removed from the text;
        '''
        self.stopwords = stop_words
        
    def fit(self, X, y=None):
        '''
            This function exists only to make the class compatible with the sklean API.
        :param X: numpy.ndarray
            This parameter is used for reading the dataset to be normalized in the transform function;
        :param y: numpy.ndarray
            Exists only to fit with the sklearn API, is usually ignored;
        '''
        return self
    
    def transform(self, X, y=None):
        '''
            Removes the stopwords from the text contained within a numpy array;
        :param X: numpy.ndarray
            For reading the text which needs to be normalized;
        :param y: numpy.ndarray
            Exists only to fit with the sklearn API, is usually ignored;
        '''
        #Removing the words that are in the list of stopwords;
        for i in range(len(X)):
            X[i] = ' '.join([word for word in word_tokenize(X[i]) if word not in self.stopwords])
        
        return X

class ApplyStemmer(BaseEstimator, TransformerMixin):
    def __init__(self, stemmer):
        '''
            Initializes the ApplyStemmer class;
        :param stemmer: python object
            The class which corresponds to the stemmer which will be used in the transform function;
        '''
        self.stemmer = stemmer
        #defining some symbols which need to be treated as a single word;
        self.words_to_keep = [("c", "#"), ("c", "++")]
        self.mwes = MWETokenizer(self.words_to_keep)
        
    def fit(self, X, y=None):
        '''
            This function exists only to make the class compatible with the sklean API.
        :param X: numpy.ndarray
            This parameter is used for reading the dataset to be normalized in the transform function;
        :param y: numpy.ndarray
            Exists only to fit with the sklearn API, is usually ignored;
        '''
        return self
    
    def transform(self, X, y=None):
        '''
            Applies a stemmer to the text contained within a numpy array;
        :param X: numpy.ndarray
            For reading the text which needs to be normalized;
        :param y: numpy.ndarray
            Exists only to fit with the sklearn API, is usually ignored;
        '''
        #Applying the stemmer each row at a time;
        for i in range(len(X)):
            X[i] = ' '.join([self.stemmer.stem(word) for word in self.mwes.tokenize(word_tokenize(X[i]))])
        
        return X

class TextNormalizerSentiment(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        '''
            This function exists only to make the class compatible with the sklean API.
        :param X: numpy.ndarray
            This parameter is used for reading the dataset to be normalized in the transform function;
        :param y: numpy.ndarray
            Exists only to fit with the sklearn API, is usually ignored;
        '''
        return self
    
    def transform(self, X, y=None):
        '''
            Normalizez the text from a numpy array; \n is replaced by space, all letters become lowercase;
        :param X: numpy.ndarray
            For reading the text which needs to be normalized;
        :param y: numpy.ndarray
            Exists only to fit with the sklearn API, is usually ignored;
        '''
        for i in range(len(X)):
            X[i] = X[i].replace('\n', " ")
            X[i] = X[i].lower()
            X[i] = ' '.join(re.findall('[a-z]+', X[i]))
        return X
            
    def fit_transform(self, X, y=None):
        '''
            Applies the fit and transform functions simultaneously;
        :param X: numpy.ndarray
            For reading the text which needs to be normalized;
        :param y: numpy.ndarray
            Exists only to fit with the sklearn API, is usually ignored;
        '''
        return self.fit(X, y).transform(X)

class StopWordsExtractorSentiment(BaseEstimator, TransformerMixin):
    def __init__(self, stopwords):
        self.stopwords = stopwords
        '''
            Initializes the Stopwords Extractor;
        :param stop_words: list
            A list which contains the stopwords which need to be removed from the text;
        '''
    def fit(self, X, y=None):
        '''
            This function exists only to make the class compatible with the sklean API.
        :param X: numpy.ndarray
            This parameter is used for reading the dataset to be normalized in the transform function;
        :param y: numpy.ndarray
            Exists only to fit with the sklearn API, is usually ignored;
        '''
        return self
    
    def transform(self, X, y=None):
        '''
            Removes the stopwords from the text contained within a numpy array;
        :param X: numpy.ndarray
            For reading the text which needs to be normalized;
        :param y: numpy.ndarray
            Exists only to fit with the sklearn API, is usually ignored;
        '''
        for i in range(len(X)):
            X[i] = ' '.join([word for word in word_tokenize(X[i]) if word not in self.stopwords])
        return X

class ApplyStemmerSentiment(BaseEstimator, TransformerMixin):
    def __init__(self, stemmer):
        '''
            Initializes the ApplyStemmer class;
        :param stemmer: python object
            The class which corresponds to the stemmer which will be used in the transform function;
        '''
        self.stemmer = stemmer
        
    def fit(self, X, y=None):
        '''
            This function exists only to make the class compatible with the sklean API.
        :param X: numpy.ndarray
            This parameter is used for reading the dataset to be normalized in the transform function;
        :param y: numpy.ndarray
            Exists only to fit with the sklearn API, is usually ignored;
        '''
        return self
    
    def transform(self, X, y=None):
        '''
            Applies a stemmer to the text contained within a numpy array;
        :param X: numpy.ndarray
            For reading the text which needs to be normalized;
        :param y: numpy.ndarray
            Exists only to fit with the sklearn API, is usually ignored;
        '''
        for i in range(len(X)):
            X[i] = ' '.join([self.stemmer.stem(word) for word in word_tokenize(X[i])])
        return X