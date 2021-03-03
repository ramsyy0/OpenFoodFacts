# create custom preprocessor with Spellcheck
from sklearn.base import TransformerMixin, BaseEstimator
from spellchecker import SpellChecker
import re
import string
import unicodedata
import pandas as pd

# with spellcheck
class CustomPreprocessor(TransformerMixin, BaseEstimator):
# TransformerMixin generates a fit_transform method from fit and transform
# BaseEstimator generates get_params and set_params methods

    def __init__(self):
        pass

    def fit(self, X, y=None):
        self.means = X.mean()
        return self

    def transform(self, X, y=None):
        # Return result as dataframe for integration into ColumnTransformer
        ## CLEAN OCR TEXT

            # Remove punctuation
        def remove_punc(text):
            for punctuation in string.punctuation:
                text = text.replace(punctuation, ' ')
            text = re.sub(" +", " ", text)
            return text

            # Remove nonalpha characters:
        def remove_nonalpha(text):
            text = ''.join(c for c in text if c.isalpha() or c == ' ')
            return re.sub(" +", " ", text)

        # Spellcheck:
        def corrected(text):
            # initialize spellchecker
            spell = SpellChecker(language='fr', distance=1, case_sensitive=False)
            # get misspellings and corrections
            text_splitted = text.split()
            misspelled = spell.unknown(text_splitted)
            correction = {word:spell.correction(word) for word in misspelled}

            # replace misspellings in text
            for k,v in correction.items():
                text = text.replace(k,v)
            return text

            # Remove accents
        def remove_accents(text):
            return ''.join(c for c in unicodedata.normalize('NFKD', text)
                          if unicodedata.category(c) != 'Mn')

        def clean_ocr_text(text, spellcheck=True):
            text = text.lower().replace('\n',' ')

            if spellcheck:
                clean_funcs = [remove_punc, remove_nonalpha, corrected, remove_accents]
            else:
                clean_funcs = [remove_punc, remove_nonalpha, remove_accents]

            for func in clean_funcs:
                text = func(text)
            return text.strip(" ")

        X = X.apply(lambda x: clean_ocr_text(x, spellcheck=True))
        return X

# without spellcheck
class CustomPreprocessorNoSpellCheck(TransformerMixin, BaseEstimator):
# TransformerMixin generates a fit_transform method from fit and transform
# BaseEstimator generates get_params and set_params methods

    def __init__(self):
        pass

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        # Return result as dataframe for integration into ColumnTransformer
        ## CLEAN OCR TEXT

            # Remove punctuation
        def remove_punc(text):
            for punctuation in string.punctuation:
                text = text.replace(punctuation, ' ')
            text = re.sub(" +", " ", text)
            return text

            # Remove nonalpha characters:
        def remove_nonalpha(text):
            text = ''.join(c for c in text if c.isalpha() or c == ' ')
            return re.sub(" +", " ", text)

        # Spellcheck:
        def corrected(text):
            # initialize spellchecker
            spell = SpellChecker(language='fr', distance=1, case_sensitive=False)
            # get misspellings and corrections
            text_splitted = text.split()
            misspelled = spell.unknown(text_splitted)
            correction = {word:spell.correction(word) for word in misspelled}

            # replace misspellings in text
            for k,v in correction.items():
                text = text.replace(k,v)
            return text

            # Remove accents
        def remove_accents(text):
            return ''.join(c for c in unicodedata.normalize('NFKD', text)
                          if unicodedata.category(c) != 'Mn')

        def clean_ocr_text(text, spellcheck=False):
            text = text.lower().replace('\n',' ')

            if spellcheck:
                clean_funcs = [remove_punc, remove_nonalpha, corrected, remove_accents]
            else:
                clean_funcs = [remove_punc, remove_nonalpha, remove_accents]

            for func in clean_funcs:
                text = func(text)
            return text.strip(" ")

        X = X.apply(lambda x: clean_ocr_text(x, spellcheck=False))
        return X
