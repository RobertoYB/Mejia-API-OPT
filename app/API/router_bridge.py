from fastapi import APIRouter

from app.API.bridge.products.routes import router as product_router

router = APIRouter()

router.include_router(
    product_router,
    prefix="/products",
    tags=["Categories"]
)
