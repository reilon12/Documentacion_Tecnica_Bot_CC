# 📖 Manual de Puesta en Marcha, Operación y Mantenimiento: Bot CC (CUECCA)

Este documento cubre la puesta en marcha técnica, la operación por parte del personal, las pruebas de aceptación y el mantenimiento de **Bot CC**.

> **Actualización 03-11-2026.** Refleja las correcciones aplicadas y verificadas (validación de entradas, N° de OT, etiquetas de Chatwoot, celular del socio, horarios). Se agregó el procedimiento para actualizar workflows sin perder las URLs (§1.3).

---

## 🛠️ 1. Puesta en marcha técnica

> Los datos marcados *a completar* no están en los exports y los tiene que cargar el responsable del despliegue.

### 1.1 Componentes y versiones

| Componente | Versión | Dónde corre | Puerto |
|---|---|---|---|
| Typebot (builder + viewer) | *a completar* (esquema de export 6.1) | Docker | *a completar* |
| n8n | *a completar* | Host / Docker | 5678 |
| Chatwoot | *a completar* | *a completar* | 3002 |
| SQL Server (SIACCOP) | *a completar* | *a completar* | 1433 (por defecto) |
| MySQL (SIGO y Bot_CC) | *a completar* | *a completar* | 3306 (por defecto) |

### 1.2 Pasos

1. **Bases de datos:** crear los usuarios de servicio con permisos mínimos ([arquitectura §3](04_arquitectura_e_integraciones.md#-3-bases-de-datos)) y la tabla `auditoria_bot` en Bot_CC (estructura *a completar*).
2. **n8n:**
    1. Crear las credenciales con **estos nombres exactos**, que son los que esperan los workflows: `Microsoft SQL SIACCOP LOCAL`, `MySQL SIGO Local`, `MySQL Bot_CC Auditoria`.
    2. Instalar el nodo comunitario `n8n-nodes-typebot` (lo usa `0.Sesion_Usuario`) y crear su credencial de Typebot.
    3. Importar los 6 workflows (`0.Sesion_Usuario` a `5.Modulo_Auditoria`) con *Workflows → Import from file*. Importar **primero el 0**: es el manejador de errores de todos.
    4. En la configuración de cada workflow (*Settings → Error workflow*), elegir `0.Sesion_Usuario`.
    5. Activarlos. Los webhooks quedan en `http://<host>:5678/webhook/<ruta>`.
3. **Typebot:**
    1. Importar el bot (*Import* → `typebot-export-*.json`).
    2. Si n8n no está en `host.docker.internal:5678`, reemplazar la URL base en los 16 bloques HTTP Request.
    3. Configurar la credencial SMTP del bloque *Email* (reclamo particular) y la dirección de destino (H-27).
    4. Verificar que el Custom CSS del tema sea el de [`estilos/`](../estilos/typebot-tema-cuecca.css) ([tema visual](05_tema_visual.md)).
    5. Publicar.
4. **Chatwoot:** crear un inbox de tipo *Website*, copiar su `websiteToken` y cargarlo, junto con la `baseUrl` pública, en los 4 bloques Chatwoot de Typebot. Crear las 6 etiquetas y los 4 atributos personalizados ([módulo 6.4](modulos/06-derivacion-chatwoot.md#64-configuración-en-chatwoot)).
5. **Verificar:** ejecutar la [matriz de pruebas](#-4-matriz-de-pruebas-y-aceptación).

### 1.3 Actualizar un workflow existente

Para reemplazar un workflow por una versión corregida **sin perder las URLs de los webhooks**:

1. Abrir el workflow existente en n8n.
2. Seleccionar todo (Ctrl+A) y borrar.
3. Pegar el contenido del JSON nuevo (Ctrl+V) o arrastrar el archivo.
4. Revisar que las credenciales de los nodos SQL sigan asignadas.
5. Guardar y activar.

Importarlo como workflow **nuevo** crea otro ID: los webhooks pasan a estar duplicados y, si es el workflow 0, los demás pierden su *Error workflow*.

En Typebot, importar el export reemplaza el bot entero. Antes, exportar la versión actual como respaldo.

### 1.4 Para producción

| Tema | Acción | Hallazgo |
|---|---|---|
| Chatwoot | Reemplazar `localhost:3002` por la URL pública | — |
| n8n | No publicar el puerto 5678 a internet; agregar *Header Auth* a los webhooks | H-03 |
| Credenciales | Usar credenciales de producción; el sufijo `LOCAL` indica desarrollo | — |
| Email de reclamo particular | Reemplazar la casilla de prueba por la institucional del área, en el bloque *Email* de `Envio_mail_r_particular` y en el texto que se le muestra al socio | H-27 |
| Alertas de error | `Envio_Mail_Error` (workflow 0) envía a una casilla personal: cambiarla por la de sistemas | H-34 |
| Datos personales | Definir la retención de `auditoria_bot` y de los *Results* de Typebot | H-24 |
| Exports | No versionar exports sin limpiar: `variablesForTest` contiene un celular real | — |

---

## 👥 2. Operación por parte del personal

### 🛡️ 2.1 Alcance del bot

**Bot CC es un canal informativo.** No da CBU ni alias, no genera enlaces de pago y no recibe comprobantes. Así lo implementa el texto de *Métodos de pago*: el CBU se pide por email y las transferencias se informan enviando el comprobante a `tramites@cuecca.com.ar`.

> ℹ️ **Funcionalidad futura:** el menú *Declarar pagos (Próximamente)* muestra un botón "Subir comprobante". Hoy no hace nada (vuelve al menú principal) y está anunciado como próximo. Cuando se implemente, esta política cambia: habrá que definir quién valida los comprobantes, dónde se guardan y cómo se le informa el resultado al socio, y actualizar esta sección (H-30).

### 2.2 Atención en Chatwoot

**Qué recibe el operador:**

| Dato | Socio validado | Invitado |
|---|---|---|
| Identificador | N° de cuenta (`user_id`) | `invitado_<DNI>` |
| Nombre | Titular según el padrón | El que escribió la persona |
| Teléfono | Celular ingresado, en formato `+549…` (vacío si no se pudo normalizar) | — |
| Email | El del padrón | — |
| Atributos del contacto | `tipo_usuario = socio`, `ultimo_motivo` | `tipo_usuario = invitado`, `ultimo_motivo`, `dni` |
| Atributo de la conversación | `motivo_consulta` | `motivo_consulta` |
| Etiqueta | Según el motivo (tabla siguiente) | Según el motivo |

| Motivo elegido en el bot | Etiqueta |
|---|---|
| Facturación y Convenios | `caja_atencion` |
| Soporte Técnico Especializado | `reclamo_tecnico_prioridad` |
| Trámites y Cambio de Titularidad | `tramites_atencion` |
| Planes y Contrataciones | `planes_contrataciones` |
| Otra Consulta | `consulta_general` |
| (mensaje fuera de horario) | `fuera_de_horario` |

La etiqueta se asigna cuando el socio envía el primer mensaje. Se puede filtrar la bandeja por etiqueta para repartir el trabajo por área.

**Fuera de horario:** el socio ve el horario de atención (L-V 8 a 12 h y 16 a 20 h; sáb. 8 a 12 h) y puede dejar un mensaje. Esas conversaciones quedan con la etiqueta `fuera_de_horario` para el siguiente turno. Detalle técnico en el [módulo 6](modulos/06-derivacion-chatwoot.md).

### 2.3 Guardia técnica (reclamos)

Los reclamos **no llegan a Chatwoot**: se crean como órdenes de trabajo en SIGO (`orden_trabajo`, `tipo = 'RECLAMO'`), con estos datos:

| Campo | Contenido |
|---|---|
| `ot_nro_socio`, `ot_asociado` | N° de cuenta y nombre del titular |
| `ot_domicilio` | Domicilio elegido en el bot |
| `ot_medidor` | Medidor de energía o agua del domicilio elegido |
| `ot_sector`, `ot_actividad` | Tipificación según servicio y motivo ([módulo 4.4](modulos/04-reclamos.md#44-registro--registrar_reclamo)) |
| `ot_tarea` | `<motivo> - Comentario Socio: <texto> - Domicilio Socio: <texto>` |

No incluye teléfono de contacto: si la guardia necesita llamar, tiene que buscarlo en SIACCOP. El socio recibe el **N° de OT** al confirmar el reclamo y puede consultarlo después en *Consultar estado de mi reclamo*.

### 2.4 Reclamos particulares

Llegan por email a la dirección configurada en el bloque *Email* de Typebot, con asunto `RECLAMO PARTICULAR - SOCIO: <cuenta>`. Incluyen nombre, cuenta, DNI, celular, domicilios, servicio, motivo, medidor y comentario. El socio recibe la respuesta por email.

---

## 🔍 3. Monitoreo y resolución de problemas

| Síntoma | Dónde mirar | Causa probable |
|---|---|---|
| El bot no responde después de un paso | n8n → *Executions*, filtrar por error. También llega un correo de `Envio_Mail_Error` | Webhook caído, error de SQL o workflow desactivado |
| Error "Entrada inválida en el campo …" | Correo de error o ejecución fallida | El socio escribió un dato no numérico. Es el comportamiento esperado: el validador corta antes de la consulta |
| "Sin deuda" a un socio que debe | Ejecución de `deuda_total` / `deuda_servicio` | Comprobantes de prefijo 80 (H-33) o datos no cargados en SIACCOP |
| "No pudimos registrar tu reclamo" | Ejecución de `registrar_reclamo` → `insert_reclamo` | Error de MySQL o SIGO caído |
| Chatwoot no abre | Consola del navegador | `baseUrl` apunta a `localhost` |
| Chatwoot sin etiqueta o sin teléfono | [Módulo 6.5](modulos/06-derivacion-chatwoot.md#65-diagnóstico) | Etiqueta no creada; celular inválido o repetido |
| Un botón perdió su color | — | Se recreó el botón y cambió su ID ([tema visual](05_tema_visual.md)) |
| Respuestas lentas | n8n → *Executions*, columna de duración | Consultas pesadas (`deuda_servicio`) |

**Respaldo:** exportar los 6 workflows y el bot después de cada cambio, **limpiar** los exports (credenciales, `variablesForTest`, `pinData`) y guardarlos en `exports/limpios/` con la fecha.

---

## 📋 4. Matriz de pruebas y aceptación

Registrar en cada prueba la fecha, quién la hizo y el resultado.

| # | Escenario | Pasos | Resultado esperado | Resultado |
|---|---|---|---|---|
| P01 | Validación correcta | Aceptar términos → cuenta + DNI válidos | Resumen de datos y menú de socio (con deuda, factura, reclamos) | |
| P02 | Validación fallida | Cuenta o DNI incorrectos, o con letras | "No encontramos coincidencias" → Reintentar / Invitado | |
| P03 | Invitado | No aceptar términos | Menú sin opciones de socio | |
| P04 | Deuda total con varios meses | Socio con deuda en 2 o más meses | Períodos en orden cronológico y total correcto respecto de SIACCOP | |
| P05 | Deuda total sin deuda | Socio al día | Mensaje "No posee deudas" y vuelta al menú | |
| P06 | Deuda por suministro | Socio con 2 domicilios | Solo la deuda del domicilio elegido | |
| P07 | Más de 8 domicilios | Socio con 9 o más domicilios | Pide búsqueda; con texto y N° de usuario correctos encuentra el domicilio | |
| P08 | Factura digital | Socio → Descargar mi factura | Abre el portal con cuenta y DNI precargados | |
| P09 | Consumos | Socio → Suministros → Mis Consumos | Lecturas de los 3 meses anteriores al actual, por medidor | |
| P10 | Reclamo con suministro suspendido | Socio con `CodEstado = 3` | Mensaje de suspendido; no permite reclamar | |
| P11 | Reclamo correcto | Energía → Cortes de luz → comentario + domicilio | OT nueva en SIGO con los datos correctos; el bot muestra el mismo N° de OT | |
| P11b | Reclamo en el segundo domicilio | Socio con 2 domicilios → reclamo de energía en el segundo | `ot_medidor` es el del segundo domicilio | |
| P11c | Reclamo con SIGO caído | Detener MySQL o n8n → reclamo | "No pudimos registrar tu reclamo"; no muestra N° de OT | |
| P12 | Reclamo duplicado | Repetir P11 | "Ya tenés un reclamo activo" | |
| P13 | Reclamo con apóstrofo y comillas | Comentario `Corte en lo de D'Angelo, dice "error"` | OT guardada con el texto exacto | |
| P14 | Cancelar reclamo | Escribir "cancelar" en el comentario | Vuelve al menú sin crear OT | |
| P15 | Reclamo de internet fuera de horario | Domingo | Aviso de guardia; permite registrar | |
| P16 | Estado de reclamos | Socio con 2 reclamos activos → elegir el segundo | Número y estado del segundo | |
| P17 | Operador en horario | Socio, L-V 10 h → Facturación | Chatwoot con nombre, cuenta, email y celular `+549…`; al escribir, etiqueta `caja_atencion` | |
| P18 | Operador fuera de horario | Socio, L-V 13 h o 20:30 h | Aviso de horario; al dejar mensaje, etiqueta `fuera_de_horario` | |
| P19 | Operador como invitado | Invitado → nombre + DNI | Chatwoot como `invitado_<DNI>`, con atributo `dni` y sin teléfono | |
| P19b | Internet: plan sin packs | Socio con plan de 500 MB y sin packs → Mis planes y packs | Muestra la tarifa y "Sin packs adicionales" | |
| P19c | Internet: sin servicio | Domicilio sin internet → Mis planes y packs | "No dispone de servicios contratados..." | |
| P20 | Auditoría | Cualquier conversación | Una fila por respuesta en `auditoria_bot` con el mismo `result_id` | |
| P21 | Móvil | P01, P04 y P11 desde un celular | Se ven bien los textos y los botones (RNF05) | |
| P22 | Sesión por canal externo | Tres POST a `sesion_usuario` ([módulo 0.4](modulos/00-sesion-usuario.md#04-prueba)) | Una fila por celular; la segunda llamada del mismo celular continúa su sesión | |

---

## 📝 5. Contenido estático del bot

Información escrita directamente en Typebot. **No se actualiza desde la base:** cualquier cambio requiere editar el bot y volver a publicarlo.

| Contenido | Grupo en Typebot | Responsable de revisar | Observación |
|---|---|---|---|
| Horarios de atención | `Horario de atención`, `Horario_no_laboral` | *a definir* | L-V 8 a 12 h y 16 a 20 h; sáb. 8 a 12 h. Si cambian, actualizar también el código de `horario_laboral` (módulo 6) |
| Horario de internet | `Fuera_de_horario` | *a definir* | **Distinto:** L-V 8 a 19 h corrido. Confirmar si es intencional |
| Teléfonos de guardia | `Horario de atención`, `Fuera_de_horario` | *a definir* | Electricidad, agua, sepelio, internet, administración, canal 4 |
| Métodos y lugares de pago | `Metodos de pago`, `metodos_pago`, `Metodos_de_pago_deuda_2` | Caja | **Tres copias** del mismo texto: hay que actualizar las tres |
| Requisitos de alta | `Requisitos_Propietarios`, `_Comerciantes`, `_inquilinos` | Trámites | — |
| Tiempos de reconexión | `msj_reconexion` | Trámites | 48 a 72 h hábiles (energía/agua); inmediata (internet) |
| Cambio de titularidad | `info_cambio_titularidad` | Trámites | **Sin contenido:** el texto dice solo "info" (H-29) |
| Instructivo de agendas de pago | `Instructivo_agendas_pago` | Caja | **Video sin cargar** (H-29) |
| Imagen de ayuda (dónde está el N° de cuenta) | `Bienvenida…`, `Validación de usuario` | — | Alojada en imgur: depende de un servicio externo. Verificar que no muestre datos reales |
| Enlaces externos | `Modulo Informacion General`, `Tarifa_Social_link`, `Subsidio_energetico` | *a definir* | 13 URLs (OCEBA, gob.ar, Google Drive, simulador PEBA). Revisar que sigan vigentes |

---

## 🔄 6. Plan de mantenimiento

| Frecuencia | Tarea | Responsable |
|---|---|---|
| Ante cada cambio regulatorio u operativo | Actualizar requisitos, horarios, teléfonos y métodos de pago (§5) | Administración |
| Trimestral | Revisar que los 13 enlaces externos funcionen | *a definir* |
| Mensual | Revisar en n8n → *Executions* los errores del mes | Sistemas |
| Mensual | Volumen de derivaciones por etiqueta en Chatwoot, para evaluar nuevas opciones automáticas | Atención al socio |
| Después de agregar o recrear botones | Regenerar los colores ([tema visual §4](05_tema_visual.md#4-regenerar-los-colores-después-de-cambiar-el-flujo)) | Desarrollo |
| Mensual | Depurar `auditoria_bot` según la política de retención que se defina (H-24) | Sistemas |
| Después de cada cambio en los flujos | Exportar, limpiar y versionar los exports; actualizar esta documentación | Desarrollo |
| Ante un pack adicional nuevo o renombrado | Agregar o corregir su `Descripcion` exacta en la lista `IN (...)` de `SQL_suscripciones_filtro` y, si hace falta, su nombre comercial en `Code_mapeo_suscripciones` (workflow 3) | Desarrollo |
| Ante un plan de internet nuevo | Verificar que su código de tarifa no contenga `25` ni `50`, porque `Code_mapeo_texto` excluye esos códigos para ocultar los planes de 25 y 50 MB. Si no tiene nombre comercial en ese nodo, se muestra la descripción de la base | Desarrollo |
