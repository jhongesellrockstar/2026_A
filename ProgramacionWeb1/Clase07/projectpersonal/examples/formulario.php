<?php
$mensaje = '';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $nombre = trim($_POST['nombre'] ?? '');
    $nota = (float)($_POST['nota'] ?? 0);

    if ($nombre === '') {
        $mensaje = 'Debe ingresar un nombre.';
    } elseif ($nota < 0 || $nota > 20) {
        $mensaje = 'La nota debe estar entre 0 y 20.';
    } elseif ($nota >= 13) {
        $mensaje = "{$nombre}, aprobaste con " . number_format($nota, 2) . '.';
    } else {
        $mensaje = "{$nombre}, necesitas reforzar el tema.";
    }
}
?>
<!doctype html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <title>Formulario PHP</title>
    <link rel="stylesheet" href="../styles.css">
</head>
<body>
    <main class="container">
        <h1>Formulario con POST</h1>
        <form method="post">
            <label for="nombre">Nombre</label>
            <input id="nombre" name="nombre" type="text">

            <label for="nota">Nota</label>
            <input id="nota" name="nota" type="number" step="0.01">

            <button type="submit">Evaluar</button>
        </form>

        <?php if ($mensaje !== ''): ?>
            <p><strong><?= $mensaje ?></strong></p>
        <?php endif; ?>

        <a href="../index.php">Volver</a>
    </main>
</body>
</html>
