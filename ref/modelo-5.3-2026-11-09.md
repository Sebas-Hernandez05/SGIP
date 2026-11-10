# Fuente consultada: modelo de datos SGIP, sección 5.3

URL: https://app.notion.com/p/3de14e04c5cb809e9250e58428b4e44a
Edición de página observada: 2026-11-09T16:18:13.889Z.
Consulta: 2026-11-09. Copia de la sección completa obtenida mediante conector Notion. Los enlaces notion-file-block son referencias estables; no se guardan URLs firmadas de descarga. No representa implementación ejecutada.

## 5.3 Modelo de Base de Datos

### 5.3.1 Diagrama entidad-relación

<embed source="notion-file-block://371b3819-eb27-44da-a65a-752ff6a9120d/a1d21d43-be02-4f4d-90b2-cd9c693ddd12?space_id=a839bb6d-31f8-4e5d-9790-0bf10e453e2e&name=SGIP_Diagrama_ER_Corregido.html">
Versión vigente: SGIP\_Diagrama\_ER\_Corregido.html — 32 entidades y 65 relaciones. El adjunto siguiente, SGIP\_Diagrama\_ER\_Interactivo.html, se conserva únicamente como antecedente histórico.
</embed>

<embed source="notion-file-block://3fc14e04-c5cb-80d8-bff2-d3db314d73b8/28f006de-9f12-4dbb-ae43-3981c395965c?space_id=a839bb6d-31f8-4e5d-9790-0bf10e453e2e&name=SGIP_Diagrama_ER_Interactivo.html" />

### 5.3.2 Propuesta y reglas del modelo

Modelo lógico revisado el <date start="2026-11-09" /> a partir de <mention url="https://app.notion.com/p/3de14e04c5cb803babfaefe03b6fbf3e">Requerimientos Específicos</mention> (RF-001 a RF-059) y <mention url="https://app.notion.com/p/3df14e04c5cb80bd8e49e1dc752421a8">Casos de Uso</mention>. La propuesta usa PostgreSQL/PostGIS y mantiene acceso exclusivo a través de la API central. Las decisiones de producto pendientes se señalan expresamente; esta revisión documental no acredita migraciones ejecutadas ni cambios en una base de datos desplegada.

El diagrama corregido y su diccionario se encuentran en [SGIP\_Diagrama\_ER\_Corregido.html](https://chatgpt.com/library?file_id=libfile_79cb51a666b081918aa03fb18c6364ef&account_id=personal). El adjunto anterior llamado SGIP\_Diagrama\_ER\_Interactivo.html queda como antecedente histórico, sustituido por esta revisión; sus anotaciones incompatibles no forman parte del modelo vigente.

#### 1. Organización general y convenciones

<code>REPORTE</code> sigue siendo la entidad central. El modelo separa identidad, parametrización, atención operativa, evidencia, IA, detección de duplicados, comunicaciones y auditoría. Los identificadores son UUID y las marcas de tiempo operativas usan <code>timestamptz</code>. <code>MIEMBRO_CUADRILLA</code> conserva fechas de pertenencia; si se necesita precisión dentro del mismo día, deberán migrarse a marcas de tiempo.

Las claves foráneas deben apuntar a registros existentes. <code>NOT NULL</code> se exige únicamente donde se documenta; una FK no implica por sí sola obligatoriedad. Los catálogos inactivos conservan sus referencias históricas. El borrado físico en cascada no se adopta para cuentas, reportes, órdenes, evidencias ni auditoría. Las políticas concretas de conservación y eliminación lógica quedan pendientes.

#### 2. Identidad, roles, permisos y sesiones

<code>USUARIO.rol_id</code> mantiene un único rol por cuenta: administrador, funcionario, cuadrilla o ciudadano. La cuenta de una persona integrante de cuadrilla se relaciona con el equipo mediante <code>MIEMBRO_CUADRILLA</code>; no se confunde la persona autenticada con la entidad operativa <code>CUADRILLA</code>. El registro público crea únicamente ciudadanos; no concede roles administrativos suministrados por el cliente.

Los permisos se expresarán mediante una <b>matriz versionada en la API</b> que relacione rol, operación y condiciones de pertenencia. Esta elección técnica no supone una interfaz para editar permisos. Si se aprueba configurar permisos dinámicamente o acumular roles, se añadirá el esquema correspondiente; no se presume ese alcance.

El correo se normaliza antes de comprobar unicidad y las contraseñas se almacenan como hash. <code>documento</code> se incluye como dato nullable y único cuando se informe para reflejar T13/T16 del seguimiento de backend; su obligatoriedad, formato y alcance requieren conciliación con 3.4.1. No se incorpora silenciosamente como nuevo campo obligatorio del registro.

<code>SESION_USUARIO</code> propone persistencia para RR-08: usuario, identificador de sesión, hash del token, dispositivo seudonimizado, canal, creación, expiración y revocación. Un índice único por usuario sobre filas no revocadas impide dos sesiones abiertas; el flujo debe revocar transaccionalmente las expiradas antes de admitir otra. La API comprueba expiración, revocación y cuenta activa en cada petición, además de la autenticidad del token. El dato de dispositivo y el canal declarados por el cliente no bastan como controles de autorización. Funcionario accede por web (RR-09), cuadrilla por móvil (RR-10). Queda pendiente si el segundo inicio se rechaza o sustituye la sesión anterior; ninguna opción permite dos sesiones vigentes.

#### 3. Catálogos, categorías y prioridades

<code>CATEGORIA</code>, <code>PRIORIDAD</code>, <code>ZONA</code>, <code>ESTADO_REPORTE</code>, <code>ESTADO_ORDEN</code>, <code>ESTADO_ACTIVIDAD</code> y <code>TIPO_EVIDENCIA</code> mantienen valores controlados. La configuración debe preservar los valores utilizados en datos históricos. Los estados posibles no constituyen automáticamente una matriz completa de transiciones: esa matriz debe documentarse por entidad, operación y rol autorizado, e implementarse en la API.

<code>CATEGORIA.prioridad_predeterminada_id</code> representa la asociación categoría–prioridad de 3.7. Se propone cargar los valores allí definidos: luminarias y residuos → baja; fugas y árboles en riesgo → media; incendios, terremotos, avalanchas y derrumbes → alta. Su uso no reemplaza la revisión del funcionario ni determina por sí solo qué eventos están dentro de la atención operativa de SGIP.

Una prioridad puede existir antes de registrar órdenes: <b>PRIORIDAD 1 → ORDEN\_TRABAJO 0..N</b>. Cada orden debe tener una prioridad. <code>nivel</code> es único; <code>tiempo_objetivo_horas</code> es positivo si se mantiene como parámetro. El tiempo por prioridad constituye una propuesta técnica; no se presenta como un acuerdo de atención definitivo. <code>ZONA</code> conserva la zona operativa; códigos externos como Z-01 pueden mapearse en los datos iniciales sin reemplazar el UUID. La selección por zona no exige polígonos si no se aprueba ese alcance.

#### 4. Registro, ubicación y clasificación del reporte

Cada reporte tiene ciudadano creador, código único, zona, estado y fechas de creación/actualización. <code>categoria_id</code> y <code>prioridad_id</code> pueden ser nulos durante la recepción, porque la clasificación se confirma después por un funcionario. No se impone una categoría ficticia para registrar el caso. Antes de crear una orden, debe existir una prioridad confirmada y la información necesaria para la asignación.

<code>ubicacion</code> admite <code>geography(Point,4326)</code> y <code>referencia_ubicacion</code> permite dirección o referencia textual. Se exige al menos una ubicación útil: coordenadas válidas o referencia textual no vacía; la API comprueba su coherencia con la zona. Esto permite registrar ubicación aproximada aunque falle la geolocalización.

El modelo admite <code>descripcion</code> nullable para no impedir técnicamente el escenario de solo fotografía de RF-031. <b>La regla funcional de admisión queda pendiente de conciliar</b> con RF-022 y CU-03: no se autoriza un reporte sin descripción ni evidencia útil. Mientras se resuelve, la validación debe exigir descripción no vacía o fotografía válida, junto con ubicación y demás datos obligatorios. Esta regla que involucra archivos se comprueba al confirmar la operación completa, no con un CHECK aislado sobre REPORTE.

<code>clasificado_por_id</code> y <code>clasificado_en</code> identifican la última confirmación humana; deben aparecer conjuntamente. Se actualizan junto con categoría y prioridad confirmadas y con un evento de historial. <code>fecha_reporte</code> y <code>creado_en</code> son fechas del servidor e iguales en el flujo actual; una fecha del hecho aportada por el ciudadano requeriría un campo y una regla separados. <code>fecha_objetivo</code> del reporte es nullable hasta definir su política, distinta de la fecha objetivo obligatoria de la orden.

#### 5. Inteligencia artificial y revisión humana

<code>EJECUCION_IA</code> conserva cada intento: reporte, proveedor, modelo, datos ficticios/anonimizados enviados, instrucción principal o versión del prompt, solicitud, respuesta, estado de ejecución y errores depurados. Una ejecución puede producir cero o una recomendación; un fallo conserva su registro aunque no haya recomendación. Los reintentos generan ejecuciones distintas. No se almacenan credenciales ni datos innecesarios en entradas, respuestas o errores. <code>RECOMENDACION_IA</code> mantiene categoría y prioridad sugeridas, confianza, resumen y justificación separados de los valores confirmados. Las sugerencias pueden ser nulas en respuestas parciales; una respuesta incompleta no autoriza aceptar una clasificación inválida. La confianza, si existe y usa la escala prevista, está entre 0 y 1. La respuesta original se conserva en la ejecución, evitando duplicarla en cada recomendación.

Las decisiones son <code>PENDIENTE</code>, <code>ACEPTADA</code>, <code>MODIFICADA</code> y <code>RECHAZADA</code>. Pendiente no lleva revisor ni fecha de revisión ni valores confirmados; las demás requieren funcionario revisor y fecha. Aceptada o modificada guardan la categoría y prioridad definitivas válidas y, si corresponde, resumen confirmado. Aceptada conserva las sugerencias aplicables; modificada registra los ajustes sin sobrescribir la propuesta original. Rechazada no aplica valores al reporte y mantiene los campos de clasificación confirmada nulos. Una clasificación manual independiente se registra por separado.

<code>ejecucion_id</code> es único en RECOMENDACION\_IA y la ejecución debe pertenecer al mismo reporte de la recomendación. La actualización del reporte, la resolución de la recomendación y el historial se realizan en una misma transacción con control de concurrencia. La IA no asigna, cierra ni reabre casos automáticamente (RR-01/RR-02). RF-031 condiciona la propuesta de categoría al escenario fotográfico; RF-032 exige propuesta de prioridad; un fallo mantiene disponible la clasificación manual.

#### 6. Detección y revisión de duplicados

<code>REGLA_DUPLICADO</code> configura criterios y <code>DETECCION_DUPLICADO</code> conserva candidatos y revisión humana. Los criterios mínimos siguen siendo zona, categoría e intervalo temporal según RF-028; la ausencia de categoría inicial puede posponer la comparación hasta que exista información suficiente. Detectar coincidencias no confirma duplicidad (RR-05), ni elimina, fusiona o cierra reportes.

Cada detección guarda reporte evaluado, posible original, regla, snapshot <code>regla_aplicada</code>, coincidencias, diferencia temporal y estado <code>PENDIENTE</code>, <code>CONFIRMADA</code> o <code>DESCARTADA</code>. Confirmada/descartada requieren funcionario revisor y fecha. Los reportes deben ser distintos, la diferencia temporal no negativa y la regla aplicada identificable aunque cambie su configuración después.

Para fotografías se guardan <code>evidencia_id</code> del reporte evaluado y <code>evidencia_original_id</code> del original; ambos son opcionales cuando no se aplica comparación fotográfica. Si se comparan fotos, ambos deben estar presentes, ser fotográficos y pertenecer a los respectivos reportes, directamente o por actividad/orden. El hash del archivo identifica bytes iguales, no escenas similares. La política sobre pares repetidos y direcciones inversas debe definirse; como mínimo no se repetirá el mismo candidato y ejecución lógica por reintentos técnicos.

RN-01 se interpreta como detección de candidato con intervalo estrictamente menor de 60 segundos, manteniendo revisión humana. Sigue pendiente qué significa «mismo ID»; el campo configurable de coincidencia de usuario no convierte esa interpretación en requisito aprobado. La redacción automática de RN-01 debe conciliarse con RR-05 fuera de 5.3.

#### 7. Evidencias y almacenamiento

Cada <code>EVIDENCIA</code> pertenece a <b>exactamente un reporte o una actividad</b>. <code>reporte_id</code> y <code>actividad_id</code> son individualmente nullable, pero se exige XOR: uno informado y el otro nulo. La fotografía ciudadana se carga al registrar el reporte sin necesitar una orden o actividad. La evidencia de campo se vincula a su reporte mediante ACTIVIDAD\_ORDEN → ORDEN\_TRABAJO → REPORTE.

<code>momento_intervencion</code> admite <code>ANTES</code>, <code>DURANTE</code> y <code>DESPUES</code>; es obligatorio en evidencias de actividad y nulo en la fotografía inicial del reporte. <code>TIPO_EVIDENCIA</code> clasifica el soporte admitido y <code>mime_type</code> representa su tipo real validado, sin confundir formato y momento de intervención. No se inventa un mínimo de fotografías por fase ni un máximo de tamaño sin parametrización aprobada.

El archivo se almacena en Storage privado y la BD conserva referencia estable (<code>url_archivo</code>, entendida como ruta/identificador canónico), tipo, autor, descripción, fecha y hash opcional. Las URLs firmadas temporales se generan al consultar; no sustituyen la referencia persistente. La API verifica permisos y pertenencia al caso también al entregar archivos. Deben contemplarse errores de carga y limpieza de archivos huérfanos sin confirmar éxito antes de completar la operación.

#### 8. Cuadrillas, capacidades y áreas responsables

<code>AREA_RESPONSABLE</code> representa dependencia o especialidad, diferente de <code>ZONA</code>. Se propone una sola área por cuadrilla mediante <code>CUADRILLA.area_responsable_id</code>, manteniendo una zona por cuadrilla como en el diseño previo. Si el equipo aprueba múltiples áreas o zonas de cobertura por cuadrilla, se introducirán las tablas intermedias correspondientes. <code>CAPACIDAD</code> normaliza las aptitudes operativas y <code>CUADRILLA_CAPACIDAD</code> resuelve la relación N:M. <code>CATEGORIA.area_responsable_id</code> y <code>CATEGORIA_CAPACIDAD</code> proponen parametrizar el área y las capacidades requeridas para cada tipo de atención. Ambos vínculos se completan antes de asignar órdenes; una configuración incompleta no equivale a compatibilidad comprobada.

La API verifica cuadrilla activa, correspondencia de área y disponibilidad de todas las capacidades requeridas (RF-019/RF-041/RR-07). Los pares cuadrilla–capacidad y categoría–capacidad son únicos. Se auditan los cambios de parametrización y se conserva en el evento de asignación la configuración usada, para no reinterpretar asignaciones antiguas con capacidades posteriores.

<code>MIEMBRO_CUADRILLA</code> conserva persona, equipo, liderazgo e intervalo de pertenencia. La fecha final no precede a la inicial; se evitan asignaciones repetidas y periodos incompatibles. La pertenencia vigente y el rol autorizan acciones de campo; tener una FK a USUARIO no acredita por sí solo autorización. La desactivación de una cuadrilla y sus efectos sobre órdenes abiertas requieren una regla pendiente; no se supone reasignación automática.

#### 9. Órdenes de trabajo, actividades y pausas

<code>ORDEN_TRABAJO.reporte_id</code> es obligatorio (RR-06). Un reporte puede tener cero o varias órdenes; no se impone una orden única. Cuadrilla y responsable pueden quedar nulos al crear y completarse según el proceso de asignación. La fecha objetivo, los recursos y la prioridad se registran conforme a RF-037–RF-041. Se propone copiar la prioridad confirmada del reporte al crear la orden; la propagación de cambios posteriores queda pendiente, sin actualizaciones silenciosas.

La aceptación de la orden se registra como evento explícito con autor, fecha y estado resultante. Cada cambio de estado o asignación conserva sus valores anteriores/nuevos en <code>HISTORIAL_ORDEN</code>. La función precisa de <code>responsable_id</code> debe concretarse antes de volverla obligatoria.

<code>ACTIVIDAD_ORDEN</code> representa las tareas de una orden. Inicio y cierre deben respetar secuencia temporal y transiciones autorizadas. <code>PAUSA_ACTIVIDAD</code> conserva cada intervalo con autores de pausa/reanudación. Solo hay una pausa abierta por actividad y los intervalos no se solapan; reanudación y autor se registran conjuntamente. Una actividad no se cierra antes de comenzar ni dejando una pausa abierta sin resolver según la política de cierre que se defina.

<code>actualizada_por_id</code> indica únicamente al último usuario; no reemplaza los eventos individuales. Inicio, pausa, reanudación y cierre se registran en auditoría y en el historial de la orden con <code>actividad_id</code> en el detalle. El cierre de una actividad no cierra automáticamente la orden ni el reporte. Las matrices de transición y los criterios de cierre de cada entidad permanecen como decisiones explícitas a completar.

#### 10. Comunicaciones y destinatarios

<code>NOTIFICACION</code> guarda mensaje, tipo, canal, contexto y creación. <code>NOTIFICACION_DESTINATARIO</code> guarda una fila por persona destinataria, con estado <code>PENDIENTE</code>, <code>ENVIADA</code> o <code>FALLIDA</code>, intentos, último intento, fecha de envío, error y lectura individuales. Se exige <code>UNIQUE(notificacion_id, usuario_id)</code>. Una notificación preparada para envío tiene al menos un destinatario y no se marca enviada por el simple hecho de guardar el mensaje.

La propuesta operativa usa exactamente un contexto: reporte u orden. Los avisos generales quedan pendientes. Los canales propuestos son <code>INTERNA</code>, <code>CORREO</code>, <code>PUSH</code> y <code>SMS</code>; la selección e implementación de canales externos no se presume aprobada por enumerarlos. <code>ENVIADA</code> acredita aceptación por el mecanismo elegido, no entrega o lectura comprobadas por el proveedor. <code>leida_en</code> corresponde a la lectura registrada por el usuario en la aplicación.

Se cubren cambios de estado y cierre para el propietario, solicitudes de información y avisos de vencimiento para funcionarios. Para RF-049, la solicitud puede representarse como tipo de notificación e historial asociado; el actor/evento disparador y un eventual flujo de respuesta siguen pendientes. La frecuencia, distribución de alertas y reintentos tampoco se inventan como nuevos requisitos.

#### 11. Validación ciudadana y reapertura

<code>VALIDACION_CIUDADANA</code> contiene reporte, ciudadano, conformidad, comentario opcional y fecha. Solo valida el ciudadano propietario del reporte: la API comprueba igualdad con <code>REPORTE.ciudadano_id</code>, además de los permisos y el estado habilitante que se defina. La unicidad de una pareja no sustituye esta comprobación de pertenencia (RR-04/CU-17).

Se conserva como propuesta inicial una validación por ciudadano y reporte mediante <code>UNIQUE(reporte_id, ciudadano_id)</code>. Permitir nuevas valoraciones tras reapertura requiere una decisión de ciclos de atención y su ajuste de esquema; no se habilita valoración de terceros. La valoración no genera automáticamente cierre ni reapertura.

La reapertura se representa como evento de historial con estado anterior/nuevo y actor autorizado. Siguen pendientes actor, canal, estados habilitantes, motivo y efecto sobre órdenes existentes. Esta sección no concede al ciudadano o funcionario un permiso que los requisitos todavía no resuelven.

#### 12. Historial y auditoría

<code>HISTORIAL_REPORTE</code> y <code>HISTORIAL_ORDEN</code> incorporan <code>operacion</code> y <code>detalle</code> JSONB para conservar también acciones que no cambian estado: clasificación, asignación, revisión y otras operaciones autorizadas. En una creación se exige el estado inicial, con anterior nulo. En cambio de estado se exige nuevo y anterior; en acciones sin transición ambos pueden quedar nulos y el detalle describe los datos afectados. Un evento automático admite usuario nulo identificado como operación del sistema.

<code>REGISTRO_AUDITORIA</code> conserva entidad, identificador, operación, usuario o sistema, fecha y detalle; IP y agente son opcionales. El detalle registra valores anteriores/nuevos cuando corresponda y referencias de reporte, orden y actividad necesarias para reconstruir la operación. No se incluyen contraseñas, tokens ni datos personales innecesarios. El acceso se restringe y los registros históricos se conservan conforme a la política que se defina.

Estado actual e historial se actualizan en la misma transacción. Los cambios de clasificación y asignación requieren control de concurrencia para no resolver dos veces una recomendación ni perder cambios simultáneos. La consulta ciudadana entrega únicamente historial y evidencias autorizados de casos propios; no expone auditoría global.

#### 13. Integridad, nulabilidad e índices

Las PK, FK, <code>NOT NULL</code>, <code>UNIQUE</code> y restricciones simples deben convertirse en migraciones versionadas. Las reglas entre varias filas o tablas —propiedad, compatibilidad, evidencias de un mismo caso, no solapamiento y requisitos de cierre— requieren validaciones transaccionales y, cuando convenga, mecanismos específicos de PostgreSQL. No se presentan como garantizadas por dibujar una línea o añadir un CHECK de una sola fila.

Identidad: Correo normalizado único; documento único cuando se informe; hash de contraseña obligatorio. Sesiones: Un usuario con máximo una sesión no revocada; expiración posterior a creación; revocar expiradas dentro del flujo atómico; cada petición comprueba vigencia. Reporte: Ciudadano, zona, código y estado obligatorios; ubicación textual no vacía o coordenadas válidas; categoría/prioridad inicialmente opcionales. Clasificación: Actor y fecha conjuntos; solo aplicar clasificación confirmada por funcionario autorizado; registrar historial. Evidencia: <code>(reporte_id IS NOT NULL) <> (actividad_id IS NOT NULL)</code>; momento obligatorio y válido solo si pertenece a actividad. IA: <code>UNIQUE(ejecucion_id)</code>; coincidencia del reporte entre ejecución y recomendación; confianza entre 0 y 1; decisión coherente con revisor, fecha y valores confirmados. Duplicados: Reportes distintos; delta no negativo; revisión terminal con revisor y fecha; dos fotos válidas y de sus respectivos reportes si se comparan fotografías. Capacidades: Pares de asociaciones únicos; cuadrilla activa, área compatible y capacidades requeridas comprobadas antes de asignar. Fechas y pausas: Cierre no anterior a inicio; fin de membresía no anterior al inicio; una pausa abierta por actividad y sin solapamientos. Historial: Creación con estado nuevo y anterior nulo; transición con ambos estados; acciones sin transición identificadas por operación y detalle. Notificaciones: Contexto único según propuesta; destinatarios únicos y existentes; intentos no negativos; envío, fallo y lectura individuales y coherentes. Validación: Solo propietario; pareja reporte/ciudadano única bajo la propuesta inicial; no automatizar transiciones por la valoración.

Índices propuestos: GiST en REPORTE.ubicacion; compuestos por ciudadano/fecha y estado/fecha; filtros de zona/categoría cuando lo justifiquen las consultas; historial por reporte/fecha y orden/fecha; órdenes por cuadrilla/estado/fecha objetivo; detecciones por reporte/estado; ejecuciones de IA por reporte/fecha; destinatarios por usuario/lectura/estado; auditoría por entidad/identificador/fecha. Las restricciones únicas crean sus índices correspondientes; no se duplican sin necesidad. La selección se valida con consultas y planes de ejecución reales.

#### 14. Indicadores e implementación

Los indicadores de RF-054–RF-059 se calculan desde reportes, órdenes, actividades e historiales; no requieren una tabla de indicadores duplicados en esta propuesta. Los tiempos dependen de definir eventos inicial/final, pausas descontables y tratamiento de reaperturas. Un caso vencido necesita fecha objetivo y estados evaluables; la fecha de la orden no se convierte automáticamente en fecha del reporte. Debe acordarse cómo tratar reportes con varias órdenes, cambios de prioridad y casos cerrados.

FastAPI valida entradas, autenticación, permisos, pertenencia y transiciones. PostgreSQL aporta integridad persistente y PostGIS el tipo geográfico. Los clientes consumen la misma API y no acceden directamente a BD; el acceso a Storage se controla desde el backend. Las modificaciones del esquema se implementarán con migraciones versionadas y pruebas; esta revisión no sustituye las migraciones ni acredita disponibilidad, rendimiento o integridad de una instancia real.

#### 15. Decisiones pendientes y criterios de aceptación

Documento obligatorio y unicidad exacta: Conciliar 3.4.1 con T13/T16; hoy nullable y único si se informa. Multirrol o permisos configurables: Hoy un rol por cuenta y matriz versionada de permisos en API. Segundo inicio de sesión: Rechazarlo o revocar la sesión previa de forma atómica; nunca dos vigentes. Descripción frente a solo fotografía: Conciliar RF-022, RF-031 y CU-03; no admitir reportes sin contenido útil. Áreas, capacidades y cobertura: Validar la propuesta por categoría, una sola área/zona por cuadrilla y tratamiento de desactivaciones. Estados, cierre y reapertura: Definir transiciones, actor, motivos y efectos sobre órdenes; distinguir cierre de actividad, orden y reporte. Prioridad y plazos: Confirmar copia inicial y cambios posteriores; fecha objetivo del reporte y cálculo de vencimientos. Duplicados: Aclarar «mismo ID», tratamiento de pares repetidos y consecuencias de confirmación; sin acciones automáticas. Valoraciones tras reapertura: Definir repetición o ciclos antes de modificar la unicidad propuesta. Comunicaciones: Confirmar canales, contexto general si aplica, disparador del seguimiento, reintentos y destinatarios de vencimientos. Conservación: Definir acceso, retención, borrado lógico y tratamiento de evidencias, auditoría y datos de IA. Trazabilidad externa: Conciliar referencias RF desplazadas y CU-25/CU-26 en 5.1 y casos detallados, sin modificar esas secciones en esta revisión.

Para aceptar el diseño físico deberán aprobarse las decisiones que afecten su implementación, concordar el diagrama con el diccionario y pasar pruebas de: foto inicial sin actividad; XOR y momento de evidencia; registro con clasificación pendiente; ubicación manual; asignación incompatible rechazada; revisión IA aceptada/modificada/rechazada y fallo trazable; máximo una sesión vigente incluso con inicios concurrentes; privacidad de reportes y validación; pausas sin solapamientos; notificaciones con resultados por destinatario; y actualización atómica de estado e historial. Las decisiones pendientes de producto no se consideran resueltas por la existencia de las tablas.

#### Diccionario, trazabilidad y alcance

El explorador corregido contiene el diccionario completo de las 32 tablas: atributos, tipos, PK, FK, unicidad y nulabilidad explícita, además de notas de integridad y las 65 relaciones. Se agregan AREA\_RESPONSABLE, CAPACIDAD, CUADRILLA\_CAPACIDAD, CATEGORIA\_CAPACIDAD, SESION\_USUARIO y EJECUCION\_IA. Evidencias, prioridad, clasificación pendiente, revisión humana, validaciones del propietario, notificaciones por destinatario y acciones auditables son coherentes con las reglas de esta sección. La comprobación de estructura verificó 32 entidades, 65 FK y 65 relaciones; las pruebas básicas de ejecución del explorador comprobaron búsqueda, inspector y visibilidad de relaciones. No sustituyen pruebas con migraciones y datos reales.

Trazabilidad: RF-001–RF-004 y RR-03/RR-08–RR-10 → identidad, sesiones, permisos y auditoría; RF-005–RF-019 → catálogos, cuadrillas, áreas y capacidades; RF-020–RF-027 → reportes, ubicación, evidencias e historial; RF-028–RF-029 → duplicados; RF-030–RF-036 → ejecución y revisión IA; RF-037–RF-047 → órdenes, actividades, pausas, evidencias y trazabilidad; RF-048–RF-053 → comunicaciones, validación e historial/reapertura según decisiones pendientes; RF-054–RF-059 → consultas, tiempos, vencimientos y avisos. La conciliación de referencias RF desplazadas y CU-25/CU-26 en 5.1 y casos detallados queda pendiente fuera del alcance de esta edición, limitada a 5.3.
