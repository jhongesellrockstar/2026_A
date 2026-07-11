<?php
class Router {
    public function dispatch(): void {
        $path = trim($_GET['url'] ?? parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH), '/');
        $path = preg_replace('#^tw_maintflow/public/?#', '', $path);
        $parts = array_values(array_filter(explode('/', $path)));
        $map = [''=>'Home','auth'=>'Auth','dashboard'=>'Dashboard','clientes'=>'Cliente','sedes'=>'Sede','equipos'=>'Equipo','tecnicos'=>'Tecnico','ordenes'=>'Orden','repuestos'=>'Repuesto','usuarios'=>'Usuario','reportes'=>'Reporte'];
        $segment = $parts[0] ?? '';
        if (!array_key_exists($segment, $map)) { http_response_code(404); require APP_ROOT.'/app/views/errors/404.php'; return; }
        $class = $map[$segment].'Controller'; $action = $parts[1] ?? ($segment === 'auth' ? 'login' : 'index');
        if ($class === 'OrdenController' && $action === 'view') $action = 'detail';
        if (!class_exists($class) || !is_callable([new $class, $action])) { http_response_code(404); require APP_ROOT.'/app/views/errors/404.php'; return; }
        (new $class)->$action();
    }
}
