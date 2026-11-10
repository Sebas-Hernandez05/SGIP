# RF-001 — conciliación independiente de calidad

Fecha: sesión de conciliación posterior al cierre del 2026-11-07. Fuentes leídas: `docs/contrato-rf-001.md`, actas de `qa-rf001.md`, `cierre-rf001-integracion.md`, `cierre-rf001-calidad.md` y declaración actual explícita del usuario transmitida al agente calidad por raíz. Solo se modifica este informe; no se ejecutan cambios de aplicación ni se repiten checks ya aprobados.

## Addendum manual reconocido

El usuario declara ahora expresamente que las pruebas del **rediseño web y móvil** incluyeron registro 201, duplicados, validaciones, doble envío, fallo de red y recuperación. Esta declaración es un addendum de la evidencia manual del responsable, complementario a las tablas de las 22:30 y 22:56. No es una ejecución observada por calidad.

En consecuencia se reconocen esos seis grupos de casos como aprobados manualmente en ambos clientes sobre el rediseño. Web 409 y validaciones básicas dejan de figurar como no ejecutados por el mero hecho de no aparecer repetidos en la tabla de las 22:30. Las frases anteriores de los informes de cierre que los mantienen pendientes quedan superadas por este addendum. No se solicita repetir los casos ya declarados.

El entorno declarado es Chrome 156.0.8078.81 en http://localhost:5173/ y Oppo A58/ColorOS/Expo Go SDK57, con API `/api/v1/ciudadanos` y PostgreSQL de pruebas sgip_test. La evidencia previa describe carga visible y controles deshabilitados, una petición ante doble envío, conservación de datos ante fallo y reintento exitoso. No es necesario adjuntar capturas para reconocer una declaración manual explícita del responsable; se conserva su procedencia y sus límites.

Esta declaración no detalla cada valor límite, cada código HTTP de error ni cada plataforma. No se inventan resultados particulares de 422, 503, espera de 15 s, confirmación distinta, ausencia de sesión, lector de pantalla o teclado. La ausencia de ese detalle tampoco convierte automáticamente esos casos adicionales en nuevos bloqueos: primero debe vincularse cada exigencia a una fuente y al alcance de aceptación acordado.

## Criterios locales y alcance operacional

| Tema | Fuente y cobertura reconocida | Tratamiento correcto |
| --- | --- | --- |
| Registro e integración local | Contrato RF-001; suite actual 19/19 con PostgreSQL, HTTP real y recuperación lógica; addendum manual de ambos clientes | Cubierto en los casos declarados y ejecutados. No mantener como falta total de E2E local. |
| Éxito/error/carga/red/doble envío | Contrato, sección Verificación requerida; actas y declaración actual | Aprobados manualmente para ambos clientes en los grupos descritos. Los detalles 422/503/timeout no se atribuyen al acta; servicios/API tienen evidencia automatizada separada. |
| Validaciones y privilegios | Contrato y suite backend; validaciones básicas declaradas en ambas pantallas | Cubierto en esa extensión. La matriz puede conservar el detalle no observado como límite de cobertura, sin exigir repetir básicos ni inventar pruebas fallidas. |
| Accesibilidad de formularios | Contrato la exige; mockup aporta etiquetas/teclado/lectores como criterios de diseño | La revisión estática confirma implementación, pero el usuario no declaró expresamente una prueba de accesibilidad. Registrar el alcance de verificación funcional que falta. No afirmar certificación WCAG formal ni exigir una auditoría integral sin acuerdo. |
| Diseño visual y teclado nativo | Solicitud del usuario: identidad HTML, adaptación nativa/teclado y verificación visual cuando haya navegador o dispositivo | Implementación estática revisada; uso funcional manual acreditado. Una comparación visual detallada y pruebas concretas de teclado no se deducen del registro exitoso. Mantener ese límite y los intentos de acceso fallidos, sin atribuir una inspección visual realizada por calidad. |
| iOS/VoiceOver | No se ha establecido una aceptación explícita para iOS en la tarea de registro probada en Oppo | No declarar iOS probado; tampoco añadirlo como bloqueo obligatorio por defecto. Cualquier aceptación iOS requiere su alcance acordado. TalkBack/lector se trata dentro de accesibilidad local, sin elevarlo a certificación formal. |
| RNF-09 | Contrato: <=2 s, entorno/concurrencia declarados; no presume carga productiva | Medición local aprobada (concurrencia 1). No exigir concurrencia, percentil o carga productiva no acordados para aceptar ese alcance local. |
| HTTPS/proxy/logs de despliegue | Contrato exige HTTPS para producción y permite desarrollo local; configuración ASGI probada | La aceptación operacional o publicación productiva requiere su verificación. Ausencia de staging no invalida por sí sola las pruebas locales con HTTP autorizado de desarrollo. No presentar despliegue como entregado. |
| Dependencias npm | JSON actuales con hallazgos; guía contempla seguridad | Revisar aplicabilidad y disposición; no se acordó un umbral de audit igual a cero. Un exit 1 de audit no prueba explotación ni establece por sí mismo un nuevo criterio de rechazo. No atribuir remediación ni aceptación de riesgo implícita. Raíz concilia este punto. |
| Documento único/endpoint y diferencias mockup | Discrepancias de requisitos registradas | Decisión de alcance separada de los resultados de prueba. No ampliar API por inferencia. No confundir decisión contractual con fallo funcional de los casos actuales. |

La regla del paso 3 de AGENTS.md continúa aplicando a las verificaciones **obligatorias del alcance acordado** pendientes o fallidas. Esa regla no crea por sí sola requisitos de certificación WCAG, iOS, auditoría npm sin hallazgos ni carga/despliegue productivos. Los informes anteriores deben leerse con esta precisión y el nuevo addendum; no se justifica rechazar los casos manuales ya declarados por falta de repetición en una tabla anterior.

No se encontró una nueva regresión de código en esta conciliación documental. No se repitieron lint/tipos/build/servicio porque no cambió la aplicación desde los checks finales aprobados. El presente informe no es aprobación de huella, commit ni publicación.

## Validación final de la matriz y las dependencias

Calidad releyó la matriz conciliada con fuentes R1–R7 y evidencias E0–E8, el addendum incorporado en qa-rf001.md, la integración final conciliada y dependencias-revision.md. La matriz reconoce correctamente las seis categorías manuales de ambos clientes y deja de tratar web409/validaciones básicas como no ejecutadas. Los casos L01–L08 separan los resultados concretos aún no declarados de los grupos ya aprobados; identifican fuente, plataforma, esperado y forma de cierre, sin exigir repetir los casos aprobados.

La distinción de alcance es coherente con el contrato: HTTPS de producción, carga operacional, iOS y un umbral audit=0 no se usan como bloqueos automáticos locales. Se mantiene la exigencia local de accesibilidad de formularios, adaptación visual/teclado y estados específicos documentados, sin convertirla en certificación WCAG integral. Las discrepancias de documento/endpoint permanecen como decisiones para fijar el contenido que se aceptará.

El informe de dependencias diferencia npm ls exitoso (coherencia del árbol) de npm audit con hallazgos. Registra web2 altas y0 en omit=dev; móvil25 totales (1 crítica,7 altas,16 moderadas,1 baja) y18 en omit=dev (1 crítica,7 altas,9 moderadas,1 baja). No confunde dependencias no marcadas dev con código incluido o explotable en el bundle nativo. Declara que no se actualizaron paquetes ni se resolvieron los hallazgos; sus opciones son propuestas de trabajo, sin aceptación de riesgo inferida.

Esta revisión documental final no detecta una contradicción nueva entre la matriz, el addendum y el alcance contractual. No se ejecutaron nuevas pruebas, no se cambió la aplicación ni se preparó Git. Se mantiene la instrucción actual del usuario: cerrar los obligatorios locales y fijar el contrato antes de generar la siguiente huella, sin huella provisional ni commit/publicación en esta conciliación.


## Dictamen final de calidad - 10/11/2026

Tras confirmar el responsable L01 web/Android y L02 web, cobertura obligatoria local completa, apta para preparar diff y nueva huella. Lectura independiente de diff HEAD, contrato, clientes, API, persistencia, pruebas y evidencia: sin defecto bloqueante nuevo. git diff HEAD --check exit0, avisos LF/CRLF. No cambia la app; no se repiten checks aprobados. La evidencia manual es del responsable. Exclusiones revisadas: entornos, dependencias, builds y archivos .env locales fuera de entrega; solo ejemplos. Barrido sin secretos reales identificados (URL usuario:clave es ejemplo); no es auditoria exhaustiva. Metadatos incompletos conservados sin inventarlos. TLS/carga productiva y hallazgos npm siguen operacionales; iOS solo si se acuerda alcance. Sin stage, commit ni push por calidad.
