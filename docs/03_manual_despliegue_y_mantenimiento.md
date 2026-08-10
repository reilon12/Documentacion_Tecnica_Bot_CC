# 📖 Manual de Puesta en Marcha, Capacitación y Mantenimiento: Bot CC (CUECCA)

Este documento establece las pautas organizacionales, procedurales y operativas para la implementación, uso por parte del personal y mantenimiento continuo del sistema **Bot CC** en la Cooperativa CUECCA (Castelli Ltda.).

---

## 📌 1. Fases del Proceso de Puesta en Marcha

El despliegue del sistema Bot CC no involucra modificaciones en la infraestructura central de CUECCA, sino la vinculación procedural de los canales existentes mediante tres etapas consecutivas:

1. **Etapa 1: Parametrización y Carga de Reglas:**
   * Verificación de la vigencia de los requisitos de trámites para los 4 servicios (Energía, Agua, Cloacas e Internet).
   * Confirmación de los horarios de atención y canales de pago habilitados (RedLink, Cuenta DNI, Cajas presenciales).
   * Carga de las plantillas de respuesta e instructivos procedurales dentro de la plataforma conversacional.

2. **Etapa 2: Vinculación de Canales y Pruebas Piloto:**
   * Conexión de la línea oficial de WhatsApp de CUECCA con la plataforma de gestión de atención (Chatwoot).
   * Ejecución de pruebas internas con personal de prueba para validar el correcto ruteo hacia las áreas de **Caja** y **Trámites / Reclamos**.

3. **Etapa 3: Lanzamiento y Operación en Vivo:**
   * Habilitación del bot para el público general.
   * Monitoreo inicial de conversaciones para ajustar la claridad de los menús y las respuestas procedurales.

---

## 👥 2. Protocolo de Operación y Uso para el Personal

El sistema automatiza las consultas masivas y derivaciones, pero requiere la intervención del personal administrativo y técnico en casos específicos. 

### 🛡️ 2.1. Política de Seguridad Operativa (Alcance del Bot)
**El Bot CC es un canal estrictamente informativo.** Bajo ninguna circunstancia el bot está autorizado para proporcionar alias, CBU, enlaces de pago directos, ni para recibir o validar comprobantes de transferencia.
* Toda consulta que requiera enviar un comprobante de pago o solicitar un alias para transferencia, activa inmediatamente la derivación a Chatwoot (Tag: `Caja_Atencion`).
* **La conciliación de pagos y verificación de comprobantes es potestad y responsabilidad exclusiva del personal humano de CUECCA (Caja / Tesorería).**

### 2.2. Sector Caja (Tesorería)
* **Atención de Derivaciones (Tag: `Caja_Atencion`):**
  * El operador recibe los chats donde el usuario solicita atención personalizada, planes de cuotas, envío de comprobantes de transferencia (alias/CBU) o reporta inconsistencias con su estado de cuenta.
  * El personal verifica en el sistema de gestión el historial del socio, comprueba los pagos enviados y responde directamente desde la plataforma Chatwoot.

### 2.3. Sector Trámites y Mesa de Entradas
* **Atención de Derivaciones (Tag: `Tramites_Atencion`):**
  * El personal recibe las solicitudes de usuarios que desean iniciar trámites presenciales o que requieren documentación especial no estandarizada.
  * Se brinda el turno o la indicación puntual antes de finalizar la sesión.

### 2.4. Sector Reclamos y Guardia Técnica
* **Atención de Reclamos Prioritarios (Tag: `Reclamo_Tecnico_Prioridad`):**
  * El área técnica visualiza los tickets ingresados por el bot que contienen: **Servicio afectado**, **Motivo del reclamo**, **Domicilio del incidente** y **Teléfono de contacto**.
  * El operador asigna la cuadrilla correspondiente y actualiza la novedad para comunicar al usuario la resolución de la falla.

---

## 📋 3. Matriz de Control de Pruebas y Aceptación

Antes de dar por completada la implementación, se debe verificar el cumplimiento funcional del sistema mediante la siguiente planilla de chequeo:

| Escenario de Prueba | Canal | Comportamiento Esperado | Criterio de Aprobación |
| :--- | :---: | :--- | :--- |
| **Consulta de Deuda Vencida** | WhatsApp | El usuario ingresa su DNI/Socio y el sistema lista los períodos impagos con su monto. | Desglose claro de períodos impagos e instrucciones informativas para agregar la cuenta a RedLink / CuentaDNI. |
| **Consulta de Usuario Al Día** | WhatsApp | El usuario ingresa DNI sin deuda y el sistema informa saldo $0. | Confirmación de estado al día e información de emisión del último comprobante. |
| **Intento de Envío de Comprobante / Pago** | WhatsApp | El usuario intenta enviar una imagen de pago o solicita un Alias/CBU. | Derivación inmediata y obligatoria a Chatwoot para atención humana en Caja. |
| **Error en Validación de DNI** | WhatsApp / Web | El usuario se equivoca de DNI 2 veces seguidas. | El sistema detiene los reintentos y deriva al operador de Caja. |
| **Consulta de Requisitos de Internet** | Web | El usuario consulta costo y requisitos de alta de fibra óptica. | Despliegue de texto procedural con planes, costos y tiempos de instalación. |
| **Registro de Reclamo Técnico** | WhatsApp | El usuario reporta interrupción de energía e ingresa su domicilio. | Generación de número de ticket y derivación prioritaria a la Guardia. |

---

## 🔄 4. Plan de Mantenimiento y Actualización Continua

Para garantizar la vigencia del sistema a lo largo del tiempo, se establecen las siguientes rutinas de mantenimiento organizativo:

1. **Revisión Trimestral de Requisitos y Tarifas:**
   * El área administrativa debe revisar y actualizar los textos de requisitos (documentación para altas de luz, agua, cloacas e internet) cada vez que la cooperativa o los marcos regulatorios (como OCEBA) modifiquen los procedimientos.
2. **Evaluación de Etiquetas y Flujos de Derivación:**
   * Control mensual del volumen de conversaciones derivadas bajo los tags `Caja_Atencion`, `Tramites_Atencion` y `Reclamo_Tecnico_Prioridad` para identificar si se deben agregar nuevas opciones automáticas al menú principal.
3. **Depuración de Registros de Reclamos:**
   * Archivo periódico de las planillas o registros de reclamos resueltos para mantener la agilidad en la consulta de reclamos activos.
