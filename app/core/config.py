from __future__ import annotations

import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

# Load env vars from .env
load_dotenv()

# Project root (tshirt-bot/)
BASE_DIR = Path(__file__).resolve().parents[2]

# app/ folder
APP_DIR = BASE_DIR / "app"
TEMPLATES_JSON = APP_DIR / "templates.json"

# media/ folders
MEDIA_DIR = BASE_DIR / "media"
TEMPLATES_DIR = MEDIA_DIR / "templates"
LOGOS_DIR = MEDIA_DIR / "logos"
MOCKUPS_DIR = MEDIA_DIR / "mockups"
EXPORTS_DIR = MEDIA_DIR / "exports"

for d in (MEDIA_DIR, TEMPLATES_DIR, LOGOS_DIR, MOCKUPS_DIR, EXPORTS_DIR):
    d.mkdir(parents=True, exist_ok=True)

# OpenAI client
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
if not OPENAI_API_KEY:
    # Don't crash import-time in production; routes can handle missing key.
    # But for local dev it’s helpful to fail loudly:
    raise RuntimeError("OPENAI_API_KEY not found. Put it in .env or environment variables.")

openai_client = OpenAI(api_key=OPENAI_API_KEY)

# App settings
N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL", "http://localhost:5678/webhook/send-to-sales")
API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")  # used for links in emails
