# 🤖 Bot CC — Sistema de Atención Automática y Derivación (CUECCA)

Este repositorio contiene la arquitectura, flujos de automatización y documentación técnica para **Bot CC**, la solución conversacional procedural diseñada para la Cooperativa CUECCA (Castelli Ltda.).

El sistema automatiza la consulta de cuenta corriente/deuda y el registro de reclamos técnicos para los servicios de Energía, Agua, Cloacas e Internet, derivando a atención humana únicamente cuando se requiere.

---

## 🛠️ Stack Tecnológico

* **Front-end Omnicanal:** [Chatwoot](https://www.chatwoot.com/)
* **Motor Conversacional:** [TypeBot](https://typebot.io/)
* **Middleware / Orquestador:** [n8n](https://n8n.io/)
* **Base de Datos:** MySQL / SQL Server

---

## 📚 Documentación del Proyecto

Toda la documentación detallada del proyecto se encuentra organizada dentro de la carpeta [`docs/`](./docs/):

1. [**`01_requerimientos_y_planificacion.md`**](./docs/01_requerimientos_y_planificacion.md): Alcance del proyecto, objetivos de automatización, requerimientos funcionales/no funcionales y planificación de entregables.
2. [**`02_especificacion_funcional_y_casos.md`**](./docs/02_especificacion_funcional_y_casos.md): Mapeo procedural de flujos, matriz de casos de uso (Consulta de Deuda y Reclamos), árboles de decisión y reglas de derivación.
3. [**`03_manual_despliegue_y_mantenimiento.md`**](./docs/03_manual_despliegue_y_mantenimiento.md): Guía de instalación, configuración de variables de entorno, importación de flujos (n8n/TypeBot) y protocolos de mantenimiento.
4. [**`04_arquitectura_e_integraciones.md`**](./docs/04_arquitectura_e_integraciones.md): Esquema de arquitectura (Mermaid), modelo conceptual de base de datos MySQL y mapa de integraciones entre TypeBot, n8n y Chatwoot.

---

## 🚀 Estructura del Repositorio

```text
.
├── docs/
│   ├── 01_requerimientos_y_planificacion.md
│   ├── 02_especificacion_funcional_y_casos.md
│   ├── 03_manual_despliegue_y_mantenimiento.md
│   └── 04_arquitectura_e_integraciones.md
├── workflows/         # Exportaciones JSON de los flujos de n8n
├── typebot/           # Exportaciones JSON de los flujos de TypeBot
└── README.md
```

---

## 🛡️ Reglas de Seguridad y Trazabilidad

* **Solo Lectura:** Las consultas financieras y de cuenta corriente ejecutadas por n8n operan bajo permisos estricta y exclusivamente de lectura.
* **Trazabilidad:** Todo reclamo técnico genera un número de ticket con registro temporal único en la base de datos para seguimiento de la guardia técnica.
