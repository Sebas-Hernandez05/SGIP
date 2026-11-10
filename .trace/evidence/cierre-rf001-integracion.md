# RF-001 — integración final para inspección

Fecha: 2026-11-07, sesión posterior a las pruebas manuales del responsable. Rama entrega/rf-001, HEAD/base 4de9c6ef29bd0bc6a5fe1d13875d278c2e4a40f8. Sin commit ni push.

> Conciliación vigente: [matriz local/operacional](paso3-matriz-actual.md) y [revisión independiente](conciliacion-calidad.md). El addendum actual del responsable completa duplicado/validaciones web. TLS/carga productiva y audit=0 no son condiciones locales acordadas. Los checks y limpieza de este informe se conservan; su estado de cobertura se concilia abajo.

## Cambios locales y limpieza

Se revisaron los cambios preparados y sin preparar, incluidos qa-rf001.md, el repositorio backend y todos los archivos nuevos. Se conservaron íntegros los resultados manuales aportados; solo se aclararon encabezados para separar historia de cobertura final. La captura no utilizada de excepción del repositorio se retiró y se normalizó su fin de archivo: el archivo final coincide con el índice anterior; mensaje público, rollback y raise from None conservados.

Se retiraron scripts/qa_rf001_respuestas.py, scripts/verificar_rf001_local.py y .trace/evidence/paso3-servidor-estados.txt, diagnósticos temporales no publicados. Se conservan los informes y logs de pruebas reales y los JSON de auditoría como evidencia de aceptación. Las menciones a utilidades retiradas en informes previos se identifican como históricas en la matriz vigente.

Actualización posterior solicitada por el responsable: **qa_rf001_respuestas.py se reincorpora** como herramienta QA versionada para corregir la referencia U2. Se conservan sus pruebas y el [procedimiento vigente](../../docs/qa-rf001-u2.md); [evidencia nueva](qa-respuestas-evidencia.md). La retirada anterior se registra como historia, no como estado actual de esa utilidad. verificar_rf001_local.py sigue retirado.

## Checks finales

| Criterio / comando | Resultado |
| --- | --- |
| web: npm run lint; npx --no-install tsc -b; npm run build (códigos individuales) | Todos0; ejecutados por calidad sobre interfaz final. Ver cierre-rf001-calidad.md. |
| mobile: npm run lint; npx --no-install tsc --noEmit; node --test tests/registration.test.mjs | Todos0; servicio4/4. Ver cierre-rf001-calidad.md. |
| Backend: PYTHONPATH=backend; TEST_DATABASE_URL de clúster exclusivo; backend/.venv/Scripts/python.exe -m pytest backend/tests -q -s -p no:cacheprovider | Exit0,19 aprobadas,0 omitidas,1 aviso Starlette/AnyIO,6.43 s; registro0.2189 s, concurrencia1. Salida cierre-backend-pytest.txt. |
| git diff --check | Exit0, sin errores de whitespace. |
| Exclusiones: git check-ignore -- web/.env.local mobile/.env.local backend/.env web/node_modules mobile/node_modules backend/.venv | Todas las rutas ignoradas. No se incluyen archivos locales ni directorios instalados. |
| Revisión de candidatos versionados/nuevos, incluidos originales de la base | 116 archivos en el barrido previo al informe final: cero rutas prohibidas. Patrones de tokens, claves privadas y URLs con credenciales: solo placeholder usuario/clave en README backend y URL ficticia de prueba negativa móvil. Lectura manual confirma que no son secretos reales. |

El primer intento de arrancar el clúster temporal anterior falló por falta del directorio interno pg_notify. No se reparó ni se usaron bases existentes. Se creó un clúster PostgreSQL16.6 nuevo exclusivo en TEMP/rf001-cierre-pg-20261107, usuario ficticio rf001_qa, escuchando solo en127.0.0.1:55439. initdb y arranque exit0; suite19/19; pg_ctl stop exit0 al terminar. Directorios temporales fuera del worktree, sin servicio activo; no forman parte de entrega. TEST_DATABASE_URL solo identifica esta BD desechable. Los tests crean/destruyen tablas y nunca se ejecutaron contra sgip_test del usuario.

## Evidencia manual y aceptación

Web rediseñada: se reconocen los casos de22:30 (201, carga, doble envío/un POST, cuenta/auditoría y red/reintento), completados por el addendum actual del responsable que confirma duplicado y validaciones del rediseño web y móvil. Móvil: se reconocen201/409, validaciones básicas, doble envío/cuenta y red/reintento de22:56 en OppoA58/ColorOS/Expo Go SDK57 y la misma declaración. Así, las seis categorías registro/duplicado/validaciones/doble envío/conexión/recuperación están aprobadas manualmente en ambos. Calidad no las ejecutó; son observaciones aportadas por el responsable. No se exige repetirlas por faltar su reiteración en una tabla anterior. Siguen sin resultados específicos confirmación distinta, presentación422/503/timeout, comparación visual, teclado/foco y lector: ver L01–L08 de la matriz con fuente individual.

La matriz conciliada enumera lo aprobado localmente y L01–L08 no observados. TLS/proxy/logs desplegados y carga operacional permanecen pendientes solo para ese alcance, sin invalidar el desarrollo HTTP local permitido. Documento/endpoint/campos resueltos por decisión explícita del usuario: nombre completo, correo y contraseña, sin documento ni teléfono; POST /api/v1/ciudadanos; ampliaciones en otra tarea. Ver contrato ratificado y matriz. Auditoría nueva: web2 altas totales y0 en omit=dev; móvil25 totales y18 en omit=dev. Árbol omit=dev no equivale a bundle nativo ni demuestra explotabilidad. Ver dependencias-revision.md; sin umbral audit=0 acordado ni cambios de dependencias.

AGENTS.md paso3 se aplica a las verificaciones obligatorias del alcance local acordado, no crea condiciones productivas ni certificaciones nuevas. En esta conciliación no se prepara una nueva huella provisional: el contrato ya está ratificado; primero deben cubrirse los casos locales pendientes. El futuro commit/push de rama de revisión no equivale a despliegue productivo. No se ejecutó commit/publicación.
