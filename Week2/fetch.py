import requests
import json
from typing import Optional


def get_page_content(url: str) -> Optional[str]:
    reader_url_prefix = "https://r.jina.ai/"
    reader_url = reader_url_prefix + url

    try:
        response = requests.get(reader_url, timeout=10)
        response.raise_for_status()  # raises for 4xx/5xx HTTP errors
        #print(response.content.decode('utf8'))
        return response.content.decode("utf-8")
    except (requests.exceptions.RequestException, UnicodeDecodeError) as e:
        print(f"Error fetching content from {url}: {e}")
        return None
    