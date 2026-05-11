from fastapi import APIRouter
from app.API.wordpress.products.routes import router as products_router
from app.API.wordpress.orders.routes import router as orders_router
from app.API.wordpress.clients.routes import router as clients_router
from app.API.wordpress.coupons.routes import router as coupons_router
from app.API.wordpress.customers.routes import router as customers_router

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

router.include_router(
    clients_router,
    prefix="/clients",
    tags=["Clients"]
)

router.include_router(    
    coupons_router,
    prefix="/coupons",
    tags=["Coupons"]
)

router.include_router(
    customers_router,
    prefix="/customers",
    tags=["Customers"]
)