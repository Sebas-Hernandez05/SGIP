"""Transactional citizen registration and audit persistence."""

from datetime import timezone
from uuid import uuid4

import psycopg
from psycopg.rows import dict_row

from app.core.database import DatabaseUnavailable, connect


class DuplicateEmail(Exception):
    """The normalized email already belongs to a citizen."""


class CitizenRepository:
    def create(self, nombre: str, correo: str, password_hash: str) -> dict:
        citizen_id = uuid4()
        try:
            with connect() as connection:
                with connection.cursor(row_factory=dict_row) as cursor:
                    cursor.execute(
                        """INSERT INTO ciudadanos (id, nombre, correo, password_hash)
                           VALUES (%s, %s, %s, %s)
                           RETURNING id, nombre, correo, rol, estado, fecha_registro""",
                        (citizen_id, nombre.strip(), correo.strip().lower(), password_hash),
                    )
                    citizen = cursor.fetchone()
                    cursor.execute(
                        """INSERT INTO auditoria_ciudadanos
                           (id, ciudadano_id, actor_id, operacion)
                           VALUES (%s, %s, %s, 'registro')""",
                        (uuid4(), citizen_id, citizen_id),
                    )
            citizen["id"] = str(citizen["id"])
            citizen["fecha_registro"] = citizen["fecha_registro"].astimezone(timezone.utc).isoformat()
            return citizen
        except psycopg.errors.UniqueViolation as error:
            if error.diag.constraint_name == "ciudadanos_correo_key":
                raise DuplicateEmail("El correo ya está registrado.") from None
            raise DatabaseUnavailable("No se pudo registrar el ciudadano.") from None
        except psycopg.Error:
            raise DatabaseUnavailable("No se pudo registrar el ciudadano.") from None
