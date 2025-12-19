from scraper.fetcher import fetch_website, fetch_rss, extract_text_from_html
from processor.cleaner import clean_text

import json
import os

def fetch_latest_articles():
    sources_file = os.path.join("config", "sources.json")
    with open(sources_file, "r", encoding="utf-8") as f:
        sources = json.load(f)["sources"]

    articles = []

    for source in sources:
        if source["type"] == "website":
            html = fetch_website(source["url"])
            text = extract_text_from_html(html)
        elif source["type"] == "rss":
            text = fetch_rss(source["url"])
        else:
            continue

        clean = clean_text(text)
        articles.append(clean)

    return articles
