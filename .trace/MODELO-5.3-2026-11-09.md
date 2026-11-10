# Actualización de contexto SGIP — modelo5.3,09/11/2026

Alcance autorizado: contexto, instrucciones del coordinador, contraste y planificación. Sin cambios de funcionalidad, migraciones, datos, contratoRF-001 ni aceptación de pruebas pendientes. Rama del worktree: entrega/rf-001. No hay stage/commit/push por esta tarea.

## Fuentes consultadas

- Modelos y Diagramas: https://app.notion.com/p/3de14e04c5cb809e9250e58428b4e44a. Sección5.3 completa, revisión lógica2026-11-09; edición de página observada2026-11-09T16:18:13.889Z. Copia [modelo-5.3-2026-11-09.md](../ref/modelo-5.3-2026-11-09.md).
- Adjunto **vigente**: [SGIP_Diagrama_ER_Corregido.html](../ref/SGIP_Diagrama_ER_Corregido.html),61691 bytes; SHA256 `4f3ac1a90a12fbcb9b0a96bfb6e12140cc6bab63c4d72ae45d62251edb1acf35`. Bloque371b3819-eb27-44da-a65a-752ff6a9120d; archivo a1d21d43-be02-4f4d-90b2-cd9c693ddd12. Se leyeron el diccionario completo de32 entidades,65 relaciones y las25 notas específicas del HTML; no se ejecutó el visor.
- Referencia estable del adjunto: `notion-file-block://371b3819-eb27-44da-a65a-752ff6a9120d/a1d21d43-be02-4f4d-90b2-cd9c693ddd12?space_id=a839bb6d-31f8-4e5d-9790-0bf10e453e2e&name=SGIP_Diagrama_ER_Corregido.html`. No se guarda la URL firmada de descarga.
- SGIP_Diagrama_ER_Interactivo.html está expresamente marcado como histórico por5.3.1. No se usa ni se presenta como vigente; no fue necesario leerlo para sustituir sus reglas incompatibles.
- Requerimientos Específicos: https://app.notion.com/p/3de14e04c5cb803babfaefe03b6fbf3e, edición observada2026-10-15T18:44:00.020Z. Leídos RF-001–059,RNF,RR,datos3.4,RN-01/02 y catálogos3.7/3.8. La edición del modelo no se atribuye a los requisitos.
- Lectura local de backend/app, migración001 up/down, contratoRF-001 y trazabilidad/evidencias existentes. No se inspeccionó ni modificó una BD desplegada. Los casos detallados externos no se releen completos; las referencias desplazadas de5.1/CU-25/CU-26 quedan explícitamente pendientes de conciliación fuera de esta tarea.

El conector Notion alternativo devolvió404, pero el conector de la sesión leyó ambas páginas y resolvió el adjunto. La descarga de S3 inicialmente falló en sandbox y pasó fuera con autorización. Por tanto ninguna fuente exigida (5.3 y HTML vigente) falta. No se afirma una lectura fallida como exitosa.

## Archivos documentales de la actualización

| Archivo | Función |
| --- | --- |
| [AGENTS.md](../AGENTS.md) | Referencia breve a fuentes, guía/contexto/plan y preservaciónRF-001; conserva las instrucciones ancestras de coordinación/aceptación |
| [docs/orquestacion-agentes.md](../docs/orquestacion-agentes.md) | Guía del coordinador incorporada al worktree con la estructura de la guía del repositorio principal. Actualiza esqueleto histórico, referencias RF actuales y reglas de lectura/delegación5.3 |
| [docs/contexto-modelo-datos.md](../docs/contexto-modelo-datos.md) | Fuentes/versiones,32 entidades,correcciones lógicas y propuestas/decisiones separadas D01–D12; no implica cumplimiento físico |
| [docs/alineacion-modelo-datos.md](../docs/alineacion-modelo-datos.md) | Comparación modelo/repositorio y tareas futuras P0–P9 con dependencias/criterios; incompatibilidad nombres/apellidos y preservación del API |
| [README.md](../README.md) | Enlaces de entrada al contexto; cierre del bloque de estructura Markdown que estaba abierto |
| ref/ y este registro | Copias fuente y evidencia de consulta/validación documental |

La guía y AGENTS ancestrales existen en C:/Users/judat/SGIP, fuera de la rama del worktree. Se incorporaron los documentos correspondientes **en el worktree**, sin escribir ni cambiar el checkout principal ni la configuración de especialistas .codex. Aquí las instrucciones del coordinador quedan en AGENTS.md y la guía, siguiendo las rutas ya utilizadas por el proyecto.

## Impacto RF-001 y brecha de implementación

RF-001 mantiene nombre completo/correo/contraseña, sin documento/teléfono, POST /api/v1/ciudadanos y sin sesión automática. La migración001 crea ciudadanos y auditoria_ciudadanos; no crea ROL/USUARIO ni el resto del modelo global. Scrypt,correo normalizado,rol ciudadano y transacción cuenta/auditoría son implementaciones existentes; no prueban que las32 tablas/65 FK estén materializadas.

El diccionario general exige USUARIO.nombres/apellidos NOT NULL y contempla documento/teléfono opcionales. Se documenta la diferencia: cualquier futura adaptación debe resolver nombres sin fabricarlos, conservar UUID/hash/fechas/auditoría y mantener contrato. No se reabre la decisión de excluir documento/teléfono del RF-001 ratificado. Migraciones/roles generales/sesiones se planifican en tareas nuevas; no se cambió001.

Las pruebas anteriores conservan sus resultados y limitaciones. No se reutilizan como aprobación del modelo global ni se ejecutan nuevas pruebas funcionales en esta tarea. La revisión documental no cierra L01–L08 del registro ni sustituye revisión humana de IA, permisos, historia o recuperación del esquema futuro.

## Comprobaciones realizadas

Validación con Python del entorno backend, extracción JSON de las constantes entities/rels/notes del HTML, sin ejecutar JavaScript descargado. Código de salida0; resultado completo [MODELO-5.3-validacion.json](MODELO-5.3-validacion.json):

- 32 entidades distintas, una PK por entidad,65 atributos FK y65 relaciones distintas por origen/destino/etiqueta.
- Todos los extremos de relaciones existen y los conteos de relaciones entrantes coinciden con FK por entidad. Esto verifica estructura, no garantiza correspondencia semántica individual de cada línea ni implementación SQL.
- Todos los atributos tienen notas leídas;25 notas específicas de integridad. El inventario de contexto coincide exactamente con las32 entidades del adjunto.
- 125 archivos existentes protegidos por SHA256 permanecen idénticos (backend,web,mobile,scripts,evidencias,contratoRF-001,guíaU2 y trazabilidadRF-001). El diff binario del índice Git tiene el mismo SHA256 que al iniciar; no hubo preparación de cambios ajenos.
- git diff --check: exit0, con avisos LF/CRLF preexistentes; 31 enlaces locales documentales comprobados, sin destinos inexistentes.

Calidad revisó de forma independiente adjunto, códigoRF-001 y documentos; no ejecutó BD/tests ni editó archivos. Se corrigieron dos precisiones de su revisión:58 RF se etiqueta como referencia histórica de5.1, pues5.3 vigente cubre001–059; nombre completo en un solo campo no se describe como nombre UNIQUE. Las etapas de evidencia contemplan que las tablas padre deben existir sin exigir una orden/actividad por cada fotografía ciudadana.

No se generó huella de aceptación ni se publicó nada. Esta actualización modifica contexto y propuestas de trabajo, no el estado de aprobación funcional ni la implementación de las etapas planificadas.
