<?php
class Auth {
    public static function user(): ?array { Session::start(); return $_SESSION['user'] ?? null; }
    public static function check(): bool { return self::user() !== null; }
    public static function requireLogin(): void { if (!self::check()) { header('Location: '.BASE_URL.'/auth/login'); exit; } }
    public static function requireRole(array $roles): void { self::requireLogin(); if (!in_array(self::user()['rol'], $roles, true)) { http_response_code(403); require APP_ROOT.'/app/views/errors/403.php'; exit; } }
}

