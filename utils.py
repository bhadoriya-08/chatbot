# ChatBot/utils.py
import os
def ensure_dirs():
    os.makedirs("db", exist_ok=True)
    os.makedirs("storage/images", exist_ok=True)
    os.makedirs("storage/uploads", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
