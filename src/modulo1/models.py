class Usuario:
    """Clase que representa un usuario del sistema."""
    def __init__(self, id_usuario: int, nombre_usuario: str, rol: str):
        self.id_usuario = id_usuario
        self.nombre_usuario = nombre_usuario
        self.rol = rol

    def es_admin(self) -> bool:
        return self.rol == 'admin'

    def __str__(self):
        return f"Usuario(ID: {self.id_usuario}, Nombre: {self.nombre_usuario}, Rol: {self.rol})"

