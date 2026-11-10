# U2: errores y timeout de RF-001 con servidor simulado

La utilidad está en `scripts/qa_rf001_respuestas.py`, dentro del worktree. Se retiró durante una limpieza anterior; se reincorpora ahora como herramienta de QA versionada con pruebas. Estas instrucciones reemplazan las referencias antiguas a U2. No hay API real ni BD detrás de esta utilidad: no crea cuentas y no persiste, imprime ni reenvía el cuerpo recibido. Usar datos ficticios.

Todos los comandos siguientes son **PowerShell desde la raíz del worktree rf-001**. El Python funcional es `backend/.venv/Scripts/python.exe`; la utilidad solo requiere biblioteca estándar de Python. Sus pruebas del servicio móvil requieren además el Node24 ya usado en el proyecto.

## 1. Servidor: puerto58010, ruta POST /api/v1/ciudadanos

En una terminal dedicada, elegir **un modo por vez**. Detener el anterior con Ctrl+C antes de iniciar otro:

```powershell
# Respuesta422 inmediata
backend/.venv/Scripts/python.exe scripts/qa_rf001_respuestas.py --status 422

# Respuesta503 inmediata
backend/.venv/Scripts/python.exe scripts/qa_rf001_respuestas.py --status 503

# Respuesta503 tras20s: el cliente debe cancelar por timeout a los15s
backend/.venv/Scripts/python.exe scripts/qa_rf001_respuestas.py --status 503 --delay 20
```

Por defecto escucha solo en `127.0.0.1:58010`; origen web permitido `http://localhost:5173`. Para conectar **web y teléfono simultáneamente**, usar la misma orden elegida añadiendo `--host 0.0.0.0`, en la red privada de pruebas:

```powershell
backend/.venv/Scripts/python.exe scripts/qa_rf001_respuestas.py --host 0.0.0.0 --status 422
# O, tras Ctrl+C:
backend/.venv/Scripts/python.exe scripts/qa_rf001_respuestas.py --host 0.0.0.0 --status 503
# O, tras Ctrl+C:
backend/.venv/Scripts/python.exe scripts/qa_rf001_respuestas.py --host 0.0.0.0 --status 503 --delay 20
```

`0.0.0.0` es la dirección de escucha, **no la URL de los clientes**. Web usa127.0.0.1; teléfono usa la IPv4 LAN del PC. No se necesita tocar API/BD reales ni abrir acceso público. Si la red o firewall impiden acceso LAN, registrar el bloqueo; el arranque local no demuestra conectividad del dispositivo.

Si abres web con otro origen, añadir `--origin http://localhost:5173 --origin http://127.0.0.1:5173` u orígenes explícitos necesarios. OPTIONS de la ruta devuelve204 para origen permitido y403 para ajeno; no se usa CORS comodín.

## 2. Conectar temporalmente web (otra terminal, desde raíz)

Detener cualquier Vite anterior del proyecto. Guardar la variable de esta sesión y arrancar con override temporal:

```powershell
$rf001SavedWebApi = $env:VITE_API_URL
$env:VITE_API_URL = 'http://127.0.0.1:58010'
npm --prefix web run dev -- --host 127.0.0.1 --port 5173 --strictPort
```

Abrir **http://localhost:5173/** para coincidir con el origen CORS predeterminado. La variable de proceso tiene precedencia; no editar `.env.local`. Confirmar en Network que POST apunta a `http://127.0.0.1:58010/api/v1/ciudadanos`, no a8000. Si se cambia la variable, reiniciar Vite.

## 3. Conectar temporalmente móvil físico (otra terminal, desde raíz)

PC y Oppo en la misma red de pruebas; servidor iniciado con `--host 0.0.0.0`. Sustituir `IPV4_LAN_DEL_PC` por la IPv4 real del adaptador usado, sin esquema ni puerto. No usar localhost ni127.0.0.1 en un teléfono físico:

```powershell
$rf001SavedMobileApi = $env:EXPO_PUBLIC_API_URL
$rf001SavedDevHost = $env:EXPO_PUBLIC_DEV_API_HOST
$rf001PcIp = 'IPV4_LAN_DEL_PC'
$env:EXPO_PUBLIC_API_URL = "http://${rf001PcIp}:58010"
$env:EXPO_PUBLIC_DEV_API_HOST = $rf001PcIp
npm --prefix mobile start -- --clear
```

Abrir el bundle actualizado en Expo Go SDK57 y recargar. La excepción HTTP solo funciona en desarrollo con hostname exactamente igual a `EXPO_PUBLIC_DEV_API_HOST`. No modificar el servicio ni debilitar su validación. Para emulador Android, usar `http://10.0.2.2:58010` en la variable API (permitido en desarrollo); en ese caso el puerto debe ser alcanzable desde el emulador.

## 4. Qué comprobar en cada cliente

Rellenar datos localmente válidos: nombre `QA Ficticia`, correo `qa@example.com`, contraseña ficticia `ficticia-segura-001` y confirmación igual. Enviar de nuevo tras cada cambio de modo del servidor.

| Modo | Resultado esperado en pantalla | Qué aportar |
| --- | --- | --- |
| 422 | Mensaje de datos rechazados/revisar campos, sin éxito; datos conservados y reintento habilitado | Cliente,HTTP422,mensaje observado,datos/reintento |
| 503 | Indisponibilidad controlada en español, sin éxito; datos conservados y botón habilitado al terminar | Cliente,HTTP503,mensaje observado,datos/reintento |
| demora20 | Carga y controles deshabilitados; aproximadamente15s después termina la espera con aviso de registro posiblemente completado/incierto; conserva datos y permite reintentar | Cliente,tiempo aproximado,mensaje observado. No esperar un201: la utilidad nunca devuelve201 |

Una línea `POST recibido` corresponde a una petición recibida. Se puede contrastar con Network para doble envío, pero este caso ya fue aprobado manualmente: no se exige repetirlo. Si se cancela por timeout puede no haber código de respuesta en el cliente; el servidor intenta503 al completar20s y tolera la desconexión.

Una prueba del servidor o del servicio con fetch real no acredita por sí sola estos mensajes en la pantalla web/nativa. Los casos L02–L04 de la matriz se cierran cuando el responsable aporte su resultado UI.

## 5. Restaurar las URLs reales al terminar

Primero Ctrl+C en la terminal del servidor simulado. Después Ctrl+C en Vite y Metro. En **la misma terminal donde se guardó cada variable**, restaurar sus valores originales:

Web:

```powershell
if ($null -eq $rf001SavedWebApi) {
    Remove-Item Env:VITE_API_URL -ErrorAction SilentlyContinue
} else {
    $env:VITE_API_URL = $rf001SavedWebApi
}
npm --prefix web run dev -- --host 127.0.0.1 --port 5173 --strictPort
```

Móvil:

```powershell
if ($null -eq $rf001SavedMobileApi) {
    Remove-Item Env:EXPO_PUBLIC_API_URL -ErrorAction SilentlyContinue
} else {
    $env:EXPO_PUBLIC_API_URL = $rf001SavedMobileApi
}
if ($null -eq $rf001SavedDevHost) {
    Remove-Item Env:EXPO_PUBLIC_DEV_API_HOST -ErrorAction SilentlyContinue
} else {
    $env:EXPO_PUBLIC_DEV_API_HOST = $rf001SavedDevHost
}
npm --prefix mobile start -- --clear
```

Recargar navegador y Expo Go. Si los valores originales no estaban definidos en la sesión, vuelven a regir los archivos `.env.local` existentes y los defaults del proyecto; esos archivos no se tocaron. Verificar en Network/log de la API que la petición vuelve a la URL real de pruebas (habitualmente puerto8000), **no58010**. Un registro201 contra API/BD reales puede usarse como control final, con correo ficticio nuevo. Si se cierra la terminal sin guardar valores, las variables temporales desaparecen con esa sesión; abrir otra terminal limpia y arrancar clientes desde la configuración local original.

## 6. Repetir la comprobación automatizada desde raíz

```powershell
backend/.venv/Scripts/python.exe scripts/tests/test_qa_rf001_respuestas.py
```

Prueba CLI en58010,422/503 JSON,CORS204/403,ruta ajena404,demora inválida y servicio móvil real por HTTP con cancelación15s ante respuesta20s. Los servidores de pruebas se detienen automáticamente; no dejar otro proceso en58010 al ejecutar la suite. Resultados reales y límites en [qa-respuestas-evidencia.md](../.trace/evidence/qa-respuestas-evidencia.md).
