TW MAINTFLOW - ARQUITECTURA MVC
Modelo: clases de app\models; encapsulan PDO, consultas preparadas, CRUD y JOIN.
Vista: archivos de app\views; presentan HTML y escapan salida con htmlspecialchars. No contienen SQL.
Controlador: clases de app\controllers; reciben la petición, validan sesión/rol, llaman modelos y seleccionan vistas.
Núcleo: Router interpreta la URL; App inicia el despacho; Auth y Session protegen rutas; Controller comparte renderizado y redirección.
Flujo: navegador -> public\index.php -> Router -> Controlador -> Modelo/PDO -> Controlador -> Vista -> respuesta HTML.

