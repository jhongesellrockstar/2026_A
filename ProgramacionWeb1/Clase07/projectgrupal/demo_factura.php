<?php

require_once __DIR__ . '/src/InvoicePdf.php';

$invoice = [
    'empresa' => 'Soluciones Web Clase 07',
    'ruc' => '20481234567',
    'fecha' => date('Y-m-d'),
    'numero' => 'F001-000123',
    'cliente' => 'Cliente de demostracion',
    'documento' => 'DNI 76543210',
    'items' => [
        ['descripcion' => 'Diseno de pagina informativa', 'cantidad' => 1, 'precio' => 180.00],
        ['descripcion' => 'Formulario PHP con validaciones', 'cantidad' => 2, 'precio' => 95.50],
        ['descripcion' => 'Reporte PDF generado automaticamente', 'cantidad' => 1, 'precio' => 120.00],
    ],
];

$builder = new InvoicePdf();
$pdf = $builder->build($invoice);
$output = __DIR__ . '/factura_demo.pdf';
$pdf->save($output);

if (PHP_SAPI === 'cli') {
    echo "PDF generado correctamente: {$output}" . PHP_EOL;
    exit;
}

header('Content-Type: text/html; charset=utf-8');
echo '<!doctype html><html lang="es"><head><meta charset="utf-8"><title>Factura PDF</title></head><body>';
echo '<h1>Factura generada</h1>';
echo '<p>Se creo el archivo <strong>factura_demo.pdf</strong> usando la libreria propia.</p>';
echo '<p><a href="factura_demo.pdf" target="_blank">Abrir PDF</a></p>';
echo '</body></html>';
