import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
nltk.download('stopwords') # first time
nltk.download('wordnet')  # first time


def clean_text(text):
    """
    Cleans the text from urls, @ mentions, special characters, numbers, and uppercase letters
    """
    # Handle URLs
    text = re.sub(r'https?://\S+|www\.\S+', '', text)

    # Handle mentions (e.g., @username)
    text = re.sub(r'@[\w_]+', '', text)

    # Remove special characters and numbers, and convert to lowercase
    text = re.sub(r'[^a-zA-Z]', ' ', text)
    text = text.lower()

    # Remove leading and trailing spaces
    text = text.strip()

    # Remove stop words
    stop_words = set(stopwords.words('english'))
    words = text.split()
    filtered_words = [word for word in words if word not in stop_words]

    # Lemmatize the remaining words
    lemmatizer = WordNetLemmatizer()
    filtered_words = [lemmatizer.lemmatize(word) for word in filtered_words]

    text = ' '.join(filtered_words)

    return text
