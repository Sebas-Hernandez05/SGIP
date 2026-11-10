# SGIP · Configuración de agentes

- Base de GitHub: `develop` en `4de9c6ef29bd0bc6a5fe1d13875d278c2e4a40f8`.
- Fuentes: [proyecto](https://app.notion.com/p/3de14e04c5cb8030af75c0a1fcb134e1), [requerimientos](https://app.notion.com/p/3de14e04c5cb803babfaefe03b6fbf3e), [modelos](https://app.notion.com/p/3de14e04c5cb809e9250e58428b4e44a) y [seguimiento](https://app.notion.com/p/3e214e04c5cb80739454d9dde0927191).
- Alcance: configuración del coordinador y cinco especialistas, guía de delegación y comprobación de aceptación. La configuración inicial la prepara el coordinador.
- Criterios de entrega: cinco perfiles TOML válidos, tareas vinculadas con Notion y controles que rechazan una rama incorrecta o un cambio de contenido posterior a la revisión.
- Evidencia: lectura de los perfiles con `tomllib`, `git diff --cached --check` y ejercicio de commit y publicación contra un remoto Git local. La ejecución de Codex CLI con el servidor de Notion queda pendiente.
