"""Script to display the text mining tools
 in an interactive  web page with Streamlit
"""


# Import main packages
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# Packages for Word Cloud
from os import path
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator


# natural language processing: n-gram ranking
import re
import unicodedata
import nltk
from nltk.corpus import stopwords

# Force settings
st.set_option('deprecation.showPyplotGlobalUse', False)


# Main Title
st.sidebar.text("© Le Wagon - Data Bootcamp #552")
st.title('Text Mining of OpenFoodFacts Dataset')


# ----------------------------------
#      UPLOAD DATA TO STREAMLIT
# ----------------------------------

DATA_FILE = './raw_data/ocr_labeled.csv'

# Add appropriate words that will be ignored in the analysis
ADDITIONAL_STOPWORDS = ['covfefe', 'dont', 'e', 'g', 'kj', 'kcal',]
# Create custom list of stopwords
stopwords = nltk.corpus.stopwords.words('english'
                                        ) + nltk.corpus.stopwords.words(
                                        'french') + ADDITIONAL_STOPWORDS

def basic_clean(text):
    """
    A simple function to clean up the data. All the words that
    are not designated as a stop word is then lemmatized after
    encoding and basic regex parsing are performed.
    """
    # Instanciate the Lemmatizer
    wnl = nltk.stem.WordNetLemmatizer()

    # Apply rules for basic cleaning
    words = (unicodedata.normalize('NFKD', text)
            .encode('ascii', 'ignore')
            .decode('utf-8', 'ignore')
            .lower())
    words = re.sub('\d+', '', words) # Remove numbers
    words = re.sub(r'[^\w\s]', '', words).split()
    return [wnl.lemmatize(word) for word in words if word not in stopwords]

#@st.cache
def load_data(nrows=10000):
    data = pd.read_csv(DATA_FILE, nrows=nrows)
    #data['clean_tokens'] = data['clean_text'].apply(lambda text: basic_clean(text))
    clean_tokens = pd.DataFrame(data['clean_text'].apply(lambda text: basic_clean(text)))
    data.insert (2, 'clean_tokens', clean_tokens)

    return data

# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
data = load_data(100)
# Remove the loading text ndication.
data_load_state.text('')

st.subheader("Load data")

st.write("Display sample data by ticking the checkbox in the sidebar.")
agree = st.sidebar.checkbox('Display raw data')
if agree:
    st.dataframe(data)


# ----------------------------------
#      SELECT DATA
# ----------------------------------

preprocessing = st.sidebar.radio("Choose a degree of text preprocessing:", 
                                ('Raw', 'Clean', 'Tokenized'),
                                index=2)
if preprocessing == 'Raw':
    process_level = 'fr_text'
elif preprocessing == 'Clean':
    process_level = 'clean_text'
else:
    process_level = 'clean_tokens'

# Create a list of categories
categories_1 = list(data.pnns_groups_1.unique())

agree = st.sidebar.checkbox("Show Analysis by Category (PNNS 1)", False)
if agree:
    select = st.sidebar.selectbox('Select a Category:', categories_1)
    #get the state selected in the selectbox
    category_data = str(select)
else:
    category_data = False


# ----------------------------------
#      VISUALIZE WORLD CLOUD
# ----------------------------------

# # Create Corpus with a Function
def aggregate_text():
    """Aggregate the text from a scpecific column and filtered by category"""

    text = ''

    if preprocessing=='Tokenized':
        if category_data is False:
            for words in data[process_level]:
                text += ' '.join(words) + ' '
        else:
            for words in data[data['pnns_groups_1']==category_data][process_level]:
                text += ' '.join(words) + ' '

    else:
        if category_data is False:
            for words in data[process_level]:
                words = words.split()
                text += ' '.join(words) + ' '
        else:
            for words in data[data['pnns_groups_1']==category_data][process_level]:
                words = words.split()
                text += ' '.join(words) + ' '
    
    return text


st.subheader("Word Cloud")

st.write("Display word cloud of the data by ticking the checkbox in the sidebar.")
agree = st.sidebar.checkbox('Display word cloud')
if agree:
    wordcloud = WordCloud(background_color='white',
                        stopwords=stopwords, 
                        max_words=100,
                        max_font_size=50, 
                        random_state=42,).generate(aggregate_text())
    # Display the generated image:
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()
    st.pyplot()



# if st.checkbox('Show raw data'):
#     st.subheader('Raw data')
#     st.write(data)

# st.subheader('Number of pickups by hour')
# hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
# st.bar_chart(hist_values)

# # Some number in the range 0-23
# hour_to_filter = st.slider('hour', 0, 23, 17)
# filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]

# st.subheader('Map of all pickups at %s:00' % hour_to_filter)
# st.map(filtered_data)
