# GUARDIAN Community 0.4.0

Conciliación local de ventas y pagos. Importa dos reportes CSV independientes, compara referencias, importes, monedas y estados, y gestiona las diferencias con responsable, notas e historial.

<p align="center"><img src="demo/fraudguard/static/guardian-emblem.png" width="360" alt="GUARDIAN"></p>

## Uso operativo

1. Instala GUARDIAN y abre la aplicación.
2. En **Compara ventas contra el procesador**, carga el reporte de ventas y el del procesador o banco.
3. Consulta el dashboard y revisa los casos detectados.
4. Asigna responsable, registra una nota y marca cada caso como confirmado, resuelto o falso positivo.
5. Exporta resultados y abre conciliaciones anteriores desde **Conciliaciones guardadas**.

[Manual completo](MANUAL_DE_USO.md) · [Notas 0.4.0](RELEASE_NOTES_0.4.0.md) · [Licencia MIT](LICENSE)

## Lo que comprueba

- Ventas ausentes del reporte de pagos y pagos sin venta asociada.
- Importes y monedas diferentes.
- Referencias repetidas en cualquiera de las dos fuentes; se marcan como ambiguas.
- Pagos aprobados que todavía no están cobrados o liquidados.
- Rechazos, pendientes, reembolsos y contracargos.
- Estados desconocidos, referencias vacías, importes inválidos y columnas ambiguas.

Los reportes deben compartir una referencia común. Los encabezados admiten sinónimos frecuentes en español e inglés; si no se reconocen, la carga explica qué campo falta. No se inventan coincidencias por nombre o importe.

## Persistencia y privacidad

Las conciliaciones, notas e historial se guardan en SQLite dentro de la carpeta local de GUARDIAN. Al reiniciar pueden abrirse los análisis guardados. Las revisiones están separadas por conciliación. El modo local escucha solo en 127.0.0.1; no envía reportes a servicios externos.

## Alcance comprobado

Procesa reportes CSV de hasta 10 MB y 50.000 filas por archivo. Admite coma, punto y coma y tabulaciones, importes con formatos 1.234,56 y 1,234.56 y estados normalizados. El motor compara lo informado por los reportes; no consulta ni mueve fondos en el banco. No convierte monedas ni concilia automáticamente comisiones o pagos parciales. Esos casos se investigan en la bandeja.

Los ejemplos integrados son sintéticos y permiten aprender; el importador acepta archivos operativos del usuario con los campos requeridos. La compatibilidad con un proveedor específico se valida con sus exportaciones.

## Desarrollo y verificación

Requiere Python 3.12 o posterior.

~~~powershell
python -m pip install -r demo/requirements.txt
cd demo
python -m unittest discover -v
python -m fraudguard.launcher
~~~

El instalador se genera con **installer/build.ps1** (PyInstaller e Inno Setup). Pruebas verifican conciliación, errores, persistencia tras reiniciar, revisiones por análisis, protección de formularios y acceso LAN.

## Trabajo profesional

Para integraciones, adaptación a reportes de proveedores o contratación, abre una consulta profesional en Issues. No publiques datos de clientes en el repositorio.
