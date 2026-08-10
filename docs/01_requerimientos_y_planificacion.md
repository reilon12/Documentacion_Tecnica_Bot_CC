# 📋 Requerimientos y Planificación de Proyecto: Bot CC (CUECCA)

Este documento detalla la pila de productos, los requerimientos funcionales y no funcionales, la lista de tareas organizadas por fases y el cronograma general del proyecto de automatización procedural **Bot CC**.

---

## 🎯 1. Pila de Productos (Product Backlog)

| ID | Funcionalidad | Prioridad |
| :---: | :--- | :---: |
| **01** | Mostrar en pantalla las secciones de temas que puede responder el Bot | **Alta** |
| **02** | Gestión de datos y conexión mediante MySQL | **Alta** |
| **03** | Panel de Usuario | **Alta** |
| **04** | Integración de base de datos de CUECCA (Carga y estructuración) | **Alta** |
| **05** | Panel de Administrador | **Alta** |
| **06** | Construcción de árbol de posibilidades (Camino procedural delimitado) | **Alta** |
| **07** | Historial de conversación | **Media** |
| **08** | Diseño de la experiencia conversacional | **Media** |
| **09** | Cambio de temática entre secciones (Trámites / Caja) | **Media** |
| **10** | Casos de derivaciones del usuario con un ser humano (Delegación a Chatwoot) | **Media** |
| **11** | Temas a elegir (Modo Oscuro / Claro – Extras) | **Baja** |
| **12** | Diseño e interacción de Personaje (Avatar guía identificador del Bot) | **Baja** |

---

## 📌 2. Especificación de Requerimientos

### ⚙️ Requerimientos Funcionales (RF)

* **RF01:** El sistema deberá permitir al usuario realizar consultas mediante un chat interactivo.
* **RF02:** El sistema deberá vinculables con la plataforma Chatwoot (WhatsApp Web de la empresa) para responder consultas y gestionar derivaciones.
* **RF03:** El sistema debe vincularse directamente con la base de datos de la Empresa.
* **RF04:** El sistema debe ser completamente neutral en el tono y tipo de respuestas que emite.
* **RF05:** El sistema deberá clasificar las consultas por categorías mediante rutas/caminos predefinidos.
* **RF06:** El sistema no debe perder el hilo de la conversación y debe ser reutilizable en múltiples sesiones.
* **RF07:** El sistema debe ser estrictamente **Procedural** en la totalidad del desarrollo.
* **RF08:** El sistema debe ser concreto en su alcance, impidiendo consultas fuera de sus capacidades predefinidas.
* **RF09:** El sistema deberá sustentarse de la base de datos para responder cada consulta, complementado con la información de relevamiento de campo.
* **RF10:** El sistema debe incluir gestión de roles para su utilización y administración en caso de modificaciones.

### 🛡️ Requerimientos No Funcionales (RNF)

* **RNF01:** El tiempo de respuesta del Bot no debe superar los 5 segundos por interacción.
* **RNF02:** El bot debe ser capaz de almacenar datos temporales de las consultas en caso de pérdida de conexión a internet.
* **RNF03:** El sistema debe garantizar alta disponibilidad (**24/7**).
* **RNF04:** La base de datos podrá actualizarse sin necesidad de modificar la estructura de código del Bot.
* **RNF05:** El sistema debe ofrecer compatibilidad nativa con dispositivos móviles.

---

## 📅 3. Cronograma y Plan de Trabajo (Gantt)

```mermaid
gantt
    dateFormat  YYYY-MM-DD
    title Cronograma de Desarrollo - Bot CC
    
    section Fase 1: Análisis
    T01 Definición de Arquitectura, Selección de herramientas y Casos de Uso :T01, 2026-07-04, 2026-07-11
    T02 Creación de tablero SCRUM y planificación de tareas               :T02, 2026-07-11, 2026-07-15

    section Fase 2: Diseño
    T03 Diseño de flujos conversacionales del Bot                         :T03, 2026-07-15, 2026-07-18
    T04 Diseño del primer prototipo (Figma)                               :T04, 2026-07-18, 2026-07-21
    T05 Validación y corrección del prototipo                             :T05, 2026-07-21, 2026-07-24
    T06 Capacitación y Prácticas en las tecnologías seleccionadas         :T06, 2026-07-24, 2026-08-02

    section Fase 3: Desarrollo
    T07 Construcción de los flujos de conversación en TypeBot            :T07, 2026-08-06, 2026-08-09
    T08 Configuración de preguntas, respuestas y validaciones             :T08, 2026-08-10, 2026-08-15
    T09 Integración con APIs externas (Chatwoot, n8n, WhatsApp)           :T09, 2026-08-15, 2026-08-20
    T10 Desarrollo de funcionalidades                                     :T10, 2026-08-20, 2026-08-25
    T11 Implementación de la lógica de Automatización                    :T11, 2026-08-26, 2026-08-30
    T12 Conexión a la base de datos                                       :T12, 2026-08-30, 2026-08-31
    T13 Diseño de interfaz gráfica                                        :T13, 2026-08-31, 2026-09-07
    T14 Diseño de Identidad visual del Bot (Avatar Guía)                 :T14, 2026-09-07, 2026-09-18
    T15 Preparación y presentación del prototipo en la Jornada Estudiantil:T15, 2026-09-18, 2026-09-21

    section Fase 4: Pruebas
    T16 Pruebas unitarias y Pruebas de Integración                       :T16, 2026-09-26, 2026-10-03
    T17 Corrección de errores detectados                                  :T17, 2026-10-03, 2026-10-12
    T18 Pruebas con usuarios finales                                      :T18, 2026-10-12, 2026-10-19

    section Fase 5: Implementación
    T19 Despliegue del Sistema                                            :T19, 2026-10-19, 2026-10-23
    T20 Capacitación a usuarios                                           :T20, 2026-10-23, 2026-10-29
    T21 Elaboración de documentación técnica y manual de usuario          :T21, 2026-10-12, 2026-10-30
    T22 Entrega final del Proyecto                                        :T22, 2026-11-05, 2026-11-05
