-- Buat database jika belum ada
CREATE DATABASE IF NOT EXISTS calorie_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE calorie_db;

-- Tabel users untuk autentikasi user
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabel prediction_history untuk menyimpan hasil prediksi
CREATE TABLE IF NOT EXISTS prediction_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    image_path VARCHAR(255) NOT NULL,          -- Simpan nama file gambar
    food_name VARCHAR(100) NOT NULL,
    calories_per_100g FLOAT NOT NULL,
    diet_suitability VARCHAR(50) NOT NULL,
    prediction_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);