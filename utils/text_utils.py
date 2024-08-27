import re
from difflib import SequenceMatcher
from hashlib import sha256

import nltk


def normalize_text(text):
    """
    Normalize text by removing special characters, markdown-like syntax, and excess whitespace.
    """
    # Remove markdown-like syntax
    text = re.sub(r'\*\*Goal Title:\*\*\s*', '', text, flags=re.IGNORECASE)

    # Continue with normal normalization
    normalized_text = text.lower().strip()  # Lowercase and trim whitespace
    normalized_text = re.sub(r'\s+', ' ', normalized_text)  # Replace multiple spaces with a single space
    normalized_text = re.sub(r'[^\w\s]', '', normalized_text)  # Remove special characters

    return normalized_text


def calculate_hash(self, goal_data):
    """
    Calculate a hash of the normalized title and description.
    """
    normalized_title = self.normalize_text(goal_data['title'])
    normalized_description = self.normalize_text(goal_data['description'])
    combined_text = normalized_title + normalized_description
    return sha256(combined_text.encode('utf-8')).hexdigest()


nltk.download('wordnet')


def lemmatize_title(title):
    lemmatizer = nltk.WordNetLemmatizer()
    words = title.lower().split()
    lemmatized_words = [lemmatizer.lemmatize(word) for word in words]
    return " ".join(lemmatized_words)


def are_titles_similar(title1, title2, threshold=0.8):
    similarity = SequenceMatcher(None, title1, title2).ratio()
    return similarity > threshold
