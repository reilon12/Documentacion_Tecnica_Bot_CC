# Corrección H-01 — Inyección SQL

> ✅ **Aplicada y verificada (03-11-2026).** Los validadores de esta guía están en los seis workflows (`exports/limpios/`). Este documento queda como explicación del criterio y referencia para agregar webhooks nuevos: todo webhook nuevo tiene que pasar por un `Validar_Entrada_*` antes de su consulta.

**Objetivo:** que ningún dato que llegue a un webhook pueda alterar una consulta SQL.

**Estrategia:** validar y limpiar los datos **antes** de que lleguen a las consultas. Así las consultas quedan como están, salvo dos. Hay dos tipos de dato:

| Tipo | Ejemplos | Qué se hace |
|---|---|---|
| Número | cuenta, socio, DNI, código, teléfono | Se quitan espacios, puntos y guiones. Si queda algo que no es un dígito, **se rechaza el pedido** |
| Texto | domicilio, comentario, nombre | Cada `'` se convierte en `''` (en MySQL, además, `\` pasa a `\\`). El texto se guarda igual que lo escribió el socio |

Cuando un pedido se rechaza, el nodo corta la ejecución con error. n8n responde 500, Typebot no recibe datos y sigue por la rama "sin resultados" de cada bloque (por ejemplo, *¿Reintentar?* en la validación).

**Efecto lateral positivo:** un DNI escrito con puntos (`30.123.456`) hoy no coincide con nada en la base; con la corrección, se acepta.

---

## Resumen de cambios

| # | Qué | Dónde | Cantidad |
|---|---|---|---|
| 1 | **Crear** el nodo Code `Validar_Entrada` | 8 webhooks | 8 nodos nuevos |
| 2 | **Modificar** el final de `Limpiar_Domicilio` | Workflows 2 y 4 | 4 nodos |
| 3 | **Reemplazar** el código de `mapeo_energia`, `mapeo_agua`, `mapeo_internet` | Workflow 4 | 3 nodos (incluye H-11) |
| 4 | **Modificar** 1 línea en `Reclamos_Activos` y `Reclamos_Cerrados` | Workflow 4 | 2 consultas |
| 5 | **Desactivar** el webhook `desglose_deuda` (sin uso) | Workflow 2 | 1 nodo |
| 6 | *(Recomendado)* No llamar a `identificar_socio` sin celular | Typebot | 1 condición |

No requieren cambios: `consultar_pack_internet`, `suscripciones` y `tarifas_comerciales` (no reciben datos), y `auditoria` (usa la operación *Insert*, que ya es parametrizada).

---

## Paso 1 · Crear `Validar_Entrada` (8 webhooks)

### 1.1 Cómo insertarlo

1. Abrir el workflow y pasar el mouse sobre la flecha entre el nodo **Webhook** y el **primer nodo SQL**.
2. Clic en **+** → **Code**.
3. Nombre: `Validar_Entrada`. Modo: **Run Once for All Items**. Lenguaje: **JavaScript**.
4. Pegar el código de 1.2 y completar las 4 líneas de configuración según la tabla 1.3.

El nodo devuelve el mismo `body` limpio, así que las consultas que usan `$json.body.campo` siguen funcionando sin cambios.

### 1.2 Código (el mismo para los 8)

```js
// ===== CONFIGURACIÓN: completar según el webhook (ver tabla) =====
const NUMERICOS = ['cuenta', 'dni'];   // Solo dígitos. Obligatorios.
const TEXTOS    = [];                  // Texto libre: se escapan las comillas.
const MOTOR     = 'mssql';             // 'mssql' = SQL Server · 'mysql' = MySQL
const LARGO_MIN = {};                  // Ej.: { telefono: 10 }
// =================================================================

const entrada = $input.first().json;
const body = { ...(entrada.body || {}) };

for (const campo of NUMERICOS) {
  const original = String(body[campo] ?? '').trim();
  const limpio = original.replace(/[\s.\-]/g, '');   // quita espacios, puntos y guiones
  const minimo = LARGO_MIN[campo] || 1;
  if (!/^\d+$/.test(limpio) || limpio.length < minimo || limpio.length > 15) {
    throw new Error(`Entrada inválida en el campo "${campo}"`);
  }
  body[campo] = limpio;
}

for (const campo of TEXTOS) {
  let texto = String(body[campo] ?? '').trim().slice(0, 200);
  if (MOTOR === 'mysql') texto = texto.replace(/\\/g, '\\\\');
  body[campo] = texto.replace(/'/g, "''");
}

return [{ json: { ...entrada, body } }];
```

### 1.3 Configuración por webhook

| Workflow | Webhook | Insertar entre | `NUMERICOS` | `TEXTOS` | `MOTOR` | `LARGO_MIN` |
|---|---|---|---|---|---|---|
| 1 | `identificar_socio` | `Webhook_celular` → `SQL_validacion_celular` | `['telefono']` | `[]` | `'mssql'` | `{ telefono: 10 }` |
| 1 | `vincular_socio` | `Vincular_Socio` → `busqueda_socio` | `['cuenta', 'dni']` | `[]` | `'mssql'` | `{}` |
| 1 | `filtrar_domicilio` | `webhook_filtrar_domicilio` → `filtro_domicilio` | `['cuenta', 'dni', 'codigo']` | `['domicilio_buscado']` | `'mssql'` | `{}` |
| 2 | `generar_link_factura` | `webhook_factura_link` → `SQL_validacion_socio` | `['cuenta', 'dni']` | `[]` | `'mssql'` | `{}` |
| 2 | `consumo_ener_agua` | `Webhook_consumos` → `Consulta_consumos_socio` | `['Socio']` | `[]` | `'mssql'` | `{}` |
| 3 | `items_internet` | `Items_Internet` → `SQL - Consulta_Items_usuario` | `['socio', 'domicilio']` | `[]` | `'mssql'` | `{}` |
| 3 | `consultar_tarifas` | `Webhook_tarifas` → `Consulta_Tarifas_usuario` | `['numCuenta']` | `[]` | `'mssql'` | `{}` |
| 4 | `estado_reclamo` | `estado_reclamo` → `if_tipo_reclamo` | `['nro_socio']` | `[]` | `'mysql'` | `{}` |

> Los nombres van **exactamente** como los envía Typebot, con mayúsculas incluidas (`Socio` en consumos, `numCuenta` en tarifas).
>
> En `items_internet`, el campo `domicilio` contiene el **código de usuario** (número), por eso va en `NUMERICOS`.

---

## Paso 2 · Modificar `Limpiar_Domicilio` (4 nodos)

Estos nodos ya preparan los datos para las consultas de deuda, estado del suministro y límite de reclamos. En cada uno, **reemplazar desde `return [{` hasta el final** por el código que corresponda. Lo de arriba (lectura del body y corte del paréntesis) no se toca.

### 2.1 SQL Server: 3 nodos

- Workflow 2 → `Limpiar_Domicilio` (deuda por suministro)
- Workflow 2 → `Limpiar_Domicilio1` (deuda total)
- Workflow 4 → `Limpiar_Domicilio` (estado del suministro)

```js
// 5. Validación (H-01)
const socioLimpio = socio.trim().replace(/[\s.\-]/g, '');
if (!/^\d{1,15}$/.test(socioLimpio)) {
  throw new Error('Entrada inválida en el campo "socio"');
}
const domicilioSeguro = domicilio.trim().toUpperCase().slice(0, 200).replace(/'/g, "''");

return [{
  json: {
    socio: socioLimpio,
    codigo: codigo.trim(),
    domicilio_limpio: domicilioSeguro
  }
}];
```

### 2.2 MySQL: 1 nodo

- Workflow 4 → `Limpiar_Domicilio1` (límite de reclamos)

```js
// 5. Validación (H-01)
const socioLimpio = socio.trim().replace(/[\s.\-]/g, '');
if (!/^\d{1,15}$/.test(socioLimpio)) {
  throw new Error('Entrada inválida en el campo "socio"');
}
const domicilioSeguro = domicilio.trim().toUpperCase().slice(0, 200)
  .replace(/\\/g, '\\\\')
  .replace(/'/g, "''");

return [{
  json: {
    socio: socioLimpio,
    domicilio_limpio: domicilioSeguro
  }
}];
```

---

## Paso 3 · Reemplazar los nodos `mapeo_*` de reclamos (workflow 4)

Estos nodos leen los datos directamente del webhook `Registrar_reclamo`, así que el validador del paso 1 no los cubre. Además, el `INSERT` mete el texto del socio dentro de comillas. Este paso resuelve también **H-11** (el apóstrofo que rompe el reclamo).

Reemplazar **todo** el código de cada nodo. La consulta `insert_reclamo` no se toca.

### 3.1 `mapeo_energia`

```js
// Escapa texto para MySQL (H-01 / H-11)
const esc = s => String(s ?? '').replace(/\\/g, '\\\\').replace(/'/g, "''");

const body = $('Registrar_reclamo').first().json.body || {};

// N° de socio: solo dígitos (H-01)
const cuenta = String(body.cuenta ?? '').trim().replace(/[\s.\-]/g, '');
if (!/^\d{1,15}$/.test(cuenta)) {
  throw new Error('Entrada inválida en el campo "cuenta"');
}

const subtipoOriginal = body.subtipo || '';
// Sin tildes ni ñ: "Cañería" → "caneria" (H-19)
const subtipo = subtipoOriginal.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
const comentario = body.comentario || '';
const domicilio_particular = body.domicilio_particular || '';

let ot_actividad = 27;
let ot_tipo_tarea = null;
let ot_zona_trabajo = null;

if (subtipo.includes('voltaje')) {
  ot_actividad = 27;
  ot_tipo_tarea = 4;
  ot_zona_trabajo = 1;
} else if (subtipo.includes('pilar')) {
  ot_actividad = 21;
}

const tareaTexto = comentario ? (subtipoOriginal + ' - ' + 'Comentario Socio: '+comentario + ' - ' + 'Domicilio Socio: ' + domicilio_particular) : subtipoOriginal;

return [{
  json: {
    tipo: "RECLAMO",
    ot_sector: 1,
    ot_actividad: ot_actividad,
    ot_tipo_tarea: ot_tipo_tarea,
    ot_zona_trabajo: ot_zona_trabajo,
    ot_asociado: esc(body.nombre),
    ot_nro_socio: cuenta,
    ot_domicilio: esc(body.domicilio),
    ot_medidor: body.medidor_energia ? esc(body.medidor_energia) : null,
    ot_tarea: esc(tareaTexto),
    ot_cierre: 1,
    ot_trabajo: 2
  }
}];
```

### 3.2 `mapeo_agua`

```js
// Escapa texto para MySQL (H-01 / H-11)
const esc = s => String(s ?? '').replace(/\\/g, '\\\\').replace(/'/g, "''");

const body = $('Registrar_reclamo').first().json.body || {};

// N° de socio: solo dígitos (H-01)
const cuenta = String(body.cuenta ?? '').trim().replace(/[\s.\-]/g, '');
if (!/^\d{1,15}$/.test(cuenta)) {
  throw new Error('Entrada inválida en el campo "cuenta"');
}

const subtipoOriginal = body.subtipo || '';
// Sin tildes ni ñ: "Cañería" → "caneria" (H-19)
const subtipo = subtipoOriginal.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
const comentario = body.comentario || '';
const domicilio_particular = body.domicilio_particular || '';

let ot_sector = 6;
let ot_actividad = 131;

if (subtipo.includes('caneria') || subtipo.includes('cloacas')) {
  ot_sector = 7;
  ot_actividad = 152;
}

const tareaTexto = comentario ? (subtipoOriginal + ' - ' + 'Comentario Socio: '+comentario + ' - ' + 'Domicilio Socio: ' + domicilio_particular) : subtipoOriginal;

return [{
  json: {
    tipo: "RECLAMO",
    ot_sector: ot_sector,
    ot_actividad: ot_actividad,
    ot_tipo_tarea: null,
    ot_zona_trabajo: null,
    ot_asociado: esc(body.nombre),
    ot_nro_socio: cuenta,
    ot_domicilio: esc(body.domicilio),
    ot_medidor: body.medidor_agua ? esc(body.medidor_agua) : null,
    ot_tarea: esc(tareaTexto),
    ot_cierre: 1,
    ot_trabajo: 2
  }
}];
```

### 3.3 `mapeo_internet`

```js
// Escapa texto para MySQL (H-01 / H-11)
const esc = s => String(s ?? '').replace(/\\/g, '\\\\').replace(/'/g, "''");

const body = $('Registrar_reclamo').first().json.body || {};

// N° de socio: solo dígitos (H-01)
const cuenta = String(body.cuenta ?? '').trim().replace(/[\s.\-]/g, '');
if (!/^\d{1,15}$/.test(cuenta)) {
  throw new Error('Entrada inválida en el campo "cuenta"');
}

const subtipoOriginal = body.subtipo || '';
const comentario = body.comentario || '';
const domicilio_particular = body.domicilio_particular || '';

const tareaTexto = comentario ? (subtipoOriginal + ' - ' + 'Comentario Socio: '+comentario + ' - ' + 'Domicilio Socio: ' + domicilio_particular) : subtipoOriginal;

return [{
  json: {
    tipo: "RECLAMO",
    ot_sector: 2,
    ot_actividad: 248,
    ot_tipo_tarea: null,
    ot_zona_trabajo: null,
    ot_asociado: esc(body.nombre),
    ot_nro_socio: cuenta,
    ot_domicilio: esc(body.domicilio),
    ot_medidor: null,
    ot_tarea: esc(tareaTexto),
    ot_cierre: 1,
    ot_trabajo: 2
  }
}];
```

---

## Paso 4 · Modificar `Reclamos_Activos` y `Reclamos_Cerrados` (workflow 4)

Estas dos consultas leen el número de socio directamente del webhook, sin comillas. Así salteaban el validador del paso 1. En las dos, reemplazar la línea:

```sql
	ot.ot_nro_socio = {{ $('estado_reclamo').item.json.body.nro_socio }}
```

por:

```sql
	ot.ot_nro_socio = '{{ $json.body.nro_socio }}'
```

(En `Reclamos_Cerrados` la línea original tiene dos espacios después del `=`; reemplazarla igual.)

`$json` ahora es la salida de `Validar_Entrada`, que pasa sin cambios por `if_tipo_reclamo`.

---

## Paso 5 · Desactivar `desglose_deuda` (workflow 2)

Typebot no lo usa (H-25) y recibe cinco campos sin validar. Clic derecho en `Webhook_desglose_deuda` → **Deactivate**. Si en el futuro se integra, hay que agregarle un `Validar_Entrada` con `NUMERICOS = ['socio', 'periodo_ener', 'periodo_agua', 'periodo_int']` y `TEXTOS = ['usuario_id', 'servicio']`.

---

## Paso 6 · *(Recomendado)* No llamar a `identificar_socio` sin celular (Typebot)

Con el paso 1, un celular vacío ya no devuelve el padrón (H-02), pero cada sesión web dejaría una ejecución con error en n8n. Para evitarlo, en el grupo `Bienvenida y Verificacion`, antes del bloque HTTP de `identificar_socio`, agregar un bloque **Condition**:

- `user_cel` **Is empty** → saltar a `Informacion y Terminos`
- Si no, continuar con el bloque HTTP

---

## Pruebas

### Funcionamiento normal (no tiene que cambiar nada)

| # | Prueba | Resultado esperado |
|---|---|---|
| 1 | Validarse con cuenta y DNI correctos | Menú de socio |
| 2 | Validarse con DNI **con puntos** (`30.123.456`) | Menú de socio (antes fallaba) |
| 3 | Deuda total y deuda por suministro | Mismos montos que antes |
| 4 | Más de 8 domicilios → buscar `O'Higgins` (o cualquier calle) | Encuentra el domicilio |
| 5 | Consumos, tarifas, mis planes de internet | Igual que antes |
| 6 | Reclamo con comentario `Corte en lo de D'Angelo, dice "error"` | OT creada; `ot_tarea` con el texto exacto |
| 7 | Estado de reclamos activos y cerrados | Igual que antes |

### Rechazo de datos inválidos

Probar llamando directamente al webhook (desde Postman o con `curl` en el mismo equipo):

```bash
curl -X POST http://localhost:5678/webhook/vincular_socio \
     -H "Content-Type: application/json" \
     -d '{"cuenta":"1\u0027 OR \u00271\u0027=\u00271","dni":"1"}'
```

Resultado esperado: error 500, y en n8n → *Executions* la ejecución en rojo en `Validar_Entrada` con el mensaje `Entrada inválida en el campo "cuenta"`. **Ninguna** consulta SQL ejecutada.

| Webhook | Campo de prueba | Valor |
|---|---|---|
| `identificar_socio` | `telefono` | `""` (vacío) |
| `filtrar_domicilio` | `domicilio_buscado` | `x%' OR 1=1 --` → no rechaza, pero no encuentra nada (el texto se busca literal) |
| `consultar_tarifas` | `numCuenta` | `1 OR 1=1` |
| `estado_reclamo` | `nro_socio` | `1 OR 1=1` |
| `registrar_reclamo` | `cuenta` | `1; DROP` |

---

## Validación hecha sobre este documento

- El validador, los cuatro `Limpiar_Domicilio` y los tres `mapeo_*` se ejecutaron en Node.js con entradas normales y maliciosas: rechazan números con caracteres extraños y escapan `'` y `\`.
- El escape se probó en una base SQL con un domicilio `O'HIGGINS 12`: la búsqueda lo encuentra y el intento de inyección devuelve 0 filas.
- **No se probó** dentro de n8n ni contra SIACCOP o SIGO. Hay que correr las pruebas de arriba antes de dar el hallazgo por cerrado.
