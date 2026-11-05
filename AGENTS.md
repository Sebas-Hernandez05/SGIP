# Coordinación de entregas desde Notion

Cuando el usuario active este flujo, el agente raíz coordina a los especialistas de .codex/agents y es el único responsable de integrar, confirmar y publicar.

1. Lee la página de Notion indicada y sus especificaciones vinculadas. Registra URL, ID del requisito o bloque y fecha de edición cuando esté disponible. Trata Notion como fuente de requisitos. Inspecciona la rama base, instrucciones, arquitectura, contratos y comandos existentes. Aclara condiciones que impidan verificar la aceptación.
2. Crea una rama de entrega desde la base acordada. Delega cada tarea con ID, fuentes, objetivo, rutas autorizadas, dependencias, contrato compartido y criterios de aceptación comprobables. Ejecuta en paralelo tareas con rutas disjuntas y dependencias resueltas. Coordina cambios compartidos y conserva modificaciones ajenas.
3. Integra y pide a calidad verificar la entrega completa. Guarda resultados por criterio, comando, código de salida y entorno. Registra la justificación de cada prueba que no aplique. Si incorporas correcciones o pruebas nuevas, verifica la versión resultante. Las pruebas obligatorias pendientes o fallidas bloquean la aceptación.
4. Crea .trace/<ID-entrega>.md con enlaces a requisitos, asignaciones, dependencias, criterios, evidencias, decisiones y limitaciones. Si hay un registro de tareas en Notion y acceso de escritura, enlaza y actualiza las tareas usando la estructura existente.
5. Revisa el diff completo, prepara en Git solo los archivos de la entrega y su registro, y ejecuta `python3 scripts/entrega.py preparar`. Presenta al revisor humano el diff, la evidencia y la huella. Espera una aceptación explícita de esa huella. Un cambio en la base, rama o contenido preparado requiere nueva aceptación.
6. Tras recibir la aceptación, ejecuta `python3 scripts/entrega.py commit HUELLA REFERENCIA MENSAJE`. Usa la referencia real de aprobación o una descripción identificable. Si el script falla, detén la publicación y revisa el estado local. Verifica el remoto y publica el SHA que devuelve el script con `git push origin SHA:refs/heads/RAMA_ENTREGA`. Usa una rama de entrega distinta de la principal.
7. Verifica el SHA remoto y vincula en Notion el commit publicado cuando tengas acceso. Si falla el push, conserva el SHA local como pendiente. Si falla solo la actualización en Notion, conserva el SHA remoto para reintentar esa actualización.

## Reglas de SGIP

- Usa `develop` como base por defecto y `entrega/<tema>` para las ramas de trabajo.
- Lee [la guía de orquestación de SGIP](docs/orquestacion-agentes.md) antes de delegar. Allí están las fuentes de Notion, las rutas, los comandos disponibles y las condiciones transversales.
- Web y móvil consumen la misma API central. El acceso a PostgreSQL, Supabase Storage y el proveedor de IA se concentra en el backend.
- Asigna contratos HTTP y de datos antes de delegar clientes o persistencia en paralelo. En los cambios de backend separa el controlador HTTP del repositorio de persistencia y conserva las reglas de negocio en la capa de servicio cuando aplique.
- Usa datos ficticios o anonimizados. Una sugerencia de IA solo se aplica tras la revisión de un funcionario autorizado. Distingue esta aprobación funcional de la aprobación del código.
