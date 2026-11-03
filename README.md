# 🤖 Bot CC — Sistema de Atención Automática y Derivación (CUECCA)

Arquitectura, flujos de automatización y documentación técnica de **Bot CC**, el asistente conversacional procedural de la Cooperativa CUECCA (Castelli Ltda.).

El bot identifica al socio y le permite consultar su deuda, facturas y consumos; ver tarifas y planes de internet; registrar reclamos técnicos de energía, agua e internet como órdenes de trabajo; y hablar con un operador cuando hace falta.

> **Estado (03-11-2026) — BOT CC v2.3:** funcional en canal web, en entorno local, con las correcciones de la auditoría aplicadas y verificadas. El canal WhatsApp está pendiente. La documentación describe la implementación real (exports del 03-11-2026 en `exports/limpios/`); donde difiere del diseño original, se marca la diferencia.

---

## 🛠️ Stack Tecnológico

| Capa | Herramienta | Rol |
|---|---|---|
| Motor conversacional | [Typebot](https://typebot.io/) | Menús, validaciones y navegación |
| Middleware / orquestador | [n8n](https://n8n.io/) | 17 webhooks: validación de entradas, consultas, reglas de negocio, formato y sesiones |
| Atención humana | [Chatwoot](https://www.chatwoot.com/) | Bandeja de operadores |
| Datos de gestión | SQL Server **SIACCOP** | Padrón, deuda, lecturas y tarifas (solo lectura) |
| Órdenes de trabajo | MySQL **SIGO** | Alta y consulta de reclamos |
| Auditoría | MySQL **Bot_CC** | Historial de conversaciones |

---

## 📚 Documentación

### Proyecto

1. [**Requerimientos y planificación**](docs/01_requerimientos_y_planificacion.md): backlog, RF/RNF con su estado y cronograma.
2. [**Especificación funcional y casos de uso**](docs/02_especificacion_funcional_y_casos.md): actores, casos de uso, reglas de negocio, flujo general y diferencias con el diseño original.
3. [**Manual de puesta en marcha, operación y mantenimiento**](docs/03_manual_despliegue_y_mantenimiento.md): instalación, qué recibe el personal, monitoreo, matriz de pruebas y contenido fijo.
4. [**Arquitectura e integraciones**](docs/04_arquitectura_e_integraciones.md): arquitectura actual y objetivo (WhatsApp), bases de datos, códigos e inventario de webhooks.
5. [**Tema visual**](docs/05_tema_visual.md): CSS del chat, colores por área y cómo regenerarlos.

### Módulos (detalle técnico)

0. [Sesiones para canales externos y manejo de errores](docs/modulos/00-sesion-usuario.md)
1. [Validación del socio y selección de domicilio](docs/modulos/01-validacion-socio.md)
2. [Deuda, facturación y consumos](docs/modulos/02-deuda-facturacion-consumos.md)
3. [Internet y tarifas](docs/modulos/03-internet-tarifas.md)
4. [Reclamos](docs/modulos/04-reclamos.md)
5. [Auditoría de conversaciones](docs/modulos/05-auditoria.md)
6. [Derivación a Chatwoot](docs/modulos/06-derivacion-chatwoot.md)

### Calidad

- [**Registro de hallazgos técnicos**](docs/hallazgos.md): problemas detectados, severidad, estado y revisión con el autor.
- Guías de corrección (aplicadas y verificadas):
    - [H-01: inyección SQL (incluye H-11)](docs/correcciones/H-01-inyeccion-sql.md)
    - [H-14: año y meses fijos en deuda y consumos](docs/correcciones/H-14-anio-fijo.md)
    - [H-28: contexto en la derivación a Chatwoot](docs/correcciones/H-28-contexto-chatwoot.md)

### Diagramas

- [Casos de uso](diagramas/casos_de_uso/README.md) (diseño de agosto de 2026)

---

## 🚀 Estructura del Repositorio

```text
.
├── README.md
├── .gitignore
├── docs/
│   ├── 01_requerimientos_y_planificacion.md
│   ├── 02_especificacion_funcional_y_casos.md
│   ├── 03_manual_despliegue_y_mantenimiento.md
│   ├── 04_arquitectura_e_integraciones.md
│   ├── 05_tema_visual.md
│   ├── hallazgos.md
│   ├── correcciones/
│   │   ├── H-01-inyeccion-sql.md
│   │   ├── H-14-anio-fijo.md
│   │   └── H-28-contexto-chatwoot.md
│   └── modulos/
│       ├── 00-sesion-usuario.md
│       ├── 01-validacion-socio.md
│       ├── 02-deuda-facturacion-consumos.md
│       ├── 03-internet-tarifas.md
│       ├── 04-reclamos.md
│       ├── 05-auditoria.md
│       └── 06-derivacion-chatwoot.md
├── estilos/
│   ├── typebot-tema-cuecca.css      # Custom CSS del tema
│   └── generar_colores_botones.py   # Regenera los colores de los submenús
├── diagramas/
│   └── casos_de_uso/
└── exports/
    └── limpios/       # Exports de n8n y Typebot revisados (sin credenciales ni datos reales)
```

---

## 🛡️ Seguridad y trazabilidad

| Regla | Estado |
|---|---|
| Las consultas sobre facturación y cuenta corriente son de solo lectura | ✅ Todas las consultas a SIACCOP son `SELECT`. Falta reforzarlo con permisos de base |
| Todo reclamo técnico genera una orden de trabajo en SIGO | ✅ Con N° de OT, que el socio ve al confirmar el reclamo (H-12) |
| Los errores de cualquier workflow se notifican | ✅ Email desde el workflow 0 (cambiar a la casilla de sistemas antes de producción) |
| Los webhooks de n8n solo son accesibles para Typebot | ⚠️ Depende del despliegue: se cumple si el puerto 5678 no se publica fuera del servidor. Para exponer n8n (por ejemplo, para WhatsApp), agregar *Header Auth* (H-03) |
| Los datos ingresados no pueden alterar las consultas | ✅ Validación y escape en n8n, verificado (03-11-2026) (H-01, H-11) |
| Los datos personales tienen retención definida | ❌ Pendiente (H-24) |

**Regla para este repositorio:** ningún archivo debe contener credenciales, tokens ni datos reales de socios. Los exports se suben solo a `exports/limpios/`, después de revisarlos.

---

## 📐 Convenciones

- Los nombres de variables, grupos y nodos se citan tal como figuran en Typebot y n8n (`así`).
- Cada módulo documenta: objetivo, flujo, contrato de los webhooks, consultas SQL, variables y hallazgos.
- Los hallazgos se numeran `H-NN` y no se renumeran: los descartados quedan tachados.
