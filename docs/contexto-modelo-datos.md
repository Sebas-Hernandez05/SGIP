# Contexto del modelo de datos SGIP

Actualizado:2026-11-09. Alcance de esta actualización: fuentes, instrucciones y planificación; ninguna modificación funcional o migración. Para el estado concreto del código y el trabajo futuro, consultar [alineación por etapas](alineacion-modelo-datos.md). El modelo lógico global es una referencia de diseño, no una declaración de que32 tablas estén implementadas o aprobadas físicamente.

## Fuentes, versiones y cobertura de lectura

| Fuente | Versión/estado observado | Uso |
| --- | --- | --- |
| [Modelos y Diagramas,5.3](https://app.notion.com/p/3de14e04c5cb809e9250e58428b4e44a) | Sección completa leída; revisión lógica09/11/2026, edición de página2026-11-09T16:18:13.889Z | Referencia lógica vigente; [copia de5.3](../ref/modelo-5.3-2026-11-09.md) |
| [SGIP_Diagrama_ER_Corregido.html](../ref/SGIP_Diagrama_ER_Corregido.html) | Adjunto vigente descargado del bloque371b3819-eb27-44da-a65a-752ff6a9120d, archivo a1d21d43-be02-4f4d-90b2-cd9c693ddd12 | Leídos entidades, atributos, relaciones y notas;32 entidades,65 atributos FK y65 relaciones verificados estructuralmente |
| SGIP_Diagrama_ER_Interactivo.html | Notion5.3.1 lo identifica expresamente como antecedente histórico | Sustituido; no se descargó ni se usa como referencia vigente |
| [Requerimientos Específicos](https://app.notion.com/p/3de14e04c5cb803babfaefe03b6fbf3e) | Página leída; última edición observada2026-10-15T18:44:00.020Z | RF-001–059, RNF, RR, datos3.4, RN-01/02 y catálogos3.7/3.8. Su fecha no se cambia a la revisión del modelo |
| [Contrato RF-001](contrato-rf-001.md) y decisiones del usuario | Nombre completo/correo/contraseña; sin documento/teléfono; POST `/api/v1/ciudadanos`; ampliaciones en otra tarea | Alcance aprobado de esta entrega; el modelo global no lo amplía implícitamente |
| [Trazabilidad RF-001](../.trace/RF-001.md) y sus evidencias | Implementación parcial con registro y auditoría específicos; resultados anteriores conservados | No se reinterpretan como pruebas del nuevo esquema global |

El conector Notion alternativo devolvió404; el conector Notion de la sesión sí permitió leer página, requisitos y resolver el adjunto vigente. No falta ninguna de las dos fuentes exigidas (sección5.3 y HTML corregido). La descarga exigió acceso fuera del sandbox. No se guardan URLs firmadas/tokens; se conservan enlaces estables, copia y SHA256 en [el registro de actualización](../.trace/MODELO-5.3-2026-11-09.md). No se ejecutó el visor ni se verificó una instancia desplegada.

Los casos detallados enlazados desde Notion no se han releído completos en esta tarea; las discrepancias de5.1/CU-25/CU-26 se registran como conciliación externa pendiente, no se resuelven por inferencia. La lectura de la sección5.3 sí es completa, incluido su apartado15 de decisiones y el diccionario HTML.

## Cómo interpretar el contexto

- **Corrección documentada:** regla o estructura que5.3 corrige en su referencia lógica. No equivale a migración ejecutada ni a autorización para implementar toda la propuesta.
- **Requisito:** comportamiento respaldado por RF/RR/RNF y el alcance de la tarea. Mantener su ID y fuente; no renumerar por copiar tablas antiguas de casos/interfaces.
- **Propuesta técnica o decisión pendiente:** variante señalada así por la fuente; requiere resolución antes de implementar lo que dependa de ella.
- **Implementado/verificado:** exige código/migración identificable y evidencia aplicable a esa versión. Una FK dibujada o una nota no acreditan integridad física.

Cuando una decisión explícita de alcance de una entrega difiere del modelo global, registrar la diferencia y planificar compatibilidad; no añadir campos ni cambiar endpoints silenciosamente.

## Inventario completo del modelo lógico

Agrupación editorial para consulta; los nombres son los del adjunto.

| Ámbito | Entidades |
| --- | --- |
| Identidad | ROL, USUARIO, SESION_USUARIO |
| Catálogos | CATEGORIA, PRIORIDAD, ZONA, ESTADO_REPORTE, ESTADO_ORDEN, ESTADO_ACTIVIDAD, TIPO_EVIDENCIA |
| Reportes y validación | REPORTE, HISTORIAL_REPORTE, COMENTARIO, VALIDACION_CIUDADANA |
| Cuadrillas y compatibilidad | AREA_RESPONSABLE, CAPACIDAD, CUADRILLA, MIEMBRO_CUADRILLA, CUADRILLA_CAPACIDAD, CATEGORIA_CAPACIDAD |
| Operación | ORDEN_TRABAJO, HISTORIAL_ORDEN, ACTIVIDAD_ORDEN, PAUSA_ACTIVIDAD |
| Evidencia | EVIDENCIA |
| IA | EJECUCION_IA, RECOMENDACION_IA |
| Duplicados | REGLA_DUPLICADO, DETECCION_DUPLICADO |
| Comunicaciones | NOTIFICACION, NOTIFICACION_DESTINATARIO |
| Auditoría | REGISTRO_AUDITORIA |

## Correcciones documentadas que deben guiar futuras tareas

| Tema/fuente5.3.2 | Referencia lógica vigente | Requisitos relacionados y límite |
| --- | --- | --- |
| Evidencias,§7/13 | Exactamente un padre: reporte o actividad (XOR); ambos FK individualmente nullable. Foto inicial sin orden/actividad. Campo: actividad→orden→reporte. Momento ANTES/DURANTE/DESPUES obligatorio solo para actividad y nulo en foto inicial; MIME y tipo son conceptos distintos | RF-024/027/047. No inventar mínimo de fotos por fase ni tamaño máximo |
| Storage,§7 | Objeto privado y referencia canónica estable; URLs firmadas solo al consultar; permisos/pertenencia al entregar archivo; tratar cargas fallidas/huérfanos | Datos3.4.2, RR-03/04. No confirmar éxito antes de completar operación |
| Clasificación pendiente/ubicación,§4 | Categoría/prioridad inicialmente nulas; no categoría ficticia. Actor/fecha de confirmación conjuntos e historial atómico. Coordenadas válidas o referencia textual útil; geography(Point,4326) propuesto | RF-020–025/RR-04. Contenido descripción/foto requiere conciliación; no admitir reporte vacío |
| Áreas/capacidades,§8 | Área responsable distinta de zona. Catálogo CAPACIDAD y asociaciones N:M únicas. API verifica cuadrilla activa, área y todas las capacidades necesarias; conservar configuración usada en asignación | RF-019/041/RR-07. Una área/zona por cuadrilla y parametrización requerida por categoría son propuestas por validar, no alcance multicobertura aprobado |
| IA,§5 | Cada intento en EJECUCION_IA incluso si falla;0..1 recomendación por ejecución. Propuesta original separada de confirmación humana; decisiones PENDIENTE/ACEPTADA/MODIFICADA/RECHAZADA con campos coherentes. Misma pertenencia de reporte y transacción para revisión/reporte/historial | RF-030–036,RR-01/02,RNF-015/016. API real externa; solo datos ficticios/anonimizados. Error no bloquea clasificación manual ni autoriza aplicación automática |
| Sesiones,§2 | Un rol por usuario; persona usuaria distinta de CUADRILLA. Modelo SESION_USUARIO con hash de token, expiración/revocación y canal; propuesta índice único por usuario no revocado y limpieza atómica de expiradas; verificar vigencia/cuenta en cada petición | RF-002/003,RR-03/08/09/10. Máximo una vigente es requisito; rechazar o sustituir segundo login sigue pendiente. Dispositivo/canal declarados no prueban autorización |
| Notificaciones,§10 | Mensaje separado de destinatarios; UNIQUE(notificacion_id,usuario_id). Estado/intentos/envío/fallo/lectura individuales; al menos un destinatario al preparar envío; guardar mensaje no significa enviarlo | RF-048/049/050/059. Contexto reporte XOR orden es propuesta operativa; canales externos/reintentos/disparadores pendientes. ENVIADA no equivale a entrega/lectura del proveedor |
| Validación del propietario,§11 | Solo ciudadano propietario de REPORTE; comprobar igualdad de usuario y propietario además de permisos/estado. UNIQUE de pareja no acredita pertenencia | RF-051,RR-04. Una valoración por pareja es propuesta inicial; ciclos tras reapertura pendientes. No cerrar/reabrir por valorar |
| Historiales,§9/12 | Operación/detalle JSONB para eventos con y sin transición; creación con estado inicial, transición con anterior/nuevo; usuario nulo solo para sistema identificado. Estado/historial atómicos y control de concurrencia | RF-004/046/053,RNF-06,datos3.4.4. Último actualizador no sustituye eventos; ciudadano no recibe auditoría global |
| Actividades/pausas,§9 | Una pausa abierta, sin solapamientos, autores/fechas coherentes; orden siempre con reporte. Cierre de actividad distinto de orden y reporte | RF-037–047,RR-06. Matrices de transición, cierre y reapertura no se deducen de los catálogos |
| Duplicados,§6 | Candidatos con regla aplicada/snapshot y revisión humana; fotos comparadas pertenecen a sus respectivos reportes, directa o indirectamente; no fusionar/eliminar/cerrar automáticamente | RF-028/029,RR-05. «Mismo ID» y efectos de confirmación RN-01 pendientes; hash igual no es similitud de escena |
| Prioridad/integridad,§3/13 | Prioridad puede existir sin órdenes; cada orden tiene prioridad. FK no implica NOT NULL; preservar nulabilidad explícita y catálogos históricos, UUID/timestamptz. Reglas multitabla requieren validación transaccional | RF-010/038 y datos3.4. No cascadas físicas adoptadas para entidades de negocio/auditoría. Índices son propuestas a validar con consultas reales |

## Propuestas y decisiones funcionales todavía pendientes

Esta lista proviene de5.3.2§15; no son requisitos aprobados por aparecer en el HTML.

| ID | Decisión por resolver antes de la tarea afectada |
| --- | --- |
| D01 | Documento: obligatoriedad/formato/unicidad exacta global frente a3.4.1/T13/T16. Para RF-001 ya está decidido excluirlo; no reabrir esa decisión sin nueva tarea |
| D02 | Multirrol o edición dinámica de permisos: no incluidos; referencia actual un rol y matriz versionada API |
| D03 | Segundo login: rechazar o revocar anterior atómicamente; ambas variantes mantienen una sola vigente |
| D04 | Descripción frente a solo foto: conciliar RF-022/031/CU-03; estructura nullable no aprueba admisión de contenido vacío |
| D05 | Área/capacidades por categoría, una área/zona por cuadrilla, cobertura adicional y efectos de desactivación |
| D06 | Transiciones, cierre/reapertura: actor/canal/estado/motivo/efecto sobre órdenes; significado de responsable_id |
| D07 | Copia inicial de prioridad y propagación futura; plazo por prioridad, fecha objetivo del reporte y cálculo de vencimiento con varias órdenes/pausas/reaperturas |
| D08 | Duplicados: «mismo ID», pares repetidos/inversos y efectos de confirmar, sin automatismos contrarios a RR-05 |
| D09 | Valoraciones repetidas o ciclos tras reapertura; no aprobar cambios de unicidad por deducción |
| D10 | Comunicaciones: canales externos, avisos generales/contexto, seguimiento y respuesta, frecuencia/reintentos/distribución y destinatarios de vencimiento |
| D11 | Acceso, retención, eliminación lógica y datos de evidencia/auditoría/IA; sin política de cascada implícita |
| D12 | Conciliación de referencias RF desplazadas y CU-25/CU-26 fuera de5.3; no renumerar pruebas históricas ni editar Notion ajeno al alcance |

Además hay una **incompatibilidad técnica nueva por conciliar**, no una ampliación funcional aprobada: USUARIO exige nombres/apellidos separados, mientras el contrato RF-001 ratificado solo recibe nombre completo. La futura alineación debe decidir cómo adaptar el modelo sin inventar ni separar automáticamente apellidos y sin exigir nuevos campos al registro.

## Impacto sobre RF-001

Se conserva íntegro [el contrato](contrato-rf-001.md), las dos tablas específicas actuales, el código, el índice Git y las evidencias previas. El modelo general contempla USUARIO/ROL/REGISTRO_AUDITORIA, teléfono/documento opcionales y datos de autenticación; su existencia documental no autoriza incorporarlos a RF-001 ni exige completar los demás dominios dentro del registro. RF-002/sesiones se planifican aparte; registro sigue sin iniciar sesión.

Las verificaciones19/19 backend,4/4 servicio,5 de utilidad U2 y las pruebas manuales conservan sus fechas/versión/límites. No se ejecutaron nuevamente por esta actualización documental ni acreditan32 tablas/65 relaciones. Los pendientes locales L01–L08 conservan el estado de [la matriz RF-001](../.trace/evidence/paso3-matriz-actual.md); leer un modelo nuevo no los aprueba ni agrega pruebas funcionales productivas retroactivamente.
