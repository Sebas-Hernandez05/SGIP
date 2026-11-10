# RF-001: revisión actual de dependencias

Ámbito: diagnóstico, sin cambiar package.json, lockfiles ni paquetes instalados. No se ejecutó audit fix ni actualización forzada. Fuente: árbol npm instalado, lockfiles y auditoría del registro oficial consultada en esta sesión.

## Comandos y códigos

| Comando | Web | Móvil |
| --- | --- | --- |
| npm ls --all --json | 0 | 0 |
| npm audit --json | 1 (2 altas) | 1 (25:1 crítica,7 altas,16 moderadas,1 baja) |
| npm audit --omit=dev --json | 0 (0 hallazgos) | 1 (18:1 crítica,7 altas,9 moderadas,1 baja) |

El intento audit dentro del sandbox falló por acceso a registro; se repitió fuera con autorización y los códigos anteriores corresponden a resultados válidos, no al fallo de red. Los árboles npm completos se retiraron como diagnóstico temporal; se conserva resumen y los cuatro JSON audit de esta sesión. npm ls0 acredita coherencia del árbol, no seguridad.

## Paquetes afectados y clasificación real

`Árbol producción` significa alcanzable por dependencias npm no marcadas dev; no demuestra que el código vulnerable entre al bundle nativo ni que el formulario lo invoque. `Solo dev` tampoco elimina el riesgo de la máquina/servidor de desarrollo.

| Área | Paquete | Versión instalada | Severidad npm | Clasificación --omit=dev |
| --- | --- | --- | --- | --- |
| web | source-map-js | 1.2.1 | high | Solo dev |
| web | vite | 8.3.0 | high | Solo dev |
| mobile | @expo/cli | 57.0.26 | high | Árbol producción |
| mobile | @expo/config | 57.0.9 | moderate | Árbol producción |
| mobile | @expo/config-plugins | 57.0.9 | moderate | Árbol producción |
| mobile | @expo/fingerprint | 0.20.13 | moderate | Árbol producción |
| mobile | @expo/metro-config | 57.0.12 | moderate | Árbol producción |
| mobile | @typescript-eslint/eslint-plugin | 8.72.1 | moderate | Solo dev |
| mobile | @typescript-eslint/parser | 8.72.1 | moderate | Solo dev |
| mobile | @typescript-eslint/type-utils | 8.72.1 | moderate | Solo dev |
| mobile | @typescript-eslint/typescript-estree | 8.72.1 | moderate | Solo dev |
| mobile | @typescript-eslint/utils | 8.72.1 | moderate | Solo dev |
| mobile | decode-uri-component | 0.2.2 | high | Árbol producción |
| mobile | deepmerge | 4.3.1 | low | Árbol producción |
| mobile | eslint-config-expo | 57.0.2 | moderate | Solo dev |
| mobile | eslint-plugin-expo | 1.2.1 | moderate | Solo dev |
| mobile | expo | 57.0.24 | moderate | Árbol producción |
| mobile | expo-router | 57.0.22 | high | Árbol producción |
| mobile | glob | 13.0.6 | moderate | Árbol producción |
| mobile | minimatch | 10.2.6 | moderate | Árbol producción |
| mobile | node-forge | 1.4.0 | high | Árbol producción |
| mobile | query-string | 7.1.3 | high | Árbol producción |
| mobile | shell-quote | 1.10.0 | critical | Árbol producción |
| mobile | source-map-js | 1.2.1 | high | Árbol producción |
| mobile | uuid | 7.0.3 | moderate | Árbol producción |
| mobile | xcode | 3.0.1 | moderate | Árbol producción |
| mobile | zod | 3.25.76 | high | Árbol producción |

## Aplicabilidad y opciones de corrección

- Web: Vite8.3.0 es devDependency; source-map-js1.2.1 llega por Vite→PostCSS. No hay hallazgos en el árbol web omit=dev; eso no es un análisis del bundle ni certifica ausencia total de vulnerabilidades. Riesgo de Vite aplica a herramientas/servidor de desarrollo; no se debe tratar como backend FastAPI expuesto ni como ruta de registro probadamente explotable.
- Móvil: shell-quote1.10.0 llega por React Native→react-devtools-core. query-string7.1.3/decode-uri-component0.2.2, node-forge1.4.0 y cadenas Expo/Router siguen en el árbol omit=dev. Expo agrupa herramientas con dependencias de producción: no es válido declarar que los18 se ejecutan en el dispositivo, ni descartarlos todos como dev. No se demostró una ruta de explotación desde nombre/correo/contraseña; queda pendiente analizar bundle/enlaces/herramientas por hallazgo.
- Lectura de código propio: web usa fetch; móvil registerCitizen/fetch y Expo Router. No hay importación directa de shell-quote, query-string, node-forge o zod en src. La ausencia de import directo no descarta alcance transitivo.
- Candidatos verificables: source-map-js>=1.2.2; Vite8.3.3 cubre el advisory de launch-editor consultado; shell-quote>=1.11.0 corrige el advisory crítico. Deben contrastarse todos los advisories del JSON y repetirse audit/checks tras cualquier cambio; no se afirma que una actualización aislada elimine todos los hallazgos.
- Opción A recomendada para remediación: trabajo de actualización dirigido compatible con SDK57 y rangos actuales, revisar diff del lockfile, npm ci, audit completo/omit=dev, lint/tipos/build/servicio y regresión afectada. Es corrección de dependencias, no una revisión ya realizada.
- Opción B: aceptar temporalmente solo el riesgo local de desarrollo con responsable/justificación/plazo/controles concretos, sin autorizar exposición pública. No se presume esa decisión del usuario.
- Opción C: actualización mayor de Expo/Router solo como cambio de alcance explícito y batería móvil completa. No aplicar automáticamente recomendaciones npm que propongan downgrade Expo52 o migración58.

## Fuentes primarias consultadas

- [source-map-js, rango y versión corregida](https://github.com/advisories/GHSA-68fv-2mgg-jv7q).
- [launch-editor/Vite, versiones afectadas y parche](https://github.com/advisories/GHSA-587h-7wmj-h5pm).
- [shell-quote, inyección en quote y parche1.11.0](https://github.com/advisories/GHSA-pqg4-j6r4-53mv).

Los recuentos son paquetes afectados y propagación de dependencias, no necesariamente vulnerabilidades independientes. No hay en el contrato RF-001 ni en AGENTS.md un umbral audit=0 acordado. Se completó la revisión disponible; remediación/disposición sigue abierta y debe ser explícita para una publicación operacional. No se convierte ese umbral inexistente en un bloqueo automático de aceptación local.
