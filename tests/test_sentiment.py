from app.nlp.sentiment import analyze_sentiment


texts = [
    "I am extremely happy with the service.",
    "My order is late and nobody is helping me.",
    "The product is okay."
]


for text in texts:
    result = analyze_sentiment(text)

    print("=" * 50)
    print("Text:", text)
    print("Sentiment:", result)
    