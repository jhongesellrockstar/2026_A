<?php
$titulo = 'Aprendiendo PHP';
$temas = ['Variables', 'Condicionales', 'Arrays', 'Funciones', 'Formularios'];

function saludar(string $nombre): string
{
    return "Hola, {$nombre}. Bienvenido al aprendizaje de PHP.";
}
?>
<!doctype html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title><?= $titulo ?></title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <main class="container">
        <h1><?= $titulo ?></h1>
        <p><?= saludar('estudiante') ?></p>

        <section>
            <h2>Temas de practica</h2>
            <ul>
                <?php foreach ($temas as $tema): ?>
                    <li><?= $tema ?></li>
                <?php endforeach; ?>
            </ul>
        </section>

        <nav>
            <a href="examples/variables.php">Ver variables y arrays</a>
            <a href="examples/formulario.php">Practicar formulario</a>
        </nav>
    </main>
</body>
</html>
