TW MAINTFLOW - INSTALACIÓN EN XAMPP
1. Copie la carpeta tw_maintflow en C:\xampp\htdocs (la ruta final debe ser C:\xampp\htdocs\tw_maintflow).
2. Inicie Apache y MySQL desde el panel de XAMPP.
3. Abra http://localhost/phpmyadmin.
4. Use Importar y seleccione database\tw_maintflow.sql. El script recrea bd_tw_maintflow.
5. Abra http://localhost/tw_maintflow/public/.
6. Usuarios: admin/admin123, recepcion/recepcion123, tecnico/tecnico123.

Rutas amigables: requieren mod_rewrite y AllowOverride All. Fallback: public/index.php?url=clientes/index.
La conexión por defecto usa servidor localhost, usuario root y contraseña vacía; edite app\config\database.php si su XAMPP difiere.

