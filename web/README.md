# SGIP Web — registro ciudadano (RF-001 / UIW-01)

Formulario ciudadano en español, conectado exclusivamente a la API central.
Usar datos ficticios; el registro no inicia una sesión (RF-002 es otro flujo).

## Desarrollo

1. `npm ci`
2. Copiar `.env.example` a `.env.local` y ajustar `VITE_API_URL`.
3. `npm run dev`

La API debe permitir el origen web explícitamente en su configuración CORS.
`VITE_API_URL` es la URL base sin `/api/v1/ciudadanos`. No contiene secretos.
En desarrollo, el valor por defecto es `http://localhost:8000`; HTTP solo se
permite para localhost, 127.0.0.1 y ::1. En producción es obligatorio definir
una URL HTTPS al compilar y servir también la web por HTTPS.

## Contrato

`POST /api/v1/ciudadanos`, JSON `{nombre, correo, contrasena}`. Nombre de 2 a
120 caracteres tras quitar espacios externos; correo válido de hasta 254
caracteres, normalizado a minúsculas; contraseña de 12 a 128 caracteres sin
recortarla. La confirmación se valida en el cliente y no se envía. Tampoco se
envía el rol. HTTP 201 confirma registro; 409 indica correo duplicado; 422 datos
rechazados; errores de servicio, red y espera se presentan de forma controlada
sin mostrar respuestas internas. Se impide doble envío y se limita la espera a
15 segundos. Un timeout no prueba que el servidor haya cancelado la creación.
Las contraseñas se borran después de una respuesta 201 y no se guardan en storage.

## Verificación

- `npm run lint`
- `npm run build`
- Funcional: formulario vacío/inválido, confirmación distinta, éxito, correo
  duplicado, datos rechazados por API, fallo de red, timeout y doble envío.
- Accesibilidad: teclado, foco visible, resumen de errores con enlaces, etiquetas
  persistentes, anuncio de carga/error/éxito y presentación a 320 y 1280 px.

Las comprobaciones estáticas no sustituyen la verificación funcional en navegador
ni las pruebas de lector de pantalla y WCAG del flujo completo.
