# Registro de hallazgos técnicos

Problemas detectados al documentar el sistema a partir de los exports del 29-10-2026. Cada uno queda **A verificar** hasta confirmarlo con una prueba real. **Confirmado** significa que el problema se ve directamente en el código y no depende de cómo se comporte en ejecución.

## Resumen

| ID | Severidad | Módulo | Hallazgo | Estado |
|---|---|---|---|---|
| H-01 | Crítica | Todos | Inyección SQL: los valores del socio se pegan en el texto de las consultas | ✅ **Verificado por el autor (03-11-2026)**: validación y escape en los 5 workflows de n8n |
| H-02 | Crítica | Validación | `identificar_socio` con teléfono vacío o corto devuelve el padrón (hoy ocurre en cada sesión web) | ✅ **Verificado por el autor (03-11-2026)**: Typebot no llama sin celular; n8n exige 10 dígitos y compara por igualdad |
| H-03 | Crítica* | General | Webhooks de n8n sin autenticación (*depende de si n8n queda accesible desde la red) | Depende del despliegue |
| H-11 | Crítica | Reclamos / general | El `INSERT` del reclamo y los body JSON se rompen con comillas o apóstrofos | ✅ **Verificado por el autor (03-11-2026)**: body con `JSON.stringify` en Typebot y escape en el `INSERT` |
| H-04 | Media | Validación | Typebot decide la validación con `user_nombre` y no con `valido` | ✅ **Verificado por el autor (03-11-2026)** |
| H-05 | Alta | Validación | El reconocimiento por celular no funciona (mapeo `data` vs `data[0]`) | Mapeo **corregido** en el flujo `typebot-BOT-CC-correcciones.json`. El resto, diferido hasta WhatsApp (H-06) |
| H-06 | Alta | Validación | El reconocimiento por celular deja la sesión incompleta | Confirmado: corregir antes de WhatsApp |
| ~~H-07~~ | — | General | ~~El menú no restringe opciones a invitados~~ | **Descartado** |
| H-12 | Media | Reclamos | Si el insert **falla**, Typebot igual informa éxito | ✅ **Verificado por el autor (03-11-2026)**: n8n responde `{ok, nro_ot}` y Typebot muestra el N° de OT o el mensaje de error |
| H-13 | Baja | Reclamos | N° de OT con `MAX()+1`: duplicados solo con inserciones simultáneas | Riesgo aceptado (volumen bajo) |
| H-14 | Alta | Deuda / consumos | Año 2026 y meses 7-8-9 fijos; períodos ordenados como texto | ✅ **Resuelto**: deuda (02-11-2026) y consumos con ventana de 3 meses (03-11-2026), verificados por el autor → [H-14](correcciones/H-14-anio-fijo.md) |
| H-15 | Alta | Deuda | Sepelio dentro del agua sumado dos veces; sepelio aparte (prefijo 34) no se mostraba | ✅ **Resuelto (02-11-2026)**: deuda total y deuda por suministro verificadas por el autor |
| H-08 | Media | Validación / reclamos | El domicilio del reclamo es correcto, pero el medidor y el código no dependen del domicilio elegido | ✅ **Verificado por el autor (03-11-2026)**: el medidor sale del domicilio elegido |
| H-16 | Media | Deuda | Casos "sin deuda" resueltos por error y un callejón sin salida | ✅ **Verificado por el autor (03-11-2026)** |
| H-17 | Media | Reclamos | El estado mostrado siempre es el del primer reclamo | ✅ **Verificado por el autor (03-11-2026)** |
| H-18 | Media | Reclamos | Mapeos incorrectos en la rama Internet | ✅ **Verificado por el autor (03-11-2026)** |
| H-19 | Media | Reclamos | "Cañería tapada" nunca se tipifica como cloacas | ✅ **Verificado por el autor (03-11-2026)**: tildes normalizadas en `mapeo_*` |
| H-20 | Media | Reclamos | Criterios de "reclamo abierto" inconsistentes y búsqueda parcial de domicilio | ✅ **Verificado por el autor (03-11-2026)**: `ot_cierre IN (1, 3)` y domicilio por igualdad |
| H-21 | Baja | Facturación | La URL del portal se arma con el DNI aunque la validación SQL falle | Aceptado: los datos ya vienen validados en la sesión |
| H-22 | Media | Tarifas | Tarifas sin filtro de domicilio; valores tomados por posición | Parcial: **Corregido en n8n (03-11-2026)**, pendiente de prueba: `n8n-corregidos/` (socio entre comillas y `Activo = 1`). Sigue sin filtro de domicilio y con valores por posición |
| H-24 | Media | Auditoría | Datos personales guardados sin política de retención | Confirmado |
| H-09 | Media | Validación / Deuda | Cadena de domicilio triplicada (una copia muerta); la rama de deuda no asigna el domicilio buscado | ✅ **Verificado por el autor (03-11-2026)**: copia muerta eliminada; quedan dos cadenas (una por rama), ambas conectadas |
| H-10 | Baja | Validación / Chatwoot | `1.1_user_email` nunca se asigna | ✅ **Verificado por el autor (03-11-2026)** |
| H-23 | Baja | Internet | Catálogo de planes y packs mantenido en el código | ✅ **Verificado por el autor (03-11-2026)**: `tiene packs` / `no tiene packs`, `LEFT JOIN USUITEM_I`. Catálogo en código: aceptado |
| H-25 | Baja | General | Webhooks expuestos que no se usan | ✅ **Resuelto (02-11-2026)**: desactivados en n8n y Typebot; se conservan para uso futuro |
| ~~H-26~~ | — | Deuda | ~~Conversión de fecha de vencimiento~~ | **Cerrado:** validado por el autor |
| H-27 | Baja | Reclamos | El reclamo particular llega a una casilla personal (desarrollo) en lugar de una del área | Aceptado: dirección fija. Pendiente: cambiar a la casilla institucional antes de producción |
| H-28 | Media | Derivación | Chatwoot no recibe el motivo ni etiquetas; al invitado se le carga el DNI como teléfono | ✅ **Resuelto (02-11-2026)**: etiquetas verificadas en Chatwoot → [H-28](correcciones/H-28-contexto-chatwoot.md) |
| H-29 | Baja | Contenido | "Cambio de titularidad" sin contenido y video del instructivo sin cargar | Pendiente de contenido: se carga cuando el área entregue la información y el video |
| H-30 | Baja | Contenido / política | "Subir comprobante" (próximamente) contradice la política de que el bot no recibe comprobantes | Aceptado (03-11-2026): funcionalidad futura, anunciada como "Próximamente". Se revisa la política cuando se implemente |
| H-31 | Media | Derivación | Variable entre comillas en el código: todos los invitados podrían compartir un contacto en Chatwoot | ✅ **Resuelto (02-11-2026)**: misma corrección que H-28, verificada |
| H-32 | Baja | Diseño 2.0 | 3 bloques *Set variable* asignan `{{av_normal}}`, `{{av_contento}}` y `{{av_procesando}}` a una variable que ya no existe | ✅ **Resuelto (03-11-2026)**: el autor borró los 3 bloques *Set variable* |
| H-33 | Media | Deuda | Comprobantes de prefijo 80 (servicio vacío) no aparecen en ninguna consulta de deuda | A definir con el autor qué concepto es |
| H-34 | Alta | Sesión | `Continuar_sesion` enviaba el texto literal `$json.session_id` como sessionId y el mensaje anterior en lugar del actual | **Corregido**, pendiente de prueba específica: el canal web no llama a `sesion_usuario` (la prueba de 3 sesiones web simultáneas del 03-11 valida Typebot y la auditoría, no este workflow). Probar con POST `{celular, mensaje}` al webhook. Quedan 3 preguntas abiertas |
| H-35 | Baja | Horarios | El código de derivación usa 8–12 y 16–20, pero los textos decían 16–19 (`Horario de atención`) y 15–19 (`Horario_no_laboral`) | ✅ **Corregido (03-11-2026)**: el autor confirmó 16–20; textos actualizados en `typebot-BOT-CC-final.json` |

## Orden de corrección sugerido

1. **Antes de exponer el bot fuera de la red local:** H-03, H-01, H-11, H-02.
2. **Integridad de los datos que ve el socio:** H-14 (corrección lista), H-15 (verificar), H-12, H-17.
3. **Antes de pasar a WhatsApp:** H-02, H-04, H-05, H-06.
4. El resto, junto con la limpieza de código muerto (H-09, H-25).

## Revisión con el autor (30-10-2026)

| ID | Respuesta del autor | Conclusión |
|---|---|---|
| H-02 | El login por celular está pensado para WhatsApp, donde el número lo da el canal | La intención es correcta. Pero el webhook ya se llama hoy, en cada sesión web, con `telefono` vacío (ver detalle) |
| H-03 | Los datos siempre vienen validados desde Typebot | La validación ocurre en Typebot; n8n acepta cualquier pedido que le llegue. Ver detalle |
| H-04 | La validación depende de que socio y DNI coincidan en la base | Correcto del lado de n8n. El riesgo está en la condición de Typebot, y hoy no se puede dar porque el Camino A no funciona. Queda latente hasta WhatsApp |
| H-05 | Todavía no funciona por lo de WhatsApp | Coincidimos. Al habilitar WhatsApp hay que corregir el mapeo a `data[0]` y el formato del número (ver H-02) |
| H-06 | Con el celular el sistema ya reconoce al socio | Reconoce *quién es*, pero no carga sus datos de sesión. Ver detalle |
| H-07 | El menú filtra por `usuario_valido` (1 socio / 0 invitado) | **Correcto. Hallazgo descartado:** las opciones de socio tienen *display condition* `usuario_valido = 1` |
| H-08 | Se probaron reclamos en distintos domicilios del mismo socio sin problemas | El domicilio viaja bien. Lo que no depende del domicilio es el **medidor**. Ver prueba sugerida |
| H-09 | Se va a eliminar la copia muerta | Pendiente |
| H-10 | Solo se usa en Chatwoot | Se mantiene: hoy Chatwoot siempre recibe el email vacío |
| H-12 | El reclamo se inserta apenas se hace | Correcto cuando el insert funciona. El hallazgo es sobre el caso de **falla**. Ver prueba sugerida |
| H-13 | Muchas pruebas sin duplicados; el bot bloquea reclamos repetidos | El bloqueo es por socio y domicilio; no impide que dos socios distintos inserten al mismo tiempo. Las pruebas de a una no pueden reproducirlo. Con el volumen esperado la probabilidad es baja: riesgo aceptado, baja a severidad Baja |
| H-14 | Pidió la corrección | Entregada en [correcciones/H-14](correcciones/H-14-anio-fijo.md). Incluye un error de orden en el JS que ya ocurre en 2026 |
| H-15 | Siempre sale el mes nuevo | El hallazgo no es sobre qué meses aparecen, sino sobre si el mismo importe se suma dos veces. Se resuelve con la consulta de verificación |
| H-21 | Depende de datos de la sesión ya validados | Correcto para el flujo de Typebot. Baja a severidad Baja |
| H-25 | Se conservan para uso futuro | Decisión válida. Recomendación: desactivar el nodo Webhook (como `vincular_socio_reclamo`) conserva el código y cierra la URL |
| H-26 | Fórmula validada | Cerrado |

---

## Críticos

### H-01 · Inyección SQL en todos los workflows

Todas las consultas `executeQuery` arman el SQL pegando valores recibidos: `'{{ $json.body.cuenta }}'`, `dni`, `codigo`, `telefono`, `domicilio_buscado`, `socio`, `domicilio_limpio`. Hay casos sin comillas, que son todavía más fáciles de explotar y que además fallan con error de sintaxis si el valor llega vacío:

| Nodo | Expresión |
|---|---|
| `Deuda_Servicio_Sepelio` | `d.NroSocio = {{ $json.socio }}` |
| `Consulta_Tarifas_usuario` | `Socio = {{ $json.body.numCuenta }}` |
| `Reclamos_Activos` / `Reclamos_Cerrados` | `ot_nro_socio = {{ ...nro_socio }}` |

**Corrección:** [correcciones/H-01-inyeccion-sql.md](correcciones/H-01-inyeccion-sql.md). Incluye también H-11 y el caso de teléfono vacío de H-02.

Lineamientos generales:

1. Agregar un nodo Code de validación al inicio de cada webhook: `cuenta`, `socio`, `dni`, `codigo`, `telefono` solo dígitos y con largo acotado; si no cumple, responder error sin consultar la base.
2. Para texto libre (`domicilio_buscado`), usar una lista blanca de caracteres y duplicar las comillas simples.
3. En MySQL, usar las operaciones *Insert* / *Select* del nodo o *Query Parameters*, que parametrizan los valores. En SQL Server, verificar si la versión instalada del nodo acepta parámetros; si no, usar stored procedures.
4. Dar permisos mínimos a los usuarios de base (ver [arquitectura](04_arquitectura_e_integraciones.md#-3-bases-de-datos)).

### H-02 · Búsqueda por celular con `LIKE '%...%'`

**Contexto:** el reconocimiento por celular está pensado para WhatsApp, donde el canal entrega el número del socio. En la versión web, `user_cel` no tiene valor al iniciar.

**Problema actual (web):** `Bienvenida y Verificacion` llama a `identificar_socio` **en cada sesión**, aunque `user_cel` esté vacío. El body queda `{"telefono": ""}`, el filtro `LIKE '%%'` coincide con todas las filas y la consulta devuelve los tres padrones completos (nombre, DNI, domicilio y celular) a n8n y a Typebot cada vez que alguien abre el chat. El bot sigue funcionando solo porque Typebot lee `data.nombre` sobre un array (H-05).

**Verificación:** en n8n → *Executions*, abrir una ejecución reciente de `Webhook_celular` y ver cuántos ítems devolvió `SQL_validacion_celular`.

**Problemas para WhatsApp:**

- WhatsApp entrega el número en formato internacional (`549` + característica + número). `LIKE '%5492245...%'` no coincide con un valor guardado como `2245...`: la búsqueda está invertida respecto de lo que se necesita.
- Un número parcial coincide con muchos socios y se toma el primero por `ORDER BY Socio`.
- Un mismo celular puede estar cargado en varias cuentas (por ejemplo, de una misma familia) y la consulta no lo contempla.
- No filtra `Activo = 1`.

**Corrección:**

1. Ya: no llamar a `identificar_socio` si `user_cel` está vacío (agregar una condición antes del webhook) y, en n8n, rechazar teléfonos de menos de 10 dígitos.
2. Para WhatsApp: normalizar los dos lados a los últimos 10 dígitos, comparar por igualdad, filtrar activos y, si hay más de una cuenta, pedir que elija.

### H-03 · Webhooks sin autenticación

**Qué significa:** un webhook de n8n es una URL HTTP pública para quien pueda llegar a ese puerto. n8n no sabe si el pedido viene de Typebot o de cualquier otro programa: ejecuta el workflow con el body que reciba. Las validaciones que hace Typebot (aceptar términos, validar cuenta + DNI, elegir domicilio) ocurren **dentro de Typebot**. Quien llame directamente a n8n no pasa por ninguna de ellas. Por ejemplo, desde cualquier equipo que llegue al puerto:

```bash
curl -X POST http://<host>:5678/webhook/deuda_total \
     -H "Content-Type: application/json" -d '{"socio":"12345"}'
```

Eso devuelve la deuda del socio 12345 sin conocer su DNI. Lo mismo vale para `registrar_reclamo` (crea una OT en SIGO a nombre de cualquiera) y para `identificar_socio` con teléfono vacío (H-02).

**Qué lo hace más o menos grave:** Typebot llama a los webhooks desde el servidor (`isExecutedOnClient: false`), así que el navegador del socio nunca ve las URLs de n8n. Por eso el riesgo depende del despliegue:

| Despliegue de n8n | Riesgo |
|---|---|
| Solo en la red interna de Docker, sin puerto publicado | Bajo |
| Puerto 5678 accesible en la LAN de la cooperativa | Medio: cualquier equipo de la red |
| Accesible desde internet (para Typebot en la nube o WhatsApp) | Crítico |

**Corrección:** las dos medidas se complementan.

1. **Red:** n8n accesible solo desde Typebot (misma red de Docker o firewall).
2. **Autenticación:** en cada nodo Webhook, *Authentication → Header Auth* con un secreto. En Typebot, agregar ese header en cada bloque HTTP Request.

### H-11 · Texto libre que rompe consultas y JSON

Dos problemas con la misma causa: el texto se inserta sin escapar.

1. **SQL (`insert_reclamo`):** `ot_tarea`, `ot_asociado` y `ot_domicilio` se pegan entre comillas simples. Un comentario como *"no anda la luz en lo de D'Angelo"* rompe el `INSERT` y el reclamo se pierde. Además es inyección SQL con escritura sobre SIGO.
2. **JSON (Typebot):** los body se arman como texto: `"comentario": "{{4.5_reclamo_comentario}}"`. Una comilla doble o un salto de línea en el comentario genera JSON inválido. El nodo `Limpiar_Domicilio` tiene un parser con expresiones regulares justamente para tolerar esto, lo que muestra que ya pasó.

**Corrección:** en n8n, usar la operación *Insert* del nodo MySQL (parametrizada). En Typebot, armar los campos de texto libre con `{{=JSON.stringify({{variable}})=}}`, como ya hace el webhook de auditoría.

## Altos

### H-04 · La validación se decide con `user_nombre`

La regla de negocio es correcta: `vincular_socio` solo devuelve datos si socio y DNI coinciden con un registro activo. El punto débil está en Typebot, que no decide con el resultado (`valido`) sino con `user_nombre Is set`.

Escenario, posible solo cuando funcione el Camino A (WhatsApp):

1. El celular se reconoce y se carga `user_nombre` con el nombre del titular.
2. La persona no sabe el número de cuenta, pasa a validar por datos y escribe cualquier cuenta y DNI.
3. `vincular_socio` responde `[{"valido": false}]`. Si Typebot no borra `user_nombre` cuando `data[0].user_nombre` no existe, la condición se cumple y entra como socio válido, con `user_id` = la cuenta que escribió.

Hoy no puede ocurrir porque el paso 1 no funciona (H-05). El comportamiento de Typebot en el paso 3 no lo pude confirmar.

**Corrección (dos cambios chicos):** mapear `data[0].valido` a una variable propia y condicionar sobre ella, y vaciar `user_nombre` y `user_id` con un *Set variable* al entrar en `Validación de usuario`.

### H-05 · El reconocimiento por celular no funciona todavía

Diferido hasta tener el canal de WhatsApp. Al habilitarlo hay que corregir además el mapeo: `Respuesta_celular` devuelve un array, así que Typebot debe leer `data[0].nombre` y `data[0].Socio`. El formato del número también tiene que cambiar (H-02).

### H-06 · Sesión incompleta tras el reconocimiento por celular

Que el sistema reconozca al socio por su celular no significa que cargue sus datos de sesión. El Camino A solo carga `user_nombre` y `user_id`. Todo lo demás lo carga `vincular_socio`, que en ese camino no se llama:

| Variable | Sin `vincular_socio` | Efecto |
|---|---|---|
| `usuario_valido` | No se asigna | El menú aplica sus *display conditions* (`= 1`) y el socio ve **solo las opciones de invitado** |
| `1.1_user_domicilios` | Vacía | La selección de domicilio no tiene botones |
| `user_dni` | Vacío | `generar_link_factura` arma la URL sin DNI |
| `1.1_nro_usuario`, medidores | Vacíos | Internet y reclamos sin código ni medidor |

**Corrección (antes de lanzar WhatsApp):** cuando `cuenta_ingresada = user_id`, llamar a un endpoint que cargue el resto de los datos por cuenta (sin DNI, porque el celular ya es el segundo factor) y asignar `usuario_valido = 1`.

### ~~H-07 · El menú no distingue socio de invitado~~ — Descartado

Error de lectura del export: las opciones de socio del `Menu Principal` (y de `Acceder a mi factura`, `Módulo de Internet.` y `Trámites`) tienen *display condition* `usuario_valido = 1`. El invitado no las ve.

### H-12 · Éxito del reclamo sin verificar

En el caso normal, el insert funciona y el mensaje es correcto. El problema es el caso de **falla**: los grupos `HTTP Reclamo*` no leen la respuesta de n8n y muestran *"¡Reclamo registrado con éxito!"* siempre. Si el `INSERT` falla, el socio cree que su reclamo quedó cargado y no es así.

**Prueba sugerida (reproduce la falla):** cargar un reclamo de energía con este comentario:

```
No hay luz en la casa de D'Angelo
```

El apóstrofo cierra el texto dentro del `INSERT` (H-11). Resultado esperado: n8n marca la ejecución con error, no aparece la OT en `orden_trabajo` y Typebot igual muestra "registrado con éxito". Otras causas de falla: base caída, o un `servicio` que el `Switch` no reconoce.

**Corrección:** devolver `{ "ok": true, "nro_ot": 123 }` desde n8n, mapearlo y condicionar el mensaje. Además, mostrarle al socio el N° de OT, que hoy no recibe.

### H-13 · Numeración de OT con `MAX()+1` — riesgo aceptado

`insert_reclamo` calcula `COALESCE(MAX(ot_nro_ot),0)+1`. Dos inserciones **en el mismo instante** leen el mismo máximo y graban el mismo número. Las pruebas manuales de a un reclamo no pueden reproducirlo, y el bloqueo de "reclamo activo" no lo evita: es por socio y domicilio, mientras que esto afecta a dos socios distintos (o al bot y a un operador cargando una OT en SIGO al mismo tiempo).

Con el volumen de una cooperativa la probabilidad es baja; se acepta el riesgo. Para dejarlo documentado:

- **Comprobar si la base lo impide:** `SHOW CREATE TABLE orden_trabajo;`. Si `ot_nro_ot` tiene índice `UNIQUE`, un choque no duplica: hace fallar el insert, y entonces importa H-12.
- **Detectar duplicados existentes:** `SELECT ot_nro_ot, COUNT(*) FROM orden_trabajo GROUP BY ot_nro_ot HAVING COUNT(*) > 1;`
- `Obtener_ultima_OT` calcula el próximo número pero nadie usa el resultado: se puede borrar.

### H-14 · Año y meses fijos

- `DEUDA_TOTAL` y los cinco `Deuda_Servicio_*`: `d.Anio = 2026`. Las deudas de 2025 no aparecen, y desde enero de 2027 el bot va a mostrar "sin deuda" a todos.
- `Consulta_consumos_socio`: `Anio = 2026 AND Mes IN (7, 8, 9)`. No son "los últimos 3 meses" como dice la documentación del nodo.

- `Code - Mapeo_Deuda_Total` ordena los períodos como texto: `10/2026` sale antes que `9/2026`. Ya pasa hoy.

**Corrección:** [correcciones/H-14-anio-fijo.md](correcciones/H-14-anio-fijo.md). Incluye las 7 consultas listas para pegar y los 2 cambios del nodo Code.

**Estado (02-11-2026):** en las consultas de deuda (`DEUDA_TOTAL` y `Deuda_Servicio_*`) se quitó `d.Anio = 2026`, y `Code - Mapeo_Deuda_Total` ordena los períodos de forma cronológica. Verificado por el autor. Falta confirmar `Consulta_consumos_socio`: quitar solo el año ahí traería todo el historial, así que necesita la ventana de "últimos 3 meses" de la guía.

### H-15 · Posible doble conteo en la deuda

- **Sepelio:** se suma el subtotal del ítem 101 de facturas con `Prefijo <> 34`. Si ese ítem viene dentro de la factura de energía, la fila de energía ya lo incluye en `Total - Imputado` y se suma dos veces.
- **Municipalidad:** `Prefijo = 99` sin filtro de servicio. Si esas facturas tienen `Servicio = 'Energia'`, también se cuentan en energía.
- En `deuda_servicio`, la consulta de municipalidad no filtra por domicilio: la misma tasa aparece en cada domicilio del socio.

**Aclaración:** el hallazgo no es sobre qué meses aparecen (eso funciona), sino sobre si **el mismo importe aparece en dos renglones**. Por ejemplo, una factura de energía de $10.000 que incluye $1.500 de sepelio se mostraría como "Energía $10.000" + "Sepelio $1.500" = $11.500.

**Verificación (dos consultas en SIACCOP):**

```sql
-- 1. ¿En qué comprobantes viene el ítem de sepelio (101)?
SELECT d.ID, d.Servicio, d.Prefijo, d.Total, d.Imputado,
       (dd.Gravado + dd.IVA + dd.Exento + dd.NoGravado) AS SubtotalSepelio
FROM DEUDA d
INNER JOIN DEUDA_DET dd ON d.ID = dd.ID
WHERE dd.Item = 101 AND d.Total <> d.Imputado AND d.NroSocio = '<socio>';

-- 2. ¿Qué servicio tienen los comprobantes de prefijo 99 (municipalidad)?
SELECT Servicio, COUNT(*) AS Cantidad
FROM DEUDA
WHERE Prefijo = 99
GROUP BY Servicio;
```

| Resultado | Conclusión |
|---|---|
| Consulta 1: `Servicio = 'Energia'` (o Agua/Internet) | Doble conteo de sepelio: ese mismo `ID` ya lo suma el bloque de energía |
| Consulta 1: otro `Servicio` (por ejemplo 'Sepelio') | Sin doble conteo |
| Consulta 2: aparece `Energia`, `Agua` o `Internet` | Doble conteo de municipalidad |
| Consulta 2: solo un valor propio (por ejemplo 'Municipalidad') | Sin doble conteo |

## Medios

### H-08 · Medidor y código no ligados al domicilio elegido

**Lo que funciona bien:** el domicilio. El que elige el socio se guarda en `1.1_user_usuario_id`, viaja como `domicilio` en `registrar_reclamo` y se graba en `ot_domicilio`. La prueba con varios domicilios lo confirma.

**Lo que no depende del domicilio:** `vincular_socio` calcula `medidor_energia`, `medidor_agua` y `user_codigo` **una sola vez** para todo el socio, antes de elegir domicilio:

```js
const medidorEnergia = items.find(item => item.json?.tipo_servicio === 'energia' && item.json?.medidor)?.json.medidor
```

Es el primer medidor de energía del socio en orden alfabético de domicilio. Typebot lo guarda en `1.1_medidor_energia` y lo envía en cada reclamo, sea cual sea el domicilio. Lo mismo pasa con el medidor de agua y con el código que usa `items_internet`.

**Prueba sugerida:** con un socio que tenga **dos suministros de energía**, cargar un reclamo en el segundo domicilio (alfabéticamente) y comparar:

```sql
-- SIGO
SELECT ot_nro_ot, ot_domicilio, ot_medidor FROM orden_trabajo WHERE ot_nro_socio = '<socio>' ORDER BY ot_nro_ot DESC;
-- SIACCOP
SELECT Domicilio, Medidor FROM USUENER WHERE Socio = '<socio>' AND Activo = 1;
```

Si `ot_medidor` corresponde al otro domicilio, el hallazgo queda confirmado. Si el socio de la prueba tenía un solo medidor, la prueba no lo detecta.

**Corrección:** incluir `codigo`, `medidor_energia` y `medidor_agua` en cada elemento de `user_domicilios_lista` y, al elegir el domicilio, tomar esos valores del elemento elegido.

### H-15 · Resultado de la verificación (02-11-2026)

Socio 96, comprobantes pendientes de 2026:

| Prefijo | Servicio | Saldo | Mostrado por el bot antes |
|---|---|---|---|
| 28 | Energia | $540.941,91 | Sí |
| 34 | *(vacío)*, ítem 101 = sepelio aparte | $46.900 | **No** (`Prefijo <> 34`) |
| 80 | *(vacío)*, 1 ítem, pagado en parte | $70.466,66 | **No** (ningún bloque lo toma) |

**Criterio aplicado:** el sepelio aparte es el comprobante con ítem 101 cuyo `Servicio` no es Energía, Agua ni Internet, con cualquier prefijo salvo el 99. Se muestra con su saldo (`Total - Imputado`). El sepelio que viene dentro de la factura de agua o energía no se vuelve a sumar en la deuda total; en la deuda por suministro se muestra con la aclaración "Pertenece a la factura de …".

**Aplicado y verificado por el autor (02-11-2026):**

- `DEUDA_TOTAL`: el bloque Sepelio toma solo el sepelio aparte (ítem 101, `Servicio` vacío o propio, cualquier prefijo salvo el 99) con su saldo `Total - Imputado`. Además se corrigió el orden cronológico de los períodos en `Code - Mapeo_Deuda_Total`.
- `Deuda_Servicio_Sepelio`: devuelve `ServicioComprobante` y `MontoaPagar`. `Code_Deuda_Servicios` muestra "🔗 Pertenece a la factura de …" cuando el sepelio viene dentro de otra factura.
- Socio 96: la deuda total pasó de $540.941,91 a $587.841,91 (se suman $46.900 de sepelio de enero a marzo).

El comprobante de prefijo 80 del mismo socio ($70.466,66) es otro concepto y se registró aparte como **H-33**.

### H-16 · Manejo de "sin deuda"

- Si una consulta SQL no devuelve filas, el nodo no emite ítems y la cadena se corta antes de *Respond*. El bot muestra "sin deuda" porque el webhook falla, no porque lo haya determinado. **Corrección:** activar *Always Output Data* en los nodos SQL.
- `No_Deuda_Total` no tiene salida: después de *"No posee deudas registradas"* la conversación termina.
- En `Detalle.`, la condición `tiene_deuda Is set` siempre es verdadera cuando n8n responde (el valor es `true` o `false`). Así, el mensaje `Sin Deuda` solo aparece cuando hay error, y un socio sin deuda ve solo el menú de opciones, sin mensaje.

### H-17 · Estado de reclamo equivocado

Typebot mapea `reclamos[0].id` y `reclamos[0].estado`. Si el socio tiene varios reclamos y elige el tercero, ve el texto del tercero con el número y el estado del primero. Además, `6.8_ejecucion_estado` (avance) se carga y nunca se muestra.

**Corrección:** usar como valor de cada botón el `id`, y con ese id buscar el reclamo en la lista (bloque Set variable con código) o llamar a un endpoint de detalle.

### H-18 · Mapeos incorrectos en la rama Internet

- `HTTP - Verificacion Estado Usuario INTERNET` mapea `servicios.energia.estado_descripcion` en `6.9_internet_estado`.
- `HTTP_Reclamo_Limite_Internet` mapea `data.mensaje`, pero n8n devuelve `mensaje_respuesta`: el aviso de "ya tenés un reclamo activo" sale vacío.

### H-19 · "Cañería tapada" mal tipificada

`mapeo_agua` busca `caneria` o `cloacas` en minúsculas. El botón envía *"Cañería Tapada."* (con ñ e í), así que la condición nunca se cumple y todo reclamo de agua va a sector 6 / actividad 131. **Corrección:** asignar `value` a cada botón de Typebot (como en energía) y comparar contra esos valores.

### H-20 · Criterios inconsistentes en reclamos

- El límite considera abierto `ot_cierre = 1`; la lista de activos usa `ot_cierre IN (1, 3)`. Con `ot_cierre = 3`, el socio ve un reclamo activo pero puede cargar otro igual.
- `usuario_activo` busca el domicilio con `LIKE '%...%'`: `SAN MARTIN 1` coincide también con `SAN MARTIN 123`.
- Si no hay suministro de ese servicio en el domicilio, `esta_ok` no llega y el socio ve el mensaje de inactivo vacío.

### H-21 · Enlace de factura — aceptado

`Mapeo_cuenta_cuit_dni` arma la URL aunque `SQL_validacion_socio` no encuentre al socio. Dentro del flujo de Typebot no tiene consecuencias, porque la cuenta y el DNI ya se validaron al iniciar sesión. Ese nodo SQL sirve en la práctica solo para elegir entre `dni` y `cuit`. Queda como dato que el DNI viaja en la URL del portal (un diseño del portal, no del bot) y que se guarda en auditoría (H-24).

### H-22 · Tarifas

- `consultar_tarifas` no filtra domicilio ni `Activo`: con varios suministros, queda la tarifa del último procesado.
- `Mapeo_tarifas` (endpoint sin uso) lee los precios por posición sin `ORDER BY`.

### H-24 · Auditoría con datos personales

`auditoria_bot` guarda cada respuesta tipeada (DNI, celular, comentarios) y una foto con montos de deuda y el enlace de factura con DNI. No hay retención definida ni enmascaramiento. Esto es relevante para la Ley 25.326 de Protección de Datos Personales; la evaluación legal corresponde al área responsable.

**Corrección:** enmascarar DNI y celular, no guardar `link_factura`, y definir un plazo de borrado.

## Bajos

### H-09 · Código muerto y domicilio sin asignar en la rama de deuda

**Código muerto (análisis de alcanzabilidad desde los eventos `start` y `reply`):** 9 grupos inalcanzables. Son la tercera copia de la cadena de domicilio (`cantidad_domicilios` `vrbg7r…`, `valida_cantidad_domicilios`, `Domicilios_Vinculados`, `Usuario Valido`, `usuario_mas_8_domicilios`, `domicilio_filtro`, `¿Domicilio Encontrado?`, `domicilio_no_encontrado`) y `HTTP - Auditoria` (con un solo espacio y el webhook vacío). Hay además 6 conexiones huérfanas, restos de bloques borrados antes.

**Error en la rama de deuda (se subió la severidad a Media):** con más de 8 domicilios, cuando la búsqueda encuentra el domicilio, `¿Domicilio Encontrado?` (`ydjssz…`) saltaba a `Usuario Valido` sin pasar por `Domicilios_Vinculados`, que es el único bloque que asigna `1.1_user_usuario_id`. La deuda por suministro se consultaba con el domicilio vacío o con el de una consulta anterior. La rama de reclamos ya lo hacía bien.

**Corrección (flujo `typebot-BOT-CC-H09-limpio.json`):** se eliminaron los 9 grupos y las 14 conexiones, y `¿Domicilio Encontrado?` de la rama de deuda ahora va a `Domicilios_Vinculados`. Resultado: 165 grupos, todos alcanzables, sin referencias rotas.

**Prueba:** con un socio de más de 8 domicilios → *Ver mis suministros* → *Ver Deuda por Suministros* → buscar un domicilio. Tiene que aparecer el botón con el domicilio y, al elegirlo, la deuda de ese domicilio.

### H-10 · `1.1_user_email` nunca se asigna

`mapeo_datos_socio` devuelve `user_email`, pero Typebot no lo mapea en `Validación de usuario`. Como `1.1_user_email` solo se usa en Chatwoot, el operador siempre recibe al socio sin email. **Corrección:** agregar el mapeo `data[0].user_email → 1.1_user_email`.

### H-23 · Catálogo de internet mantenido en el código — Aceptado

**Decisión del autor:** los planes de 25 y 50 MB se excluyen a propósito, y los packs adicionales se mantienen a mano en el código: cuando haya un pack nuevo, se agrega a la consulta. El procedimiento está en el [manual §6](03_manual_despliegue_y_mantenimiento.md#-6-plan-de-mantenimiento).

**Verificaciones pendientes (posibles errores, no de diseño):**

| Verificación | Por qué | Cómo |
|---|---|---|
| ~~¿Aparece el plan de 500 MB?~~ | ✅ Verificado por el autor (02-11-2026): aparece. Su código no contiene `"50"` | — |
| Socio con internet y sin packs | Confirmado por el autor: ve "Sin servicios activos", con el nombre y la tarifa vacíos. El nodo tiene un mensaje propio para ese caso ("Sin packs adicionales") al que nunca se llega por el `INNER JOIN USUITEM_I` | Si se quiere ese mensaje: cambiar a `LEFT JOIN USUITEM_I uii` en `SQL - Consulta_Items_usuario` |

### H-25 · Webhooks sin uso — Resuelto

`desglose_deuda`, `tarifas_comerciales` y `vincular_socio_reclamo` están **desactivados** en n8n y en Typebot (confirmado por el autor el 02-11-2026). Se conservan por si se vuelve a pedir esa funcionalidad. En los exports del 29-10 los dos primeros figuraban activos: confirmarlo en el próximo export, o con un `curl` a la URL, que tiene que responder 404.

Si se reactivan, agregar antes un `Validar_Entrada` ([H-01, paso 5](correcciones/H-01-inyeccion-sql.md)).

### ~~H-26 · Fecha de vencimiento~~ — Cerrado

El autor validó la fórmula `DATEADD(day, FechaVencimiento - 4, '1801-01-01')` contra facturas reales. Queda una observación menor: el mismo día del vencimiento se muestra como "VENCIDO" después de las 00:00, porque se compara contra la fecha **y hora** actual.

### H-27 · Destino del email de reclamo particular

**Criterio del autor (aceptado):** la dirección tiene que ser fija y de CUECCA.

**Pendiente para producción:** hoy el destinatario es una casilla **personal** de desarrollo, y el mensaje al socio la muestra ("Email enviado a: …"). Antes de publicar, reemplazarla en el bloque *Email* (`Envio_mail_r_particular`) y en el texto que lo sigue por la casilla institucional del área que atiende los reclamos (por ejemplo `tramites@cuecca.com.ar`, que ya figura en *Métodos de pago*). Así la recepción no depende de una persona.

### H-28 · Derivación a Chatwoot sin contexto

- `Modulo Operador.` pide el motivo (Facturación, Soporte técnico, Trámites, Planes, Otra), pero el botón no guarda el valor en ninguna variable y los bloques Chatwoot solo envían `id`, `name`, `email` y `phoneNumber`. El operador no sabe por qué lo contactan y tiene que preguntarlo de nuevo.
- En las ramas de invitado, `phoneNumber` se carga con `{{6.4_user_dni_invitado}}` (el DNI). Chatwoot puede rechazar un teléfono que no tenga formato internacional, y si lo acepta, el operador ve el DNI como teléfono.
- Las etiquetas del diseño original (`Caja_Atencion`, `Tramites_Atencion`, `Reclamo_Tecnico_Prioridad`) no se envían.

**Corrección:** guardar el motivo en una variable (por ejemplo `6.11_motivo_operador`, con `value` en cada botón) y enviarlo al widget como atributo personalizado (`window.$chatwoot.setCustomAttributes`) o como etiqueta (`window.$chatwoot.setLabel`) con un bloque *Script* después de abrir el widget. En invitados, no cargar el DNI en `phoneNumber`.

### H-29 · Contenido incompleto

- `info_cambio_titularidad` muestra solo el texto "info".
- `Instructivo_agendas_pago` tiene un bloque de video sin URL: el socio ve "Instructivo:" y nada más.

### H-30 · "Subir comprobante" contra la política del bot

El manual define que el bot no recibe comprobantes de pago: se envían por email a Trámites. La opción *Declarar pagos (Próximamente)* ya muestra un botón "Subir comprobante". Antes de implementarla hay que decidir quién valida esos comprobantes, dónde se guardan y cómo se le informa el resultado al socio.

**Decisión del autor (03-11-2026):** se mantiene visible como funcionalidad futura. La contradicción es intencional y temporal: el botón no procesa nada y el menú lo anuncia como *Próximamente*. Cuando se implemente, se actualiza la política del manual (§2.1).

### H-31 · Variables entre comillas dentro de código en Typebot

En los bloques *Script* y *Set variable* (código), Typebot evalúa `{{variable}}` como una variable de JavaScript. Escrita entre comillas, el código recibe el **ID interno** de la variable y no su valor. Caso detectado: `Usuario_invitado_operario` → `6.2_usuario_invitado` usa `"{{6.4_user_dni_invitado}}"`. Si se comporta así, todos los invitados reciben el identificador `invitado_6518` (los dígitos del ID de la variable) y Chatwoot los une en un único contacto.

**Verificación:** en Chatwoot → *Contactos*, comparar el identificador de dos invitados distintos.
**Corrección:** `const entrada = String({{6.4_user_dni_invitado}} ?? "");`

### H-32 · Restos del avatar (Diseño 2.0)

En `Menu Principal`, `No_Deuda_Total` y `usuario_mas_8_domicilios` hay bloques *Set variable* que asignan `{{av_normal}}`, `{{av_contento}}` y `{{av_procesando}}`. Ni la variable de destino (`ftivfuzunalcamhw1955dtm4`) ni esas tres existen en el bot. Parece un avatar que cambia de expresión según el paso. Si la función sigue en desarrollo, hay que recrear las variables; si se descartó, borrar los tres bloques.

### H-33 · Comprobantes de prefijo 80 sin mostrar

En la verificación de H-15, un socio de prueba tiene un comprobante de **prefijo 80**, `Servicio` vacío, 1 ítem, total $105.700, imputado $35.233,34 (un tercio) y saldo $70.466,66. No es energía, agua, internet, sepelio (no tiene el ítem 101) ni municipalidad (prefijo 99), así que ninguna consulta de deuda lo toma. Por el pago parcial parece un plan de pagos o convenio, o un concepto de artículos del hogar.

**A definir:** qué representa el prefijo 80 y si el socio lo tiene que ver. Si corresponde mostrarlo, se agrega un bloque "Otros conceptos" en `DEUDA_TOTAL` y en la deuda por suministro, con la descripción del ítem.

**Para medir el alcance:**

```sql
SELECT d.Prefijo, ISNULL(d.Servicio, '(vacío)') AS Servicio, COUNT(*) AS Comprobantes, SUM(d.Total - d.Imputado) AS Saldo
FROM DEUDA d
WHERE d.Total <> d.Imputado AND d.Anio = 2026
  AND ISNULL(d.Servicio, '') NOT IN ('Energia', 'Agua', 'Internet')
  AND d.Prefijo <> 99
  AND NOT EXISTS (SELECT 1 FROM DEUDA_DET dd WHERE dd.ID = d.ID AND dd.Item = 101)
GROUP BY d.Prefijo, ISNULL(d.Servicio, '(vacío)');
```

Lista todos los comprobantes pendientes que hoy no muestra ninguna consulta de deuda del bot.

### Observaciones menores

- En el reconocimiento por celular, si la cuenta no coincide, el mensaje dice *"No encontramos una cuenta vinculada a este número"*, aunque sí se encontró una.
- `Validación de usuario` pide el celular pero n8n no lo valida: en la práctica son dos factores (cuenta + DNI).
- No hay límite de reintentos en la validación.
- `mapeo_lista_domicilio` tiene la plantilla de etiqueta rota (`\({item.domicilio} (\){detalle})`). No se nota porque Typebot usa `.domicilio`.
- El sticky note del workflow 1 menciona "MySQL Server", pero la consulta es sobre SQL Server.
- El export de Typebot contiene un celular real en `variablesForTest`: hay que borrarlo antes de versionar cualquier export.

---

## Correcciones aplicadas en n8n (03-11-2026)

Archivos en `n8n-corregidos/`. Se verificaron con: carga JSON, integridad de conexiones y referencias `$('Nodo')`, sintaxis de los nodos Code, parseo de las 26 consultas (T-SQL / MySQL) y simulación de validadores y `mapeo_*` con apóstrofos, barras invertidas y `1' OR '1'='1`. **No se probaron contra las bases reales.**

| Workflow | Cambios |
|---|---|
| 0. Sesion_Usuario | H-34. `errorWorkflow` propio (ya contiene el *Error Trigger*) |
| 1. Validaciones_Socio | Validadores en los 3 webhooks (H-01). Celular: `Activo = 1` + últimos 10 dígitos por igualdad (H-02). Etiqueta de domicilio corregida. *Always Output Data* (H-16) |
| 2. consultar_deuda | Validación en `Limpiar_Domicilio*`, factura y consumos (H-01). Sin año fijo y consumos con ventana de 3 meses (H-14). *Always Output Data*; sin deuda devuelve `monto_total_formateado: null` (H-16) |
| 3. Modulo_Internet | Validación en items y tarifas (H-01). Tarifas: socio entre comillas y `Activo = 1` (H-22 parcial). `tarifas_comerciales` desactivado (H-25) |
| 4. Modulo_Reclamos | `Validar_Reclamo` + escape MySQL en `mapeo_*` (H-01/H-11). Medidor por domicilio elegido (H-08). Tildes normalizadas (H-19). Respuesta `{ok, nro_ot}` (H-12). `ot_cierre IN (1, 3)` y domicilio por igualdad (H-20) |
| 5. Modulo_Auditoria | Solo `errorWorkflow` |

**Efecto colateral:** un dato inválido hace fallar el workflow y el webhook responde error 500. Typebot debe tratarlo como error (mensaje genérico), no como "sin datos".

### H-34 · Sesion_Usuario

- `Continuar_sesion.sessionId` era `={{ '$json.session_id' }}`: el texto literal, igual para todos los socios. Ahora toma el `session_id` del registro.
- El mensaje enviado era `ultimo_mensaje` (el guardado), no el que acaba de llegar. Ahora usa `mapeo_body.mensaje`.
- `If_tiempo_transcurrido` comparaba un valor mal referenciado. Ahora usa `$json.tiempo_transcurrido`.

Preguntas abiertas:

1. *Respond to Webhook* devuelve la fila de la Data Table, no los mensajes de Typebot. ¿Qué tiene que recibir quien llama a este webhook?
2. La limpieza programada usa `createdAt` y el webhook usa `updatedAt`: una sesión activa puede borrarse por haber empezado hace mucho.
3. Las alertas de error van a un correo personal (igual que H-27).
