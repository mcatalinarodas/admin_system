import sqlite3

class DatabaseManager:
    """Gestiona la conexión y las operaciones con la base de datos SQLite."""
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn = None

    def conectar(self):
        """Establece la conexión con la base de datos."""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row # Para acceder a las columnas por nombre
            self.conn.execute("PRAGMA foreign_keys = ON;")
        except sqlite3.Error as e:
            print(f"Error al conectar con la base de datos: {e}")
            self.conn = None

    def desconectar(self):
        """Cierra la conexión con la base de datos."""
        if self.conn:
            self.conn.close()
            self.conn = None

    def ejecutar_consulta(self, query: str, params: tuple = ()) -> list[sqlite3.Row]:
        """Ejecuta una consulta SELECT y devuelve los resultados."""
        if not self.conn:
            return []
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error al ejecutar consulta: {e}")
            return []

    def ejecutar_modificacion(self, query: str, params: tuple = ()) -> bool:
        """Ejecuta una consulta de modificación (INSERT, UPDATE, DELETE)."""
        if not self.conn:
            return False
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, params)
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error al ejecutar modificación: {e}")
            self.conn.rollback()
            return False
            
    def ejecutar_script(self, script_path: str):
        """Ejecuta un script SQL desde un archivo."""
        if not self.conn:
            return
        try:
            with open(script_path, 'r') as f:
                script = f.read()
            self.conn.executescript(script)
            self.conn.commit()
            print(f"Script '{script_path}' ejecutado exitosamente.")
        except sqlite3.Error as e:
            print(f"Error al ejecutar script: {e}")

