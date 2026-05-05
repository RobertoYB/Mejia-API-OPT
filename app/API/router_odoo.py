from fastapi import APIRouter
from app.API.odoo.providers_o.routes import router as providers_router
from app.API.odoo.products.routes import router as products_router
from app.API.odoo.orders.routes import router as orders_router
from app.API.odoo.stock.routes import router as stock_router  
from app.API.odoo.categories.routes import router as categories_router


router = APIRouter()

router.include_router(
    categories_router,
    prefix="/categories",
    tags=["Categories"]
)

router.include_router(
    providers_router,
    prefix="/providers",
    tags=["Providers"]
)

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
    stock_router,
    prefix="/stock",
    tags=["Stock"]
)

