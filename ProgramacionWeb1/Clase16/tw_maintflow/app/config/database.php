<?php
class Database {
    private static ?PDO $pdo = null;
    public static function connection(): PDO {
        if (!self::$pdo) {
            self::$pdo = new PDO('mysql:host=localhost;dbname=bd_tw_maintflow;charset=utf8mb4', 'root', '', [
                PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
                PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
                PDO::ATTR_EMULATE_PREPARES => false,
            ]);
        }
        return self::$pdo;
    }
}

