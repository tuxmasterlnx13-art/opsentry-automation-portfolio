# GUARDIAN Community 0.4.0

Conciliación local operativa de dos fuentes CSV.

- Guarda análisis y revisiones en SQLite y recupera resultados al reiniciar.
- Separa las revisiones por conciliación y ofrece historial de cambios.
- Distingue aprobación, cobro y liquidación; identifica pendientes, rechazos, devoluciones y estados desconocidos.
- Detecta referencias repetidas y vacías sin inventar coincidencias.
- Reconoce encabezados frecuentes en español e inglés, separadores CSV e importes de ambos formatos regionales.
- Exporta resultados y seguimiento como CSV.
- Protege los formularios contra solicitudes sin token de sesión.
- Incluye modo claro/oscuro, selector de idiomas y animación del emblema.

No necesita servicios de nube para el cruce. El importador usa exportaciones del usuario y no mueve dinero. La compatibilidad específica de un proveedor requiere validar sus reportes. No hay conversión de divisas ni compensación automática de comisiones o pagos parciales.
