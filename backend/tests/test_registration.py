"""RF-001 acceptance tests. TEST_DATABASE_URL must point to an empty disposable DB."""
import os
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from uuid import UUID

import psycopg
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.controllers.citizens import get_citizen_repository
from app.core.security import hash_password
from app.repositories.citizens import CitizenRepository, DatabaseUnavailable, DuplicateEmail

PASSWORD = "ficticia-segura-001"
PAYLOAD = {"nombre": "Ciudadana Ficticia", "correo": "persona@example.com", "contrasena": PASSWORD}
client = TestClient(app)


class FakeRepository:
    def __init__(self, error=None):
        self.error = error
        self.received = None

    def create(self, nombre, correo, password_hash):
        self.received = (nombre, correo, password_hash)
        if self.error:
            raise self.error
        return {"id": "12345678-1234-5678-1234-567812345678", "nombre": nombre, "correo": correo,
                "rol": "ciudadano", "estado": "activo", "fecha_registro": "2026-11-05T12:00:00+00:00"}


@pytest.fixture(autouse=True)
def clear_overrides():
    yield
    app.dependency_overrides.clear()


def use_repository(repository):
    app.dependency_overrides[get_citizen_repository] = lambda: repository


def test_public_registration_normalizes_and_hashes():
    repository = FakeRepository()
    use_repository(repository)
    response = client.post("/api/v1/ciudadanos", json={**PAYLOAD, "nombre": "  Ciudadana Ficticia  ", "correo": "  PERSONA@EXAMPLE.COM  "})
    assert response.status_code == 201
    body = response.json()
    UUID(body["id"])
    assert set(body) == {"id", "nombre", "correo", "rol", "estado", "fecha_registro"}
    assert body["nombre"] == "Ciudadana Ficticia"
    assert body["correo"] == "persona@example.com"
    assert body["rol"] == "ciudadano" and body["estado"] == "activo"
    assert PASSWORD not in response.text and "password_hash" not in response.text
    assert repository.received[2].startswith("scrypt$32768$8$1$")
    assert PASSWORD not in repository.received[2]
    assert response.headers["cache-control"] == "no-store"


@pytest.mark.parametrize("changes", [
    {"nombre": " "}, {"nombre": "a" * 121}, {"correo": "invalido"},
    {"contrasena": "corta"}, {"contrasena": "x" * 129}, {"nombre": 123},
    {"rol": "administrador"}, {"estado": "activo"}, {"id": "injected"},
    {"nombre": "\x00Ana Maria"}, {"nombre": "Ana\x00Maria"}, {"nombre": "Ana Maria\x00"},
])
def test_invalid_input_rejected_without_secrets(changes):
    repository = FakeRepository()
    use_repository(repository)
    response = client.post("/api/v1/ciudadanos", json={**PAYLOAD, **changes})
    assert response.status_code == 422
    assert PASSWORD not in response.text
    assert "input" not in response.text and "password_hash" not in response.text
    assert repository.received is None


def test_missing_and_malformed_payload_do_not_leak_input():
    for payload in [{}, {"correo": "persona@example.com", "contrasena": PASSWORD}]:
        response = client.post("/api/v1/ciudadanos", json=payload)
        assert response.status_code == 422 and PASSWORD not in response.text
    response = client.post("/api/v1/ciudadanos", content='{"contrasena":"ficticia-segura-001",', headers={"Content-Type": "application/json"})
    assert response.status_code == 422 and PASSWORD not in response.text


@pytest.mark.parametrize("error,status,message", [
    (DuplicateEmail(), 409, "El correo ya está registrado."),
    (DatabaseUnavailable(), 503, "El servicio no está disponible. Intenta más tarde."),
])
def test_controlled_persistence_errors(error, status, message):
    use_repository(FakeRepository(error))
    response = client.post("/api/v1/ciudadanos", json=PAYLOAD)
    assert response.status_code == status
    assert response.json() == {"detail": message}
    assert PASSWORD not in response.text


def test_hash_uses_random_salt_and_preserves_whitespace():
    first, second = hash_password(PASSWORD), hash_password(PASSWORD)
    assert first != second
    assert first.split("$")[:4] == ["scrypt", "32768", "8", "1"]
    import base64, hashlib
    parts = first.split("$")
    derived = hashlib.scrypt(PASSWORD.encode(), salt=base64.b64decode(parts[4]), n=32768, r=8, p=1, dklen=64, maxmem=64*1024*1024)
    assert derived == base64.b64decode(parts[5])
    assert hashlib.scrypt((" " + PASSWORD).encode(), salt=base64.b64decode(parts[4]), n=32768, r=8, p=1, dklen=64, maxmem=64*1024*1024) != derived


@pytest.fixture
def database(monkeypatch):
    url = os.getenv("TEST_DATABASE_URL")
    if not url:
        pytest.skip("TEST_DATABASE_URL missing: PostgreSQL acceptance remains pending")
    monkeypatch.setenv("DATABASE_URL", url)
    migration = Path(__file__).parents[1] / "migrations"
    with psycopg.connect(url, autocommit=True) as conn:
        conn.execute((migration / "001_ciudadanos.up.sql").read_text(encoding="utf-8"))
    yield url
    with psycopg.connect(url, autocommit=True) as conn:
        conn.execute((migration / "001_ciudadanos.down.sql").read_text(encoding="utf-8"))


def test_postgres_registration_persists_audit_and_duplicate(database):
    started = time.perf_counter()
    response = client.post("/api/v1/ciudadanos", json=PAYLOAD)
    elapsed = time.perf_counter() - started
    assert response.status_code == 201
    with psycopg.connect(database) as conn:
        citizen = conn.execute("SELECT nombre,correo,password_hash,rol,estado FROM ciudadanos").fetchone()
        audit = conn.execute("SELECT ciudadano_id,actor_id,operacion FROM auditoria_ciudadanos").fetchone()
        assert citizen[:2] == (PAYLOAD["nombre"], PAYLOAD["correo"])
        assert citizen[2].startswith("scrypt$") and PASSWORD not in citizen[2]
        assert citizen[3:] == ("ciudadano", "activo")
        assert str(audit[0]) == response.json()["id"] and audit[0] == audit[1] and audit[2] == "registro"
    duplicate = client.post("/api/v1/ciudadanos", json={**PAYLOAD, "correo": "PERSONA@EXAMPLE.COM"})
    assert duplicate.status_code == 409
    print(f"RF001 local registration concurrency=1 elapsed_seconds={elapsed:.4f}")
    assert elapsed <= 2


def test_postgres_audit_failure_rolls_back_citizen(database):
    with psycopg.connect(database) as conn:
        conn.execute("CREATE FUNCTION qa_fail_audit() RETURNS trigger LANGUAGE plpgsql AS $$ BEGIN RAISE EXCEPTION 'qa audit failure'; END; $$")
        conn.execute("CREATE TRIGGER qa_fail_audit BEFORE INSERT ON auditoria_ciudadanos FOR EACH ROW EXECUTE FUNCTION qa_fail_audit()")
    try:
        response = client.post("/api/v1/ciudadanos", json=PAYLOAD)
        assert response.status_code == 503 and "qa audit" not in response.text
        with psycopg.connect(database) as conn:
            assert conn.execute("SELECT count(*) FROM ciudadanos").fetchone()[0] == 0
    finally:
        with psycopg.connect(database) as conn:
            conn.execute("DROP TRIGGER qa_fail_audit ON auditoria_ciudadanos")
            conn.execute("DROP FUNCTION qa_fail_audit()")


def test_postgres_concurrent_duplicate_is_atomic(database):
    def register(_):
        try:
            CitizenRepository().create(PAYLOAD["nombre"], "race@example.com", "fictitious-hash")
            return "created"
        except DuplicateEmail:
            return "duplicate"
    with ThreadPoolExecutor(max_workers=2) as executor:
        results = list(executor.map(register, range(2)))
    assert sorted(results) == ["created", "duplicate"]
    with psycopg.connect(database) as conn:
        assert conn.execute("SELECT count(*) FROM ciudadanos").fetchone()[0] == 1
        assert conn.execute("SELECT count(*) FROM auditoria_ciudadanos").fetchone()[0] == 1


def test_postgres_database_constraints(database):
    cases = [
        ("Nombre", "valid@example.com", "administrador"),
        ("Nombre", "UPPER@EXAMPLE.COM", "ciudadano"),
        (" ", "valid@example.com", "ciudadano"),
    ]
    for nombre, correo, rol in cases:
        with psycopg.connect(database) as conn:
            with pytest.raises(psycopg.errors.CheckViolation):
                conn.execute(
                    "INSERT INTO ciudadanos (id,nombre,correo,password_hash,rol) "
                    "VALUES (gen_random_uuid(),%s,%s,'fictitious-hash',%s)",
                    (nombre, correo, rol),
                )


def test_production_https_and_cors(monkeypatch):
    import subprocess, sys
    env = {**os.environ, "APP_ENV": "production", "CORS_ORIGINS": "https://web.example.com"}
    code = """
from fastapi.testclient import TestClient
from app.main import app
client = TestClient(app, follow_redirects=False)
redirect = client.post('http://testserver/api/v1/ciudadanos', json={})
assert redirect.status_code == 307
assert redirect.headers['location'].startswith('https://')
for origin, allowed in [('https://web.example.com', True), ('https://attacker.example.com', False)]:
    response = client.options('https://testserver/api/v1/ciudadanos', headers={'Origin': origin, 'Access-Control-Request-Method': 'POST', 'Access-Control-Request-Headers': 'Content-Type'})
    assert ('access-control-allow-origin' in response.headers) == allowed
"""
    result = subprocess.run([sys.executable, "-c", code], env=env, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    from app.core.config import cors_origins
    monkeypatch.setenv("APP_ENV", "production")
    monkeypatch.setenv("CORS_ORIGINS", "http://web.example.com")
    with pytest.raises(ValueError):
        cors_origins()
