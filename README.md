# SGIP

## Sistema de Gestión de Incidencias en Pereira

Sistema de reporte y mantenimiento urbano que permite centralizar la
recepción, clasificación, asignación y seguimiento de incidencias
reportadas por la ciudadanía.

## Arquitectura

El sistema está compuesto por tres componentes principales:

- Web: React + TypeScript + Vite
- Mobile: React Native + Expo
- Backend: Python + FastAPI
- Base de datos: PostgreSQL / Supabase

La aplicación Web y la aplicación Mobile se comunican exclusivamente
con el Backend mediante la API.

## Estructura

```text
SGIP/
├── backend/
├── web/
├── mobile/
├── docs/
└── .github/
```

## Contexto y coordinación

- [Guía de coordinación de agentes](docs/orquestacion-agentes.md).
- [Modelo de datos: fuentes y contexto vigente](docs/contexto-modelo-datos.md), revisado 09/11/2026.
- [Comparación con la implementación y plan de alineación por etapas](docs/alineacion-modelo-datos.md).
- [Contrato RF-001 ratificado](docs/contrato-rf-001.md).

El modelo lógico de 32 entidades y 65 relaciones es una referencia documental; su actualización no significa que las migraciones o funcionalidades estén implementadas. El estado observado del código y las decisiones pendientes se detallan en los documentos anteriores.

## Desarrollo coordinado

Consulta la [guía de orquestación](docs/orquestacion-agentes.md) para trabajar
con los requisitos de Notion, delegar tareas y verificar entregas antes de publicarlas.
