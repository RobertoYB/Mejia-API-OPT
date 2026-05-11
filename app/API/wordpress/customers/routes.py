from fastapi import APIRouter, HTTPException
from app.Core.woocommerce_client import wcapi
from .schema_json import CustomerOut

router = APIRouter()


@router.get("/", response_model=list[CustomerOut])
def obtener_clientes(per_page: int = 100):
    """
    Obtiene la lista de clientes de WordPress/WooCommerce
    
    - **per_page**: Número de clientes a obtener (máximo 100)
    """
    try:
        response = wcapi.get("customers", params={"per_page": per_page})

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=response.text
            )

        customers = response.json()

        clean_customers = []

        for customer in customers:
            clean_customers.append({
                "id": customer["id"],
                "username": customer["username"],
                "email": customer["email"],
                "first_name": customer.get("first_name", ""),
                "last_name": customer.get("last_name", "")
            })

        return clean_customers

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{customer_id}", response_model=CustomerOut)
def obtener_cliente_por_id(customer_id: int):
    """
    Obtiene un cliente específico de WordPress/WooCommerce por su ID

    - **customer_id**: ID del cliente a consultar
    """
    try:
        response = wcapi.get(f"customers/{customer_id}")

        if response.status_code == 404:
            raise HTTPException(
                status_code=404,
                detail=f"No se encontró el cliente con id {customer_id}"
            )

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=response.text
            )

        customer = response.json()

        clean_customer = {
            "id": customer["id"],
            "username": customer["username"],
            "email": customer["email"],
            "first_name": customer.get("first_name", ""),
            "last_name": customer.get("last_name", "")
        }

        return clean_customer

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))