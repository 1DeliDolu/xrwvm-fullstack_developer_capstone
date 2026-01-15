# Uncomment the imports below before you add the function code
import requests
import os
from urllib.parse import quote

backend_url = os.getenv("backend_url", default="http://localhost:3030")
sentiment_analyzer_url = os.getenv("sentiment_analyzer_url", default="http://localhost:5050/")

def get_request(endpoint, **kwargs):
    """
    Calls the Node backend with GET.
    Example:
      get_request("/fetchDealers")
      get_request("/fetchDealers/TX")
    """
    request_url = backend_url.rstrip("/") + endpoint

    try:
        response = requests.get(request_url, params=kwargs if kwargs else None, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Network exception occurred in get_request: {e}")
        return None


def analyze_review_sentiments(text):
    """
    Calls sentiment analyzer service.
    Expects something like:
      GET {sentiment_analyzer_url}/analyze/<text>
    Returns:
      {"sentiment": "positive" | "negative" | "neutral", ...}
    """
    if text is None:
        return {"sentiment": "neutral"}

    # URL encode (space, Turkish chars, punctuation vs.)
    encoded_text = quote(str(text))

    request_url = sentiment_analyzer_url.rstrip("/") + "/analyze/" + encoded_text

    try:
        response = requests.get(request_url, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Güvenli fallback: sentiment anahtarı yoksa neutral dön
        if isinstance(data, dict) and "sentiment" in data:
            return data
        return {"sentiment": "neutral"}
    except Exception as e:
        print(f"Network exception occurred in analyze_review_sentiments: {e}")
        return {"sentiment": "neutral"}


def post_review(data_dict):
    """
    Posts review to Node backend.
    Expects:
      POST {backend_url}/insert_review   (body: JSON)
    """
    request_url = backend_url.rstrip("/") + "/insert_review"
    try:
        response = requests.post(request_url, json=data_dict, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Network exception occurred in post_review: {e}")
        return None
