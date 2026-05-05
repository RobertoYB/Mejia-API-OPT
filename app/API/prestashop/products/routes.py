from fastapi import APIRouter
from app.Core.prestashop_client import prestashop_get, prestashop_put, prestashop_get_xml
from app.API.prestashop.utils import ps_success, ps_error
import xml.etree.ElementTree as ET
from app.API.prestashop.products.schema_json import ProductUpdate
import re

router = APIRouter()

fieldsproducts = "id,name,price,wholesale_price,quantity,reference,active,id_category_default,date_add,date_upd"

@router.get("/")
def get_products():
    try:
        data = prestashop_get("products", fieldsproducts)

        if not data:
            return ps_error("404", "No se encontraron productos")
        
        return ps_success(data)
    
    except Exception as e:
        return ps_error("500",str(e) )
    
    
@router.get("/{reference}")
def get_orders_ref(reference: str):
    try:
        data = prestashop_get("products", fieldsproducts, filters={"reference": reference})

        if not data:
            return ps_error("404", "No se encontró un producto con la referencia dada")
        
        return ps_success(data)
    
    except Exception as e:
        return ps_error("500",str(e) )

@router.put("/{reference}")
def update_product(reference: str, payload: ProductUpdate):
    try:
        search = prestashop_get("products", filters={"reference": reference})

        if "products" not in search or len(search["products"]) == 0:
            return ps_error("404", "Producto no encontrado")

        product_id = search["products"][0]["id"]

        xml_data = prestashop_get_xml(f"products/{product_id}")
        root = ET.fromstring(xml_data)
        product_node = root.find("product")

        non_writable_fields = [
        "manufacturer_name",
        "quantity",
        "id_default_image",
        "position_in_category",
        "type",
        "date_add",
        "date_upd"
    ]

        for field in non_writable_fields:
            node = product_node.find(field)
            if node is not None:
                product_node.remove(node)

        update_data = payload.model_dump(exclude_none=True)

        for field, value in update_data.items():
            node = product_node.find(field)
            if node is not None:
                node.text = str(value)

        xml_body = ET.tostring(root, encoding="utf-8").decode("utf-8")

        prestashop_put(f"products/{product_id}", xml_body)

        return ps_success("Producto actualizado correctamente")

    except Exception as e:
        return ps_error("500", str(e))