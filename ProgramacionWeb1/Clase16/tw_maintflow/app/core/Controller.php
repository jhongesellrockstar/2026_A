<?php
abstract class Controller {
    protected function view(string $view, array $data = []): void { extract($data); require APP_ROOT.'/app/views/layouts/header.php'; require APP_ROOT.'/app/views/'.$view.'.php'; require APP_ROOT.'/app/views/layouts/footer.php'; }
    protected function redirect(string $path): never { header('Location: '.BASE_URL.'/'.$path); exit; }
    protected function id(): int { return filter_input(INPUT_GET, 'id', FILTER_VALIDATE_INT) ?: 0; }
}

