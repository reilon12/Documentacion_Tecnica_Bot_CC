# 🤖 Bot CC (CUECCA) - Documentación Técnica 

**Sistema Procedural de Atención al Cliente, Consultas y Derivación de Reclamos**

> **Proyecto Integrador de Práctica Profesional III**  
> **Institución / Cliente:** CUECCA (Cooperativa de Usuarios de Electricidad y de Consumo de Castelli Ltda.)

---

## 📌 1. Visión General y Modelo de Negocio

El **Bot CC** es una solución de software procedural diseñada para optimizar y automatizar el canal de atención al cliente de la Cooperativa CUECCA vía WhatsApp (integrado con Chatwoot) y Web. El sistema permite responder consultas frecuentes, consultar saldos y deudas por período, brindar información de requisitos para trámites y derivar eficientemente reclamos complejos hacia los sectores correspondientes (*Caja, Reclamos, Internet, Cloacas*).

### Objetivos Principales
- **Reducción de carga operativa:** Automatizar consultas masivas repetitivas (monto adeudado, fechas de vencimiento, requisitos de alta, medios de pago).
- **Precisión y Trazabilidad:** Consultar la base de datos MySQL mediante filtros estrictos (*DNI, Nombre del Titular y Domicilio*).
- **Integración Procedural:** Derivar reclamos y solicitudes técnicas a los operadores humanos en Chatwoot sin intervención de IA generativa no controlada.

---

## 🛠️ 2. Stack Tecnológico e Integraciones

| Componente | Tecnología / Herramienta | Descripción / Rol |
| :--- | :--- | :--- |
| **Motor Conversacional** | TypeBot | Construcción del flujo procedural y árbol de decisiones. |
| **Atención Omnicanal** | Chatwoot + WhatsApp API | Gestión de chats, canal oficial y derivación a operadores humanos. |
| **Middleware / Automatización** | n8n | Orquestación de flujos, validación de datos y llamados HTTP/APIs. |
| **Base de Datos** | MySQL / SQL Server | Almacenamiento y lectura de saldos, períodos, tarifas y usuarios. |

---

## 🏗️ 3. Esquema General de Arquitectura

```text
[ Usuario (WhatsApp / Web) ]
           │
           ▼
     [ Chatwoot ]
           │
           ▼
     [ TypeBot ] (Lógica Procedural / Árbol de Respuestas)
           │
           ▼
       [ n8n ] (Middleware)
      /       \
     ▼         ▼
[ Base de Datos MySQL ]   [ Operador Humano (Chatwoot) ]
(Saldos, Periodos, Tarifas)  (Derivación de reclamos)
