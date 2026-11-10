# RF-001 — revisión independiente actual del diseño

> Actualización del paso 3: [matriz vigente](paso3-matriz-actual.md) y [revisión de calidad](paso3-revision-calidad.md). Las cuatro pruebas PostgreSQL omitidas en esta ejecución se completaron posteriormente: 19/19 actuales, además de HTTP real y recuperación lógica. UI/dispositivo/TLS siguen pendientes según la matriz.

Fecha: 2026-11-07. Agente: calidad. Entorno: Windows/PowerShell, worktree `rf-001`. Referencia: `ref/SGIP-Mockups.html`, UIW-01 y registro de UIM-01; contrato: `docs/contrato-rf-001.md`. Se inspeccionaron el inventario de cambios contra HEAD, implementación backend, contrato, formularios, estilos, servicio y pruebas. Los cambios locales anteriores se conservaron.

## Comandos ejecutados por calidad

| Comando | Código | Resultado y límite |
| --- | --- | --- |
| `$env:PYTHONPATH='backend'; Remove-Item Env:TEST_DATABASE_URL -ErrorAction SilentlyContinue; backend/.venv/Scripts/python.exe -m pytest backend/tests -q -s -p no:cacheprovider` | 0 | 15 aprobadas, 4 saltadas, 1 aviso de deprecación de Starlette/AnyIO; 7.77 s. Sin BD externa: los cuatro casos PostgreSQL permanecen sin revalidación en esta ejecución. |
| `node --test tests/registration.test.mjs` desde mobile | 0 | 4 aprobadas, 0 fallidas; 893.1921 ms. Aviso MODULE_TYPELESS_PACKAGE_JSON. Fetch sustituido, no prueba UI ni integración real. |
| `npm run lint; npx --no-install tsc -b; npm run build` desde web | 0 | Secuencia finalizó correctamente; build TypeScript/Vite 8.3.0, 17 módulos, 2.21 s. Los códigos individuales también los registra frontend_web. |
| `git diff --check` | 0 | Sin errores de whitespace; avisos de conversión LF/CRLF. |
| `npm ci --no-audit --no-fund` desde mobile | 0 | Reportado por frontend_movil y documentado en mobile/RF001.md: 839 paquetes; avisos deprecados uuid/eslint. |
| `npm run lint` desde mobile | 0 | Reportado por frontend_movil: Expo lint sin diagnósticos. |
| `npx --no-install tsc --noEmit` desde mobile | 0 | Reportado por frontend_movil: sin errores de tipos. |

## Revisión estática

- Web conserva exclusivamente `{nombre,correo,contrasena}` y POST `/api/v1/ciudadanos`, normalización de nombre/correo, contraseña sin recortar, límites 2–120/254/12–128, confirmación local, bloqueo inmediato de doble envío, timeout y errores controlados. Mantiene etiquetas, errores vinculados, resumen enfocable, estado de carga y foco en éxito. Mostrar/Ocultar no envía formulario y queda deshabilitado por el fieldset durante carga.
- Móvil conserva `registerCitizen`, payload y validaciones. Usa TextInput, Pressable, ScrollView y KeyboardAvoidingView nativos, teclado email, Siguiente/Hecho, foco del primer error, anuncios accesibles y controles deshabilitados durante carga. El teclado se descarta al éxito. No hay almacenamiento de contraseñas ni inicio automático de sesión.
- Paleta bosque #173d35, verde #17634e, lima #d8ec91; bordes, tipografía de sistema, espaciados, campos y estados textuales toman el HTML como referencia. Esta comparación de código no acredita fidelidad visual en pantalla ni funcionamiento del teclado.
- No se incorporan selector, marco de teléfono ni navegación simulada del atlas. Nombres/Apellidos separados y teléfono opcional no se añaden al contrato; se mantiene Nombre completo. Se mantiene mínimo 12 frente a 8 del mockup. Ingreso pertenece a RF-002; confirmación solo cliente y Mostrar/Ocultar son acciones locales.

## Pendientes y no aplicables

Frontend_movil finalizó instalación, lint y tipos correctamente; sus resultados finales se cotejaron con mobile/RF001.md. Calidad volvió a calcular el SHA256 del formulario móvil final: coincide con el archivo revisado que figura abajo. El agente también repitió servicio: 4/4, exit 0, 1716.9 ms.

Pendientes de ejecución observada: inspección visual final, Android/iOS con teclado, TalkBack/VoiceOver, flujos finales de ambos clientes contra API/PostgreSQL y TLS desplegado. Calidad no ejecutó navegador ni dispositivo y no convierte la revisión estática en aprobación visual. Las verificaciones históricas se conservan en sus informes originales, sin atribuirlas a esta pantalla final.

Intento visual actual comunicado por raíz: el host del navegador no estuvo disponible y `getApp` de Chrome terminó con `Computer Use app approval timed out`. No hubo inspección visual en esta revisión ni se atribuye conformidad visual a esos intentos.

Cámara, ubicación y navegación de reportes no aplican al registro RF-001. No se añadieron pruebas que solo repitan valores CSS. No existe suite UI web/nativa configurada. Las pruebas de servicio y ASGI no sustituyen los flujos funcionales requeridos. La aceptación completa sigue condicionada a las verificaciones obligatorias pendientes y las discrepancias históricas del contrato.

Archivos de interfaz revisados (SHA256 del archivo local, no huella de aceptación):

| Archivo | SHA256 |
| --- | --- |
| web/src/App.tsx | 8074419df463f01da356eb2a0514d60c1acf704476ca4d0224ae5a0070024fb8 |
| web/src/App.css | e4a594da95e4cc0162d2b90f72565f29494601e95e50f07909049bf4d6f18131 |
| web/src/index.css | c948fb93067c2ab5e0fe03dd39e197d500734026a5f3a944ab85aea11a197c6a |
| mobile/src/app/index.tsx | 89e4fd958367fcce64dd56db8f8282b3bea38ebc06d9927f8ea2702ac248a1fb |
| mobile/src/services/registration.ts | 3c3e5af2adaf70422ac0ac44a9b871269f2dd72d9ec79db9524897705b3768c0 |
