# RF001-QA — verificación integrada

> Registro cronológico: los apartados iniciales son históricos; las dos últimas secciones acreditan los casos manuales expresamente descritos de la versión rediseñada. Para el estado vigente por criterio, consultar [paso3-matriz-actual.md](paso3-matriz-actual.md). Los fallos iniciales de dependencias están superados; las casillas históricas sin completar no son aprobaciones. Se preservan sin alterar los resultados aportados por el responsable.

Estado vigente al10/11/2026: todos los criterios obligatorios locales cubiertos. L01 web/móvil y L02 web cerrados por confirmación explícita del responsable en esta conversación; ver acta final al pie. Los resultados históricos se conservan y la matriz vigente prevalece sobre pendientes anteriores.

Fuentes: RF-001 «El sistema permitirá el registro del Ciudadano», [requisitos](https://app.notion.com/p/3de14e04c5cb803babfaefe03b6fbf3e), versión observada por coordinador 2026-10-15T18:44:00.020Z; CU-01, UIW-01 y UIM-01 en [modelos](https://app.notion.com/p/3de14e04c5cb809e9250e58428b4e44a), 2026-10-17T00:26:37.030Z.

## Entorno y ejecución

Windows/PowerShell; rama entrega/rf-001, base 4de9c6ef29bd0bc6a5fe1d13875d278c2e4a40f8; Python 3.13 del lanzador py, entorno backend/.venv con requirements fijados; FastAPI 0.115.12, Pydantic 2.11.4, psycopg 3.2.9, pytest 8.3.5. PostgreSQL 16 alpine mediante imagen Docker local y contenedor exclusivo sgip-rf001-qa, puerto loopback 55432 y datos ficticios en tmpfs. No se usó el contenedor PostgreSQL ajeno existente. No hay datos reales ni credenciales de servicios externos en evidencias.

La ejecución usa TEST_DATABASE_URL apuntando **exclusivamente a una base desechable vacía**, y PYTHONPATH=backend desde la raíz del worktree. La fixture crea el esquema y ejecuta down tras cada prueba PostgreSQL; no ejecutar contra una base compartida. Para reproducir, crear contenedor propio con postgres:16-alpine y volumen tmpfs, configurar URL local de pruebas, y ejecutar:

`backend/.venv/Scripts/python -m pytest backend/tests -q -s -p no:cacheprovider`

Resultado final: **exit 0, 19 passed, 1 warning, 5.17 s**. Evidencia: [backend-pytest.txt](backend-pytest.txt). Aviso deprecación Starlette/AnyIO sin fallo; no demuestra compatibilidad con versiones futuras.

| Categoría / criterio | Resultado observado | Estado |
| --- | --- | --- |
| Conexión API a PostgreSQL real | POST con TestClient y repositorio real conectó a PostgreSQL 16 local; persistió cuenta | Aprobado en entorno local |
| Migración base vacía y reversión | up ejecutada antes y down después de cada una de 4 pruebas PG; repetición confirma recreación sin residuos | Aprobado |
| Actualización desde versión anterior | Primera migración; no existe esquema anterior soportado en develop | No aplica justificado |
| Contrato HTTP público | 201, UUID y campos exactos; nombre/correo normalizados; rol ciudadano y estado activo; no abre sesión | Aprobado |
| Validación y seguridad de privilegios | Nombre vacío/largo, correo inválido, contraseña corta/larga, tipos erróneos, rol/estado/id extra y JSON malformado rechazados con 422 | Aprobado |
| Protección credenciales | Respuesta/errores sin input ni contraseña/hash; scrypt con sal aleatoria; derivación comprobada y espacios no recortados | Aprobado |
| Duplicados y concurrencia | 409 con correo case-insensitive; 2 hilos compiten: una cuenta y una auditoría | Aprobado |
| Transacción y recuperación | Trigger provoca fallo auditoría; HTTP503 controlado, ninguna cuenta parcial; trigger retirado en finally | Aprobado |
| Restricciones PostgreSQL | Rechaza rol administrador, correo sin normalizar y nombre vacío | Aprobado |
| Fallos persistencia | 503 sin detalles internos, prueba de error inducido real y doble de repositorio | Aprobado |
| Autenticación y propiedad de recurso | Registro es público; no consulta ni modifica recursos ajenos; login RF-002 no implementado por alcance | No aplica al endpoint de registro |
| HTTPS y CORS configuración | APP_ENV production redirige HTTP con307; permite origen explícito y deniega origen ajeno; rechaza origen HTTP en producción | Aprobado como configuración ASGI |
| TLS desplegado y secretos operativos | Sin despliegue HTTPS disponible; revisión de código no sustituye conexión TLS real ni configuración de proxy | Pendiente |
| RNF-09 operación sencilla | Registro completo FastAPI/PG/hash, datos ficticios, concurrencia1, 0.1793s observado, umbral2s | Aprobado solo medición local; carga productiva por acordar |
| Rendimiento operación compleja | RF-001 no contiene operación compleja | No aplica |
| IA / Storage / cámara / ubicación | Registro no invoca IA, Storage, cámara ni ubicación | No aplica |

## Clientes y flujo completo

`node --test mobile/tests/registration.test.mjs`: **exit0, 4 passed**; evidencia [mobile-service-tests.txt](mobile-service-tests.txt). Comprueba payload API y ausencia de rol/confirmación, errores409/422/503, fallo de red y reintento, rechazo HTTP remoto. Usa fetch sustituido: **no es E2E ni valida React Native**. Node emitió aviso MODULE_TYPELESS_PACKAGE_JSON sin fallo.

Web informa `npm ci` exit1 ENOSPC; `npm run lint` exit1 por oxlint ausente; `npm run build` exit1 por tsc ausente. Se retiró únicamente node_modules parcial creado durante esta entrega por instrucción del coordinador. No hay resultado satisfactorio de compilación/lint. Fuente: agente web_rf001, log npm local 2026-11-06T00_49_25_405Z-debug-0.log.

Móvil informa npm ci no ejecutado para evitar agotar ~0.14GB libres; `npm run lint` exit1 por expo ausente y `npx --no-install tsc --noEmit` exit1 por TypeScript ausente. Fuente: agente movil_rf001, mobile/RF001.md.

Revisión estática: ambos clientes usan exclusivamente POST a la API común, mensajes controlados y HTTPS salvo excepciones locales de desarrollo; web ofrece etiquetas/errores vinculados, foco al resumen, bloqueo de doble envío y anuncios; móvil contiene controles accesibles y manejo de teclado/red. **No certifica accesibilidad**. No se ejecutaron navegador, dispositivo ni emulador, TalkBack/VoiceOver, zoom/reflujo/contraste ni teclado de forma funcional. Flujo web→API→PG y móvil→API→PG pendiente; pruebas funcionales de los tres componentes exigidas por RS-010/RNF-014 no quedan satisfechas con TestClient y dobles fetch.

`git diff --check`: exit0 en revisión integrada, con avisos LF/CRLF. No hubo stage, commit ni push por calidad.

## Bloqueos y continuación

1. Espacio insuficiente en C: impidió instalación reproducible de clientes. Liberar espacio con intervención del propietario; no borrar archivos ajenos. Ejecutar npm ci y todos los comandos obligatorios después.
2. Preparar navegador y Android/iOS o dispositivos autorizados para flujos completos, errores/red, teclado y accesibilidad; registrar dispositivos y evidencias.
3. Verificar HTTPS real de despliegue y acordar condiciones de carga RNF-09 si se requiere aceptación operacional.
4. Repetir calidad sobre la versión final si cambia código/contrato. La huella, si se prepara para revisión, no elimina estos bloqueos.

El Python3 de PATH (MSYS) falla con ModuleNotFoundError: encodings por prefijo D:/a inexistente; py -3 y backend/.venv/Scripts/python sí funcionaron. El coordinador debe resolverlo o registrar invocación equivalente al preparar huella con scripts/entrega.py.

## Verificación estática del cliente web

| Comando | Código de salida | Resultado |
|---|---:|---|
| `npm run lint` | 0 | Aprobado |
| `npm run build` | 0 | Aprobado |

La prueba funcional del formulario de registro contra la API y PostgreSQL sigue pendiente.

## Prueba Funcional del Formulario de Registro contra la API y PostgreSQL

- Registro web válido con datos ficticios: aprobado. `POST /api/v1/ciudadanos` devolvió `201 Created` con PostgreSQL de pruebas en Docker.

- Registro web inválido con el mismo correo electrónico ya registrado: aprobado. `POST /api/v1/ciudadanos` devolvió `201 Created` con PostgreSQL de pruebas en Docker. `POST /api/v1/ciudadanos` devolvió `409 Conflict` y el formulario mostró El correo ya está registrado.

- Registro web inválido con un correo mal formado del tipo @hotmail.com: aprobado. El formulario muestra un error y no se realiza ninguna operación sobre la BD.

- Validación del Cliente Web Aprobada!.


## Prueba Funcional del Formulario de Registro contra la API y PostgreSQL (Móvil)

- Registro móvil válido con datos ficticios: aprobado. `POST /api/v1/ciudadanos` devolvió `201 Created` con PostgreSQL de pruebas en Docker.

- Registro web inválido con el mismo correo electrónico ya registrado: aprobado. `POST /api/v1/ciudadanos` devolvió `201 Created` con PostgreSQL de pruebas en Docker. `POST /api/v1/ciudadanos` devolvió `409 Conflict` y el formulario mostró El correo ya está registrado.

- Registro web inválido con un correo mal formado del tipo @hotmail.com: aprobado. El formulario muestra un error y no se realiza ninguna operación sobre la BD.

Finalicé las validaciones de RF-001 en web y móvil con Expo Go y todos los checks ejecutados pasaron. Revisa la evidencia y el diff completo de entrega/rf-001, incorpora las correcciones manuales y confirma que todos los criterios de aceptación estén cubiertos. Revisa también los pendientes de documento único, la ruta del endpoint y los hallazgos de npm audit. Actualiza la trazabilidad con los resultados reales, prepara los archivos de la entrega y presenta el diff final junto con una nueva huella para mi aceptación.

## Entorno de validación

- Rama: entrega/rf-001.
- API: http://127.0.0.1:8000.
- Endpoint: POST /api/v1/ciudadanos.
- Web: http://localhost:5173 [confirmar puerto utilizado].
- Móvil: dispositivo físico con Expo Go, SDK 57.
- Dispositivo y sistema operativo: - OppoA58,ColorOS, Usando ExpoGo con su SDK57.
- Acceso móvil a la API: http://<IPv4-local-del-PC>:8000.
- PostgreSQL de pruebas en Docker: 127.0.0.1:55432.
- Base de datos: sgip_test.
- Migración: 001_ciudadanos.up.sql.
- Fecha de ejecución: [07/11/2026].

## Resultados

- Registro con correo nuevo: HTTP 201 y confirmación en pantalla.
- Correo duplicado: HTTP 409 y mensaje correspondiente.
- Validaciones de campos: [casos y resultados observados].
- API detenida: [resultado observado].
- Web: lint y build aprobados.
- Móvil: lint, tipos y pruebas del servicio aprobados.

## Condición de desarrollo

La prueba móvil utilizó HTTP en la red local con datos ficticios.
El cliente permite ese acceso únicamente en desarrollo mediante
EXPO_PUBLIC_DEV_API_HOST. En producción exige HTTPS.


- Validación del Cliente Móvil Aprobada!.

## Pruebas manuales del formulario web rediseñado

- Fecha y hora: [07-11-2026, 10:30 pm].
- Rama: entrega/rf-001.
- Navegador y versión: [Google Chrome Versión 156.0.8078.81 (Build oficial) (64 bits)].
- URL web: [http://localhost:5173/].
- API: POST /api/v1/ciudadanos.
- Base de pruebas: sgip_test, PostgreSQL en Docker, puerto local 55432.
- Datos utilizados: ficticios.

| Caso | Resultado observado | Estado |
|---|---|---|
| Doble envío | Al pulsar dos veces Registrar se generó un solo POST. El botón se deshabilitó durante el envío y se mostró la confirmación tras HTTP 201. | Aprobado |
| API detenida | Se mostró un error de conexión comprensible. El formulario conservó los datos esperados y permitió volver a intentar. | Aprobado |
| Reintento tras reiniciar la API | El registro terminó con HTTP 201 y confirmación visible. | Aprobado |

### Evidencia complementaria

- Cantidad de POST durante el doble clic: [1].
- Comprobación en BD de una cuenta y su auditoría: [observado].
- Estado de carga visible durante la solicitud: [observado].
- Capturas o logs depurados: [observacion manual].

Estos resultados corresponden a la versión rediseñada ejecutada durante esta sesión.

## Validación funcional del formulario móvil rediseñado

- Fecha y hora: [07/11/2026, 10:56 Pm].
- Rama: entrega/rf-001.
- Dispositivo: [OppoA58].
- Sistema operativo: [ColorOS].
- Expo Go: Proyecto SDK 57.
- API: POST /api/v1/ciudadanos.
- PostgreSQL de pruebas: sgip_test, puerto local 55432.
- Datos utilizados: ficticios.
- Ejecución y resultados: verificación manual del responsable de pruebas.

| Caso | Resultado observado | Estado |
|---|---|---|
| Registro válido | Un POST, HTTP 201 y confirmación visible. | Aprobado |
| Correo duplicado | HTTP 409 y mensaje comprensible. | Aprobado |
| Validaciones | Campos vacíos, correo inválido y contraseña inválida rechazados con errores visibles. | Aprobado |
| Doble envío | Una solicitud, botón deshabilitado durante la carga y una cuenta creada. | Aprobado |
| Fallo de conexión | Error claro, datos conservados según [U2 vigente](../../docs/qa-rf001-u2.md) y reintento disponible. | Aprobado |
| Recuperación | Tras reiniciar la API, HTTP 201 y confirmación visible. | Aprobado |

## Addendum de conciliación aportado en conversación

En la solicitud de conciliación, el responsable confirma expresamente que las pruebas manuales del **rediseño web y móvil** incluyen registro, duplicado, validaciones, doble envío, fallo de conexión y recuperación. Se vincula esta declaración actual a las secciones anteriores: esas seis categorías quedan aprobadas manualmente para ambos clientes, incluido web409 y validación básica. No se atribuye esa ejecución al agente ni se inventa hora/captura adicional.

La tabla web de22:30 no repetía duplicado/validaciones; el addendum del responsable resuelve esa falta de detalle, sin exigir repetición. Las observaciones previas al rediseño permanecen históricas. La declaración no especifica confirmación distinta, rechazo422/503 presentado, timeout15 s, revisión visual por tamaños, teclado o lector de pantalla: esos casos se enumeran por separado en [la matriz conciliada](paso3-matriz-actual.md), con su fuente y alcance local u operacional.


### L03 — Respuesta 503 en web

- Fecha y hora: [09-11-2026].
- Navegador y versión: [Google Chrome Versión 156.0.8078.81 (Build oficial) (64 bits)].
- Entorno: simulador local en el puerto 58010, sin persistencia.
- Procedimiento: enviar una vez el formulario con datos ficticios válidos.
- HTTP observado: 503.
- Mensaje mostrado: [POST recibido; simulacion=503; demora=0s; sin persistencia].
- Resultado: mensaje de indisponibilidad visible, carga finalizada,
  datos conservados y botón habilitado para reintentar.
  No se mostró confirmación de registro exitoso.
- Estado: APROBADO mediante verificación manual.


### L04 — Timeout en web

- Fecha y hora: [09-11-2026].
- Navegador y versión: [Google Chrome Versión 156.0.8078.81 (Build oficial) (64 bits)].
- Simulación: puerto 58010, respuesta 503 demorada 20 segundos.
- Tiempo observado hasta el aviso: aproximadamente 14–15 segundos.
- Mensaje: “La solicitud tardó demasiado. No pudimos confirmar
  el registro. Comprueba si tu cuenta fue creada antes de reintentar.”
- Carga finalizada, datos previstos conservados y reintento habilitado.
- Estado: APROBADO mediante verificación manual.


### L02 — Respuesta 422 en móvil

- Fecha y hora: [09-11-2026].
- Dispositivo y SO: [OppoA58, ColorOS].
- Entorno: Expo Go SDK 57; simulador en el puerto 58010.
- Procedimiento: enviar una vez el formulario con datos ficticios válidos.
- Respuesta simulada: HTTP 422.
- Mensaje mostrado: “Revisa el nombre, correo y contraseña e intenta de nuevo”.
- Resultado observado: error controlado, datos previstos conservados,
  carga finalizada y botón habilitado para reintentar.
  No se mostró confirmación de registro exitoso.
- Estado: APROBADO mediante verificación manual.

### L03 — Respuesta 503 en móvil

- Fecha y hora: [10-11-2026].
- Dispositivo y SO: [OppoA58, ColorOS].
- Entorno: Expo Go SDK 57; simulador en el puerto 58010.
- Respuesta simulada: HTTP 503, sin demora ni persistencia.
- Mensaje: “El servicio no está disponible. Intenta más tarde”.
- Resultado: carga finalizada, datos previstos conservados,
  reintento habilitado y ninguna confirmación de éxito.
- Estado: APROBADO mediante verificación manual.


### L04 — Timeout en móvil

- Fecha y hora: [10-11-2026].
- Dispositivo y SO: [OppoA58, ColorOS].
- Entorno: Expo Go SDK 57; simulador en el puerto 58010.
- Simulación: respuesta 503 demorada 20 segundos, sin persistencia.
- Tiempo observado hasta el aviso: [segundos medidos].
- Mensaje: “La solicitud tardó demasiado. El registro podría haberse
  completado; si reintentas y el correo ya existe, tu cuenta puede estar creada”.
- Resultado: carga finalizada, datos previstos conservados
  y reintento habilitado.
- Estado: APROBADO mediante verificación manual.

### L05 — Revisión visual del formulario rediseñado

- Fecha y hora: [10-11-2026].
- Referencia: ref/SGIP-Mockups.html, UIW-01 y registro UIM-01.
- Navegador: [Google Chrome Versión 156.0.8078.81 (Build oficial) (64 bits)].
- Dispositivo móvil y SO: [OppoA58, ColorOS].

| Escenario | Resultado observado |
|---|---|
| Web a 1280 px | [Visible] |
| Web a 320 px | [Visible] |
| Web con zoom al 200 % | [Visible] |
| Estados de error, carga y éxito | [Visibles] |
| Móvil en vertical y horizontal | [Visible] |
| Móvil con teclado abierto | [Se conserva el foco] |
| Móvil con texto ampliado | [Visible] |

- Incidencias: [Ninguna].
- Estado: [APROBADO].

### L06 — Accesibilidad web

- Fecha y hora: [fecha y hora].
- Navegador y versión: [datos].
- Lector de pantalla y versión: [datos, o pendiente].

| Verificación | Resultado |
|---|---|
| Tab y Shift+Tab: orden lógico y sin trampas | [Aprobado] |
| Foco visible en todos los controles | [Visible] |
| Mostrar/Ocultar contraseña con teclado | [Visible] |
| Errores asociados y acceso al campo afectado | [Visible] |
| Etiquetas, obligatoriedad y botones anunciados | [Visible] |
| Mensajes de error y éxito anunciados | [Visible] |

- Incidencias: [Ninguno].
- Estado: [Aprobado].

### L07 — Teclado y desplazamiento móvil

- Fecha y hora: [10-11-2026].
- Dispositivo y SO: [OppoA58, ColorOS].
- Entorno: Expo Go SDK 57, API real y PostgreSQL de pruebas.
- Resultado: teclado de correo y acciones Siguiente/Hecho correctos.
  Campos, errores y botón alcanzables con el teclado abierto.
  Mostrar/Ocultar contraseña funciona.
  Tras HTTP 201, el teclado se cerró automáticamente
  y la confirmación quedó visible.
- Estado: APROBADO mediante verificación manual.


### L08 — Lectura accesible móvil con TalkBack

- Fecha y hora: [10-11-2026].
- Dispositivo y Android: [OppoA58, ColorOS].
- TalkBack: [17.1].
- Entorno: Expo Go SDK 57, formulario rediseñado.
- Resultado: etiquetas, campos obligatorios y botones anunciados
  comprensiblemente. Errores y confirmación de éxito anunciados.
  Orden de lectura lógico y controles alcanzables.
- Incidencias: ninguna observada.
- Estado: APROBADO mediante verificación manual.


## Cierre manual L01 y L02 web — 10/11/2026

Fuente: confirmación explícita del responsable en esta conversación. Resultados aportados por el usuario, no ejecutados por el coordinador; no se inventan hora ni capturas.

| Caso | Resultado declarado | Estado |
| --- | --- | --- |
| L01 web y móvil | Las contraseñas distintas muestran un error visible y no generan ningún POST. | Aprobado en ambos clientes |
| L02 web | La respuesta422 se presenta correctamente, conserva los datos previstos, termina la carga y permite reintentar. | Aprobado |

Con L02 móvil y L03–L08 previamente documentados se cierran los obligatorios locales. Metadatos incompletos anteriores se preservan como limitaciones de reproducibilidad. Este cierre funcional no acepta una huella, no remedia hallazgos npm ni acredita despliegue productivo.
