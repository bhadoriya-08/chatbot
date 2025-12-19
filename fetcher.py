import requests
from bs4 import BeautifulSoup
import feedparser

def fetch_website(url):
    response = requests.get(url)
    return response.text

def fetch_rss(url):
    feed = feedparser.parse(url)
    summaries = [entry.summary for entry in feed.entries if "summary" in entry]
    return "\n".join(summaries)

def extract_text_from_html(html):
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text(separator="\n")
