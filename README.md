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