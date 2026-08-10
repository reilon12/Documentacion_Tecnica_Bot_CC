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

1. [**`01_manual_usuario_operadores.md`**](./docs/01_manual_usuario_operadores.md): Guía operativa para el personal de atención y guardia en Chatwoot (gestión de etiquetas, derivaciones y estados).
2. [**`02_matriz_casos_de_uso.md`**](./docs/02_matriz_casos_de_uso.md): Mapeo completo de árboles de decisión, caminos principales, excepciones y tags asignados.
3. [**`03_diseno_mensajes_e_interfaz.md`**](./docs/03_diseno_mensajes_e_interfaz.md): Textos exactos, tono de comunicación y estructura visual de las opciones presentadas en TypeBot.
4. [**`04_arquitectura_e_integraciones.md`**](./docs/04_arquitectura_e_integraciones.md): Esquema de arquitectura (Mermaid), modelo conceptual de la base de datos MySQL y mapa de integración procedural entre TypeBot, n8n y Chatwoot.

---

## 🚀 Estructura del Repositorio

```text
.
├── docs/
│   ├── 01_manual_usuario_operadores.md
│   ├── 02_matriz_casos_de_uso.md
│   ├── 03_diseno_mensajes_e_interfaz.md
│   └── 04_arquitectura_e_integraciones.md
├── workflows/         # Exportaciones JSON de los flujos de n8n
├── typebot/           # Exportaciones JSON de los flujos de TypeBot
└── README.md
```

---

## 🛡️ Reglas de Seguridad y Trazabilidad

* **Solo Lectura:** Las consultas financieras y de cuenta corriente ejecutadas por n8n operan bajo permisos estricta y exclusivamente de lectura.
* **Trazabilidad:** Todo reclamo técnico genera un número de ticket con registro temporal único en la base de datos para seguimiento de la guardia técnica.
