
import trafilatura
import requests

def extract_text(url):

    try:
        response = requests.get(url, timeout=10)
        downloaded = response.text

        text = trafilatura.extract(downloaded)

        return text[:4000] if text else None

    except Exception as e:
        return None
