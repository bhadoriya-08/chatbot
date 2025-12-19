# ChatBot/scheduler.py  (update your existing file's scheduled_update to include images)
from apscheduler.schedulers.background import BackgroundScheduler
from ingestion.sources_fetcher import fetch_latest_articles
from ingestion.ingestor import ingest_text_document, ingest_image_file
import os, time

WATCH_IMAGES_FOLDER = "storage/images"

def scheduled_update():
    print("Running scheduled update...")
    # ingest articles (existing)
    try:
        articles = fetch_latest_articles()
        for idx, article in enumerate(articles):
            path = f"scheduled_article_{int(time.time())}_{idx}.txt"
            with open(path, "w", encoding="utf-8") as f:
                f.write(article)
            ingest_text_document(path)
    except Exception as e:
        print("Scheduled text fetch failed:", e)

    # ingest any new images found in WATCH_IMAGES_FOLDER
    try:
        os.makedirs(WATCH_IMAGES_FOLDER, exist_ok=True)
        for fname in os.listdir(WATCH_IMAGES_FOLDER):
            fpath = os.path.join(WATCH_IMAGES_FOLDER, fname)
            # simplistic: ingest every file (idempotency can be improved)
            if os.path.isfile(fpath):
                # read image and generate caption via multimodal pipeline before ingest
                from multimodal.image_understanding import analyze_image_bytes
                with open(fpath, "rb") as f:
                    b = f.read()
                caption = analyze_image_bytes(b)
                ingest_image_file(fpath, caption)
    except Exception as e:
        print("Scheduled image ingestion failed:", e)

    print("Scheduled update completed!")

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(scheduled_update, "interval", hours=24)
    scheduler.start()
    print("Scheduler started.")
