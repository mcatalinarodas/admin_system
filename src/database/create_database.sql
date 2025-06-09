PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS roles (
    id_rol INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_rol TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_usuario TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    contraseña_hash TEXT NOT NULL,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    id_rol INTEGER NOT NULL,
    FOREIGN KEY (id_rol) REFERENCES roles(id_rol) ON DELETE RESTRICT ON UPDATE CASCADE
);

INSERT OR IGNORE INTO roles (nombre_rol) VALUES ('admin');
INSERT OR IGNORE INTO roles (nombre_rol) VALUES ('estandar');

CREATE INDEX IF NOT EXISTS idx_nombre_usuario ON usuarios (nombre_usuario);

SELECT 'Base de datos y tablas creadas exitosamente.' AS status;
