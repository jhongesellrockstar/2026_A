<?php
require_once dirname(__DIR__).'/app/config/config.php';
require_once APP_ROOT.'/app/config/database.php';
spl_autoload_register(function(string $class): void { foreach (['core','models','controllers'] as $dir) { $file=APP_ROOT.'/app/'.$dir.'/'.$class.'.php'; if (is_file($file)) { require_once $file; return; } } });
Session::start();
try { (new App())->run(); } catch (Throwable $e) { error_log($e); http_response_code(500); require APP_ROOT.'/app/views/errors/500.php'; }
