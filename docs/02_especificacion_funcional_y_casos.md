# ⚙️ Especificación Funcional y Casos de Uso: Bot CC (CUECCA)

Este documento contiene la especificación técnica completa del proyecto **Bot CC**. Define la matriz de casos de uso detallada, las reglas de negocio aplicadas a los dos sectores operativos de la cooperativa (**Caja** y **Trámites / Reclamos**), las consultas e integraciones con la base de datos MySQL y el diagrama de flujo procedural.

---

## 📌 1. Matriz Ampliada de Casos de Uso

| ID Caso | Sector / Módulo | Caso de Uso | Descripción | Disparador / Actor | Requerimientos |
| :---: | :--- | :--- | :--- | :--- | :---: |
| **CU01** | Menú Principal | Selección de Sector | Presenta la división primaria: Sector Caja o Sector Trámites y Reclamos. | Usuario abre el chat en WhatsApp/Web. | RF01, RF05, RF08 |
| **CU02** | Caja | Consulta de Deuda e Impagos | Valida el DNI o N° de Socio en MySQL y devuelve los períodos pendientes con monto total y enlace de pago. | Selección de "Caja" e ingreso de datos. | RF03, RF09, RNF01 |
| **CU03** | Caja | Obtención de Comprobantes | Devuelve el último comprobante o cupón de pago para usuarios que no registran deuda. | Validación de cuenta en MySQL sin deuda activa. | RF03, RF09 |
| **CU04** | Trámites | Requisitos por Servicio | Muestra la documentación y pasos para alta, baja o cambio de titularidad en Energía, Agua, Cloacas e Internet. | Selección del servicio y tipo de trámite. | RF07, RF08 |
| **CU05** | Reclamos | Registro Técnico | Toma los datos del reclamo (falla, corte, daño) junto al domicilio del usuario y guarda el registro en MySQL. | Selección de "Reclamo Técnico / Emergencia". | RF03, RF07, RNF02 |
| **CU06** | Integración | Handover a Chatwoot | Suspende las respuestas del bot, asigna la etiqueta contextual y deriva la sesión a la bandeja de un operador humano. | Solicitud explícita, reclamo o fallo reiterado de validación. | RF02, RNF03 |

---

## 🔀 2. Diagrama de Flujo Procedural

```mermaid
graph TD
    A[Inicio: WhatsApp / Web] --> B[Bienvenida & Menú Principal]

    %% SECTOR 1: CAJA
    B --> C[1. Sector Caja / Facturación]
    C --> C1[Solicitar DNI / CUIT o N° de Socio]
    C1 --> C2[Consulta MySQL: Deudas y Estado]
    C2 --> C3{¿Validación Exitosa?}
    
    C3 -- No / Sin Registro --> C4[Notificar Error / Permitir 2° Intento]
    C4 --> C1
    C4 -- Falla Reincidente --> H1[Derivación a Chatwoot: Tag 'Caja_Atencion']

    C3 -- Sí --> C5{¿Registra Deuda?}
    C5 -- Con Deuda --> C6[Mostrar Períodos Pendientes + Link de Pago Web]
    C5 -- Al Día --> C7[Informar Estado al Día + Enviar Comprobante]
    C6 & C7 --> Z1{¿Desea Derivar a Cajero?}
    Z1 -- Sí --> H1
    Z1 -- No --> END1[Fin de Sesión]

    %% SECTOR 2: TRÁMITES Y RECLAMOS
    B --> D[2. Sector Trámites y Reclamos]
    D --> D1[Seleccionar Servicio: Energía / Agua / Cloacas / Internet]
    D1 --> D2{Tipo de Solicitud}

    %% SUBFLUJO TRÁMITES
    D2 -- 1. Trámites y Requisitos --> T1[Seleccionar: Alta / Cambio Titular / Baja]
    T1 --> T2[Consultar Requisitos y Horarios en MySQL]
    T2 --> T3[Desplegar Pasos Procedurales y Documentación]
    T3 --> Z2{¿Solicitar Atención Presencial?}
    Z2 -- Sí --> H2[Derivación a Chatwoot: Tag 'Tramites_Atencion']
    Z2 -- No --> END2[Fin de Sesión]

    %% SUBFLUJO RECLAMOS
    D2 -- 2. Reclamo Técnico / Emergencia --> R1[Seleccionar Motivo: Corte / Intermitencia / Daño]
    R1 --> R2[Solicitar Domicilio del Incidente y Teléfono]
    R2 --> R3[INSERT INTO reclamos_temporales en MySQL]
    R3 --> R4[Generar N° de Ticket]
    R4 --> H3[Derivación Urgente a Chatwoot: Tag 'Reclamo_Tecnico_Prioridad']
