-- Script con ejemplos de consultas CRUD para la gestión de usuarios

-- CREATE: Registrar un nuevo usuario estándar (rol 2)
-- La contraseña 'Password123' debe ser hasheada por la aplicación ANTES de insertarla.
INSERT INTO usuarios (nombre_usuario, email, contraseña_hash, id_rol)
VALUES ('juanperez', 'juan.perez@email.com', 'hash_de_la_contraseña_aqui', 2);

-- READ: Obtener todos los usuarios con el nombre de su rol
SELECT
    u.id_usuario,
    u.nombre_usuario,
    u.email,
    u.fecha_creacion,
    r.nombre_rol
FROM
    usuarios u
JOIN
    roles r ON u.id_rol = r.id_rol;

-- READ: Obtener un usuario específico por su nombre de usuario para el login
SELECT
    u.id_usuario,
    u.nombre_usuario,
    u.contraseña_hash,
    r.nombre_rol
FROM
    usuarios u
JOIN
    roles r ON u.id_rol = r.id_rol
WHERE
    u.nombre_usuario = 'juanperez';

-- UPDATE: Cambiar el rol de un usuario a 'admin' (rol 1)
UPDATE usuarios
SET id_rol = 1
WHERE id_usuario = 1; -- Asumiendo que juanperez tiene id_usuario 1

-- DELETE: Eliminar un usuario por su id
DELETE FROM usuarios
WHERE id_usuario = 1;
