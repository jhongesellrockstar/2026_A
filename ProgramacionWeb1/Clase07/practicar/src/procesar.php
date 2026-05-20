<?php

const MAX_MONTO = 500000;

function validarDatos(array $datos): array
{
    $errores = [];
    $nombre = trim($datos['nombre'] ?? '');
    $monto = (float)($datos['monto'] ?? 0);
    $interes = (float)($datos['interes'] ?? 0);
    $anios = (int)($datos['anios'] ?? 0);
    $tipo = trim($datos['tipo'] ?? '');

    if ($nombre === '' || $tipo === '' || ($datos['monto'] ?? '') === '' || ($datos['interes'] ?? '') === '' || ($datos['anios'] ?? '') === '') {
        $errores[] = 'Ningun campo debe estar vacio.';
    }

    if ($monto <= 0) {
        $errores[] = 'El monto debe ser mayor que 0.';
    } elseif ($monto > MAX_MONTO) {
        $errores[] = 'El monto no puede superar S/ ' . number_format(MAX_MONTO, 2) . '.';
    }

    if ($interes < 0 || $interes > 100) {
        $errores[] = 'El interes anual debe estar entre 0 y 100.';
    }

    if ($anios <= 0) {
        $errores[] = 'Los anios deben ser mayores que 0.';
    }

    if (!in_array($tipo, ['personal', 'vehicular', 'hipotecario', 'educativo'], true)) {
        $errores[] = 'Debe seleccionar un tipo de prestamo valido.';
    }

    return [
        'errores' => $errores,
        'datos' => compact('nombre', 'monto', 'interes', 'anios', 'tipo'),
    ];
}

function ajustarInteres(float $interes, string $tipo): float
{
    switch ($tipo) {
        case 'personal':
            return $interes + 3.00;
        case 'vehicular':
            return $interes + 1.50;
        case 'hipotecario':
            return max(0, $interes - 1.00);
        case 'educativo':
            return max(0, $interes - 0.50);
        default:
            return $interes;
    }
}

function calcularCuota(float $monto, float $interesAnual, int $anios): float
{
    $interesMensual = ($interesAnual / 100) / 12;
    $meses = $anios * 12;

    if ($interesMensual == 0.0) {
        return $monto / $meses;
    }

    return $monto * (($interesMensual * pow(1 + $interesMensual, $meses)) / (pow(1 + $interesMensual, $meses) - 1));
}

function generarAmortizacion(float $monto, float $interesAnual, int $anios, float $cuota): array
{
    $interesMensual = ($interesAnual / 100) / 12;
    $meses = $anios * 12;
    $saldo = $monto;
    $tabla = [];

    for ($mes = 1; $mes <= $meses; $mes++) {
        $interesCuota = $saldo * $interesMensual;
        $amortizacionCapital = $cuota - $interesCuota;
        $saldo = max(0, $saldo - $amortizacionCapital);

        $tabla[] = [
            'mes' => $mes,
            'cuota' => $cuota,
            'interes' => $interesCuota,
            'capital' => $amortizacionCapital,
            'saldo' => $saldo,
        ];
    }

    return $tabla;
}

$resultado = validarDatos($_POST);
$errores = $resultado['errores'];
$datos = $resultado['datos'];
?>
<!doctype html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Resultado del Prestamo</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <main class="container wide">
        <h1>Resultado del Prestamo</h1>

        <?php if (count($errores) > 0): ?>
            <section class="alert">
                <h2>Revise los datos ingresados</h2>
                <ul>
                    <?php foreach ($errores as $error): ?>
                        <li><?= htmlspecialchars($error) ?></li>
                    <?php endforeach; ?>
                </ul>
            </section>
            <a class="button" href="index.html">Volver al formulario</a>
        <?php else: ?>
            <?php
            $interesAjustado = ajustarInteres($datos['interes'], $datos['tipo']);
            $interesMensual = ($interesAjustado / 100) / 12;
            $meses = $datos['anios'] * 12;
            $cuota = calcularCuota($datos['monto'], $interesAjustado, $datos['anios']);
            $amortizacion = generarAmortizacion($datos['monto'], $interesAjustado, $datos['anios'], $cuota);
            $totalPagado = $cuota * $meses;
            $totalIntereses = $totalPagado - $datos['monto'];
            ?>

            <section class="summary">
                <p><strong>Cliente:</strong> <?= htmlspecialchars($datos['nombre']) ?></p>
                <p><strong>Tipo:</strong> <?= ucfirst(htmlspecialchars($datos['tipo'])) ?></p>
                <p><strong>Monto:</strong> S/ <?= number_format($datos['monto'], 2) ?></p>
                <p><strong>Interes anual ajustado:</strong> <?= number_format($interesAjustado, 2) ?>%</p>
                <p><strong>Interes mensual:</strong> <?= number_format($interesMensual * 100, 4) ?>%</p>
                <p><strong>Meses:</strong> <?= $meses ?></p>
                <p><strong>Cuota mensual:</strong> S/ <?= number_format($cuota, 2) ?></p>
                <p><strong>Total pagado:</strong> S/ <?= number_format($totalPagado, 2) ?></p>
                <p><strong>Total intereses:</strong> S/ <?= number_format($totalIntereses, 2) ?></p>
                <p><strong>Archivo:</strong> <?= htmlspecialchars(__FILE__) ?></p>
            </section>

            <h2>Tabla de amortizacion</h2>
            <div class="table-wrap">
                <table>
                    <thead>
                        <tr>
                            <th>Mes</th>
                            <th>Cuota</th>
                            <th>Interes</th>
                            <th>Capital</th>
                            <th>Saldo</th>
                        </tr>
                    </thead>
                    <tbody>
                        <?php foreach ($amortizacion as $fila): ?>
                            <tr>
                                <td><?= $fila['mes'] ?></td>
                                <td>S/ <?= number_format($fila['cuota'], 2) ?></td>
                                <td>S/ <?= number_format($fila['interes'], 2) ?></td>
                                <td>S/ <?= number_format($fila['capital'], 2) ?></td>
                                <td>S/ <?= number_format($fila['saldo'], 2) ?></td>
                            </tr>
                        <?php endforeach; ?>
                    </tbody>
                </table>
            </div>

            <script type="application/json" id="resultado-json">
                <?= json_encode([
                    'datos' => $datos,
                    'interes_ajustado' => $interesAjustado,
                    'cuota' => $cuota,
                    'total_pagado' => $totalPagado,
                    'total_intereses' => $totalIntereses,
                    'amortizacion' => $amortizacion,
                ], JSON_PRETTY_PRINT) ?>
            </script>

            <a class="button" href="index.html">Realizar otro calculo</a>
        <?php endif; ?>
    </main>
</body>
</html>
