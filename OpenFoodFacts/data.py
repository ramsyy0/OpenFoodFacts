import pandas as pd
from google.cloud import storage
from OpenFoodFacts.config import gcs_config

def get_data():
    client = storage.Client()
    bucket = client.get_bucket(gcs_config['BUCKET_NAME'])

    blob = bucket.blob(gcs_config['BUCKET_DATA_FILE'])
    blob.download_to_filename('ocr_labeled_spellcheck.csv')

    # import file in dataframe
    df = pd.read_csv('ocr_labeled_spellcheck.csv')
    return df

if __name__ == '__main__':
    get_data()
