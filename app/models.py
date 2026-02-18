from __future__ import annotations

from typing import Optional, Literal
from pydantic import BaseModel

LogoStyle = Literal["minimal", "mascot", "vintage", "modern", "luxury"]

class MockupRequest(BaseModel):
    shirt_id: str
    placement: str
    logo_id: str

    # Preview controls
    scale: float = 1.0
    offset_x: int = 0
    offset_y: int = 0

class SendToSalesRequest(BaseModel):
    customer_name: str
    customer_email: str  # keep as str to avoid EmailStr dependency issues
    shirt_id: str
    placement: str
    mockup_filename: str

class GenerateLogoRequest(BaseModel):
    brand_name: Optional[str] = None
    prompt: str
    style: LogoStyle = "minimal"
    color_palette: Optional[str] = None
    transparent_background: bool = True
    size: str = "1024x1024"
