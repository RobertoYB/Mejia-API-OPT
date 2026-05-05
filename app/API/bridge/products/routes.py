from fastapi import APIRouter
from app.API.bridge.products.service import sync_products, create_one_product_by_reference
from app.API.prestashop.utils import ps_success, ps_error
from app.Core.prestashop_client import prestashop_get, prestashop_put
from app.API.bridge.products.mapper_product_deactivation import product_update


router = APIRouter()

@router.get("/")
def sync():

    try:
        result = sync_products()
        return ps_success(result)

    except Exception as e:
        return ps_error("500", str(e))
    
@router.get("/create-one/{reference}")
def create_one(reference: str):
  try:
    result = create_one_product_by_reference(reference)
    return ps_success(result)
  except Exception as e:
    return ps_error("500", str(e))


@router.delete("/ref/{reference}")  
def deactivate_product(reference: str):
    try:
        data = prestashop_get("products", filters={"reference": reference})

        if not data:
            return ps_error("404", "No se encontró un producto con la referencia dada")
        
        product = data['products'][0]
        id = product['id']
        price = product['price']

        if (isinstance(product['name'], list)):
           name = product['name'][0]['value']
        else:
           name = product['name']

        xml = product_update(id = id, active = "0", price = price, reference= reference, slug= reference, name = name, category_id = 2)

        prestashop_put(f"products/{id}", xml)

        updated_product = {
           "id": id,
            "name": name,
            "reference": reference,
            "active": "0",
        }

        return ps_success(updated_product)
    
    except Exception as e:
        return ps_error("500",str(e) )