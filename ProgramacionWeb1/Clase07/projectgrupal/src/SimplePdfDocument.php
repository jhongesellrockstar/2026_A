<?php

class SimplePdfDocument
{
    private float $width;
    private float $height;
    private int $fontSize = 11;
    private array $pages = [];
    private string $currentContent = '';

    public function __construct(float $width = 595.28, float $height = 841.89)
    {
        $this->width = $width;
        $this->height = $height;
        $this->addPage();
    }

    public function addPage(): void
    {
        if ($this->currentContent !== '') {
            $this->pages[] = $this->currentContent;
        }

        $this->currentContent = '';
    }

    public function setFontSize(int $size): void
    {
        $this->fontSize = $size;
    }

    public function text(float $x, float $y, string $text, ?int $fontSize = null): void
    {
        $size = $fontSize ?? $this->fontSize;
        $safeText = $this->escape($text);
        $pdfY = $this->height - $y;

        $this->currentContent .= "BT /F1 {$size} Tf {$x} {$pdfY} Td ({$safeText}) Tj ET\n";
    }

    public function line(float $x1, float $y1, float $x2, float $y2): void
    {
        $pdfY1 = $this->height - $y1;
        $pdfY2 = $this->height - $y2;

        $this->currentContent .= "{$x1} {$pdfY1} m {$x2} {$pdfY2} l S\n";
    }

    public function rectangle(float $x, float $y, float $width, float $height): void
    {
        $pdfY = $this->height - $y - $height;
        $this->currentContent .= "{$x} {$pdfY} {$width} {$height} re S\n";
    }

    public function title(string $text, float $x, float $y): void
    {
        $this->text($x, $y, $text, 20);
        $this->line($x, $y + 8, $this->width - 40, $y + 8);
    }

    public function table(float $x, float $y, array $headers, array $rows, array $widths, float $rowHeight = 22): float
    {
        $cursorY = $y;
        $this->setFontSize(10);
        $this->drawRow($x, $cursorY, $headers, $widths, $rowHeight, true);
        $cursorY += $rowHeight;

        foreach ($rows as $row) {
            $this->drawRow($x, $cursorY, $row, $widths, $rowHeight, false);
            $cursorY += $rowHeight;
        }

        return $cursorY;
    }

    public function save(string $filePath): void
    {
        file_put_contents($filePath, $this->render());
    }

    public function render(): string
    {
        if ($this->currentContent !== '') {
            $this->pages[] = $this->currentContent;
            $this->currentContent = '';
        }

        $objects = [];
        $pageObjectNumbers = [];
        $fontObjectNumber = 3 + (count($this->pages) * 2);

        $objects[1] = '<< /Type /Catalog /Pages 2 0 R >>';

        $nextObject = 3;
        foreach ($this->pages as $content) {
            $contentObjectNumber = $nextObject++;
            $pageObjectNumber = $nextObject++;
            $pageObjectNumbers[] = $pageObjectNumber;

            $objects[$contentObjectNumber] = "<< /Length " . strlen($content) . " >>\nstream\n{$content}endstream";
            $objects[$pageObjectNumber] = "<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {$this->width} {$this->height}] /Contents {$contentObjectNumber} 0 R /Resources << /Font << /F1 {$fontObjectNumber} 0 R >> >> >>";
        }

        $kids = implode(' ', array_map(fn ($number) => "{$number} 0 R", $pageObjectNumbers));
        $objects[2] = "<< /Type /Pages /Kids [{$kids}] /Count " . count($pageObjectNumbers) . " >>";
        $objects[$fontObjectNumber] = '<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>';
        ksort($objects);

        $pdf = "%PDF-1.4\n";
        $offsets = [0];

        foreach ($objects as $number => $object) {
            $offsets[$number] = strlen($pdf);
            $pdf .= "{$number} 0 obj\n{$object}\nendobj\n";
        }

        $xrefPosition = strlen($pdf);
        $pdf .= "xref\n0 " . (count($objects) + 1) . "\n";
        $pdf .= "0000000000 65535 f \n";

        for ($i = 1; $i <= count($objects); $i++) {
            $pdf .= sprintf("%010d 00000 n \n", $offsets[$i]);
        }

        $pdf .= "trailer\n<< /Size " . (count($objects) + 1) . " /Root 1 0 R >>\n";
        $pdf .= "startxref\n{$xrefPosition}\n%%EOF";

        return $pdf;
    }

    private function drawRow(float $x, float $y, array $values, array $widths, float $rowHeight, bool $header): void
    {
        $cursorX = $x;
        foreach ($widths as $index => $width) {
            $this->rectangle($cursorX, $y, $width, $rowHeight);
            $value = (string)($values[$index] ?? '');
            $this->text($cursorX + 5, $y + 15, $header ? strtoupper($value) : $value, $header ? 10 : 9);
            $cursorX += $width;
        }
    }

    private function escape(string $text): string
    {
        $text = iconv('UTF-8', 'ISO-8859-1//TRANSLIT//IGNORE', $text);
        return str_replace(['\\', '(', ')'], ['\\\\', '\\(', '\\)'], $text);
    }
}
