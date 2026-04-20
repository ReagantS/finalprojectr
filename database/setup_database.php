<?php
$host = '127.0.0.1';
$user = 'root';
$password = '';
$database = 'inventory_db';

try {
    $pdo = new PDO("mysql:host=$host;charset=utf8mb4", $user, $password, [
        PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
        PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
    ]);

    $pdo->exec("CREATE DATABASE IF NOT EXISTS `$database` CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;");
    $pdo->exec("USE `$database`;");
    $pdo->exec("CREATE TABLE IF NOT EXISTS inventory_items (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(128) NOT NULL,
        category VARCHAR(64) NOT NULL,
        description VARCHAR(255),
        location VARCHAR(64) NOT NULL,
        quantity INT NOT NULL DEFAULT 0,
        unit_price DOUBLE NOT NULL DEFAULT 0.0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    ) ENGINE=InnoDB;");

    echo "Database and table created successfully.\n";
} catch (PDOException $e) {
    echo "Database setup failed: " . $e->getMessage() . "\n";
    exit(1);
}
