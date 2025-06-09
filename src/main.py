import getpass
from .database.database_manager import DatabaseManager
from .modulo1.services import UserManager
from .modulo1.models import Usuario
from .utils import limpiar_consola, validar_contraseña

DB_PATH = 'database/usuarios.db'
SCRIPT_PATH = 'src/database/create_database.sql'

class Application:
    def __init__(self):
        self.db_manager = DatabaseManager(DB_PATH)
        self.user_manager = UserManager(self.db_manager)
        self.usuario_actual: Usuario | None = None

    def inicializar_bd(self):
        """Crea la BD y las tablas si no existen."""
        self.db_manager.conectar()
        # Verificar si las tablas ya existen
        tablas = self.db_manager.ejecutar_consulta("SELECT name FROM sqlite_master WHERE type='table' AND name='usuarios';")
        if not tablas:
            print("Base de datos no encontrada. Creando estructura inicial...")
            self.db_manager.ejecutar_script(SCRIPT_PATH)
        self.db_manager.desconectar()

    def mostrar_menu_principal(self):
        limpiar_consola()
        print("===== BIENVENIDO AL SISTEMA DE GESTIÓN DE USUARIOS =====")
        print("1. Iniciar Sesión")
        print("2. Registrarse")
        print("3. Salir")
        return input("Seleccione una opción: ")

    def accion_registrar(self):
        limpiar_consola()
        print("--- Registro de Nuevo Usuario ---")
        nombre_usuario = input("Nombre de usuario: ")
        email = input("Email: ")
        
        while True:
            contraseña = getpass.getpass("Contraseña: ")
            es_valida, mensaje = validar_contraseña(contraseña)
            if es_valida:
                contraseña_confirm = getpass.getpass("Confirme la contraseña: ")
                if contraseña == contraseña_confirm:
                    break
                else:
                    print("Las contraseñas no coinciden. Intente de nuevo.")
            else:
                print(f"Error: {mensaje}")

        exito, mensaje = self.user_manager.registrar_usuario(nombre_usuario, email, contraseña)
        print(mensaje)
        input("\nPresione Enter para continuar...")

    def accion_iniciar_sesion(self):
        limpiar_consola()
        print("--- Inicio de Sesión ---")
        nombre_usuario = input("Nombre de usuario: ")
        contraseña = getpass.getpass("Contraseña: ")
        
        usuario, mensaje = self.user_manager.iniciar_sesion(nombre_usuario, contraseña)
        print(mensaje)
        
        if usuario:
            self.usuario_actual = usuario
            self.mostrar_menu_sesion_iniciada()
        else:
            input("\nPresione Enter para continuar...")

    def mostrar_menu_sesion_iniciada(self):
        if self.usuario_actual.es_admin():
            self.menu_admin()
        else:
            self.menu_estandar()
        self.usuario_actual = None # Cerrar sesión al salir del menú específico

    def menu_estandar(self):
        while True:
            limpiar_consola()
            print(f"--- MENÚ DE USUARIO ESTÁNDAR - Bienvenido, {self.usuario_actual.nombre_usuario} ---")
            print("1. Ver mis datos")
            print("2. Cerrar Sesión")
            opcion = input("Seleccione una opción: ")
            
            if opcion == '1':
                print("\n--- Tus Datos ---")
                print(f"ID de Usuario: {self.usuario_actual.id_usuario}")
                print(f"Nombre de Usuario: {self.usuario_actual.nombre_usuario}")
                print(f"Rol: {self.usuario_actual.rol}")
                input("\nPresione Enter para volver...")
            elif opcion == '2':
                print("Cerrando sesión...")
                break
            else:
                print("Opción no válida.")
                input("\nPresione Enter para continuar...")
                
    def menu_admin(self):
        while True:
            limpiar_consola()
            print(f"--- MENÚ DE ADMINISTRADOR - Bienvenido, {self.usuario_actual.nombre_usuario} ---")
            print("1. Ver listado de usuarios")
            print("2. Cambiar rol de un usuario")
            print("3. Eliminar un usuario")
            print("4. Cerrar Sesión")
            opcion = input("Seleccione una opción: ")

            if opcion == '1':
                self.accion_admin_ver_usuarios()
            elif opcion == '2':
                self.accion_admin_cambiar_rol()
            elif opcion == '3':
                self.accion_admin_eliminar_usuario()
            elif opcion == '4':
                print("Cerrando sesión...")
                break
            else:
                print("Opción no válida.")
                input("\nPresione Enter para continuar...")

    def accion_admin_ver_usuarios(self):
        usuarios = self.user_manager.obtener_todos_los_usuarios()
        print("\n--- Listado de Usuarios Registrados ---")
        print("{:<5} {:<20} {:<25} {:<10}".format("ID", "Usuario", "Email", "Rol"))
        print("-" * 65)
        for user in usuarios:
            print("{:<5} {:<20} {:<25} {:<10}".format(user['id_usuario'], user['nombre_usuario'], user['email'], user['nombre_rol']))
        input("\nPresione Enter para volver...")

    def accion_admin_cambiar_rol(self):
        try:
            id_usuario = int(input("Ingrese el ID del usuario a modificar: "))
            nuevo_rol = input("Ingrese el nuevo rol (admin/estandar): ").lower()
            if nuevo_rol not in ['admin', 'estandar']:
                print("Rol no válido.")
            elif self.user_manager.cambiar_rol_usuario(id_usuario, nuevo_rol):
                print("Rol actualizado exitosamente.")
            else:
                print("No se pudo actualizar el rol. Verifique el ID del usuario.")
        except ValueError:
            print("ID no válido. Debe ser un número.")
        input("\nPresione Enter para volver...")

    def accion_admin_eliminar_usuario(self):
        try:
            id_usuario = int(input("Ingrese el ID del usuario a eliminar: "))
            if id_usuario == self.usuario_actual.id_usuario:
                print("No puedes eliminarte a ti mismo.")
            else:
                confirmacion = input(f"¿Está seguro que desea eliminar al usuario con ID {id_usuario}? (s/n): ").lower()
                if confirmacion == 's':
                    if self.user_manager.eliminar_usuario(id_usuario):
                        print("Usuario eliminado exitosamente.")
                    else:
                        print("No se pudo eliminar el usuario.")
        except ValueError:
            print("ID no válido. Debe ser un número.")
        input("\nPresione Enter para volver...")

    def run(self):
        self.inicializar_bd()
        while True:
            opcion = self.mostrar_menu_principal()
            self.db_manager.conectar()
            
            if opcion == '1':
                self.accion_iniciar_sesion()
            elif opcion == '2':
                self.accion_registrar()
            elif opcion == '3':
                print("¡Hasta luego!")
                break
            else:
                print("Opción no válida. Intente de nuevo.")
                input("\nPresione Enter para continuar...")
            
            self.db_manager.desconectar()

if __name__ == '__main__':
    app = Application()
    app.run()
