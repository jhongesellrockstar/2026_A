import pyodbc
import tkinter as tk
from tkinter import messagebox

class ConexionDB:
    _instancia = None  # Almacena la única instancia de la clase

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super(ConexionDB, cls).__new__(cls)
            cls._instancia._link = None  # Atributo encapsulado (privado) para la conexión real
        return cls._instancia

    def __init__(self):
        self._servidor = r"localhost\SQLEXPRESS"
        self._base_datos = "hospital_interop"
        driver = self._obtener_driver_sql_server()
        self._connection_string = (
            f"DRIVER={{{driver}}};"
            "SERVER=" + self._servidor + ";"
            "DATABASE=" + self._base_datos + ";"
            "Trusted_Connection=yes;"
            "TrustServerCertificate=yes;"
            "Connection Timeout=5;"
        )

    def _obtener_driver_sql_server(self):
        drivers = pyodbc.drivers()
        preferidos = [
            "ODBC Driver 18 for SQL Server",
            "ODBC Driver 17 for SQL Server",
            "SQL Server",
        ]
        for driver in preferidos:
            if driver in drivers:
                return driver
        return "ODBC Driver 17 for SQL Server"

    def obtener_conexion(self):
        """Abre la conexión si no existe o si se cerró, y la devuelve."""
        try:
            if self._link is None or self._link.closed:
                self._link = pyodbc.connect(self._connection_string)
            return self._link
        except pyodbc.Error as e:
            if tk._default_root is not None:
                messagebox.showerror("Error de Conexión", f"No se pudo conectar a la Base de Datos:\n{e}")
            raise e

    def cerrar(self):
        """Cierra la conexión de forma segura."""
        if self._link and not self._link.closed:
            self._link.close()

if __name__ == "__main__":
    import tkinter as tk

    root = tk.Tk()
    root.withdraw()

    print("--- Probando Conexión del Sistema de Interoperabilidad ---")

    try:
        db1 = ConexionDB()
        db2 = ConexionDB()

        print(f"Instancia 1 (ID Memoria): {id(db1)}")
        print(f"Instancia 2 (ID Memoria): {id(db2)}")
        print(f"¿Es la misma instancia?: {'SÍ (Patrón exitoso)' if db1 is db2 else 'NO'}\n")

        print("Conectando a SQL Server...")
        con = db1.obtener_conexion()

        cursor = con.cursor()
        cursor.execute("SELECT @@VERSION")
        version = cursor.fetchone()

        print("\n¡CONEXIÓN EXITOSA!")
        print(f"Versión del Servidor: {version[0]}")
        messagebox.showinfo("Prueba Exitosa", "La plataforma se ha conectado correctamente a SQL Server.")

        cursor.close()
        db1.cerrar()

    except Exception as err:
        print(f"\n[ERROR EN LA PRUEBA]: {err}")
