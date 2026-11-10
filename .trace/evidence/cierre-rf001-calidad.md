# RF-001 — revisión de cierre de calidad

Fecha: 2026-11-07, sesión de cierre posterior a la evidencia manual de las 22:56. Entorno: Windows/PowerShell, worktree rf-001, rama entrega/rf-001. Se releen AGENTS.md ancestro y la guía de orquestación. Edición de calidad limitada a este informe; sin stage, commit ni cambios de aplicación.

## Revisión del contenido

Se revisaron inventario y diff contra HEAD, los nuevos archivos de evidencia y las nuevas modificaciones sin preparar de qa-rf001.md y backend/app/repositories/citizens.py, junto con formularios, estilos, servicio, configuración, contrato, migraciones y pruebas. El lockfile generado se examinó estructuralmente: las URLs resueltas pertenecen a registry.npmjs.org. Los hallazgos npm actuales permanecen en sus JSON; no se atribuye resolución de vulnerabilidades.

Un barrido de patrones de secretos recorrió los 51 archivos modificados/nuevos presentes al inicio de esta revisión. Las únicas coincidencias fueron el ejemplo de conexión con usuario/clave de backend/README.md y la URL ficticia con credenciales que prueba el rechazo de configuración en mobile/tests/registration.test.mjs. No se identificaron secretos reales. La IP de mobile/.env.example es una dirección de API pública de configuración, sin credenciales; no se presume alcanzable. Este barrido y la lectura de código no son una certificación exhaustiva de seguridad operacional.

El nuevo alias `except psycopg.Error as error` no se utiliza; es una observación menor de limpieza, sin cambio de comportamiento. Se conserva la excepción pública controlada con `from None`. No se detectó una regresión funcional nueva en la revisión estática. La raíz revisa y prueba el backend final por separado; este informe no atribuye a los clientes las pruebas del backend.

## Verificaciones de clientes ejecutadas de nuevo

| Comando y directorio | Código | Resultado |
| --- | --- | --- |
| web: `npm run lint` | 0 | Sin diagnósticos |
| web: `npx --no-install tsc -b` | 0 | Sin errores |
| web: `npm run build` | 0 | TypeScript y Vite 8.3.0; 17 módulos, 1.62 s |
| móvil: `npm run lint` | 0 | Expo lint sin diagnósticos |
| móvil: `npx --no-install tsc --noEmit` | 0 | Sin errores |
| móvil: `node --test tests/registration.test.mjs` | 0 | 4 aprobadas, 0 fallidas, 249.2008 ms; aviso MODULE_TYPELESS_PACKAGE_JSON; fetch sustituido |
| `git diff --check` | 0 | Sin errores de whitespace; avisos LF/CRLF |

No se reinstalaron dependencias porque los lockfiles no cambiaron desde la instalación aprobada y los ejecutables estaban presentes. Los códigos individuales se capturaron explícitamente para los seis comandos de clientes; las pruebas del servicio no equivalen a pruebas de interfaz.

## Cobertura de la nueva evidencia manual

Se reconoce como evidencia aportada por el responsable, no como ejecución observada directamente por calidad:

- Web rediseñada, Chrome 156.0.8078.81, http://localhost:5173/, PostgreSQL de pruebas Docker sgip_test: un POST ante doble clic, carga/botón deshabilitado, confirmación 201, una cuenta/auditoría, error al detener API, conservación de datos y reintento 201. Fecha declarada 07-11-2026 22:30. Esta sección no repite 409 ni validaciones de la pantalla final; las pruebas web anteriores siguen siendo históricas.
- Móvil rediseñado, Oppo A58/ColorOS/Expo Go SDK57, misma API y BD de pruebas: 201, 409, campos vacíos/correo inválido/contraseña inválida, doble envío con una petición/cuenta, fallo de conexión con conservación y reintento tras reiniciar API. Fecha declarada 07-11-2026 22:56. No se infieren límites concretos de contraseña/nombre, confirmación distinta, comprobación de auditoría móvil ni ausencia de sesión automáticamente a partir de esos resúmenes.

Estas pruebas permiten cerrar los casos concretamente descritos de carga, doble envío y red/reintento en ambos clientes, y los casos 201/409/inválidos descritos en móvil. No corresponde mantener esos casos como completamente no ejecutados en la matriz; tampoco corresponde cerrar la totalidad de P01–P03 con esa evidencia parcial.

## Cobertura pendiente

Continúan sin evidencia final explícita: 422/503 presentados por las pantallas y timeout con aviso de resultado incierto; casos de validación y confirmación/límites no detallados; 409 y validaciones locales web sobre el rediseño; fidelidad visual con tamaños/estados, reflujo/zoom y texto ampliado; teclado/foco/scroll nativo y web; TalkBack/VoiceOver; HTTPS/proxy/logs desplegados. Se mantienen las decisiones pendientes de documento único/endpoint y la disposición de los hallazgos de dependencias. El rendimiento local y la integración backend no sustituyen esos criterios.

No aplican al registro cámara, ubicación, Storage, IA, navegación de reportes, login/propiedad de recursos ajenos, operaciones complejas y migración desde un esquema previo inexistente. La falta de dispositivo o entorno no convierte una prueba en no aplicable. Las verificaciones obligatorias pendientes siguen bloqueando la aceptación completa según AGENTS.md paso 3; preparar una huella solo identifica contenido.
