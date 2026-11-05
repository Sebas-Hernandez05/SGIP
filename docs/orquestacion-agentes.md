# Orquestación de entregas de SGIP

## Fuentes

- [Proyecto SGIP](https://app.notion.com/p/3de14e04c5cb8030af75c0a1fcb134e1)
- [Requerimientos específicos](https://app.notion.com/p/3de14e04c5cb803babfaefe03b6fbf3e)
- [Modelos, diagramas y pantallas](https://app.notion.com/p/3de14e04c5cb809e9250e58428b4e44a)
- [SGIP Seguimiento Trello](https://app.notion.com/p/3e214e04c5cb80739454d9dde0927191)

Consulta la versión vigente para cada entrega. Cita el requisito por su ID y descripción breve. La especificación actual usa RF-037 para crear una orden y RR-01 para los límites de la IA. Los modelos describen una cobertura de 58 RF, mientras que la especificación incluye RF-059 y la tabla de interfaces lo referencia. Registra esta diferencia si afecta una entrega de alertas por vencimiento. Para RF-051, confirma quién puede reabrir un reporte y bajo qué condiciones. Para RF-048, confirma el disparador de la solicitud de seguimiento si se necesita implementarlo.

## Delegación y verificación

| Agente | Rutas de trabajo | Aceptación según el alcance |
|---|---|---|
| `frontend_web` | `web/` | Consume el contrato de la API central. Verifica las pantallas UIW afectadas, los estados de carga, error y vacío aplicables y la interacción por teclado. Ejecuta `npm ci`, `npm run lint` y `npm run build` desde `web/`. |
| `frontend_movil` | `mobile/` | Sigue `mobile/AGENTS.md` y Expo Router. Verifica las pantallas UIM, los permisos de cámara o ubicación cuando apliquen y el manejo de fallos de red. Ejecuta `npm ci`, `npm run lint` y `npx tsc --noEmit` desde `mobile/`. Registra los dispositivos o emuladores usados. |
| `backend_api` | `backend/app/` y dependencias del backend asignadas | FastAPI con controlador y repositorio separados. Verifica contrato, validación, permisos por rol y por recurso, errores y trazabilidad. Alinea las dependencias con el agente de datos. |
| `base_datos` | Migraciones y configuración de PostgreSQL/Supabase que determine la entrega | Verifica migraciones en base vacía y desde una versión soportada si existe. Comprueba restricciones, integridad, recuperación y configuración sin secretos. Coordina cualquier edición de `backend/app/core/` con backend. |
| `calidad` | Archivos de pruebas expresamente asignados y revisión de la versión integrada | Cubre conexión, BD, API, módulos, flujos funcionales y de extremo a extremo, rendimiento y seguridad. Documenta por separado aprobado, fallido, pendiente y no aplicable. |

La rama de partida contiene el esqueleto de la aplicación. Los archivos de arranque del backend y de configuración de base de datos están vacíos en la revisión inicial. No hay una suite de pruebas ni una ruta de migraciones versionadas. Define su ubicación y comandos en la primera tarea que los requiera. Los comandos de compilación y análisis estático de los clientes no sustituyen las pruebas funcionales.

Para RNF-09 registra las operaciones medidas, entorno, datos, concurrencia y latencia observada. La especificación fija máximos de **2 segundos** para consultas y registros sencillos y **10 segundos** para operaciones complejas. Confirma con el responsable las condiciones de carga cuando el requisito no las detalle. Para seguridad incluye casos negativos de autenticación, rol y propiedad del recurso, y verificación de HTTPS y manejo de secretos según el alcance. Para IA comprueba que la recomendación queda pendiente hasta la decisión del funcionario y que un fallo del proveedor no aplica cambios al caso.

## Registro por entrega

En `.trace/<ID-entrega>.md`, registra la rama y el SHA base, las URL de Notion y sus versiones observadas, la lista de tareas y sus dependencias, el agente responsable y la evidencia por criterio. Incluye el comando, entorno, resultado y ubicación de la evidencia sin incluir credenciales ni datos sensibles. Registra decisiones y bloqueos.

Usa las tarjetas existentes del tablero cuando correspondan y evita duplicarlas. Verifica el estado actual antes de cambiarlo. El tablero contempla `Dev`, `Code Review` y `Testing`. Actualiza solo estados que reflejen trabajo observado y añade la referencia al commit una vez publicado. Conserva la referencia en Git si la escritura en Notion no está disponible.

## Inicio y aceptación

Con Codex CLI, desde el repositorio de confianza, ejecuta `codex mcp login notion` y abre `codex`. Pide al agente raíz que coordine un requisito concreto y que presente la entrega para tu revisión. Usa una rama y un directorio de trabajo exclusivos.

La aprobación se da sobre la huella que imprime `python3 scripts/entrega.py preparar`. El script comprueba la rama, el SHA base y el contenido del índice. El coordinador obtiene del revisor la huella y la referencia de aprobación, ejecuta el commit y verifica la publicación del SHA en GitHub. Las instrucciones reservan el commit y el push al coordinador. Los permisos efectivos se administran en el entorno y GitHub.
