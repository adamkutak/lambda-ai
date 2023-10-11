from fastapi.responses import JSONResponse
from typing import Dict, Any
from fastapi import FastAPI, Request


app = FastAPI()


@app.exception_handler(Exception)
async def server_error_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"message": str(exc)},
    )


@app.get("/xyz_123_abc_789/multiply_quantity")
def multiply_quantity(item_id: int, status: bool, bought: int) -> Dict[str, Any]:
    quantity = 100
    if status:
        quantity -= bought
    return {"item_id": item_id, "quantity": quantity}
