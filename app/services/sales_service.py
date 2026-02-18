from __future__ import annotations

import requests
from fastapi import HTTPException

from app.core.config import N8N_WEBHOOK_URL, API_BASE_URL

def send_to_sales_webhook(payload: dict) -> None:
    try:
        r = requests.post(N8N_WEBHOOK_URL, json=payload, timeout=10)
        if r.status_code >= 400:
            raise HTTPException(status_code=500, detail=f"n8n webhook error: {r.text}")
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to contact n8n webhook: {str(e)}")

def build_download_url(mockup_filename: str) -> str:
    return f"{API_BASE_URL}/mockups/{mockup_filename}"
