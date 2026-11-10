# RF-001: matriz conciliada de aceptación local y operacional

Estado vigente al10/11/2026: **todos los criterios obligatorios locales cubiertos; lista para revisión de huella**. La conciliación siguiente prevalece sobre los apartados históricos. La aceptación explícita de la nueva huella sigue pendiente; sin commit ni push.

## Conciliación final de la evidencia manual

Coordinación y calidad contrastaron el QA completo, incluidos los resultados añadidos del09–10/11. Se reconoce la declaración actual del responsable de haber terminado las verificaciones documentadas; no se exige repetir resultados explícitamente aprobados ni se atribuye su ejecución a los agentes.

| Caso | Estado vigente y evidencia en qa-rf001.md |
| --- | --- |
| L01 | Aprobado web y Android por confirmación explícita del responsable: contraseñas distintas, error visible y ningún POST. Ver acta final de QA. |
| L02 | Móvil aprobado09/11. Web aprobado por confirmación explícita actual:422 presentado correctamente, datos previstos conservados, carga terminada y reintento disponible. |
| L03 | Aprobado web09/11 y móvil10/11: indisponibilidad visible, carga finalizada, reintento y sin éxito falso. El campo de mensaje web contiene un log del simulador; el resultado declara el error visible. No se inventa una cita de pantalla. |
| L04 | Aprobado en ambos: aviso de incertidumbre, fin de carga y reintento. Web aprox.14–15s; segundos móviles sin completar, limitación de metadatos. La medición del servicio E9 no se atribuye a UI. |
| L05 | Aprobado10/11: web320/1280, zoom200%, estados y escenarios móviles, sin incidencias declaradas. |
| L06 | Aprobado manualmente: Tab/Shift+Tab, foco, Mostrar/Ocultar, errores y anuncios. Fecha, navegador y lector/versiones específicos siguen sin completar: limitación de reproducibilidad, sin inventarlos ni exigir repetición automática. |
| L07 | Aprobado10/11 en Oppo: teclado de correo, Siguiente/Hecho, controles alcanzables y cierre tras201. |
| L08 | Aprobado10/11 en Oppo/ColorOS, TalkBack17.1: etiquetas, obligatorios, botones, errores y éxito anunciados; lectura lógica. |

No quedan pendientes obligatorios locales: el acta final de QA cierra L01 en ambos y L02 web. Calidad verificó el cierre y no detectó defecto bloqueante nuevo. TLS/carga productiva y disposición de hallazgos npm conservan su alcance operacional; no hay remediación ni aceptación de riesgo implícitas. Contrato ratificado sin cambios.

Rama efectiva `entrega/rf-001` (no es una carpeta). Se leyó `.codex/config.toml` y `.codex/agents/` del repositorio ancestro; no existe `.codex` local. Esta conciliación solo cambia documentación, conserva código/evidencias y no invalida los checks aprobados. Todas las acciones históricas inferiores que solicitan L01–L08 quedan superadas por este apartado y el acta final de QA.

## Fuentes y autoridad de cada criterio

- **R1** [Contrato RF-001, Verificación requerida](../../docs/contrato-rf-001.md#verificación-requerida): «Ambos clientes: éxito, error, carga, red, prevención de doble envío y accesibilidad de formularios». Es contrato de implementación compartido; no se presenta como texto literal ampliado del RF original.
- **R2** [Contrato compartido](../../docs/contrato-rf-001.md#contrato-compartido): payload,201/409/422/503, confirmación solo cliente, sin sesión; HTTPS **para producción**, HTTP local limitado a desarrollo.
- **R3** [web/README.md, Verificación](../../web/README.md#verificación): «confirmación distinta», «datos rechazados por API», «timeout», teclado/foco/errores/anuncios y presentación320/1280 px. Son criterios de verificación de la implementación; no se atribuyen como redacción literal de RF-001.
- **R4** [mobile/RF001.md](../../mobile/RF001.md): mensajes409/422/503/red, timeout15 s con incertidumbre, conservación de datos y manejo de teclado/foco/anuncios.
- **R5** Solicitud del usuario en esta conversación: reproducir identidad UIW-01/UIM-01 de [ref/SGIP-Mockups.html](../../ref/SGIP-Mockups.html), adaptación a componentes nativos/teclado y verificación visual cuando se disponga de navegador/dispositivo.
- **R6** [Contrato RNF-09](../../docs/contrato-rf-001.md#verificación-requerida): <=2 s, entorno y concurrencia documentados; no presume carga productiva. Guía docs/orquestacion-agentes.md del repositorio principal pide confirmar carga cuando no esté definida.
- **R7** AGENTS.md ancestro, paso3: pruebas obligatorias pendientes/fallidas bloquean aceptación; registrar resultados/no aplicables y verificar correcciones. Esta regla **no crea** requisitos de iOS, certificación WCAG integral, audit=0 ni despliegue productivo.

## Evidencias vinculadas

| Clave | Evidencia y versión | Procedencia / uso |
| --- | --- | --- |
| E0 | [qa-rf001.md, apartados iniciales](qa-rf001.md) | Historia anterior al rediseño; no acredita por sí sola pantalla final. |
| E1 | [qa-rf001.md, web rediseñada22:30](qa-rf001.md#pruebas-manuales-del-formulario-web-rediseñado) | Chrome156, localhost5173, API/PG de pruebas.201, carga/deshabilitado, un POST, cuenta/auditoría, red y recuperación observados por responsable. |
| E2 | [qa-rf001.md, móvil rediseñado22:56](qa-rf001.md#validación-funcional-del-formulario-móvil-rediseñado) | OppoA58/ColorOS/Expo Go SDK57.201/409, vacíos/correo/contraseña inválidos, carga/doble envío, red/recuperación, responsable. |
| E3 | [qa-rf001.md, addendum de conversación](qa-rf001.md#addendum-de-conciliación-aportado-en-conversación) | Usuario confirma expresamente registro, duplicado, validaciones, doble envío, fallo de conexión y recuperación del rediseño **web y móvil**. Complementa E1/E2 y cierra web409/validación básica; no pide repetición ni captura para reconocerlo. |
| E4 | [cierre-backend-pytest.txt](cierre-backend-pytest.txt), [integración final](cierre-rf001-integracion.md#checks-finales) | Backend actual19/19,0 omitidas, exit0, PG16 real, concurrencia1,0.2189 s. Contrato, validación, privilegios, hash, persistencia, auditoría, concurrencia, rollback/migración. |
| E5 | [paso3-http-recuperacion-actual.txt](paso3-http-recuperacion-actual.txt) | HTTP real201/409/422+CORS, PG/auditoría y dump/restore;0.1913 s. Sin UI. Utilidad temporal retirada, resultado histórico actual de API conservado. |
| E6 | [cierre-rf001-calidad.md, checks](cierre-rf001-calidad.md#verificaciones-de-clientes-ejecutadas-de-nuevo) | Diseño actual: web lint/tipos/build; móvil lint/tipos y servicio4/4, todos0. No son E2E. No cambió lógica desde estos checks. |
| E7 | [conciliacion-calidad.md](conciliacion-calidad.md) | Revisión independiente del addendum, alcance y límites. |
| E8 | [dependencias-revision.md](dependencias-revision.md) | Revisión actual npm/árbol/advisories, sin actualizar paquetes. |
| E9 | [qa-respuestas-evidencia.md](qa-respuestas-evidencia.md), [U2 ejecutable](../../docs/qa-rf001-u2.md) | Utilidad reincorporada y5 pruebas aprobadas;422/503 HTTP y cancelación del servicio móvil real a15.010s ante demora20s. No prueba UI. |

## Criterios ya cubiertos: no repetir

| Criterio | Fuente | Web actual | Móvil actual | Evidencia |
| --- | --- | --- | --- | --- |
| Registro e integración real API/PG | R1/R2 | Aprobado manual201 | Aprobado manual201 | E1/E2/E3; E4/E5 backend |
| Duplicado409 | R1/R2 | Aprobado manual por addendum | Aprobado manual | E3/E2, con prueba backend concurrente E4 |
| Validación básica (vacíos/correo/contraseña inválidos) | R1/R2 | Aprobado manual por addendum | Aprobado manual | E3/E2. La declaración no enumera todos los valores límite; los límites y validaciones API sí están probados E4. No se exige repetir toda la matriz de límites en UI como nuevo bloqueo. |
| Carga, deshabilitado y un POST ante doble envío | R1 | Aprobado manual | Aprobado manual | E1/E2/E3 |
| Error de conexión, conservación y recuperación/reintento | R1/R4 | Aprobado manual | Aprobado manual | E1/E2/E3 |
| Persistencia/auditoría/transacción/seguridad API | R1/R2 | API común aprobada | API común aprobada | E4/E5; E1 confirma cuenta/auditoría manual. No hace falta repetir auditoría por cada cliente para demostrar la misma transacción backend. |
| No iniciar sesión y exclusión de rol/confirmación del payload | R2 | Implementación revisada | Implementación/servicio revisados | E4/E6; no hay tokens ni ruta de login. No se convierte la falta de mención manual en un nuevo bloqueo independiente. |
| Lint/tipos/build y servicio | Guía, R7 | Aprobado | Aprobado | E6 |
| RNF-09 local <=2 s, concurrencia1 | R6 | API común aprobada | API común aprobada | E4/E5; no se inventa carga productiva. |

## Casos exactamente no cubiertos en aceptación local

**No son fallos observados**: falta una ejecución de la pantalla final para los casos descritos. La ejecución API/servicio y revisión estática ya existen; no se presentan como prueba de pantalla. Cuando se aporte resultado manual explícito se cierra el caso sin exigir grabación obligatoria.

| ID | Caso concreto que falta / plataformas | Fuente que lo exige en RF-001 | Esperado y evidencia para cerrar | Motivo actual |
| --- | --- | --- | --- | --- |
| L01 | Confirmación de contraseña distinta, web y Android | R3 explicita prueba; R2 confirmación solo formulario | Mensaje visible/asociado, sin POST; aportar resultado por cliente. | «Validaciones» generales no detalla este caso; no se inventa aprobación particular. |
| L02 | Presentación de rechazo422 del servidor, web y Android | R2 contrato422; R3 datos rechazados por API; R4 mensajes422 | Con formulario local válido y respuesta422, error controlado en español, datos conservados y reintento; no incluir cuerpo arbitrario. | E4/E6 prueban API/servicio, no su presentación en ambos formularios. |
| L03 | Presentación503 de servicio, web y Android | R1 errores de servicio controlados y ambos clientes error; R2/R4 código503 | Error de indisponibilidad, datos conservados, controles habilitados al acabar, sin éxito falso. | API detenida prueba conexión rechazada, no una respuestaHTTP503; no se exige repetir red. |
| L04 | Espera>15 s/timeout, web y Android | R3 timeout; R4 incertidumbre15 s | Termina carga y avisa que registro podría haberse completado; conserva datos y permite reintentar, sin confirmar éxito. | No descrito en E1–E3. No hace falta provocar creación incierta real en BD: sirve respuesta demorada controlada de QA. |
| L05 | Comparación visual final UIW-01 a320/1280 px y registro UIM-01 en Oppo | R5 diseño solicitado; R3 tamaños web | Colores/fuente/espaciado/controles/estados coherentes con HTML; sin recortes o superposición que impidan uso. Breve observación con tamaño/dispositivo; capturas útiles pero no condición formal para reconocer prueba. | Registro funcional no describe comparación visual. Agente sin host de navegador; no observó pantalla. |
| L06 | Teclado/foco/accesibilidad web del formulario | R1 accesibilidad; R3 teclado/foco/resumen/enlaces/anuncios | Tab/Shift+Tab y Mostrar/Ocultar utilizables, foco visible/orden lógico; error conduce al campo, carga/error/éxito perceptibles; aportar orden/resultado y anuncios con lector disponible. | ARIA/código revisados; sin ejecución accesible final declarada. |
| L07 | Teclado/scroll nativo en Oppo | R5 adaptación al teclado; R4 manejo nativo | Correo abre teclado adecuado; Siguiente/Hecho en orden; primer error enfocado, botón alcanzable con teclado abierto; cierre tras201. Resultado explícito por acción. | E2/E3 describen flujos, no comportamiento del teclado. |
| L08 | Lectura accesible móvil en plataforma local probada | R1 accesibilidad; criterio UIM-01 del HTML: etiquetas, errores anunciados y foco/lectura en orden lógico | TalkBack en Oppo lee nombre/obligatorio, botones/ocupado y error/éxito en orden lógico. Aportar anuncios breves; no se exige auditoría WCAG integral. | Revisión estática no equivale a lector ejecutado; no hay resultado manual declarado. |

No se añaden como bloqueos locales independientes: repetir todos los límites en UI ya cubiertos en API; probar cada orientación/escala posible; certificación WCAG completa; VoiceOver/iOS sin alcance de aceptación iOS acordado; screenshot de cada clic. Texto ampliado/zoom puede incorporarse a L05/L06 como comprobación de legibilidad, sin certificar WCAG.

Para ejecutar L02–L04, seguir [U2 vigente](../../docs/qa-rf001-u2.md): comandos desde raíz, puerto58010, modos422/503/demora20, overrides temporales de web/Expo y restauración exacta. E9 acredita el servidor y el servicio móvil HTTP real; L02–L04 mantienen pendiente únicamente su presentación en las pantallas. La retirada histórica de la utilidad queda corregida: ahora se conserva como herramienta QA con pruebas.

## Local frente a despliegue operacional

| Tema | Fuente/estado | ¿Bloquea aceptación local de RF-001? | ¿Qué falta para operación? |
| --- | --- | --- | --- |
| TLS/proxy/logs y configuración desplegada | R2: HTTPS para producción; ASGI/CORS aprobado E4, HTTP local de desarrollo permitido | No por falta de staging. La matriz anterior lo mezclaba con aceptación local. | Antes de habilitar entorno público: certificado válido sin -k, sin contenido mixto, orígenes CORS explícitos, proxy confiable, configuración/logs sin credenciales/cuerpos. Requiere URL/entorno autorizado. |
| RNF-09 bajo carga productiva | R6 no presume carga | No: local1 concurrente ya aprobado | Definir carga/entorno representativo con responsable y medir<=2 s según alcance; no inventar percentiles. |
| Hallazgos npm | E8, sin política audit=0 acordada en R1/R7 | No por el mero exit1/conteo. Revisión solicitada ejecutada; no se afirma resuelto ni seguro. | Resolver aplicabilidad/remediación o disposición explícita del riesgo antes de apertura pública. Web:2 altas solo árbol dev, producción0; móvil:25 total/18 en árbol omit=dev, sin demostrar inclusión/explotabilidad en bundle. |
| iOS/VoiceOver | No hay aceptación iOS específica acordada; dispositivo declarado Android | No como requisito añadido por ausencia de equipo; no se declara iOS verificado | Si se solicita entregar iOS, acordar alcance y ejecutar dispositivo/VoiceOver correspondiente. |
| Commit/push de rama de revisión | AGENTS.md pasos5–6 requieren huella y aprobación explícita | No equivale a desplegar a producción; solo después de cerrar obligatorios locales y decisiones de alcance necesarias | Push no acredita ni autoriza por sí solo despliegue público. |

## Decisiones de contrato resueltas

Fuente: instrucción explícita del usuario en esta conversación, posterior a la conciliación. Se ratifica el [alcance del contrato](../../docs/contrato-rf-001.md#alcance-ratificado-por-el-responsable); no se presume una decisión por silencio. Las discrepancias de alcance dejan de estar pendientes para RF-001.

| Tema | Decisión ratificada | Impacto |
| --- | --- | --- |
| Datos del registro | Nombre completo, correo y contraseña; sin documento ni teléfono | Payload existente `{nombre,correo,contrasena}` conservado. No se separan nombres/apellidos. |
| Endpoint | POST /api/v1/ciudadanos | Sin alias ni migración a /api/auth/register. |
| Ampliaciones | Cualquier ampliación se tramita en otra tarea | No se amplía esta entrega por tarjetas o mockup. Límites12–128, confirmación local y RF-002 separado siguen como estaban. |

## Acciones históricas del responsable - completadas

1. **Funcional restante:** en ambos clientes probar L01–L04 en entorno QA controlado. Aportar por caso esperado/observado, HTTP si aplica y si conservó datos/permitió reintento. No hace falta repetir201/409/validaciones básicas/doble envío/red/recuperación.
2. **Visual web+móvil:** comparar con UIW-01/UIM-01; web320/1280 y móvil con teclado abierto. Resultado esperado: diseño coherente y controles legibles/alcanzables; indicar cualquier recorte (L05).
3. **Teclado/foco:** Tab/Shift+Tab web, error/enlaces/éxito y Mostrar/Ocultar; correo/Siguiente/Hecho/scroll en Oppo. Resultado esperado: orden lógico, foco perceptible y ningún control inaccesible (L06/L07).
4. **Lectura:** TalkBack en Oppo y lector web disponible; escuchar etiquetas/obligatorio/error/éxito. Resultado esperado: anuncios comprensibles y orden lógico (L06/L08). Basta descripción de lo oído; no se solicita certificación integral.
5. **Contrato:** resuelto por el responsable; no requiere otra confirmación. Las ampliaciones quedan para otra tarea.

## Limpieza, checks y siguiente huella

No cambió lógica de aplicación en esta conciliación; no se repiten tests aprobados sin un cambio que los invalide. El diff aparente del repositorio backend no tiene cambio de contenido respecto al índice (aviso de fin de línea); no se introduce modificación funcional. Se retiraron árboles npm JSON temporales tras extraer resumen y se conservan cuatro JSON audit válidos. Diagnósticos de sesiones anteriores siguen retirados. No se incluyen entornos/dependencias locales ni secretos nuevos.

El alcance contractual está fijado y ya no bloquea aceptación. R7 mantiene pendientes las verificaciones **locales** L01–L08 aún no observadas en su alcance. No se usa TLS/carga productiva/audit0/iOS como bloqueo local automático. Cuando se cierre lo obligatorio, se revisará el conjunto, se preparará el diff y se generará nueva huella. Esta decisión documental no aprueba pruebas pendientes ni autoriza commit/push; la huella anterior no abarca esta actualización.
