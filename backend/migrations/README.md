# Migración RF-001

`001_ciudadanos.up.sql` es la primera versión del esquema. Se aplica una sola vez
en una base PostgreSQL vacía; no existe una versión de esquema previa soportada
en `develop`. No modifica tablas preexistentes con otros nombres. No usa
`IF NOT EXISTS`: una instalación incompatible falla y revierte la transacción.

Configura `DATABASE_URL` en el entorno del backend y aplica con un cliente
PostgreSQL autorizado (sin escribir contraseñas en el historial):

```powershell
$env:PGDATABASE = $env:DATABASE_URL
psql -X -v ON_ERROR_STOP=1 -f backend/migrations/001_ciudadanos.up.sql
```

El backend utiliza psycopg 3. La restricción única del correo normalizado resuelve
también registros concurrentes; la creación del ciudadano y de su auditoría
ocurren dentro de la misma transacción. Los clientes no acceden a esta base.
La auditoría solo conserva identificadores, operación y fecha, nunca contraseñas.
Los identificadores se generan con UUID en el backend. Los tiempos son
`TIMESTAMPTZ`; su representación UTC se normaliza al consultar desde la API.

Antes de actualizar una base con datos, genera una copia de seguridad con
`pg_dump` según la operación del entorno y valida su restauración en una base de
prueba. La reversión `001_ciudadanos.down.sql` elimina ambas tablas y sus datos:
úsala únicamente en una base de prueba desechable o con un respaldo validado.
Para recuperar datos en un entorno real, restaura el respaldo; no ejecutes la
reversión como sustituto de una restauración.

La aceptación requiere probar instalación vacía, unicidad ante concurrencia,
restricciones, rollback si falla auditoría, reversión y reaplicación en PostgreSQL
real. La revisión de SQL o un repositorio simulado no sustituyen esas pruebas.
