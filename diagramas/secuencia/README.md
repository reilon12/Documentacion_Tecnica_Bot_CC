## 🔁 Diagramas de Secuencia

> **Diseño de agosto de 2026.** Describen la interacción planificada entre el socio, el bot, n8n y las bases de datos. La secuencia implementada (con los nodos de validación, el N° de OT y las etiquetas de Chatwoot) está documentada en cada [módulo](../../docs/modulos/).

Cada imagen tiene al lado su fuente `.drawio`.

| Diagrama | Módulo vigente | Diferencias principales con lo implementado |
|---|---|---|
| 1. Consulta de deuda, desglose y medios de pago | [Módulo 2](../../docs/modulos/02-deuda-facturacion-consumos.md) | El desglose (`desglose_deuda`) está desactivado |
| 2. Contrataciones y autogestión de WiFi | [Módulo 3](../../docs/modulos/03-internet-tarifas.md) | La autogestión de WiFi está como *Próximamente* |
| 3. Creación de reclamo | [Módulo 4](../../docs/modulos/04-reclamos.md) | Se agregaron la validación de entrada, la búsqueda del medidor por domicilio y la respuesta con N° de OT |
| 4. Derivación a Chatwoot | [Módulo 6](../../docs/modulos/06-derivacion-chatwoot.md) | Canal web con widget; la derivación por WhatsApp está pendiente |

### 1. Consulta de deuda, desglose y medios de pago

![Consulta de deuda](<1. Consulta de Deuda, Desglose y Medios de Pago.jpg>)

### 2. Contrataciones y autogestión de WiFi

![Contrataciones y WiFi](<2. Contrataciones y Autogestion de WIFI.jpg>)

### 3. Creación de reclamo

![Creación de reclamo](<3. Creacion de Reclamo.jpg>)

### 4. Derivación a Chatwoot

![Derivación a Chatwoot](<4. Derivacion a Chatwoot.jpg>)
