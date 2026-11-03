# Corrección H-14 — Año y meses fijos

> ✅ **Aplicada y verificada.** Deuda: 02-11-2026. Consumos (ventana de 3 meses): 03-11-2026.

Workflow: `2.consultar_deuda`. Siete nodos SQL y un nodo Code.

| Nodo | Cambio |
|---|---|
| `DEUDA_TOTAL` | Quitar `d.Anio = 2026` (5 veces) y ordenar por año y mes |
| `Deuda_Servicio Energia` / `_Agua` / `_Internet` | Quitar `d.Anio = 2026` y ordenar por año y mes |
| `Deuda_Servicio_Sepelio` / `_Municipalidad` | Ídem |
| `Consulta_consumos_socio` | Reemplazar `Mes IN (7,8,9)` por "últimos 3 períodos con lectura" |
| `Code - Mapeo_Deuda_Total` | Ordenar los períodos como números, no como texto |
| `Code_Deuda_Servicios`, `Mapeo_consumos` | Sin cambios |

**Criterio:** una deuda pendiente se define por `Total <> Imputado`. El filtro por año no aporta nada a esa definición y deja afuera deudas de años anteriores.

## 0. Antes de aplicar

Al quitar el filtro de año pueden aparecer saldos viejos que hoy no se ven (diferencias de centavos, comprobantes mal imputados). Corré esto en SIACCOP para saber qué va a aparecer:

```sql
SELECT Anio, Servicio, COUNT(*) AS Comprobantes, SUM(Total - Imputado) AS Saldo
FROM DEUDA
WHERE Total <> Imputado
GROUP BY Anio, Servicio
ORDER BY Anio, Servicio;
```

Si aparecen años viejos con saldos que no son deuda real, usá la **variante con ventana** del final en lugar de quitar el filtro.

## 1. `DEUDA_TOTAL`

```sql
SELECT 
    d.ID,
    d.Usuario,
    d.NroSocio,
    d.Domicilio,
    'Energia' AS Servicio,
    d.Mes,
    d.Anio,
    CONVERT(VARCHAR(10), DATEADD(day, CAST(d.FechaVencimiento AS INT) - 4, CAST('1801-01-01' AS DATE)), 103) AS FechaVencimientoFormateada,
    (d.Total - d.Imputado) AS MontoaPagar,
    NULL AS ItemFacturado
FROM DEUDA d 
INNER JOIN USUENER ue ON ue.Socio = d.NroSocio AND ue.Codigo = d.Usuario 
WHERE d.NroSocio = '{{ $json.socio }}' 
  AND d.Total <> d.Imputado AND d.Servicio = 'Energia'

UNION ALL

SELECT 
    d.ID,
    d.Usuario,
    d.NroSocio,
    d.Domicilio,
    'Agua' AS Servicio,
    d.Mes,
    d.Anio,
    CONVERT(VARCHAR(10), DATEADD(day, CAST(d.FechaVencimiento AS INT) - 4, CAST('1801-01-01' AS DATE)), 103) AS FechaVencimientoFormateada,
    (d.Total - d.Imputado) AS MontoaPagar,
    NULL AS ItemFacturado
FROM DEUDA d 
INNER JOIN USUAGUA ua ON ua.Socio = d.NroSocio AND ua.Codigo = d.Usuario 
WHERE d.NroSocio = '{{ $json.socio }}' 
  AND d.Total <> d.Imputado AND d.Servicio = 'Agua'

UNION ALL

SELECT 
    d.ID,
    d.Usuario,
    d.NroSocio,
    d.Domicilio,
    'Internet' AS Servicio,
    d.Mes,
    d.Anio,
    CONVERT(VARCHAR(10), DATEADD(day, CAST(d.FechaVencimiento AS INT) - 4, CAST('1801-01-01' AS DATE)), 103) AS FechaVencimientoFormateada,
    (d.Total - d.Imputado) AS MontoaPagar,
    NULL AS ItemFacturado
FROM DEUDA d 
INNER JOIN USUINTE ui ON ui.Socio = d.NroSocio AND ui.Codigo = d.Usuario 
WHERE d.NroSocio = '{{ $json.socio }}' 
  AND d.Total <> d.Imputado AND d.Servicio = 'Internet'

UNION ALL

SELECT 
    d.ID,
    d.Usuario,
    d.NroSocio,
    d.Domicilio,
    'Sepelio' AS Servicio,
    d.Mes,
    d.Anio,
    CONVERT(VARCHAR(10), DATEADD(day, CAST(d.FechaVencimiento AS INT) - 4, CAST('1801-01-01' AS DATE)), 103) AS FechaVencimientoFormateada,
    (dd.Gravado + dd.IVA + dd.Exento + dd.NoGravado) AS MontoaPagar,
    dd.Descripcion AS ItemFacturado
FROM DEUDA d 
INNER JOIN DEUDA_DET dd ON d.ID = dd.ID
INNER JOIN ITEMS it ON dd.Item = it.ID
WHERE d.NroSocio = '{{ $json.socio }}' 
  AND d.Prefijo <> 34 
  AND it.ID = 101 
  AND (dd.Gravado + dd.IVA + dd.Exento + dd.NoGravado) > 0 
  AND d.Total <> d.Imputado

UNION ALL

SELECT 
    d.ID,
    d.Usuario,
    d.NroSocio,
    d.Domicilio,
    'Municipalidad' AS Servicio,
    d.Mes,
    d.Anio,
    CONVERT(VARCHAR(10), DATEADD(day, CAST(d.FechaVencimiento AS INT) - 4, CAST('1801-01-01' AS DATE)), 103) AS FechaVencimientoFormateada,
    (d.Total - d.Imputado) AS MontoaPagar,
    NULL AS ItemFacturado
FROM DEUDA d 
WHERE d.NroSocio = '{{ $json.socio }}' 
  AND d.Prefijo = 99 
  AND d.Total <> d.Imputado

ORDER BY Servicio, Anio ASC, Mes ASC;
```

## 2. `Deuda_Servicio Energia`

```sql
SELECT 
    d.ID,
    ue.Codigo AS Usuario,
    d.NroSocio,
    ue.Domicilio,
    d.Servicio,
    d.Mes,
    d.Anio,
    CONVERT(VARCHAR(10), DATEADD(day, CAST(d.FechaVencimiento AS INT) - 4, CAST('1801-01-01' AS DATE)), 103) AS FechaVencimientoFormateada,
    (d.Total - d.Imputado) AS MontoaPagar
FROM DEUDA d 
INNER JOIN USUENER ue 
    ON ue.Socio = d.NroSocio 
   AND ue.Codigo = d.Usuario 
WHERE 
    d.NroSocio = '{{ $json.socio }}' 
    AND UPPER(TRIM(ue.Domicilio)) = UPPER(TRIM('{{ $json.domicilio_limpio }}')) 
    AND d.Total <> d.Imputado 
    AND d.Servicio = 'Energia'
ORDER BY d.Anio DESC, d.Mes DESC;
```

## 3. `Deuda_Servicio_Agua`

```sql
SELECT 
    d.ID,
    ua.Codigo,
    d.NroSocio,
    ua.Domicilio,
    d.Servicio,
    d.Mes,
    d.Anio,
    CONVERT(VARCHAR(10), DATEADD(day, CAST(d.FechaVencimiento AS INT) - 4, CAST('1801-01-01' AS DATE)), 103) AS FechaVencimientoFormateada,
    (d.Total - d.Imputado) AS MontoaPagar
FROM DEUDA d 
INNER JOIN USUAGUA ua 
    ON ua.Socio = d.NroSocio 
   AND ua.Codigo = d.Usuario 
WHERE 
    d.NroSocio = '{{ $json.socio }}'
    AND UPPER(TRIM(ua.Domicilio)) = UPPER(TRIM('{{ $json.domicilio_limpio }}'))
    AND d.Total <> d.Imputado 
    AND d.Servicio = 'Agua'
ORDER BY d.Anio DESC, d.Mes DESC;
```

## 4. `Deuda_Servicio_Internet`

```sql
SELECT 
    d.ID,
    ui.Codigo,
    d.NroSocio,
    ui.Domicilio,
    d.Servicio,
    d.Mes,
    d.Anio,
    CONVERT(VARCHAR(10), DATEADD(day, CAST(d.FechaVencimiento AS INT) - 4, CAST('1801-01-01' AS DATE)), 103) AS FechaVencimientoFormateada,
    (d.Total - d.Imputado) AS MontoaPagar
FROM DEUDA d 
INNER JOIN USUINTE ui 
    ON ui.Socio = d.NroSocio 
   AND ui.Codigo = d.Usuario 
WHERE 
    d.NroSocio = '{{ $json.socio }}' 
    AND UPPER(TRIM(ui.Domicilio)) = UPPER(TRIM('{{ $json.domicilio_limpio }}'))
    AND d.Total <> d.Imputado 
    AND d.Servicio = 'Internet'
ORDER BY d.Anio DESC, d.Mes DESC;
```

## 5. `Deuda_Servicio_Sepelio`

Además del año, le agregué comillas a `NroSocio`, igual que en las otras consultas. Sin ellas, si `socio` llega vacío la consulta falla por error de sintaxis.

```sql
SELECT 
    d.Usuario,
    d.Mes,
    d.Anio,
    d.FechaVencimiento,
    dd.Descripcion AS ItemFacturado,
    dd.Gravado,
    dd.NoGravado,
    dd.IVA,
    dd.Exento,
    d.Prefijo,
    d.Domicilio,
    d.Total,
    d.Imputado,
    (dd.Gravado + dd.IVA + dd.Exento + dd.NoGravado) AS SubtotalItem
FROM DEUDA d 
INNER JOIN DEUDA_DET dd ON d.ID = dd.ID
INNER JOIN ITEMS it ON dd.Item = it.ID
WHERE 
    d.NroSocio = '{{ $json.socio }}'
    AND d.Prefijo <> 34
    AND it.ID = 101
    AND d.Domicilio LIKE '%{{ $json.domicilio_limpio }}%'
    AND (dd.Gravado + dd.IVA + dd.Exento + dd.NoGravado) > 0
    AND d.Total <> d.Imputado
ORDER BY d.Anio ASC, d.Mes ASC, dd.Item ASC;
```

> Esta consulta devuelve `FechaVencimiento` sin formatear, así que en el bot las tarjetas de sepelio salen con "Vencimiento: A confirmar". Ya pasaba antes de este cambio. Si querés corregirlo, reemplazá `d.FechaVencimiento,` por la misma línea `CONVERT(...) AS FechaVencimientoFormateada,` de las otras consultas.

## 6. `Deuda_Servicio_Municipalidad`

```sql
SELECT 
    d.NroSocio,
    d.Usuario,
    d.Domicilio,
    d.Mes,
    d.Anio,
    CONVERT(VARCHAR(10), DATEADD(day, CAST(d.FechaVencimiento AS INT) - 4, CAST('1801-01-01' AS DATE)), 103) AS FechaVencimientoFormateada,
    d.Total,
    d.Imputado,
    (d.Total - d.Imputado) AS MontoaPagar
FROM DEUDA d 
WHERE 
    d.NroSocio = '{{ $json.socio }}'
    AND d.Prefijo = 99
    AND d.Total <> d.Imputado
ORDER BY d.Anio ASC, d.Mes ASC;
```

## 7. `Consulta_consumos_socio`

### Opción A (aplicada): cambio de una línea, últimos 3 meses del calendario

En los dos `SELECT` (energía y agua), reemplazar:

```sql
  AND est.Anio = 2026 AND est.Mes IN (7, 8, 9)
```

por:

```sql
  AND (est.Anio * 100 + est.Mes) BETWEEN (YEAR(DATEADD(MONTH, -3, GETDATE())) * 100 + MONTH(DATEADD(MONTH, -3, GETDATE())))
                                     AND (YEAR(DATEADD(MONTH, -1, GETDATE())) * 100 + MONTH(DATEADD(MONTH, -1, GETDATE())))
```

Toma los 3 meses anteriores al actual (en octubre de 2026: 7, 8 y 9). Funciona también cuando cambia el año. Si falta la lectura de un mes, se muestran menos de 3 períodos.

### Opción B: últimas 3 lecturas de cada medidor

Úsala solo si las lecturas se cargan con atraso. Trae las 3 más recientes que existan, sea cual sea el mes o el año.

```sql
WITH Lecturas AS (
    SELECT 
        ue.Nombre,
        ue.Socio,
        ue.Codigo,
        ue.Domicilio,
        ue.Medidor,
        'Energia' AS Servicio,
        est.Mes,
        est.Anio,
        est.Consumo,
        ROW_NUMBER() OVER (PARTITION BY ue.Codigo ORDER BY est.Anio DESC, est.Mes DESC) AS Orden
    FROM USUENER ue 
    INNER JOIN ESTADOS est ON ue.Codigo = est.Usuario
    WHERE ue.Socio = '{{ $json.body.Socio }}'
      AND est.Servicio = 'Energia'

    UNION ALL

    SELECT 
        ua.Nombre,
        ua.Socio,
        ua.Codigo,
        ua.Domicilio,
        ua.Medidor,
        'Agua' AS Servicio,
        est.Mes,
        est.Anio,
        est.Consumo,
        ROW_NUMBER() OVER (PARTITION BY ua.Codigo ORDER BY est.Anio DESC, est.Mes DESC) AS Orden
    FROM USUAGUA ua 
    INNER JOIN ESTADOS est ON ua.Codigo = est.Usuario
    WHERE ua.Socio = '{{ $json.body.Socio }}'
      AND est.Servicio = 'Agua'
)
SELECT Nombre, Socio, Codigo, Domicilio, Medidor, Servicio, Mes, Anio, Consumo
FROM Lecturas
WHERE Orden <= 3
ORDER BY Servicio, Domicilio, Anio DESC, Mes DESC;
```

Para cambiar la cantidad de períodos, modificá `Orden <= 3`. Si un medidor tiene dos lecturas en el mismo mes, cuentan como dos de las tres.

`Mapeo_consumos` no necesita cambios: arma los textos en el orden en que llegan las filas.

## 8. `Code - Mapeo_Deuda_Total`

Hoy los períodos se ordenan como texto (`Object.keys(...).sort()`). Eso ya ordena mal dentro de un mismo año, y con varios años queda peor:

| | Resultado |
|---|---|
| Actual | `1/2026 · 10/2026 · 12/2025 · 9/2026` |
| Corregido | `12/2025 · 1/2026 · 9/2026 · 10/2026` |

Son **dos cambios** en el código.

**Cambio 1:** dentro del `items.forEach`, reemplazá:

```js
    if (!periodosMap[periodoKey]) {
      periodosMap[periodoKey] = {
        montoTotalPeriodo: 0,
        conceptos: []
      };
    }
```

por:

```js
    if (!periodosMap[periodoKey]) {
      periodosMap[periodoKey] = {
        orden: Number(item.Anio) * 100 + Number(item.Mes),
        montoTotalPeriodo: 0,
        conceptos: []
      };
    }
```

**Cambio 2:** reemplazá:

```js
  Object.keys(periodosMap).sort().forEach(periodo => {
```

por:

```js
  Object.keys(periodosMap).sort((a, b) => periodosMap[a].orden - periodosMap[b].orden).forEach(periodo => {
```

## Variante con ventana (solo si el paso 0 muestra saldos viejos que no son deuda real)

En las consultas de deuda, en lugar de borrar la línea `AND d.Anio = 2026`, reemplazala por esta, que toma los últimos 24 meses:

```sql
AND (d.Anio * 100 + d.Mes) >= (YEAR(DATEADD(MONTH, -24, GETDATE())) * 100 + MONTH(DATEADD(MONTH, -24, GETDATE())))
```

## Verificación después de aplicar

1. Ejecutar *Consultar deuda total* con un socio que tenga deuda en más de un mes y verificar que los períodos salgan en orden cronológico.
2. Comparar el total del bot con el saldo del socio en SIACCOP.
3. *Mis Consumos*: tienen que aparecer las 3 lecturas más recientes de cada medidor.
