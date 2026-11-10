"""Central API used by the SGIP web and mobile clients."""
import os
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
from app.controllers.citizens import router
from app.core.config import cors_origins

app = FastAPI(title="SGIP API", version="0.1.0")
app.add_middleware(CORSMiddleware, allow_origins=cors_origins(), allow_methods=["POST"], allow_headers=["Content-Type"])
if os.getenv("APP_ENV") == "production":
    app.add_middleware(HTTPSRedirectMiddleware)


@app.exception_handler(RequestValidationError)
async def validation_error(request: Request, error: RequestValidationError):
    # Default errors include submitted input, which may contain a password.
    details = [{"loc": list(item["loc"]), "type": item["type"], "msg": "Revisa el valor de este campo."} for item in error.errors()]
    return JSONResponse(status_code=422, content={"detail": details}, headers={"Cache-Control": "no-store"})


app.include_router(router)
