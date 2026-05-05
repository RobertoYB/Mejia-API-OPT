from fastapi import APIRouter
from app.API.wordpress.products.routes import router as products_router
from app.API.wordpress.orders.routes import router as orders_router

router = APIRouter()

router.include_router(
    products_router,
    prefix="/products",
    tags=["Products"]
)

router.include_router(
    orders_router,
    prefix="/orders",
    tags=["Orders"]
)