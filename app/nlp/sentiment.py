from functools import lru_cache

from transformers import pipeline


@lru_cache(maxsize=1)
def get_sentiment_pipeline():
    return pipeline(
        "sentiment-analysis",
        model="distilbert-base-uncased-finetuned-sst-2-english"
    )


def analyze_sentiment(text: str) -> str:
    """
    Returns Positive, Negative or Neutral.

    The underlying model provides Positive/Negative.
    Neutral is assigned when confidence is relatively low.
    """

    classifier = get_sentiment_pipeline()

    result = classifier(text[:512])[0]

    label = result["label"]
    confidence = result["score"]

    if confidence < 0.65:
        return "Neutral"

    if label == "POSITIVE":
        return "Positive"

    return "Negative"