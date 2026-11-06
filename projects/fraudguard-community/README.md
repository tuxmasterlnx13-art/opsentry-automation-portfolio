# GUARDIAN Community

### Fraude visible. Decisiones humanas.

<p align="center">
  <img src="demo/fraudguard/static/guardian-emblem.png" width="360" alt="GUARDIAN: casco antiguo con dos espadas">
</p>

Aplicación de escritorio gratuita y de código abierto para convertir operaciones en señales de fraude explicables. Se instala en Windows con **Siguiente → Siguiente → Finalizar**, funciona localmente y permite ajustar reglas sin programación.

[![Licencia MIT](https://img.shields.io/badge/licencia-MIT-8b5cf6.svg)](LICENSE)
![Privacidad local](https://img.shields.io/badge/datos-locales-16a34a.svg)
![Windows](https://img.shields.io/badge/Windows-instalador-2563eb.svg)
![Sin código](https://img.shields.io/badge/configuración-sin%20código-d97706.svg)

## Pruébalo sin datos reales

1. Descarga `Guardian-Community-Setup.exe` desde **Releases**.
2. Instala y abre GUARDIAN.
3. Pulsa **Probar con datos de demostración**.
4. Explora el informe y ajusta las reglas visualmente.

Consulta el [manual completo en español](MANUAL_DE_USO.md) para preparar Excel/CSV, asignar reglas, interpretar resultados y habilitar acceso en la red de una empresa.

## Qué resuelve

| Señal explicable | Ejemplo de uso |
|---|---|
| Transacción duplicada | Errores, reintentos o abuso de identificadores |
| Importe inusualmente alto | Priorizar operaciones fuera del patrón del negocio |
| Alta velocidad | Varias operaciones del mismo cliente en pocos minutos |
| Cambio rápido de país | Movimientos geográficos incompatibles en una ventana corta |
| Dispositivo compartido | Varias identidades usando el mismo equipo |

Cada resultado incluye puntuación, nivel y razones legibles. Una alerta es una pista para revisión humana, nunca una prueba ni una acusación.

## Diseñado para adopción real

- Instalador y asistente en español.
- Plantilla CSV compatible con Excel.
- Demostración sintética integrada.
- Reglas configurables desde la interfaz.
- Procesamiento local, sin telemetría y sin nube.
- Exportación del informe a CSV.
- Modo individual y modo LAN protegido con clave.

## Formato de entrada

```text
transaction_id,customer_id,amount,timestamp,country,device_id,payment_method
```

El manual explica cada columna con ejemplos. No publiques archivos con datos reales en GitHub.

## Arquitectura auditable

```text
CSV local → validación → reglas explicables → puntuación → revisión humana → exportación
```

El motor no depende de un proveedor, modelo opaco ni servicio externo. Las reglas están en [`demo/fraudguard/engine.py`](demo/fraudguard/engine.py) y las pruebas automatizadas cubren el análisis, la interfaz, el acceso LAN y la configuración visual.

## Seguridad y privacidad

- El modo local solo responde en `127.0.0.1`.
- Los archivos no salen de la computadora.
- El modo LAN exige una clave compartida.
- No se incluyen credenciales ni datos reales en el repositorio.
- No debe publicarse directamente en Internet sin HTTPS, identidad empresarial y revisión profesional.

## Para equipos y empresas

Este proyecto demuestra competencias en automatización, Python, detección de anomalías, UX para usuarios no técnicos, empaquetado de Windows, pruebas y seguridad por diseño.

¿Quieres adaptar las reglas, integrar una fuente de datos, añadir auditoría o preparar una implantación empresarial? Abre un **Issue** con el caso de uso, sin información confidencial. El proyecto está disponible para colaboración y trabajo profesional.

## Desarrollo

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r demo\requirements.txt
Set-Location demo
python -m unittest discover -v
python -m fraudguard.launcher
```

El instalador se genera con `installer/build.ps1`. La licencia es [MIT](LICENSE): puede usarse, estudiarse y modificarse libremente, sin garantía.
