<?php
const CURSO = 'Programacion Web 1';

$nombre = 'Estudiante';
$edad = 20;
$promedio = 16.75;
$aprobado = $promedio >= 13;

$lenguajes = ['HTML', 'CSS', 'PHP'];
$perfil = [
    'nombre' => $nombre,
    'curso' => CURSO,
    'promedio' => $promedio,
];
?>
<!doctype html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <title>Variables en PHP</title>
    <link rel="stylesheet" href="../styles.css">
</head>
<body>
    <main class="container">
        <h1>Variables, constantes y arrays</h1>
        <p>Nombre: <?= $nombre ?></p>
        <p>Edad: <?= $edad ?></p>
        <p>Curso: <?= CURSO ?></p>
        <p>Promedio: <?= number_format($promedio, 2) ?></p>
        <p>Estado: <?= $aprobado ? 'Aprobado' : 'En proceso' ?></p>

        <h2>Lenguajes practicados</h2>
        <ul>
            <?php foreach ($lenguajes as $lenguaje): ?>
                <li><?= $lenguaje ?></li>
            <?php endforeach; ?>
        </ul>

        <h2>Array asociativo</h2>
        <pre><?php print_r($perfil); ?></pre>
        <a href="../index.php">Volver</a>
    </main>
</body>
</html>
