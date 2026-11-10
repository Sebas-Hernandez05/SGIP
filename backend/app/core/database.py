"""PostgreSQL connections owned exclusively by the central API."""

import os

import psycopg


class DatabaseUnavailable(Exception):
    """Persistence cannot complete the requested operation."""


def connect():
    """Open a bounded connection without exposing configuration in errors."""
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        raise DatabaseUnavailable("La base de datos no está disponible.")
    try:
        return psycopg.connect(database_url, connect_timeout=5)
    except psycopg.Error:
        raise DatabaseUnavailable("La base de datos no está disponible.") from None
