import requests
import logging

def fetch_url_title(url):
    try:
        response = requests.get(url)
        response.raise_for_status()

        title = "No title found"
        if response.content:
            # Simple title extraction (you could use BeautifulSoup for more complex parsing)
            title_start = response.content.find(b"<title>")
            title_end = response.content.find(b"</title>")
            if title_start != -1 and title_end != -1:
                title = response.content[title_start + 7:title_end].decode("utf-8")
        
        logging.info(f"Fetched title: {title} from URL: {url}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching URL {url}: {e}")
