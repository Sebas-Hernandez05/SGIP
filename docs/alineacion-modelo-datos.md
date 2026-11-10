# Comparación y plan de alineación del modelo SGIP

Fecha:2026-11-09. **Plan de trabajo futuro, no implementación autorizada.** Fuentes/estados en [contexto](contexto-modelo-datos.md) y [sección5.3 íntegra](../ref/modelo-5.3-2026-11-09.md). Consultar también [la guía del coordinador](orquestacion-agentes.md).

## Modelo documentado frente al repositorio

Inspección estática de backend/app, backend/migrations, clientes, contrato y trazabilidad locales. No se consultó una BD desplegada; «ausente» significa sin código/migración en este worktree. La migración001 crea únicamente ciudadanos y auditoria_ciudadanos, con dos FK hacia ciudadanos; no hay migración del esquema global ni extensión PostGIS. No se interpreta que la BD de producción tenga o no esas tablas.

| Ámbito / modelo5.3 | Implementación observada | Correspondencia y trabajo faltante |
| --- | --- | --- |
| ROL/USUARIO | ciudadanos: UUID,nombre,correo,password_hash,rol fijo,estado,fecha_registro; schemas/controllers/services/repository de registro | Correspondencia parcial de identidad. No existen ROL/USUARIO globales. Mantener contrato público y diseñar adaptación de persistencia futura |
| SESION_USUARIO/permisos | Registro público, no tokens/login ni middleware de sesión; no matriz general de permisos | No implementado. Planificar con RF-002/003 y RR-08–10, no añadirlo al registro RF-001 |
| REGISTRO_AUDITORIA | auditoria_ciudadanos con ciudadano/actor/operación/fecha, inserción atómica con cuenta | Auditoría específica probada, no equivalente al historial/auditoría general JSONB. Preservar eventos al evolucionar |
| Catálogos,áreas/capacidades y membresías | No tablas ni endpoints de estos dominios | Diseñar contratos, catálogos/versionado, FK y comprobación de compatibilidad; no declarar cubierto RF-019/041 |
| REPORTE/clasificación pendiente/ubicación | No repositorio/API/tablas de reportes | Modelo lógico admite clasificación pendiente y ubicación manual/geométrica; falta implementación y decisiones D04/D07 |
| EVIDENCIA/Storage | Sin tablas/endpoints de evidencias ni cliente Storage | Falta XOR,padres,momento,MIME,privacidad y carga consistente; los mockups no son implementación |
| ORDEN/ACTIVIDAD/PAUSA e historiales | Ausentes en backend/migraciones | Falta integridad reporte→orden,transiciones,pausas y eventos atómicos; no suponer cierres automáticos |
| EJECUCION_IA/RECOMENDACION_IA | Sin integración de proveedor ni tablas | Falta API real, intentos/fallos, revisión humana y aplicación transaccional; no sustituir por simulación |
| Duplicados | Sin detección/revisión persistente | Falta candidato/snapshot/fotos con pertenencia/revisión; RN-01 pendiente no autoriza fusión automática |
| NOTIFICACION/DESTINATARIO | Sin almacenamiento, envío ni estado por destinatario | Falta separación,unicidad,intentos/lectura e implementación de canales confirmados |
| VALIDACION_CIUDADANA/consulta propia | Sin reportes ni endpoint de validación | Falta control del propietario y permisos; UNIQUE por sí solo insuficiente |
| Indicadores/PostGIS/índices | psycopg/PostgreSQL para registro; sin migración de geography/GiST ni consultas de indicadores | Falta esquema/consultas/plazos decididos y pruebas con planes reales. No duplicar indicadores en una tabla por defecto |

No son «30 tablas fallidas de RF-001»: son dominios futuros fuera del registro ratificado. Tampoco se dice que las dos tablas actuales cumplan físicamente el modelo global porque sus funciones sean parecidas.

## RF-001: compatibilidad que debe resolver una futura tarea

| Elemento actual | Modelo general | Tratamiento futuro obligatorio antes de migrar |
| --- | --- | --- |
| nombre completo en un solo campo (sin unicidad del nombre) | USUARIO.nombres y apellidos NOT NULL | Resolver el modelo de nombre o una compatibilidad explícita; no dividir una cadena arbitrariamente, fabricar apellidos ni pedir nuevos campos en RF-001 por inferencia |
| rol='ciudadano' | rol_id→ROL | Sembrar/resolver rol ciudadano desde servidor; no aceptar privilegios del cliente |
| password_hash scrypt | hash_contrasena | Preservar hash/sal/parámetros tal cual; no recalcular con texto inexistente ni solicitar contraseñas |
| estado activo/inactivo | activo y eliminado_en | Correspondencia explícita, sin reactivar cuentas ni inventar fechas de baja |
| UUID y fecha_registro UTC | id,creado_en,actualizado_en | Conservar UUID/fecha conocida, decidir campos históricos desconocidos sin fingirlos |
| auditoria_ciudadanos | REGISTRO_AUDITORIA | Preservar autor/cuenta/fecha/operación,referencias e integridad; sin credenciales en JSON |
| Sin documento/teléfono | Documento nullable único y teléfono nullable | Exclusión RF-001 sigue ratificada. Datos globales opcionales no alteran payload ni validación pública |
| POST /api/v1/ciudadanos | Modelo no define ruta HTTP sustituta | Mantener endpoint/payload/respuestas201/409/422/503; adaptación detrás del repositorio, si se autoriza |

No editar001 para fingir que ya contenía el nuevo modelo. Cualquier futuro cambio requiere tarea aprobada, migración adicional versionada, respaldo/restauración, ensayo desde esquema001 con datos ficticios representativos y recuperación validada. La referencia actual puede necesitar corrección del diccionario de nombres antes de diseñar ese cambio; no es una aprobación para ejecutar DDL ahora.

## Etapas propuestas y tareas verificables

Todas las tareas siguientes están **planificadas/no iniciadas**; esta actualización solo completa la lectura/comparación/documentación. Los responsables son propuestas para delegaciones futuras, no agentes ejecutando cambios ahora. La raíz fija contrato/datos antes de asignar rutas disjuntas.

| Etapa / tarea | Dependencias/decisiones previas | Trabajo futuro y responsables propuestos | Evidencia de aceptación futura |
| --- | --- | --- | --- |
| P0. Fijar fuentes y decisiones de diseño | Contexto actual; D01–D12 según dominio; incompatibilidad de nombres | Coordinador/responsable: concordar diccionario/diagrama,RN/RF y alcance; ADR con fuente/fecha/decisión, sin transformar pendientes en reglas | Matriz RF/RR→regla→constraint/API→prueba; desacuerdos identificados y resueltos solo en su ámbito |
| P1. Identidad y auditoría compatibles | P0 de nombres/estado/auditoría; preservar contratoRF-001 | base_datos: nueva migración/transformación; backend_api: repositorio detrás del mismo endpoint; calidad: regresión. Clientes solo si existe cambio acordado, no por renombrado físico | UUID,correo único normalizado,hashes/fechas/auditoría preservados; mismo contrato; migración001→nueva/base vacía,rollback y restauración. Repetir19 pruebas y casos afectados, no reciclar evidencia antigua |
| P2. Autenticación/sesiones y permisos | P1 y D03; matriz rol/operación/pertenencia | backend_api/base_datos, luego clientes por contrato; RF-002/003 separado. Una vigente,revocación/expiración/canales,cuenta activa | Dos logins concurrentes nunca dejan dos vigentes; segundo login según decisión; token revocado/expirado rechazado; funcionarioWEB/cuadrillaMOVIL; registro no inicia sesión |
| P3. Catálogos y compatibilidad de cuadrillas | Claves identidad; D05/D07 | Catálogos,áreas≠zonas,capacidades/membresías y asociaciones únicas; administración autorizada; snapshot de asignación | Área/capacidad incorrectas y cuadrilla inactiva rechazadas; configuración incompleta no se da por compatible; historia conservada |
| P4. Reportes y estados/historial | P2 para permisos,P3 para catálogos; D04/D06/D07 | Registro con clasificación pendiente,ubicación manual o PostGIS,consulta propia,comentarios e historial atómico; definir contenido útil y contratos de carga | Registro sin clasificación ficticia y con ubicación manual; actor/fecha confirmación conjuntos; acceso ajeno denegado; estado+evento atómicos. No marcar RF-024 de foto como completo hasta P6 |
| P5. Órdenes/actividades/pausas | P3/P4; transiciones/aceptación/cierre y responsable decididos | Orden→reporte obligatoria,prioridad confirmada,asignación compatible,aceptación explícita,actividad/pausas con autores e historial | Rechazo incompatible,una pausa abierta,sin solapamientos/fechas invertidas; aceptación/cambios auditados; cerrar actividad no cierra orden/reporte |
| P6. Evidencias y Storage | P4/P5 proveen tablas padre; política de formatos/retención/carga | Modelo EVIDENCIA completo con XOR y momento,objetos privados,ruta estable y acceso API; clientes de carga | Foto inicial sin que exista una orden/actividad para ese caso; XOR ambos/nada rechazados; momento solo actividad,MIME validado,pertenencia y URLs temporales correctos; fallo de carga sin éxito falso. Si se requiere foto antes de P5, agrupar las dependencias de tablas en una migración coherente, nunca dejar FK a tabla inexistente |
| P7. IA y duplicados con decisión humana | P4/P6; D04/D08/D11; proveedor real aprobado | EJECUCION_IA y recomendación separadas; revisión aceptada/modificada/rechazada transaccional,fallos/reintentos; candidatos duplicados y regla/fotos del mismo caso | Proveedor real con datos ficticios/anonimizados,fallo conserva ejecución; una ejecución0..1 recomendación; no aplicación sin humano; concurrencia no resuelve dos veces; candidato no cierra/fusiona |
| P8. Comunicaciones/validación/reapertura | P4/P5 y D06/D09/D10 | Mensaje+destinatarios con estado individual; validar solo propietario; reapertura únicamente con actor/efectos autorizados | Dos destinatarios pueden tener resultados distintos,unique pareja,lectura individual; valoración de tercero denegada; sin transiciones automáticas por valoración |
| P9. Indicadores y preparación operacional | Etapas relevantes y D07/D10/D11 | Consultas desde hechos/historial,índices con EXPLAIN,plazos/vencimientos definidos; seguridad/retención,TLS,carga y observabilidad del entorno | Métricas reproducibles y avisos por destinatario; backup/restore,planes,concurrencia y tiempos medidos según entorno. Aceptación local separada de despliegue |

Los checks estructurales del adjunto verifican conteos, referencias y diccionario; no sustituyen ninguna aceptación funcional de la tabla. No hay avance funcional acreditado en P1–P9 por esta tarea. Las decisiones de alcance explícitas del usuario siguen teniendo prioridad para RF-001; la incorporación general se hará en nuevas tareas.
