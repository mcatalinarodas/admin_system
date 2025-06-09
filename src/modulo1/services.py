from ..database.database_manager import DatabaseManager
from ..utils import hashear_contraseña, verificar_contraseña
from .models import Usuario

class UserManager:
    """Lógica de negocio para la gestión de usuarios."""
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def registrar_usuario(self, nombre_usuario: str, email: str, contraseña: str) -> tuple[bool, str]:
        """Registra un nuevo usuario con rol estándar."""
        # Verificar si el usuario o email ya existen
        if self.db_manager.ejecutar_consulta("SELECT id_usuario FROM usuarios WHERE nombre_usuario = ?", (nombre_usuario,)):
            return False, "El nombre de usuario ya está en uso."
        if self.db_manager.ejecutar_consulta("SELECT id_usuario FROM usuarios WHERE email = ?", (email,)):
            return False, "El email ya está en uso."
        
        # Rol estándar por defecto es 2
        id_rol_estandar = self.db_manager.ejecutar_consulta("SELECT id_rol FROM roles WHERE nombre_rol = 'estandar'")[0]['id_rol']
        
        hash_contraseña = hashear_contraseña(contraseña)
        query = "INSERT INTO usuarios (nombre_usuario, email, contraseña_hash, id_rol) VALUES (?, ?, ?, ?)"
        params = (nombre_usuario, email, hash_contraseña, id_rol_estandar)
        
        if self.db_manager.ejecutar_modificacion(query, params):
            return True, "Usuario registrado exitosamente."
        else:
            return False, "Ocurrió un error durante el registro."

    def iniciar_sesion(self, nombre_usuario: str, contraseña: str) -> tuple[Usuario | None, str]:
        """Valida las credenciales e inicia sesión."""
        query = """
            SELECT u.id_usuario, u.nombre_usuario, u.contraseña_hash, r.nombre_rol
            FROM usuarios u
            JOIN roles r ON u.id_rol = r.id_rol
            WHERE u.nombre_usuario = ?
        """
        resultado = self.db_manager.ejecutar_consulta(query, (nombre_usuario,))
        
        if not resultado:
            return None, "Usuario o contraseña incorrectos."
        
        usuario_db = resultado[0]
        if verificar_contraseña(contraseña, usuario_db['contraseña_hash']):
            usuario_logueado = Usuario(
                id_usuario=usuario_db['id_usuario'],
                nombre_usuario=usuario_db['nombre_usuario'],
                rol=usuario_db['nombre_rol']
            )
            return usuario_logueado, "Inicio de sesión exitoso."
        else:
            return None, "Usuario o contraseña incorrectos."
    
    def obtener_todos_los_usuarios(self) -> list[dict]:
        """Devuelve una lista de todos los usuarios y sus roles."""
        query = """
            SELECT u.id_usuario, u.nombre_usuario, u.email, r.nombre_rol
            FROM usuarios u
            JOIN roles r ON u.id_rol = r.id_rol
            ORDER BY u.id_usuario
        """
        return self.db_manager.ejecutar_consulta(query)

    def cambiar_rol_usuario(self, id_usuario: int, nuevo_rol: str) -> bool:
        """Cambia el rol de un usuario específico."""
        id_nuevo_rol = self.db_manager.ejecutar_consulta("SELECT id_rol FROM roles WHERE nombre_rol = ?", (nuevo_rol,))
        if not id_nuevo_rol:
            print(f"Error: El rol '{nuevo_rol}' no existe.")
            return False
            
        query = "UPDATE usuarios SET id_rol = ? WHERE id_usuario = ?"
        return self.db_manager.ejecutar_modificacion(query, (id_nuevo_rol[0]['id_rol'], id_usuario))

    def eliminar_usuario(self, id_usuario: int) -> bool:
        """Elimina un usuario de la base de datos."""
        query = "DELETE FROM usuarios WHERE id_usuario = ?"
        return self.db_manager.ejecutar_modificacion(query, (id_usuario,))
