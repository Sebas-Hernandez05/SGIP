# Contexto e instrucciones SGIP

Mantén el flujo de coordinación y aceptación de las instrucciones ancestras. Antes de planificar cambios de datos, consulta [la guía del coordinador](docs/orquestacion-agentes.md), [el contexto del modelo](docs/contexto-modelo-datos.md) y [la comparación y plan por etapas](docs/alineacion-modelo-datos.md).

Fuente lógica vigente: [Notion, sección5.3](https://app.notion.com/p/3de14e04c5cb809e9250e58428b4e44a), revisión09/11/2026; [adjunto corregido](ref/SGIP_Diagrama_ER_Corregido.html),32 entidades/65 relaciones. El adjunto Interactivo anterior es histórico. Distingue correcciones documentadas, propuestas pendientes e implementación probada; una actualización de Notion no ejecuta migraciones.

RF-001 conserva el [contrato ratificado](docs/contrato-rf-001.md): nombre completo/correo/contraseña, sin documento/teléfono, POST `/api/v1/ciudadanos`, sin sesión automática. Cualquier ampliación requiere otra tarea. Conserva código, cambios locales y evidencia; esta actualización solo autoriza contexto, instrucciones y planificación.
