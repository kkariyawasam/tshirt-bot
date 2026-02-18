from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Any
from fastapi import HTTPException, UploadFile

from app.core.config import TEMPLATES_JSON

def safe_filename(name: str) -> str:
    return Path(name).name

def ensure_png(upload: UploadFile) -> None:
    ct = (upload.content_type or "").lower()
    if ct not in ("image/png", "image/x-png"):
        raise HTTPException(status_code=400, detail="Only PNG files are supported for now.")

def load_templates() -> Dict[str, Any]:
    if not TEMPLATES_JSON.exists():
        raise HTTPException(status_code=500, detail="templates.json not found in app/")
    with TEMPLATES_JSON.open("r", encoding="utf-8") as f:
        data = json.load(f)

    if "shirts" not in data or not isinstance(data["shirts"], list):
        raise HTTPException(status_code=500, detail="templates.json invalid format: missing shirts[]")
    return data

def get_shirt_config(shirt_id: str) -> Dict[str, Any]:
    data = load_templates()
    for s in data["shirts"]:
        if s.get("id") == shirt_id:
            return s
    raise HTTPException(status_code=404, detail=f"Unknown shirt_id: {shirt_id}")
