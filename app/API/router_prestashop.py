from fastapi import APIRouter
from app.API.prestashop.products.routes import router as products_router
from app.API.prestashop.orders.routes import router as orders_router
from app.API.prestashop.payments.routes import router as payments_router
from app.API.prestashop.proveedores.routes import router as proveedores_router
from app.API.prestashop.customers.routes import router as customers_router

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
    payments_router,
    prefix="/payments",
    tags=["Payments"]
)
router.include_router(
    proveedores_router,
    prefix="/suppliers",
    tags=["Suppliers"]
)
router.include_router(
    customers_router,
    prefix="/customers",
    tags=["PrestaShop Customers"]
)