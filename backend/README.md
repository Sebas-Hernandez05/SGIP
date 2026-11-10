# API central de SGIP

RF-001: registro ciudadano para UIW-01 y UIM-01. La autenticación (RF-002)
corresponde a otra entrega; el registro no abre una sesión.

## Entorno local

Desde backend/, con Python 3.11 o posterior:

```powershell
python -m venv .venv
.venv/Scripts/python -m pip install -r requirements.txt
$env:DATABASE_URL = 'postgresql://usuario:clave@localhost:5432/sgip_pruebas'
$env:CORS_ORIGINS = 'http://localhost:5173'
.venv/Scripts/python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Usar únicamente una base de pruebas con datos ficticios. Aplicar antes la
migración inicial en migrations/ siguiendo sus instrucciones. Las dependencias
directas están fijadas; el entorno local no modifica paquetes globales.

## Contrato de registro

POST /api/v1/ciudadanos, JSON con nombre, correo, contrasena.
Nombre recortado de 2 a 120 caracteres, correo válido recortado y en minúsculas
(máximo 254), contraseña de 12 a 128 caracteres conservada exactamente como
se recibe. Estas longitudes son decisiones de implementación, no reglas
explícitas en Notion. No se aceptan campos adicionales, incluidos rol y estado.

201 devuelve id UUID, nombre, correo, rol: ciudadano, estado: activo
 y fecha_registro UTC. Nunca devuelve credenciales ni hash. 409 devuelve
{ "detail": "El correo ya está registrado." }; 422 devuelve una lista detail
con loc, type, msg, sin valores enviados; 503 devuelve
{ "detail": "El servicio no está disponible. Intenta más tarde." }.
La unicidad la impone PostgreSQL para cubrir solicitudes concurrentes. La
cuenta y la auditoría se crean en una transacción. Las contraseñas se derivan
mediante scrypt (N=32768, r=8, p=1, sal aleatoria de 16 bytes, clave de 64 bytes).

## Producción y seguridad

Configurar APP_ENV=production, DATABASE_URL con TLS y CORS_ORIGINS con
orígenes HTTPS explícitos separados por comas. Sin configuración CORS no se
habilitan orígenes de navegador. La API redirige HTTP a HTTPS en producción;
el proxy inverso debe terminar TLS y aceptar tráfico externo únicamente por
HTTPS. Configurar Uvicorn --proxy-headers --forwarded-allow-ips exclusivamente
con las IP del proxy confiable (nunca * en una red abierta).

No guardar .env, URLs con credenciales ni datos reales en Git. Desactivar
captura de cuerpos y datos sensibles en logs del proxy y del despliegue. El
endpoint público no admite elegir privilegios. La respuesta de duplicado es
explícita para el formulario; agregar controles de abuso/rate limiting en el
despliegue antes de abrirlo a tráfico público. La conformidad HTTPS y las
latencias reales se verifican en el entorno desplegado.

## Verificación

Desde backend/: .venv/Scripts/python -m pytest -q cuando la suite asignada a
calidad esté integrada. /openapi.json documenta la API. Para revisar el hash
sin imprimir datos sensibles, comprobar que dos registros con la misma
contraseña producen hashes distintos y que ninguno coincide con el texto plano.
Documentación consultada para errores sin inputs: https://fastapi.tiangolo.com/tutorial/handling-errors/
