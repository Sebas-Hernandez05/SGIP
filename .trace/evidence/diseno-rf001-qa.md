# RF-001 — revisión QA del rediseño

Fecha: 2026-11-07. Entorno: Windows/PowerShell, worktree `rf-001`, rama `entrega/rf-001`. Referencia visual local: `ref/SGIP-Mockups.html`, UIW-01 y registro de UIM-01. Contrato: `docs/contrato-rf-001.md`.

## Resultados de esta revisión

| Comando | Salida | Evidencia / límite |
| --- | --- | --- |
| `npm ci` en web | 0 | Reportado por frontend_web sobre el rediseño final |
| `npm run lint` en web | 0 | Reportado por frontend_web |
| `npx tsc -b` en web | 0 | Reportado por frontend_web |
| `npm run build` en web | 0 | Vite 8.3.0; 17 módulos; 715 ms, reportado por frontend_web |
| `node --test mobile/tests/registration.test.mjs` | 0 | QA: 4 pruebas aprobadas, 0 fallidas; 2104.7889 ms; aviso MODULE_TYPELESS_PACKAGE_JSON. Fetch sustituido: no verifica interfaz ni E2E |
| `backend/.venv/Scripts/python -m pytest backend/tests -q -s -p no:cacheprovider` | 0 | QA con PYTHONPATH=backend y TEST_DATABASE_URL ausente: 15 aprobadas, 4 saltadas, 1 aviso, 21.42 s. Los saltos corresponden a PostgreSQL; no se conectó a BD ajena |
| `git diff --check` | 0 | QA; avisos de conversión LF/CRLF, sin errores de whitespace |

## Revisión estática integrada

- Web conserva URL, payload exclusivo `{nombre,correo,contrasena}`, normalización, límites, confirmación local, bloqueo de doble envío, timeout y mensajes 409/422/503/red. Conserva etiquetas, vínculos de errores y foco en resumen/éxito. Mostrar contraseña usa `type="button"`, `aria-controls`, estado accesible y se desactiva durante envío; la visibilidad vuelve a oculta al éxito.
- Móvil conserva servicio API, payload, validación, guard de envío y anuncios accesibles. El diseño usa componentes React Native, correo con teclado email, next/done, desplazamiento y KeyboardAvoidingView (padding iOS/height Android). Mostrar contraseña se desactiva durante envío y se reinicia al éxito. Estas comprobaciones son lectura de código y no acreditan funcionamiento del teclado en un dispositivo.
- Paleta bosque/verde/lima, tipografía de sistema, tamaños, espaciados, controles y estados se alinean con el HTML mediante revisión del código. No se incorporan marco de teléfono, selector del estudio ni navegación simulada.
- Sin hallazgos bloqueantes en la regresión estática. No hay suite UI web/nativa configurada; las pruebas del servicio y del backend no sustituyen pruebas funcionales de las pantallas.

## Alcance y pendientes

El mockup propone Nombres/Apellidos separados, teléfono opcional, mínimo de contraseña 8 y acceso a ingreso. Se conserva nombre único, sin teléfono, mínimo 12 y sin implementar RF-002. Documento único y alternativa de endpoint siguen siendo discrepancias funcionales previas, sin resolución inferida por el rediseño.

La inspección visual actual quedó pendiente: el coordinador intentó CUA; el inventario de navegadores devolvió `browser access host unavailable`, y la captura de Chrome nativo se detuvo porque no pudo determinar la URL con confianza. No se verificaron Android/iOS, teclado real, TalkBack/VoiceOver ni flujos actuales contra API/PostgreSQL. Las pruebas previas aportadas por el usuario en qa-rf001.md corresponden a la interfaz anterior y no se cuentan como evidencia del rediseño.

La aceptación funcional completa permanece bloqueada por esas verificaciones pendientes conforme a AGENTS.md; una huella identifica contenido para revisión y no elimina los pendientes.
