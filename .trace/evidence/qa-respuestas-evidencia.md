# RF-001: U2 reparado y comprobación de respuestas simuladas

La utilidad no estaba en el worktree: se retiró durante la limpieza anterior. La referencia histórica «según U2» quedó sin un procedimiento ejecutable. No se localizó una copia de esa utilidad en scripts ni en el archivo temporal consultado; sí existía un antiguo comprobador en TEMP, que no sustituye a la utilidad. Se reincorporó **scripts/qa_rf001_respuestas.py** como herramienta QA versionada y se añadió **docs/qa-rf001-u2.md** como procedimiento vigente.

Entorno: Windows/PowerShell, worktree rf-001, Python del entorno backend y Node24 del proyecto. No se cambió lógica de la aplicación, configuración local ni URL de clientes. No se conecta a BD, no se crean cuentas y no se registra el cuerpo. Puerto por defecto58010; ruta POST /api/v1/ciudadanos; origen CORS por defecto http://localhost:5173. Servidor normal loopback, modo LAN opcional explícito. [Instrucciones U2](../../docs/qa-rf001-u2.md).

## Ejecución final observada

Desde raíz:

```powershell
backend/.venv/Scripts/python.exe scripts/tests/test_qa_rf001_respuestas.py
node --test mobile/tests/registration.test.mjs
git diff --check
```

| Verificación | Resultado real |
| --- | --- |
| Suite de la utilidad y servicio HTTP | Exit0;5 pruebas aprobadas;20.021s. Salida qa-respuestas-verificacion.txt. |
| CLI real en puerto58010 | Arranque del script con --status422, línea de escucha127.0.0.1:58010 y POST422 comprobados; proceso detenido por la prueba. |
| HTTP422/503 inmediatos | JSON detail, Content-Type/CORS y Cache-Control:no-store comprobados; sin eco de contraseña ficticia en respuesta. |
| CORS/ruta | OPTIONS204 al origen autorizado,403 sin permiso CORS al ajeno; ruta distinta404. |
| Demora inválida | Se rechazan valores negativos/no finitos al crear servidor. |
| Servicio móvil sin fetch sustituido | Importación del servicio real en Node; POST por HTTP a servidores loopback de puertos efímeros de la suite.422 produjo error de revisión de campos (0.108s);503 indisponibilidad (0.073s). |
| Timeout real del servicio móvil | Servidor configurado503/demora20s; fetch real canceló a15.010s y el servicio emitió aviso de registro posiblemente completado, antes de recibir la respuesta demorada. No se cambió el timeout15s de la aplicación. |
| Regresión servicio móvil existente | Exit0;4/4;1177.6978ms; aviso MODULE_TYPELESS_PACKAGE_JSON sin fallo. Estos cuatro casos usan fetch sustituido, distintos de la nueva prueba HTTP. |
| Whitespace | git diff --check exit0; avisos LF/CRLF. |

El primer intento del nuevo comprobador falló en tres casos por usar HTTPConnection como context manager. Se corrigió el **comprobador** usando contextlib.closing; la ejecución final completa de5 pruebas aprobó. No se convierte aquel fallo del harness en fallo de las pantallas ni se oculta su corrección.

Los servidores lanzados por la suite se cerraron; no se dejó la utilidad escuchando. Los overrides de web/Expo y su restauración están documentados, **no fueron ejecutados en navegador/dispositivo por el agente**. No se acreditan todavía L02–L04 en UI ni prueba LAN física. Para cerrarlos, el responsable sigue U2 y comunica HTTP/tiempo/mensaje/conservación/reintento por cliente. La revisión estática de calidad no detectó defectos bloqueantes en utilidad/documentación y no se atribuye a calidad una ejecución de tests.
