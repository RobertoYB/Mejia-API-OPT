from fastapi import FastAPI
from app.API.router_odoo import router as api_router_odoo
from app.API.router_prestashop import router as api_router_prestashop
from app.API.router_bridge import router as api_router_bridge
from app.API.router_wordpress import router as api_router_wordpress

app = FastAPI()

@app.get("/")
def root():
    return {"mensaje": "api funcionado nene"}

app.include_router(api_router_odoo, prefix="/api/odoo")

app.include_router(api_router_prestashop, prefix="/api/prestashop")

app.include_router(api_router_bridge, prefix="/api/bridge")

app.include_router(api_router_wordpress, prefix="/api/wordpress")