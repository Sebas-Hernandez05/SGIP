# RF-001: registro ciudadano

Fuente: [Requerimientos específicos](https://app.notion.com/p/3de14e04c5cb803babfaefe03b6fbf3e), RF-001, «El sistema permitirá el registro del Ciudadano». Edición observada: 2026-10-15T18:44:00.020Z. [Modelos](https://app.notion.com/p/3de14e04c5cb809e9250e58428b4e44a), CU-01, UIW-01 y UIM-01; edición 2026-10-17T00:26:37.030Z.

## Contrato compartido

### Alcance ratificado por el responsable

Decisión explícita del usuario en esta conversación, posterior a la conciliación de aceptación: RF-001 mantiene **nombre completo, correo y contraseña**, sin documento ni teléfono. El nombre completo se representa en `nombre`; correo y contraseña en `correo` y `contrasena`. Se conserva **`POST /api/v1/ciudadanos`** como endpoint canónico, sin migración ni alias `/api/auth/register` en esta entrega.

Esta decisión cierra para RF-001 las discrepancias previas de documento único, endpoint alternativo y campos adicionales del mockup. Cualquier ampliación se tramitará en otra tarea. No modifica los límites, normalización, confirmación local ni respuestas definidos a continuación; tampoco constituye aprobación de la huella, commit, publicación o verificaciones pendientes.

`POST /api/v1/ciudadanos`, público, JSON `{nombre,correo,contrasena}`. Nombre recortado de 2 a 120 caracteres; correo válido, recortado y normalizado a minúsculas, máximo 254; contraseña de 12 a 128 caracteres sin recortar. No se aceptan propiedades adicionales. Estos límites son decisiones de implementación, no texto literal del requisito.

201: `{id,nombre,correo,rol:"ciudadano",estado:"activo",fecha_registro}`. Identificador UUID y fecha UTC ISO 8601. Nunca se devuelve contraseña ni hash. No se inicia sesión (RF-002 fuera de alcance).

409: `{detail:"El correo ya está registrado."}`. 422: errores de validación sin valores recibidos ni credenciales. 503: `{detail:"El servicio no está disponible. Intenta más tarde."}`.

Clientes web y móvil usan exclusivamente esta API. La confirmación de contraseña solo existe en los formularios. Credenciales transformadas con scrypt y sal aleatoria; persistencia PostgreSQL mediante backend, unicidad del correo y auditoría de creación dentro de una transacción.

HTTPS para producción; HTTP local limitado al desarrollo. Las variables públicas de clientes solo contienen URL de API, nunca credenciales de base de datos. Datos de prueba ficticios.

## Verificación requerida

Registro válido persistido y auditable; validación negativa; rechazo de rol inyectado; duplicado incluso concurrente; rollback; errores de servicio controlados; ausencia de secretos en respuestas. Migración sobre base vacía y recuperación. Ambos clientes: éxito, error, carga, red, prevención de doble envío y accesibilidad de formularios. Lint/build web y lint/typecheck móvil no sustituyen pruebas funcionales.

RNF-09: máximo 2 s para registro sencillo, documentando entorno y concurrencia. No se presume una carga de producción no especificada. La aceptación queda bloqueada si faltan verificaciones obligatorias; cualquier huella preparada identifica contenido, no acredita por sí sola aceptación.
