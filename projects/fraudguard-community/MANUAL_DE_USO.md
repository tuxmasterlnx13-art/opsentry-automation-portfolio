# Manual de uso — GUARDIAN Community

> Detecta señales que merecen investigación sin enviar tus operaciones a la nube y sin escribir código.

## Inicio rápido en 5 minutos

1. Instala GUARDIAN con **Siguiente → Siguiente → Instalar → Finalizar**.
2. Abre **GUARDIAN Community** desde el escritorio o el menú Inicio.
3. Pulsa **Probar con datos de demostración** para conocer el informe sin usar datos reales.
4. Descarga **Plantilla para Excel** dentro de la aplicación.
5. Sustituye el ejemplo por tus operaciones, guarda como CSV y pulsa **Analizar con Guardian**.

GUARDIAN no declara que exista fraude. Ordena señales para que una persona investigue primero los casos con mayor riesgo.

## Qué archivo debes subir

Usa un archivo `.csv` UTF-8 de hasta 10 MB. Una fila representa una operación y la primera fila conserva exactamente estos nombres:

| Columna | Qué debes colocar | Ejemplo |
|---|---|---|
| `transaction_id` | Identificador único de la operación | `VENTA-10025` |
| `customer_id` | Identificador interno del cliente | `CLIENTE-204` |
| `amount` | Importe, sin símbolo de moneda | `1250.50` |
| `timestamp` | Fecha y hora en formato ISO | `2026-11-06T10:15:00` |
| `country` | País, preferentemente código de dos letras | `BO` |
| `device_id` | Identificador del equipo, navegador o dispositivo | `DISPOSITIVO-88` |
| `payment_method` | Medio de pago | `card`, `wallet` o `transfer` |

### Prepararlo con Excel

1. Descarga `plantilla_guardian.csv` desde GUARDIAN.
2. Ábrela con Excel.
3. Conserva los títulos de la primera fila y reemplaza la fila de ejemplo.
4. Agrega una operación por fila.
5. Elige **Archivo → Guardar como → CSV UTF-8 (delimitado por comas)**.
6. Carga ese archivo en GUARDIAN.

No incluyas contraseñas, números completos de tarjetas, documentos de identidad ni otros secretos. Usa identificadores internos cuando sea posible.

## Cómo asignar reglas sin programar

En la pantalla principal busca **Reglas de tu empresa**, cambia los números y pulsa **Guardar reglas**. Los nuevos valores se aplican al siguiente análisis durante esa sesión. Al cerrar GUARDIAN se recuperan los valores iniciales.

| Regla | Valor inicial | Cuándo genera una señal |
|---|---:|---|
| Importe alto | 5000 | La operación alcanza o supera el importe indicado |
| Operaciones rápidas | 4 en 10 min | El mismo cliente realiza varias operaciones en poco tiempo |
| Cambio rápido de país | 60 min | Un cliente aparece en más de un país dentro de la ventana |
| Dispositivo compartido | 3 clientes | Un dispositivo es usado por varias identidades |
| ID duplicado | Siempre activo | El mismo identificador de operación aparece más de una vez |

Ejemplo: si tu negocio considera inusual una compra superior a 1.000, escribe `1000` en **Importe alto desde**. Si el comportamiento normal varía por temporada o país, valida los límites con las áreas de fraude, riesgo y cumplimiento antes de usarlos operativamente.

## Cómo leer el informe

- **Alto:** combinación de patrones; revisar con prioridad.
- **Medio:** señal relevante que necesita contexto.
- **Bajo:** señal aislada; observar o contrastar.
- **Sin alerta:** ninguna regla configurada coincidió.

Cada fila explica sus razones. Pulsa **Exportar CSV** para entregar los resultados al equipo que realizará la investigación.

## Acceso de empresa

- **GUARDIAN Community:** abre el sistema únicamente en esta computadora.
- **GUARDIAN — acceso de empresa:** permite acceso desde la red local y solicita una clave compartida.
- **GUARDIAN — restablecer clave de empresa:** crea una clave nueva si se pierde la anterior.

No expongas el modo de red directamente a Internet. Una implantación remota necesita HTTPS, identidades individuales, registro de auditoría y una revisión profesional de seguridad.

## Problemas frecuentes

| Mensaje o situación | Solución |
|---|---|
| “Faltan columnas” | Compara la primera fila con la tabla de este manual |
| “Solo se aceptan archivos CSV” | Guarda desde Excel como CSV UTF-8 |
| Importe o fecha inválidos | Usa `1250.50` y `AAAA-MM-DDTHH:MM:SS` |
| No aparece ninguna alerta | Revisa los límites o prueba primero la demostración |
| Otra persona no puede entrar | Confirma que abriste **acceso de empresa** y que ambos equipos están en la misma red |

## Uso responsable

GUARDIAN es una herramienta de priorización, no una decisión automática. Una alerta nunca debe ser la única razón para rechazar pagos, bloquear cuentas o acusar a una persona. Documenta la revisión humana y respeta las leyes de privacidad aplicables.

## Soporte y colaboración

Para informar un problema, proponer una regla o conversar sobre una implantación empresarial, abre un **Issue** en el repositorio público. No adjuntes datos reales de clientes.
