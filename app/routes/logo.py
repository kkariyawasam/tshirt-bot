from __future__ import annotations

import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from PIL import Image
from io import BytesIO

from app.core.config import LOGOS_DIR
from app.models import GenerateLogoRequest
from app.services.template_service import ensure_png, safe_filename
from app.services.ai_service import generate_logo

router = APIRouter(tags=["logo"])

@router.post("/logo/upload")
async def upload_logo(file: UploadFile = File(...)):
    ensure_png(file)

    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Empty upload.")

    # Validate
    try:
        with Image.open(BytesIO(content)) as img:
            img.verify()
    except Exception:
        raise HTTPException(status_code=400, detail="Uploaded file is not a valid PNG image.")

    logo_id = f"{uuid.uuid4().hex}.png"
    (LOGOS_DIR / logo_id).write_bytes(content)
    return {"logo_id": logo_id}

@router.post("/logo/generate")
def logo_generate(req: GenerateLogoRequest):
    return generate_logo(req)

@router.get("/logos/{logo_filename}")
def get_logo(logo_filename: str):
    fn = safe_filename(logo_filename)
    path = LOGOS_DIR / fn
    if not path.exists():
        raise HTTPException(status_code=404, detail="Logo not found.")
    return FileResponse(path, media_type="image/png", filename=fn)
