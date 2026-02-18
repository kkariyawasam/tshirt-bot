from __future__ import annotations

from fastapi import FastAPI

from app.routes.tshirts import router as tshirts_router
from app.routes.logo import router as logo_router
from app.routes.mockup import router as mockup_router
from app.routes.sales import router as sales_router

app = FastAPI(title="Tshirt Mockup API")

@app.get("/health")
def health():
    return {"ok": True}

app.include_router(tshirts_router)
app.include_router(logo_router)
app.include_router(mockup_router)
app.include_router(sales_router)
