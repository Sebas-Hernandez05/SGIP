BEGIN;

CREATE TABLE ciudadanos (
    id UUID PRIMARY KEY,
    nombre TEXT NOT NULL CHECK (nombre = btrim(nombre) AND char_length(nombre) BETWEEN 2 AND 120),
    correo TEXT NOT NULL CONSTRAINT ciudadanos_correo_key UNIQUE,
    password_hash TEXT NOT NULL CHECK (char_length(password_hash) > 0),
    rol TEXT NOT NULL DEFAULT 'ciudadano' CHECK (rol = 'ciudadano'),
    estado TEXT NOT NULL DEFAULT 'activo' CHECK (estado IN ('activo', 'inactivo')),
    fecha_registro TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CHECK (correo = lower(btrim(correo)) AND char_length(correo) BETWEEN 3 AND 254)
);

CREATE TABLE auditoria_ciudadanos (
    id UUID PRIMARY KEY,
    ciudadano_id UUID NOT NULL REFERENCES ciudadanos(id) ON DELETE RESTRICT,
    actor_id UUID NOT NULL REFERENCES ciudadanos(id) ON DELETE RESTRICT,
    operacion TEXT NOT NULL CHECK (operacion = 'registro'),
    fecha TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (ciudadano_id, operacion)
);

COMMIT;
