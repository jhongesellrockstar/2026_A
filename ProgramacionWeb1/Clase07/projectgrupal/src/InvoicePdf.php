<?php

require_once __DIR__ . '/SimplePdfDocument.php';

class InvoicePdf
{
    private SimplePdfDocument $pdf;

    public function __construct()
    {
        $this->pdf = new SimplePdfDocument();
    }

    public function build(array $invoice): SimplePdfDocument
    {
        $this->pdf->title('FACTURA', 40, 45);
        $this->pdf->text(40, 80, 'Empresa: ' . $invoice['empresa']);
        $this->pdf->text(40, 98, 'RUC: ' . $invoice['ruc']);
        $this->pdf->text(40, 116, 'Fecha: ' . $invoice['fecha']);
        $this->pdf->text(360, 80, 'Nro: ' . $invoice['numero']);
        $this->pdf->text(360, 98, 'Cliente: ' . $invoice['cliente']);
        $this->pdf->text(360, 116, 'Documento: ' . $invoice['documento']);

        $rows = [];
        $subtotal = 0;

        foreach ($invoice['items'] as $item) {
            $totalItem = $item['cantidad'] * $item['precio'];
            $subtotal += $totalItem;
            $rows[] = [
                $item['descripcion'],
                (string)$item['cantidad'],
                'S/ ' . number_format($item['precio'], 2),
                'S/ ' . number_format($totalItem, 2),
            ];
        }

        $finalY = $this->pdf->table(
            40,
            155,
            ['Descripcion', 'Cant.', 'Precio', 'Total'],
            $rows,
            [285, 60, 90, 90]
        );

        $igv = $subtotal * 0.18;
        $total = $subtotal + $igv;

        $this->pdf->text(365, $finalY + 25, 'Subtotal: S/ ' . number_format($subtotal, 2), 11);
        $this->pdf->text(365, $finalY + 45, 'IGV 18%: S/ ' . number_format($igv, 2), 11);
        $this->pdf->text(365, $finalY + 65, 'Total: S/ ' . number_format($total, 2), 13);

        $this->pdf->text(40, $finalY + 105, 'Observacion: Documento generado con una libreria propia en PHP.');

        return $this->pdf;
    }
}
