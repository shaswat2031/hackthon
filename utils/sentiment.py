from transformers import pipeline

# Load once, reuse (runs fully locally, no API)
_sentiment_pipeline = None

def get_sentiment(text: str) -> dict:
    global _sentiment_pipeline
    if _sentiment_pipeline is None:
        try:
            _sentiment_pipeline = pipeline(
                "sentiment-analysis",
                model="cardiffnlp/twitter-roberta-base-sentiment",
                # Note: return_all_scores is deprecated in some versions, using top_k
            )
        except Exception as e:
            print(f"Error loading sentiment model: {e}")
            return {"label": "neutral", "score": 0.0}

    try:
        result = _sentiment_pipeline(text[:512])[0]
        # In newer transformers, result is a dict with label and score
        return {"label": result["label"], "score": result["score"]}
    except:
        return {"label": "neutral", "score": 0.0}
