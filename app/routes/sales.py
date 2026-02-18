from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.core.config import MOCKUPS_DIR
from app.models import SendToSalesRequest
from app.services.template_service import safe_filename
from app.services.sales_service import send_to_sales_webhook, build_download_url

router = APIRouter(tags=["sales"])

@router.post("/send-to-sales")
def send_to_sales(req: SendToSalesRequest):
    fn = safe_filename(req.mockup_filename)
    mockup_path = MOCKUPS_DIR / fn
    if not mockup_path.exists():
        raise HTTPException(status_code=404, detail="Mockup file not found.")

    download_url = build_download_url(fn)

    payload = {
        "customer_name": req.customer_name,
        "customer_email": req.customer_email,
        "shirt_id": req.shirt_id,
        "placement": req.placement,
        "download_url": download_url,
    }

    send_to_sales_webhook(payload)

    return {"message": "Mockup sent to sales successfully.", "download_url": download_url}
