from app.Core.odoo_client import models, uid
from app.Core.config import settings
from app.Core.prestashop_client import prestashop_get, prestashop_post, prestashop_put
from app.API.bridge.products.mapper import odoo_to_prestashop
from app.API.bridge.products.mapper_stock import stock_xml
import xml.etree.ElementTree as ET

def sync_products():
  odoo_products = models.execute_kw(
    settings.ODOO_DB,
    uid,
    settings.ODOO_PASSWORD,
    'product.template',
    'search_read',
    [[]],
    {'fields':['id','name','list_price','default_code','qty_available']}
  )

  prestashop_data = prestashop_get("products",fields="id,reference")

  existing_refs = set()

  if "products" in prestashop_data:
    for prod in prestashop_data["products"]:
      if prod.get("reference"):
        existing_refs.add(prod["reference"])

  created_products = []
  skipped_products = []
  created = 0
  skipped = 0

  for product in odoo_products:
    ref = product.get("default_code")
    price = product.get("list_price")
    stock = product.get("qty_available")
    name = product.get("name")

    if not ref:
      skipped += 1
      skipped_products.append(name)
      continue

    if ref in existing_refs:
      skipped += 1
      skipped_products.append(name)
      continue

    if price is None or float(price) <=0:
      skipped += 1
      skipped_products.append(name)
      continue

    if stock is None or float(stock) <=0:
      skipped += 1
      skipped_products.append(name)
      continue

    xml = odoo_to_prestashop(product)

    response = prestashop_post("products", xml)

    root = ET.fromstring(response)

    product_id = int(root.find(".//id").text)

    stock_data = prestashop_get("stock_availables",filters={"id_product": product_id})

    stock_id = stock_data["stock_availables"][0]["id"]

    stock_body = stock_xml(stock_id, product_id, stock)

    prestashop_put(f"stock_availables/{stock_id}", stock_body)

    created +=1
    created_products.append(name)
  
  return {
    "Creados" : created_products,
    "Saltados": skipped_products,
    "Total creados": created,
    "Total saltados": skipped
  }

def create_one_product_by_reference(reference: str):

  # Buscar en Odoo por default_code
  rows = models.execute_kw(
    settings.ODOO_DB,
    uid,
    settings.ODOO_PASSWORD,
    'product.product',
    'search_read',
    [[['default_code', '=', reference]]],
    {'fields':['id','name','list_price','default_code','qty_available']}
  )

  if not rows:
    raise Exception("Producto no encontrado en Odoo con esa referencia")

  product = rows[0]

  if product.get("default_code") is False:
    product["default_code"] = None

  ref = product.get("default_code")
  if not ref:
    raise Exception("El producto no tiene referencia (default_code)")

  price = float(product.get("list_price") or 0)
  stock = float(product.get("qty_available") or 0)

  # No crear si precio 0 y stock 0
  if price == 0 and stock == 0:
    return {
      "created": False,
      "skipped": True,
      "message": "No se crea: precio 0 y stock 0",
      "reference": ref,
      "price": price,
      "stock": stock
    }

  # No duplicar en PrestaShop
  ps = prestashop_get("products", fields="id,reference", filters={"reference": ref})

  if "products" in ps and ps["products"]:
    return {
      "created": False,
      "message": "Ya existe en PrestaShop",
      "reference": ref
    }

  xml = odoo_to_prestashop(product)
  prestashop_post("products", xml)

  return {
    "created": True,
    "message": "Producto creado en PrestaShop",
    "reference": ref,
    "price": price,
    "stock": stock
  }