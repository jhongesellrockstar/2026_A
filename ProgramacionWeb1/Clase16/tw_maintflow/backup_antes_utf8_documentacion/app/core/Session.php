<?php
class Session {
    public static function start(): void { if (session_status() !== PHP_SESSION_ACTIVE) session_start(); }
    public static function flash(string $key, ?string $value = null): ?string {
        self::start();
        if ($value !== null) { $_SESSION['_flash'][$key] = $value; return null; }
        $message = $_SESSION['_flash'][$key] ?? null; unset($_SESSION['_flash'][$key]); return $message;
    }
}

