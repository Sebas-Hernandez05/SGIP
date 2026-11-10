"""Environment configuration; no credentials are stored in source control."""
import os
from urllib.parse import urlsplit


def cors_origins() -> list[str]:
    origins = [value.strip() for value in os.getenv("CORS_ORIGINS", "").split(",") if value.strip()]
    for origin in origins:
        parsed = urlsplit(origin)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc or parsed.path or parsed.query or parsed.fragment or parsed.username or parsed.password:
            raise ValueError("CORS_ORIGINS debe contener orígenes HTTP(S) explícitos sin rutas ni credenciales.")
        if os.getenv("APP_ENV") == "production" and parsed.scheme != "https":
            raise ValueError("En producción los orígenes CORS deben usar HTTPS.")
    return origins
