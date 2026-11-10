# Integración de develop en RF-001

## Alcance y padres

Preparación del 10 de noviembre de 2026 para el [PR #2](https://github.com/Sebas-Hernandez05/SGIP/pull/2). El responsable pidió resolver la integración después de publicar RF-001.

- Rama de entrega y primer padre previsto: entrega/rf-001 en efbc6306f7e1ba7891ab8c81335f31f9c9327acb.
- Segundo padre previsto: develop en a1b40026fae3ca699e24378b405800b638e5d796.
- Base común: 4de9c6ef29bd0bc6a5fe1d13875d278c2e4a40f8.
- Develop aporta el commit de configuración 47bbec97804622197cf4d002decf07f29b82e480 y su integración mediante PR #1.

## Resolución

Los conflictos estaban en AGENTS.md, README.md y docs/orquestacion-agentes.md. AGENTS.md combina las reglas generales de coordinación de develop con el contexto del modelo y el contrato RF-001. README conserva los enlaces de ambas ramas y el bloque de estructura cerrado. La guía conserva la versión actualizada de RF-001, con sus fuentes y aclaraciones del modelo. Se incorporan los cinco perfiles de agentes, la configuración MCP y el registro histórico de orquestación procedentes de develop.

El script scripts/entrega.py rechazaba MERGE_HEAD y solo admitía un padre. Ahora permite preparar una integración resuelta, añade los padres secundarios ordenados a la huella y verifica todos los padres y el árbol tras el commit. El formato de huella de commits normales se conserva. Se mantienen los bloqueos de conflictos sin resolver, cherry-pick, revert y rebase. Se añaden pruebas específicas en scripts/tests/test_entrega.py y una explicación del flujo en la guía.

## Validación del contenido preparado

Entorno de esta revisión: Linux, Python 3.12 y Node 24.22.1. Las pruebas del script crean repositorios Git temporales exclusivos. La utilidad de respuestas usa servidores de prueba locales sin persistencia.

| Verificación | Resultado |
| --- | --- |
| python3 -m unittest discover -s scripts/tests -p test_entrega.py -v | 6/6 aprobadas. Commit normal, merge con padres/árbol correctos, rechazo tras cambiar contenido o padre, conflictos y otras operaciones. |
| node --test mobile/tests/registration.test.mjs | 4/4 aprobadas. Aviso de Node por inferencia de módulo ES en el archivo TypeScript, sin fallo. |
| python3 -m unittest discover -s scripts/tests -p test_qa_rf001_respuestas.py -v | 5/5 aprobadas. Respuestas 422/503, CORS, CLI, demora inválida y timeout HTTP real del servicio móvil a los 15,004 segundos. |
| Lectura TOML de .codex/config.toml y .codex/agents/*.toml | Configuración y cinco perfiles válidos. |
| git diff --exit-code efbc6306f7e1ba7891ab8c81335f31f9c9327acb -- backend mobile web | Código 0. Mismos archivos de aplicación y pruebas que la entrega aceptada. |
| git diff --check y git diff --cached --check | Aprobados. |
| git ls-files -u | Vacío, todos los conflictos resueltos. |
| Revisión independiente de calidad | Sin defectos bloqueantes nuevos en resolución, script y compatibilidad de aceptación. |

Las pruebas backend con PostgreSQL, lint/tipos/build y pruebas manuales de UI se conservan como evidencia de la entrega aceptada. Esta integración conserva íntegros backend/, mobile/ y web/, por lo que no se repiten. Esta revisión no declara una nueva ejecución de esos checks ni una certificación operacional. Los hallazgos de dependencias y el alcance operacional conservan sus registros previos.

## Aceptación y publicación

La integración queda preparada, con MERGE_HEAD apuntando al segundo padre previsto, para solicitar la huella de este conjunto actualizado. La aprobación anterior identifica RF-001 antes de incorporar develop. AGENTS.md paso 5 exige aceptación de la nueva huella al cambiar base o contenido. La actualización remota posterior deberá comprobar que entrega/rf-001 siga en efbc6306f7e1ba7891ab8c81335f31f9c9327acb y que develop siga en el segundo padre revisado. Este informe registra preparación y validación, sin acreditar publicación de la integración.
