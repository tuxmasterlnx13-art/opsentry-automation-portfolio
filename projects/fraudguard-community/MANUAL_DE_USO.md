# GUARDIAN — manual de uso operativo

## 1. Instalar y abrir

Ejecuta Guardian-Community-Setup.exe, sigue el asistente y abre GUARDIAN desde Inicio. Se abrirá en el navegador de esta computadora.

## 2. Preparar las dos fuentes

El archivo de ventas representa lo que debía ocurrir. El archivo del banco/procesador representa lo que ese proveedor informa. Ambos deben contener la misma referencia del pago.

| Campo | Ventas | Procesador | Ejemplos de encabezado admitidos |
|---|---|---|---|
| Referencia | transaction_id | transaction_id | Referencia, payment_id, ID de pago, id_orden |
| Comercio | merchant_id, opcional | — | Comercio, Tienda, merchant |
| Importe | expected_amount | charged_amount | Importe esperado, Monto cobrado, amount |
| Moneda | currency | currency | Moneda, Divisa, currency_code |
| Estado | expected_status | actual_status | Estado esperado, Estado del pago, status |
| Fecha de liquidación | — | settled_at | Fecha de liquidación, paid_at |

En cada fuente el encabezado genérico amount o status se interpreta según el papel del archivo. Dos columnas que representan el mismo campo se rechazan: hay que distinguirlas antes de cargar.

Exporta desde Excel como CSV UTF-8. Se reconocen coma, punto y coma y tabulación. Una fila por registro, sin títulos decorativos encima del encabezado. Máximo 10 MB por solicitud y 50.000 filas por reporte. La referencia debe conservarse como texto, incluidos ceros iniciales.

Importes admitidos: 120, 120.50, 120,50, 1.234,56 y 1,234.56. Usa cifras sin símbolo monetario. Un formato ambiguo se señala; no se adivina. La moneda debe ser un código como BOB, USD o EUR.

## 3. Conciliar

En **Compara ventas contra el procesador**, selecciona ambos CSV y pulsa **Conciliar los dos reportes**. Puedes descargar dos ejemplos desde esa misma sección para aprender el formato.

Las referencias se cruzan exactamente después de quitar espacios exteriores. Si una referencia se repite, el resultado indica cuántas filas la contienen y solicita revisión; no declara una coincidencia correcta eligiendo una fila al azar.

## 4. Interpretar los estados

| Estado | Significado |
|---|---|
| approved / aprobado / autorizado | Autorización, todavía no confirma cobro ni abono |
| paid / pagado / cobrado / captured | Cobro registrado, distinto de liquidación |
| settled / liquidado / acreditado | Liquidación informada en el reporte |
| declined / rejected / rechazado / failed | Rechazo o fallo |
| pending / pendiente / processing | Proceso todavía sin completar |
| refunded / reembolsado | Devolución que debe revisarse |
| chargeback / contracargo | Disputa o reversión que debe revisarse |

Un estado no reconocido genera revisión. Que dos importes coincidan no prueba que el dinero haya llegado: el estado también debe corresponder a lo esperado. GUARDIAN usa los datos de los archivos; comprueba el abono definitivo con tu proveedor si su reporte no lo acredita.

## 5. Trabajar las diferencias

El dashboard muestra referencias revisadas, diferencias, rechazos y casos abiertos. Cada fila explica qué no coincide. Registra un responsable y una nota, y selecciona Pendiente, Confirmada, Resuelta o Falso positivo. Confirmada sigue contando como trabajo abierto.

**Historial** muestra los últimos veinte cambios del caso con fecha UTC. Las revisiones se vinculan al análisis, por lo que una referencia de otro período no hereda automáticamente la resolución anterior.

## 6. Volver y exportar

GUARDIAN guarda cada análisis en esta computadora. **Conciliaciones guardadas** permite abrir los últimos 25; el almacenamiento conserva los demás. El archivo exportado incluye resultado, responsable, estado de revisión y nota. Los textos peligrosos para Excel se exportan como texto.

Al cerrar y abrir GUARDIAN se recupera el último análisis. En Windows el archivo operativo está en **%LOCALAPPDATA%/GuardianCommunity/guardian-reviews.sqlite3**. Para conservar un respaldo, cierra GUARDIAN y copia ese archivo a una ubicación de respaldo bajo tu control.

## Alcance

El uso individual funciona localmente. El acceso LAN usa clave compartida y no equivale a cuentas individuales con identidad auditada. No expongas ese modo directamente a Internet. Los datos y notas permanecen en el equipo que ejecuta GUARDIAN.

Comisiones, netos frente a brutos, pagos parciales, conversiones de moneda y varios eventos por referencia necesitan reglas del proveedor. La aplicación identifica la ambigüedad para revisión humana; no inventa su significado. Si el banco y ventas no tienen una referencia común, primero hay que acordar el campo de cruce.
