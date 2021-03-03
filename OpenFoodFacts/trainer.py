from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.linear_model import RidgeClassifier
from sklearn.pipeline import Pipeline
import joblib
from google.cloud import storage

from OpenFoodFacts.config import gcs_config
from OpenFoodFacts.encoders import CustomPreprocessorNoSpellCheck
from OpenFoodFacts.data import get_data

def train_model():
    df = get_data()
    X = df['clean_text']
    y = df['pnns_groups_2']

    # pipeline

    pipeline = Pipeline([
        ('custom_preprocessor_no_spellcheck', CustomPreprocessorNoSpellCheck()),
        ('tfidf', TfidfVectorizer(ngram_range=(1, 2), min_df=50)),
        ('lsa', TruncatedSVD(n_components=2500)),
        ('model', RidgeClassifier())
    ])

    pipeline.fit(X,y)

    return pipeline

def save_model(pipe_model):
    filename = joblib.dump(pipe_model, 'trained_model.joblib')
    return filename

def upload_model(path_model):

    client = storage.Client()
    bucket = client.get_bucket(gcs_config['BUCKET_NAME'])

    blob = bucket.blob(gcs_config['BUCKET_MODEL_FILE'])
    blob.upload_from_filename('trained_model.joblib')

    return None

if __name__ == '__main__':
    fitted_model = train_model()
    model_file = save_model(fitted_model)
    upload_model(model_file)
