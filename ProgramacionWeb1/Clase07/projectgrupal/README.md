# Project Grupal - Libreria PDF en PHP

Este proyecto implementa una pequena libreria en PHP para construir documentos PDF sin depender de Composer ni paquetes externos. La demostracion genera una factura simple con datos de cliente, detalle de productos, totales y observaciones.

## Estructura

- `src/SimplePdfDocument.php`: clase base para crear paginas, texto, lineas, rectangulos y tablas en PDF.
- `src/InvoicePdf.php`: clase especializada para construir una factura usando la libreria base.
- `demo_factura.php`: ejemplo listo para ejecutar y generar `factura_demo.pdf`.

## Como ejecutar

Desde una terminal ubicada en esta carpeta:

```bash
php demo_factura.php
```

Tambien se puede copiar la carpeta a `htdocs` o al servidor local usado en clase y abrir `demo_factura.php` desde el navegador.

## Que demuestra

- Uso de clases y metodos en PHP.
- Construccion de un documento PDF.
- Arrays asociativos y multidimensionales.
- Separacion entre libreria (`src`) y ejemplo de uso (`demo_factura.php`).
- Generacion dinamica de totales para una factura.
