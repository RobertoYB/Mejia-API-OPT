from fastapi import FastAPI
from app.API.router_odoo import router as api_router_odoo
from app.API.router_prestashop import router as api_router_prestashop
from app.API.router_bridge import router as api_router_bridge
from app.API.router_wordpress import router as api_router_wordpress
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"mensaje": "api funcionado nene"}

app.include_router(api_router_odoo, prefix="/api/odoo")

app.include_router(api_router_prestashop, prefix="/api/prestashop")

app.include_router(api_router_bridge, prefix="/api/bridge")

app.include_router(api_router_wordpress, prefix="/api/wordpress")