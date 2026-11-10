# RF-001 · Rechazo de NUL en nombre

Revisión del 10 de noviembre de 2026 sobre el commit 6546098f8988b38eb3cb408c83f491a594e17d62 del PR #2. El responsable autorizó corregir el hallazgo P2 del registro ciudadano.

El esquema admitía NUL en nombre. El adaptador PostgreSQL rechazaba ese texto y la ruta respondía 503. El campo nombre ahora rechaza NUL durante la validación de entrada y responde 422 mediante el manejador existente, antes de invocar el repositorio. Se conserva la normalización y el manejo de errores existente.

Se amplía la prueba parametrizada de entradas inválidas con NUL al principio, en medio y al final. Cada caso verifica HTTP 422, ausencia de credenciales en la respuesta y que el repositorio no recibe una operación de creación.

- Antes de corregir el esquema, los tres casos nuevos fallaron porque la validación admitía la entrada y el repositorio simulado devolvía 201.
- Después de corregirlo, `PYTHONPATH=backend /tmp/sgip-pr2-review-venv/bin/python -m pytest backend/tests -q -p no:cacheprovider` terminó con 18 aprobadas y 4 omitidas por falta de TEST_DATABASE_URL. Aviso de deprecación Starlette/AnyIO, sin fallo.
- Las cuatro pruebas PostgreSQL no se volvieron a ejecutar en este entorno. La regresión verifica que las entradas rechazadas nunca llegan al repositorio; los registros válidos, normalización y errores controlados siguen cubiertos por las pruebas ejecutadas.
- `git diff --check` aprobado. Cambios funcionales limitados al esquema de entrada backend.

La aceptación de la huella de esta corrección queda pendiente del responsable antes del commit y la publicación.
