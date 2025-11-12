-- Script de creación de base de datos para el Sistema de Donaciones
-- Ejecuta este script en MySQL para crear la estructura necesaria

CREATE DATABASE IF NOT EXISTS proyecto_comba_final;
USE proyecto_comba_final;

-- Tabla de roles
CREATE TABLE IF NOT EXISTS roles (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(50) NOT NULL
);

-- Insertar roles por defecto
INSERT INTO roles (id, nombre) VALUES 
(1, 'Administrador'),
(2, 'Donador')
ON DUPLICATE KEY UPDATE nombre=nombre;

-- Tabla de usuarios
CREATE TABLE IF NOT EXISTS usuarios (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    fullname VARCHAR(100) NOT NULL,
    correo VARCHAR(100) NOT NULL,
    id_rol INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_rol) REFERENCES roles(id)
);

-- Tabla de donaciones (opcional, para futuras funcionalidades)
CREATE TABLE IF NOT EXISTS donaciones (
    id INT PRIMARY KEY AUTO_INCREMENT,
    id_usuario INT NOT NULL,
    monto DECIMAL(10, 2) NOT NULL,
    categoria VARCHAR(50),
    mensaje TEXT,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id)
);

