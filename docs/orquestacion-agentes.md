# Orquestación de entregas de SGIP

## Fuentes

- [Proyecto SGIP](https://app.notion.com/p/3de14e04c5cb8030af75c0a1fcb134e1)
- [Requerimientos específicos](https://app.notion.com/p/3de14e04c5cb803babfaefe03b6fbf3e)
- [Modelos, diagramas y pantallas](https://app.notion.com/p/3de14e04c5cb809e9250e58428b4e44a)
- [SGIP Seguimiento Trello](https://app.notion.com/p/3e214e04c5cb80739454d9dde0927191)

Consulta la versión vigente para cada entrega. Cita el requisito por su ID y descripción breve. La especificación actual usa RF-037 para crear una orden y RR-01 para los límites de la IA. La referencia de5.1 a58 RF es histórica/inconsistente con los requisitos; la sección5.3 vigente del09/11/2026 ya abarca RF-001–059. La conciliación externa de5.1/casos detallados sigue pendiente. Registra esta diferencia si afecta una entrega de alertas por vencimiento. La fuente de requisitos consultada el09/11/2026 identifica RF-051 como validación ciudadana, RF-052 como reapertura y RF-049 como solicitud de seguimiento. Confirma actor/condiciones de RF-052 y disparador/respuesta de RF-049 antes de implementarlos; registra el desplazamiento de referencias en5.1/casos detallados sin renumerar evidencia histórica.

## Delegación y verificación

| Agente | Rutas de trabajo | Aceptación según el alcance |
|---|---|---|
| `frontend_web` | `web/` | Consume el contrato de la API central. Verifica las pantallas UIW afectadas, los estados de carga, error y vacío aplicables y la interacción por teclado. Ejecuta `npm ci`, `npm run lint` y `npm run build` desde `web/`. |
| `frontend_movil` | `mobile/` | Sigue `mobile/AGENTS.md` y Expo Router. Verifica las pantallas UIM, los permisos de cámara o ubicación cuando apliquen y el manejo de fallos de red. Ejecuta `npm ci`, `npm run lint` y `npx tsc --noEmit` desde `mobile/`. Registra los dispositivos o emuladores usados. |
| `backend_api` | `backend/app/` y dependencias del backend asignadas | FastAPI con controlador y repositorio separados. Verifica contrato, validación, permisos por rol y por recurso, errores y trazabilidad. Alinea las dependencias con el agente de datos. |
| `base_datos` | Migraciones y configuración de PostgreSQL/Supabase que determine la entrega | Verifica migraciones en base vacía y desde una versión soportada si existe. Comprueba restricciones, integridad, recuperación y configuración sin secretos. Coordina cualquier edición de `backend/app/core/` con backend. |
| `calidad` | Archivos de pruebas expresamente asignados y revisión de la versión integrada | Cubre conexión, BD, API, módulos, flujos funcionales y de extremo a extremo, rendimiento y seguridad. Documenta por separado aprobado, fallido, pendiente y no aplicable. |

Estado de referencia del worktree RF-001 al09/11/2026: backend/app tiene registro ciudadano, backend/migrations contiene001_ciudadanos y backend/tests contiene pruebas de registro; existen clientes y evidencias locales. La descripción anterior de esqueleto vacío era histórica. Revalida siempre rama, cambios locales, esquema y pruebas antes de delegar; no des por implementado el modelo global por esta descripción. Los comandos de compilación y análisis estático de los clientes no sustituyen las pruebas funcionales.

Para RNF-09 registra las operaciones medidas, entorno, datos, concurrencia y latencia observada. La especificación fija máximos de **2 segundos** para consultas y registros sencillos y **10 segundos** para operaciones complejas. Confirma con el responsable las condiciones de carga cuando el requisito no las detalle. Para seguridad incluye casos negativos de autenticación, rol y propiedad del recurso, y verificación de HTTPS y manejo de secretos según el alcance. Para IA comprueba que la recomendación queda pendiente hasta la decisión del funcionario y que un fallo del proveedor no aplica cambios al caso.

## Registro por entrega

En `.trace/<ID-entrega>.md`, registra la rama y el SHA base, las URL de Notion y sus versiones observadas, la lista de tareas y sus dependencias, el agente responsable y la evidencia por criterio. Incluye el comando, entorno, resultado y ubicación de la evidencia sin incluir credenciales ni datos sensibles. Registra decisiones y bloqueos.

Usa las tarjetas existentes del tablero cuando correspondan y evita duplicarlas. Verifica el estado actual antes de cambiarlo. El tablero contempla `Dev`, `Code Review` y `Testing`. Actualiza solo estados que reflejen trabajo observado y añade la referencia al commit una vez publicado. Conserva la referencia en Git si la escritura en Notion no está disponible.

## Inicio y aceptación

Con Codex CLI, desde el repositorio de confianza, ejecuta `codex mcp login notion` y abre `codex`. Pide al agente raíz que coordine un requisito concreto y que presente la entrega para tu revisión. Usa una rama y un directorio de trabajo exclusivos.

La aprobación se da sobre la huella que imprime `python3 scripts/entrega.py preparar`. El script comprueba la rama, el SHA base y el contenido del índice. El coordinador obtiene del revisor la huella y la referencia de aprobación, ejecuta el commit y verifica la publicación del SHA en GitHub. Las instrucciones reservan el commit y el push al coordinador. Los permisos efectivos se administran en el entorno y GitHub.

Para integrar una rama con `git merge --no-commit --no-ff`, resuelve los conflictos y prepara todos los archivos antes de generar la huella. El script incluye los padres de integración en la huella y comprueba su orden y el árbol al crear el commit. Un cambio en cualquiera de los padres requiere una nueva aceptación. Los conflictos sin resolver y las operaciones de cherry-pick, revert o rebase en curso bloquean la preparación.


## Contexto de datos vigente y reglas del coordinador

Actualización documental 09/11/2026: esta guía conserva la estructura de la guía del repositorio principal y se incorpora al worktree para quedar versionada con el contexto. Las instrucciones ancestras de aceptación/commit siguen vigentes.

1. Lee [contexto del modelo](contexto-modelo-datos.md), [comparación y etapas](alineacion-modelo-datos.md), Notion5.3 revisado09/11/2026 y el adjunto SGIP_Diagrama_ER_Corregido.html. Mantén el Interactivo anterior como histórico; no mezcles sus restricciones incompatibles. Registra URL/fecha/adjunto y conserva referencias estables, nunca URLs firmadas o credenciales.
2. Clasifica cada afirmación: requisito con fuente, corrección lógica documentada, propuesta técnica/decisión pendiente, implementación encontrada y evidencia aplicable. Una edición de Notion no acredita migración ejecutada ni habilita todo lo representado en el modelo.
3. Antes de asignar trabajo, compara diccionario/diagrama con migraciones/API/clientes/pruebas de la rama efectiva. Verifica nulabilidad explícita: una FK no implica NOT NULL. Identifica reglas de varias filas/tablas y su validación transaccional; no prometerlas con un CHECK aislado. No introduzcas cascadas, políticas de retención, límites de archivo, transiciones o canales no aprobados.
4. En futuras tareas de evidencia exige padre reporte XOR actividad y momento de intervención condicionado; foto inicial no requiere orden. En reportes conserva clasificación pendiente y ubicación manual. No conviertas descripción nullable en permiso para reportes vacíos; la admisión foto/descripción sigue pendiente de conciliación.
5. Distingue áreas de zonas y capacidades normalizadas; asignación requiere cuadrilla activa, área compatible y todas las capacidades necesarias. La propuesta una área/zona por cuadrilla o capacidades por categoría no resuelve las decisiones de cobertura/desactivación. Coordina esas decisiones antes del contrato de asignación.
6. IA: API externa real, datos ficticios/anonimizados y registro de cada intento/fallo. Propuesta separada de confirmación, revisión humana y actualización atómica del reporte/recomendación/historial, sin operaciones críticas autónomas. Duplicado detectado sigue siendo candidato hasta revisión humana; no interpretar «mismo ID» como decisión aprobada.
7. Sesiones: máximo una vigente (RR-08), expiración/revocación verificadas por servidor y cuenta activa; funcionarioWEB/cuadrillaMOVIL. Resolver segundo login rechazado o sustitución antes de implementar. No confiar autorización al canal/dispositivo declarado ni crear sesión como efecto del registroRF-001.
8. Comunicaciones: seguimiento individual por destinatario; guardar mensaje no prueba envío ni lectura. Validación ciudadana solo por propietario; unicidad no reemplaza comprobación de pertenencia. Historial y estado son transaccionales e incluyen acciones sin transición; el último actualizador no reemplaza eventos completos.
9. Protege el [contrato RF-001 ratificado](contrato-rf-001.md): nombre completo/correo/contraseña, sin documento/teléfono, POST /api/v1/ciudadanos. El modelo general tiene diferencias (USUARIO/ROL,auditoría genérica,nombres/apellidos); documenta correspondencias y decisiones técnicas futuras. No amplíes el registro por un campo opcional del modelo. Conserva UUID,hashes,fechas,unicidad y auditoría al planificar una futura migración; no reescribas001 ni fabriques apellidos.
10. Usa las etapas del plan como propuestas, no como tareas ejecutadas. Fija datos/HTTP/decisiones antes de delegar a base_datos y backend_api; web/móvil solo cuando haya contrato aprobado. Pide a calidad pruebas negativas,concurrencia,migración/recuperación y flujos afectados. Preserva cambios ajenos/evidencias e identifica la versión probada. Contexto documental y aprobación física/funcional son entregas distintas.

La tarea de actualización de contexto actual no autoriza DDL, cambios funcionales, modificaciones de contratos ratificados, commit ni push. Para implementación futura, obtener alcance de tarea explícito y aplicar el flujo de aceptación habitual. Las decisiones pendientes se mantienen en el contexto con ID D01–D12; no se promueven a requisitos por copiar este apartado.
