from __future__ import annotations

import uuid
from pathlib import Path
from typing import Dict, Any

from fastapi import HTTPException
from PIL import Image

from app.core.config import BASE_DIR, LOGOS_DIR, MOCKUPS_DIR
from app.services.template_service import safe_filename

def resize_logo_for_placement(
    logo: Image.Image,
    box_w: int,
    box_h: int,
    padding_pct: float = 0.10,
    max_fill_pct: float = 0.85,
    scale: float = 1.0,
) -> Image.Image:
    if box_w <= 0 or box_h <= 0:
        raise HTTPException(status_code=400, detail="Invalid placement box size.")

    padding_pct = max(0.0, min(0.40, float(padding_pct)))
    max_fill_pct = max(0.10, min(1.0, float(max_fill_pct)))
    scale = max(0.10, min(3.0, float(scale)))

    w, h = logo.size
    if w <= 0 or h <= 0:
        raise HTTPException(status_code=400, detail="Invalid logo image size.")

    avail_w = max(1, int(box_w * (1 - 2 * padding_pct)))
    avail_h = max(1, int(box_h * (1 - 2 * padding_pct)))

    scale_fit = min(avail_w / w, avail_h / h)
    scale_cap = min((box_w * max_fill_pct) / w, (box_h * max_fill_pct) / h)

    base_scale = min(scale_fit, scale_cap)
    final_scale = base_scale * scale

    new_w = max(1, int(w * final_scale))
    new_h = max(1, int(h * final_scale))
    return logo.resize((new_w, new_h), resample=Image.LANCZOS)

def generate_mockup(
    shirt_cfg: Dict[str, Any],
    placement: str,
    logo_id: str,
    scale: float,
    offset_x: int,
    offset_y: int,
) -> str:
    template_path = BASE_DIR / shirt_cfg["template_path"]
    if not template_path.exists():
        raise HTTPException(status_code=500, detail=f"Template image not found: {template_path}")

    placement_cfg = (shirt_cfg.get("placements") or {}).get(placement)
    if not placement_cfg:
        raise HTTPException(status_code=400, detail=f"Placement not configured: {placement}")

    x = int(placement_cfg["x"])
    y = int(placement_cfg["y"])
    w = int(placement_cfg["w"])
    h = int(placement_cfg["h"])

    padding_pct = float(placement_cfg.get("padding_pct", 0.10))
    max_fill_pct = float(placement_cfg.get("max_fill_pct", 0.85))

    logo_filename = safe_filename(logo_id)
    logo_path = LOGOS_DIR / logo_filename
    if not logo_path.exists():
        raise HTTPException(status_code=404, detail="Logo not found. Upload or generate first.")

    shirt_img = Image.open(template_path).convert("RGBA")
    logo_img = Image.open(logo_path).convert("RGBA")

    logo_resized = resize_logo_for_placement(
        logo=logo_img,
        box_w=w,
        box_h=h,
        padding_pct=padding_pct,
        max_fill_pct=max_fill_pct,
        scale=scale,
    )

    px = x + (w - logo_resized.size[0]) // 2 + int(offset_x)
    py = y + (h - logo_resized.size[1]) // 2 + int(offset_y)

    # Clamp to image bounds
    shirt_w, shirt_h = shirt_img.size
    px = max(0, min(px, shirt_w - logo_resized.size[0]))
    py = max(0, min(py, shirt_h - logo_resized.size[1]))

    shirt_img.paste(logo_resized, (px, py), logo_resized)

    mockup_filename = f"{shirt_cfg['id']}_{placement}_{uuid.uuid4().hex}.png"
    out_path = MOCKUPS_DIR / mockup_filename
    shirt_img.save(out_path, format="PNG")

    return mockup_filename
