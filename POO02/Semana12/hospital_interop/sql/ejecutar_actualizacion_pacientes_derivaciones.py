from pathlib import Path
import pyodbc

SERVIDOR = r"localhost\SQLEXPRESS"
BASE_DATOS = "hospital_interop"

def obtener_driver():
    preferidos = [
        "ODBC Driver 18 for SQL Server",
        "ODBC Driver 17 for SQL Server",
        "SQL Server",
    ]
    drivers = pyodbc.drivers()
    for driver in preferidos:
        if driver in drivers:
            return driver
    return "ODBC Driver 17 for SQL Server"

def ejecutar_script():
    ruta_script = Path(__file__).with_name("actualizar_pacientes_derivaciones.sql")
    contenido = ruta_script.read_text(encoding="utf-8")
    bloques = []
    actual = []

    for linea in contenido.splitlines():
        if linea.strip().upper() == "GO":
            bloque = "\n".join(actual).strip()
            if bloque:
                bloques.append(bloque)
            actual = []
        else:
            actual.append(linea)

    ultimo = "\n".join(actual).strip()
    if ultimo:
        bloques.append(ultimo)

    driver = obtener_driver()
    cadena = (
        f"DRIVER={{{driver}}};"
        f"SERVER={SERVIDOR};"
        f"DATABASE={BASE_DATOS};"
        "Trusted_Connection=yes;"
        "TrustServerCertificate=yes;"
        "Connection Timeout=5;"
    )

    conexion = pyodbc.connect(cadena, autocommit=True)
    cursor = conexion.cursor()
    for bloque in bloques:
        cursor.execute(bloque)
    cursor.close()
    conexion.close()
    print("Actualizacion de pacientes y derivaciones completada.")

if __name__ == "__main__":
    ejecutar_script()
