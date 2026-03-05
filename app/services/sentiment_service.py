from textblob import TextBlob  # For simplicity; you can use a more advanced model

def analyze_sentiment(text: str) -> float:
    """Return sentiment score between -1 and 1."""
    blob = TextBlob(text)
    return blob.sentiment.polarity