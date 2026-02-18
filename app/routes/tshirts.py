from __future__ import annotations

from fastapi import APIRouter
from app.services.template_service import load_templates

router = APIRouter(tags=["tshirts"])

@router.get("/tshirts")
def get_tshirts():
    return load_templates()
