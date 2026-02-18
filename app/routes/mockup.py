from __future__ import annotations

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from app.core.config import MOCKUPS_DIR
from app.models import MockupRequest
from app.services.template_service import get_shirt_config, safe_filename
from app.services.image_service import generate_mockup

router = APIRouter(tags=["mockup"])

@router.post("/mockup/generate")
def mockup_generate(req: MockupRequest):
    shirt_cfg = get_shirt_config(req.shirt_id)

    mockup_filename = generate_mockup(
        shirt_cfg=shirt_cfg,
        placement=req.placement,
        logo_id=req.logo_id,
        scale=req.scale,
        offset_x=req.offset_x,
        offset_y=req.offset_y,
    )

    return {
        "mockup_filename": mockup_filename,
        "download_url": f"/mockups/{mockup_filename}",
    }

@router.get("/mockups/{mockup_filename}")
def get_mockup(mockup_filename: str):
    fn = safe_filename(mockup_filename)
    path = MOCKUPS_DIR / fn
    if not path.exists():
        raise HTTPException(status_code=404, detail="Mockup not found.")
    return FileResponse(path, media_type="image/png", filename=fn)
