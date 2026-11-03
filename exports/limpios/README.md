# Exports limpios

Exports de n8n y Typebot **revisados** antes de subirlos. Al limpiar se reemplaza o quita:

| Dato | Tratamiento |
|---|---|
| Credenciales de n8n | Se conserva solo el **nombre** (`Microsoft SQL SIACCOP LOCAL`, etc.); se quita el ID |
| `variablesForTest` (Typebot) | Vaciado: contenía un celular real |
| `pinData`, `staticData`, `meta` (n8n) | Quitados |
| `websiteToken` de Chatwoot | `<WEBSITE_TOKEN>` |
| Correos de destino y remitente | `<EMAIL_DESTINO>` / `<EMAIL>` |
| IDs de workspace, carpeta y dominio (Typebot) | Quitados |

Al importar, reasignar las credenciales en n8n, cargar el `websiteToken` en los 4 bloques Chatwoot y los correos en el bloque *Email* (reclamo particular) y en `Envio_Mail_Error`.

Nombre: `AAAA-MM-DD_<herramienta>_<nombre>.json`.

## Versión vigente (03-11-2026)

| Archivo | Contenido |
|---|---|
| `2026-11-03_n8n_0.Sesion_Usuario.json` | Sesiones para canal externo y manejador de errores ([módulo 0](../../docs/modulos/00-sesion-usuario.md)) |
| `2026-11-03_n8n_1.Validaciones_Socio.json` | [Módulo 1](../../docs/modulos/01-validacion-socio.md) |
| `2026-11-03_n8n_2.consultar_deuda.json` | [Módulo 2](../../docs/modulos/02-deuda-facturacion-consumos.md) |
| `2026-11-03_n8n_3.Modulo_Internet.json` | [Módulo 3](../../docs/modulos/03-internet-tarifas.md) |
| `2026-11-03_n8n_4.Modulo_Reclamos.json` | [Módulo 4](../../docs/modulos/04-reclamos.md) |
| `2026-11-03_n8n_5.Modulo_Auditoria.json` | [Módulo 5](../../docs/modulos/05-auditoria.md) |
| `2026-11-03_typebot_BOT-CC-v2.3.json` | Bot completo, con el tema visual incluido |

Importación sin perder las URLs de los webhooks: [manual §1.3](../../docs/03_manual_despliegue_y_mantenimiento.md#13-actualizar-un-workflow-existente).
