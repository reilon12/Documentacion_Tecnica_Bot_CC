# Corrección H-28 — Contexto en la derivación a Chatwoot

> ✅ **Aplicada y verificada (02-11-2026).** El comportamiento actual, incluido el celular en formato `+549`, está documentado en el [módulo 6](../modulos/06-derivacion-chatwoot.md).

**Objetivo:** que el operador vea, al recibir el chat, **por qué** lo contactan y **quién** es (socio o invitado), sin tener que preguntarlo.

**No hace falta un módulo nuevo** en n8n ni una tabla nueva. El motivo queda guardado en:

- **Chatwoot:** como etiqueta y atributo de la conversación. Se puede filtrar en la bandeja y contar en *Reports → Labels*.
- **Auditoría:** la elección del botón ya se registra hoy en `auditoria_bot` (evento *reply*).

## Qué ve el operador antes y después

| Dato | Hoy | Con la corrección |
|---|---|---|
| Motivo | No llega | Etiqueta + atributo `motivo_consulta` en la conversación |
| Socio o invitado | Solo se deduce del ID (`invitado_…`) | Atributo `tipo_usuario` del contacto |
| Teléfono del socio | `2245000000` (puede ser rechazado, ver nota) | `+5492245000000` |
| Teléfono del invitado | **El DNI** | Vacío; el DNI pasa al atributo `dni` |
| Fuera de horario | Sin distinción | Etiqueta `fuera_de_horario` |

> **Nota sobre el teléfono:** Chatwoot valida los teléfonos de contacto en formato internacional (E.164: `+54…`). Si un valor no cumple, puede rechazar el teléfono o la actualización del contacto. Para verificarlo: abrir en Chatwoot un contacto creado por el bot y ver si tiene el teléfono cargado.

---

## Resumen de cambios

| # | Dónde | Qué |
|---|---|---|
| 1 | Chatwoot | Crear 6 etiquetas y 4 atributos personalizados |
| 2 | Typebot | Crear 2 variables |
| 3 | Typebot → `Modulo Operador.` | Guardar el motivo y asignar un valor a cada botón |
| 4 | Typebot → `Usuario_Valido_Operario` | Limpiar el motivo y armar el teléfono en formato internacional |
| 5 | Typebot → 4 bloques Chatwoot | Corregir el teléfono |
| 6 | Typebot → después de cada bloque Chatwoot | Agregar el bloque *Script* (el mismo en los 4) |

---

## Paso 1 · Chatwoot

### 1.1 Etiquetas (*Settings → Labels → Add label*)

Chatwoot acepta letras, números, guiones y guiones bajos.

| Etiqueta | Motivo | Sugerencia de color |
|---|---|---|
| `caja_atencion` | Facturación y Convenios | Verde |
| `reclamo_tecnico_prioridad` | Soporte Técnico Especializado | Rojo |
| `tramites_atencion` | Trámites y Cambio de Titularidad | Azul |
| `planes_contrataciones` | Planes y Contrataciones | Violeta |
| `consulta_general` | Otra consulta | Gris |
| `fuera_de_horario` | Mensaje dejado fuera de horario (sin motivo) | Naranja |

Si la etiqueta no existe en Chatwoot, el widget no la asigna.

### 1.2 Atributos personalizados (*Settings → Custom Attributes → Add*)

| Se aplica a | Nombre visible | Clave (*key*) | Tipo |
|---|---|---|---|
| Conversation | Motivo de consulta | `motivo_consulta` | Text |
| Contact | Tipo de usuario | `tipo_usuario` | Text |
| Contact | Último motivo | `ultimo_motivo` | Text |
| Contact | DNI | `dni` | Text |

La clave tiene que ser exactamente la de la tabla: es la que usa el script.

---

> ⚠️ **Variables dentro de código en Typebot.** En los bloques *Script* y en *Set variable* con código, `{{variable}}` se evalúa como una variable de JavaScript, **no** se reemplaza como texto. Va **sin comillas**: `String({{mi_variable}} ?? "")`. Con comillas (`"{{mi_variable}}"`), el código recibe el ID interno de la variable (por ejemplo `ti73v7clrz…`) en lugar de su valor. Esta guía tenía ese error en su primera versión: hacía que todas las conversaciones salieran como `fuera_de_horario`.

## Paso 2 · Variables en Typebot

Crear (*Variables* en el panel lateral):

- `6.11_motivo_operador`
- `6.12_cel_chatwoot`

---

## Paso 3 · `Modulo Operador.`: guardar el motivo

En el bloque de botones:

1. Configuración del bloque → **Save answer in variable** → `6.11_motivo_operador`.
2. En cada botón, completar el **valor interno** (*Internal value*):

| Botón | Valor interno |
|---|---|
| 💰 Facturación y Convenios | `facturacion` |
| 🛠️ Soporte Técnico Especializado | `soporte_tecnico` |
| 📝 Trámites y Cambio de Titularidad | `tramites` |
| 🌐 Planes y Contrataciones | `planes` |
| 💬 Otra Consulta / Asistencia General | `otra` |
| ↩️ Volver al menú principal | *(vacío)* |

---

## Paso 4 · `Usuario_Valido_Operario`: preparar los datos

Al **principio** del grupo, antes de la condición `usuario_valido = 1`, agregar dos bloques **Set variable**:

1. `6.11_motivo_operador` → **Empty**. Así se borra un motivo de una derivación anterior en la misma sesión.
2. `6.12_cel_chatwoot` → **Custom** (código):

```js
const digitos = String({{user_cel}} ?? "").replace(/\D/g, "");
return digitos.length === 10 ? "+549" + digitos : "";
```

Convierte un celular de 10 dígitos (característica sin 0 + número sin 15) al formato `+549…`. Si el formato no es ese, lo deja vacío antes que mandar un teléfono inválido.

---

## Paso 5 · Corregir el teléfono en los 4 bloques Chatwoot

| Grupo | Campo *Phone number* hoy | Cambiar a |
|---|---|---|
| `Chatwoot - Operario.` | `{{user_cel}}` | `{{6.12_cel_chatwoot}}` |
| `Mensaje_fuera_de_horario_validado` | `{{user_cel}}` | `{{6.12_cel_chatwoot}}` (y agregar *Email* `{{1.1_user_email}}`, que falta en este bloque) |
| `Chatwoot - Operario/Invitado.` | `{{6.4_user_dni_invitado}}` | *(vacío)* |
| `mensaje_fuera_horario_invitado` | `{{6.4_user_dni_invitado}}` | *(vacío)* |

---

## Paso 6 · Bloque *Script* después de cada bloque Chatwoot

En los 4 grupos del paso 5, agregar un bloque **Script** (*Logic → Script*) **entre** el bloque Chatwoot y el *Jump* al menú:

- Nombre: `Contexto_Chatwoot`
- **Execute on client:** activado (tiene que correr en el navegador, donde está el widget)
- Código (el mismo en los 4):

```js
// Contexto para el operador de Chatwoot (H-28)
const motivo     = String({{6.11_motivo_operador}} ?? "");
const enHorario  = String({{6.1_horario_habil}} ?? "") === "true";
const esSocio    = String({{usuario_valido}} ?? "") === "1";
const dni        = String({{6.4_user_dni_invitado}} ?? "").replace(/\D/g, "");

const ETIQUETAS = {
  facturacion:     "caja_atencion",
  soporte_tecnico: "reclamo_tecnico_prioridad",
  tramites:        "tramites_atencion",
  planes:          "planes_contrataciones",
  otra:            "consulta_general"
};
const NOMBRES = {
  facturacion:     "Facturación y Convenios",
  soporte_tecnico: "Soporte Técnico Especializado",
  tramites:        "Trámites y Cambio de Titularidad",
  planes:          "Planes y Contrataciones",
  otra:            "Otra consulta"
};

const etiqueta    = enHorario ? (ETIQUETAS[motivo] || "consulta_general") : "fuera_de_horario";
const textoMotivo = NOMBRES[motivo] || "Sin motivo (mensaje fuera de horario)";

// 1. Datos del contacto: se pueden cargar apenas el widget está listo
function cargarContacto() {
  const atributos = { tipo_usuario: esSocio ? "socio" : "invitado", ultimo_motivo: textoMotivo };
  if (!esSocio && dni) atributos.dni = dni;
  window.$chatwoot.setCustomAttributes(atributos);
}

// 2. Etiqueta y motivo de la conversación: la conversación recién existe
//    cuando el socio envía su primer mensaje
function cargarConversacion() {
  window.$chatwoot.setLabel(etiqueta);
  window.$chatwoot.setConversationCustomAttributes({ motivo_consulta: textoMotivo });
}

if (window.$chatwoot && window.$chatwoot.hasLoaded) {
  cargarContacto();
} else {
  window.addEventListener("chatwoot:ready", cargarContacto, { once: true });
}
window.addEventListener("chatwoot:on-message", cargarConversacion);
```

### Cómo funciona

| Momento | Qué carga | Por qué en ese momento |
|---|---|---|
| Cuando el widget termina de cargar (`chatwoot:ready`) | Atributos del **contacto**: tipo de usuario, último motivo, DNI del invitado | El contacto ya existe: lo crea el bloque Chatwoot |
| Cuando el socio envía su primer mensaje (`chatwoot:on-message`) | **Etiqueta** y `motivo_consulta` de la **conversación** | Chatwoot crea la conversación recién con el primer mensaje. Antes, la etiqueta no tiene a qué asignarse |

Con cada mensaje nuevo, el script vuelve a asignar la misma etiqueta. No duplica nada: Chatwoot no repite etiquetas.

---

## Pruebas

| # | Escenario | Resultado esperado en Chatwoot |
|---|---|---|
| 1 | Socio, en horario, elige *Facturación* y escribe "hola" | Conversación con etiqueta `caja_atencion` y atributo *Motivo de consulta* = Facturación y Convenios. Contacto con tipo `socio` y teléfono `+549…` |
| 2 | Socio elige *Soporte Técnico* | Etiqueta `reclamo_tecnico_prioridad` |
| 3 | Invitado, en horario, elige *Otra consulta* | Etiqueta `consulta_general`; contacto con tipo `invitado`, atributo DNI y **sin** teléfono |
| 4 | Socio fuera de horario | Etiqueta `fuera_de_horario` |
| 5 | En la misma sesión: derivación por *Planes* y, después, otra por *Trámites* | La segunda conversación lleva `tramites_atencion` |
| 6 | *Reports → Labels* | Conteo de conversaciones por etiqueta |

Si la prueba 1 no asigna la etiqueta, abrir la consola del navegador (F12) y revisar si hay errores de `$chatwoot`. El nombre de los eventos y de los métodos del SDK depende de la versión de Chatwoot: `setConversationCustomAttributes` requiere una versión reciente.

## Validación hecha sobre este documento

- El script se ejecutó en Node.js con un `$chatwoot` simulado, para socio en horario e invitado fuera de horario: llama a los métodos con los valores esperados.
- La conversión del celular se probó con `2245000000`, `(2245) 00-0000`, `224515000000` y vacío.
- **Probado contra la instancia de Chatwoot el 02-11-2026:** las etiquetas y los atributos se asignan correctamente con los eventos `chatwoot:ready` y `chatwoot:on-message`.
