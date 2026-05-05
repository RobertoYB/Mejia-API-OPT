def ps_success(data):
    return {
        "status": "success",
        "data": data,
        "errors": []
    }

def ps_error(code: str, message: str):
    return {
        "status": "error",
        "data": None,
        "errors": [
            {
                "code": code,
                "message": message
            }
        ]
    }