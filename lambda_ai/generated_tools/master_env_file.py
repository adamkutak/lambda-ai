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

