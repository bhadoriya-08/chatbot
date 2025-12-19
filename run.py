from dotenv import load_dotenv
load_dotenv()     

import argparse
import uvicorn
from scheduler import start_scheduler

def start_api():
    uvicorn.run("api.app:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--chat", action="store_true")
    parser.add_argument("--schedule", action="store_true")
    args = parser.parse_args()

    if args.chat:
        print("Starting API server with scheduler...")
        start_scheduler()
        start_api()
    elif args.schedule:
        print("Starting scheduler only...")
        start_scheduler()
    else:
        print("Use one option:")
        print("python run.py --chat")
        print("python run.py --schedule")
