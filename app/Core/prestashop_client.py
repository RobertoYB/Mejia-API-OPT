import requests
from app.Core.config import settings

def prestashop_get(endpoint: str, fields: str|None = None, filters: dict|None = None):

  url = f"{settings.PRESTASHOP_URL}/{endpoint}"

  params = {
      "ws_key": settings.API_KEY,
      "output_format": "JSON"
  }

  if fields:
    params["display"] = f"[{fields}]"
  else:
    params["display"] = "full"

  if filters:
      for key, value in filters.items():
         params[f"filter[{key}]"] = f"[{value}]"
    
  response = requests.get(url, params=params)

  response.raise_for_status()

  return response.json()

def prestashop_post(endpoint:str, xml_body: str):
  url = f"{settings.PRESTASHOP_URL}/{endpoint}"

  headers = {
      "Content-Type": "application/xml"
  }

  params = {
      "ws_key": settings.API_KEY
  } 

  response = requests.post(url,params=params,data=xml_body.encode("utf-8"),headers=headers)

  response.raise_for_status()

  return response.text

def prestashop_put(endpoint: str, xml_body: str):
    url = f"{settings.PRESTASHOP_URL}/{endpoint}"

    headers = {
        "Content-Type": "application/xml"
    }

    params = {
        "ws_key": settings.API_KEY
    }

    response = requests.put(
        url,
        params=params,
        data=xml_body.encode("utf-8"),
        headers=headers
    )

    print("STATUS:", response.status_code)
    print("RESPONSE:", response.text)  # 👈 AGREGA ESTO

    if response.status_code != 200:
        # PrestaShop envía un XML detallando el error exacto aquí
        print(f"DEBUG PRESTASHOP ERROR: {response.text}")

    response.raise_for_status()

    return response.text
def prestashop_get_xml(endpoint: str):
    url = f"{settings.PRESTASHOP_URL}/{endpoint}"

    params = {
        "ws_key": settings.API_KEY
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    return response.text