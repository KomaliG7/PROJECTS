from transformers import pipeline


sentiment_pipeline = pipeline("sentiment-analysis")

def analyze_feedback(feedback_text):
    result = sentiment_pipeline(feedback_text)[0]
    label = result['label']   # POSITIVE or NEGATIVE
    score = result['score']   # Confidence score
    return label, round(score, 2)

if __name__ == "__main__":
    feedback = "It was not good "
    sentiment, confidence = analyze_feedback(feedback)
    print(f"Sentiment: {sentiment}, Confidence: {confidence}")
