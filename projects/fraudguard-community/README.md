# GUARDIAN Community

Aplicación visual y gratuita para revisar archivos CSV y encontrar patrones que merecen investigación. Está pensada para personas sin conocimientos de programación: en Windows se instala con **Siguiente → Siguiente → Finalizar** y se abre desde el menú Inicio.

## Qué detecta

- identificadores de transacción duplicados;
- importes inusualmente altos;
- muchas operaciones del mismo cliente en pocos minutos;
- cambios rápidos de país para un mismo cliente;
- un dispositivo compartido por demasiados clientes.

Cada alerta muestra una puntuación y razones legibles. Una alerta **no prueba un fraude**: sirve para priorizar revisión humana.

## Privacidad y acceso

- Modo local: solo responde en `127.0.0.1`; los datos no salen de la computadora.
- Modo Empresa/LAN: permite acceso desde la red local y exige una clave compartida.
- El menú Inicio incluye una opción para restablecer la clave de empresa si se pierde.
- No incluye telemetría, nube ni credenciales de terceros.
- No debe exponerse directamente a Internet. Para uso remoto se necesita HTTPS, identidad empresarial y una revisión profesional de seguridad.

## Archivo esperado

CSV UTF-8 con estas columnas:

```text
transaction_id,customer_id,amount,timestamp,country,device_id,payment_method
```

`timestamp` usa ISO 8601, por ejemplo `2026-11-06T10:15:00`.

## Desarrollo

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r demo\requirements.txt
Set-Location demo
python -m unittest discover -v
python -m fraudguard.launcher
```

## Instalador de Windows

Ejecuta `installer\build.ps1`. El script genera el ejecutable con PyInstaller y, si Inno Setup 6 está instalado, produce `Guardian-Community-Setup.exe`.

## Licencia

La edición GUARDIAN Community se distribuye bajo licencia MIT. Puede usarse, estudiarse y modificarse libremente, sin garantía y respetando la licencia incluida.

