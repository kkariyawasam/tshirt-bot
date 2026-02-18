from __future__ import annotations

import base64
import uuid
from fastapi import HTTPException

from app.core.config import openai_client, LOGOS_DIR
from app.models import GenerateLogoRequest

def build_logo_prompt(req: GenerateLogoRequest) -> str:
    parts = []
    if req.brand_name:
        parts.append(f"Brand name: {req.brand_name}.")
    parts.append(f"Concept: {req.prompt}.")
    parts.append(f"Style: {req.style}.")
    if req.color_palette:
        parts.append(f"Color palette: {req.color_palette}.")

    parts.append(
        "Design a clean, print-ready logo. Centered composition. High contrast. "
        "No background scene. No mockup. No shadows. No gradients unless necessary. "
        "Crisp edges, suitable for placing on a t-shirt."
    )
    if req.transparent_background:
        parts.append("Transparent background.")
    return " ".join(parts)

def generate_logo(req: GenerateLogoRequest) -> dict:
    prompt = build_logo_prompt(req)

    try:
        result = openai_client.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            size=req.size,
            output_format="png",
            background="transparent" if req.transparent_background else "opaque",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OpenAI image generation failed: {str(e)}")

    try:
        b64 = result.data[0].b64_json
        img_bytes = base64.b64decode(b64)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to decode image: {str(e)}")

    logo_id = f"{uuid.uuid4().hex}.png"
    (LOGOS_DIR / logo_id).write_bytes(img_bytes)

    return {
        "logo_id": logo_id,
        "preview_url": f"/logos/{logo_id}",
        "prompt_used": prompt,
    }
