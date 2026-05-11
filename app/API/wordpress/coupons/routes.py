from fastapi import APIRouter, HTTPException
from app.Core.woocommerce_client import wcapi

router = APIRouter()

@router.get("/")
def get_coupons(per_page: int = 100):
    try: 
        response = wcapi.get("coupons", params={"per_page":per_page})
        
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=response.text
            )
        
        coupons = response.json()

        clean_coupons = []
        for coupon in coupons:
            clean_coupons.append({
                "id": coupon["id"],
                "code": coupon["code"],
                "amount": coupon["amount"],
                "discount_type": coupon["discount_type"],
                "description": coupon["description"],
                "date_created": coupon["date_created"],
                "date_expires": coupon["date_expires"],
                "usage_count": coupon["usage_count"],
                "individual_use": coupon["individual_use"],
                "free_shipping": coupon["free_shipping"]
            })

        return clean_coupons

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{coupon_id}")
def get_coupon_by_id(coupon_id: int):

    try:
        response = wcapi.get(f"coupons/{coupon_id}")

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=response.text
            )

        coupon = response.json()

        clean_coupon = {
            "id": coupon["id"],
            "code": coupon["code"],
            "amount": coupon["amount"],
            "discount_type": coupon["discount_type"],
            "description": coupon["description"],
            "date_created": coupon["date_created"],
            "date_expires": coupon["date_expires"],
            "usage_count": coupon["usage_count"],
            "individual_use": coupon["individual_use"],
            "free_shipping": coupon["free_shipping"]
        }

        return clean_coupon

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    