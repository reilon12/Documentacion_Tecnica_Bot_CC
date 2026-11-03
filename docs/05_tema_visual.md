# 🎨 Tema visual del bot (Typebot)

El aspecto del chat se define en **Typebot → Tema → Custom CSS**. El CSS completo está en [`estilos/typebot-tema-cuecca.css`](../estilos/typebot-tema-cuecca.css) y viaja también dentro del export de Typebot (`theme.customCss`).

## 1. Base

| Elemento | Definición |
|---|---|
| Fuente | Poppins (Tema → Font). El export tiene Raleway en `theme.general.font`; el CSS la pisa |
| Fondo | Gris azulado `#edf1f5` con dos luces suaves y el logo como marca de agua (opacidad 5 %) |
| Franja superior | 4 px con los seis colores del logo |
| Burbujas del bot | Blancas con borde fino |
| Burbujas del socio | Degradé azul marino |
| Menús | Tarjeta blanca titulada "Elegí una opción", una opción por fila con marca de color a la izquierda y flecha `›` |
| Avatares | `bot-cuecca-v3-256.png` y `user-cuecca-v3-256.png`, servidos desde el repositorio `botcc-avatares` por jsDelivr |

Todas las variables de Typebot (`--typebot-*`) se redefinen con `!important`, porque Typebot las aplica en línea.

## 2. Colores por área

Cada botón tiene una marca izquierda (`--accent`) que indica el área. El mismo criterio vale para el menú principal y los submenús.

| Color | Variable | Área |
|---|---|---|
| Naranja `#f59e0b` | `--px-orange` | Deuda, facturas y pagos |
| Rojo `#e53935` | `--px-red` | Reclamos y soporte técnico |
| Amarillo `#f6c90e` | `--px-yellow` | Suministros y energía |
| Verde `#2ea44f` | `--px-green` | Internet y confirmaciones |
| Azul `#1e63c6` | `--px-blue` | Agua, información, operador y reintentos |
| Violeta `#7b3fb5` | `--px-violet` | Trámites, tarifas y alta de servicio |
| Gris `#cfd6df` | — | Opciones secundarias ("No los acepto", "Continuar como invitado") |
| Azul marino | `--cuecca-navy-2` | Botones sin categoría (listas dinámicas) |

Dentro de **Reclamos**, cada servicio usa su color en todo el recorrido: energía amarillo, agua azul, internet verde.

Los botones de **navegación** ("Volver…", "Salir", "Cerrar sesión") no llevan marca ni flecha y se ven como pie de la tarjeta, en gris y más chicos. "Próximamente" se muestra apagado.

## 3. Cómo se asigna el color

El CSS no puede seleccionar un botón por su texto. Se usa el atributo `data-itemid`, que es el `id` del botón en el export de Typebot:

```css
[data-itemid="rtzxpz4vf19n6ecm1zp3powe"],   /* Módulo de Reclamos · ⚡ Reclamo de Energía */
[data-itemid="z9wtndolnsx3sib128dr54v0"]    /* Reclamo de Energia · Medicion de Voltaje  */
  { --accent: var(--px-yellow); }
```

El color por defecto se declara con `:where(...)`, que tiene especificidad 0, para que nunca pise a un `[data-itemid]`.

**Limitaciones**

- **Si se borra un botón y se crea de nuevo, cambia su ID** y pierde el color, sin ningún error visible.
- Las **listas dinámicas** (domicilios vinculados y lista de reclamos) se generan en tiempo de ejecución con IDs propios de Typebot: toman el azul marino por defecto.

## 4. Regenerar los colores después de cambiar el flujo

[`estilos/generar_colores_botones.py`](../estilos/generar_colores_botones.py) arma la sección de submenús a partir del export:

```bash
python estilos/generar_colores_botones.py typebot-export.json typebot-con-css.json tema.css
```

El script **falla a propósito** si un ID de su lista ya no existe o si aparece un botón nuevo sin categoría, y muestra cuál. Para resolverlo, agregar el ID nuevo a la lista de color correspondiente (`C`) o a la de navegación (`NAV`) y volver a correrlo. Después, pegar `tema.css` en Tema → Custom CSS o importar `typebot-con-css.json`.

Los 14 botones del menú principal están en el CSS a mano (sección "Categorías del menú principal").
