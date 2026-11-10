# RF-001 — revisión independiente del paso 3

Fecha: 2026-11-07. Responsable: calidad. Revisión de código y evidencia producida por raíz; calidad no repitió las ejecuciones PostgreSQL ni auditorías npm y no realizó una inspección visual. Se leyeron `scripts/verificar_rf001_local.py`, `scripts/qa_rf001_respuestas.py` y los cinco archivos `paso3-*` de resultados y auditoría. No se modificaron código funcional, dependencias, índice Git ni contratos.

## Evidencia actual revisada

| Criterio | Evidencia | Resultado y límite |
| --- | --- | --- |
| Suite backend con PostgreSQL real | `paso3-backend-actual.txt` | 19 aprobadas, 1 aviso Starlette/AnyIO, 5.31 s. Raíz informa exit 0, PostgreSQL 16 nativo temporal en 127.0.0.1:55439, aislado del Docker detenido. Sustituye los cuatro saltos de la última ejecución sin BD para esta verificación actual. |
| RNF-09 local | Mismo archivo | Registro ASGI/hash/PG 0.2627 s, concurrencia 1, menor que 2 s. No acredita carga de producción. |
| Transporte HTTP real y persistencia | `paso3-http-recuperacion-actual.txt` y script | HTTP 201, 409, 422 por rol inyectado y correo inválido, preflight CORS; se comprueba auditoría del ciudadano y hash persistido. Registro 0.1913 s, concurrencia 1. Raíz informa exit 0. Es integración HTTP/API/BD, sin formulario web ni aplicación móvil. |
| Backup y recuperación | Mismo archivo y script | pg_dump formato custom y pg_restore a segunda BD temporal; comparación de cuenta, correo, hash y relación de auditoría. Exit 0 según ejecución de raíz. Complementa rollback transaccional y up/down de la suite; no es un ensayo de recuperación de infraestructura de producción. |
| Limpieza | Mismo archivo | API temporal detenida, migración revertida y BD de restauración retirada. Raíz informa además pg_ctl stop exit 0. |
| Utilidad para pruebas manuales 422/503/carga | `paso3-servidor-estados.txt` y script | Casos status 422, status 503 y status 503 con demora de 1 s informan OK; raíz informa exit 0. La utilidad no persiste ni conecta a PostgreSQL; no implica que las pantallas hayan sido probadas con ella. |
| Auditoría web | `paso3-audit-web.json` | 2 paquetes afectados con severidad alta: source-map-js y vite. Raíz informa npm audit exit 1. |
| Auditoría móvil | `paso3-audit-mobile.json` | 25 paquetes afectados: 1 crítico, 7 altos, 16 moderados y 1 bajo. Raíz informa npm audit exit 1. Los recuentos incluyen propagación por dependencias y no equivalen necesariamente a 25 vulnerabilidades independientes. |

El script de integración fija host/puertos y usuario de QA, exige ausencia de `ciudadanos` antes de migrar y crea una BD separada de restauración. Su uso se limita al clúster desechable preparado expresamente para RF-001: no utilizar en bases compartidas. El servidor de estados es una herramienta manual, con CORS para `http://localhost:5173`; cambiar el puerto/origen del cliente exige ajustar el entorno de prueba. Los scripts no constituyen pruebas automatizadas de interfaz.

## Estado de aceptación y pendientes

La nueva evidencia cubre actualmente PostgreSQL, migración/reversión, rollback, auditoría, concurrencia, transporte HTTP y recuperación lógica. Los resultados históricos permanecen históricos: ni las validaciones del usuario sobre la pantalla anterior ni una comparación estática del rediseño validan la pantalla final.

Siguen pendientes: inspección visual UIW-01/UIM-01; flujos de ambos clientes finales hacia API/PG (éxito, error, carga, red, timeout y doble envío); teclado/dispositivo y lectores de pantalla; HTTPS/proxy desplegado; condiciones operacionales de carga si se pretende esa aceptación; decisiones de documento único y endpoint alternativo. Las diferencias del mockup siguen registradas, sin ampliar contrato. Lint, tipos y build aprobados no se repitieron porque no hubo cambios funcionales posteriores que lo justificaran.

Las auditorías npm son hallazgos actuales sin remediación aplicada. Se requiere revisar alcance y rutas de explotación y acordar corrección/aceptación de riesgo; no ejecutar arreglos forzados de dependencias como parte de un rediseño sin verificar compatibilidad. El recuento por sí solo no prueba explotación del registro, y tampoco permite declarar resueltos los hallazgos.

No aplican al registro: cámara, ubicación, Storage, IA, navegación de reportes, login/propiedad de recursos ajenos, operaciones complejas RNF-09 y migración desde versión anterior inexistente. La aceptación completa continúa bloqueada por las verificaciones obligatorias pendientes conforme al paso 3 de AGENTS.md. La huella identifica contenido preparado y no sustituye esta aceptación.
