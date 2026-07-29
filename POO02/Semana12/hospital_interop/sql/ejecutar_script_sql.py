import os
import pyodbc

def obtener_cadena_master():
    drivers = pyodbc.drivers()
    servidor = r"localhost\SQLEXPRESS"

    if "ODBC Driver 18 for SQL Server" in drivers:
        return (
            "DRIVER={ODBC Driver 18 for SQL Server};"
            "SERVER=" + servidor + ";"
            "DATABASE=master;"
            "Trusted_Connection=yes;"
            "TrustServerCertificate=yes;"
            "Connection Timeout=5;"
        )

    if "ODBC Driver 17 for SQL Server" in drivers:
        return (
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=" + servidor + ";"
            "DATABASE=master;"
            "Trusted_Connection=yes;"
            "Connection Timeout=5;"
        )

    return (
        "DRIVER={SQL Server};"
        "SERVER=" + servidor + ";"
        "DATABASE=master;"
        "Trusted_Connection=yes;"
        "Connection Timeout=5;"
    )

def separar_bloques_go(contenido):
    bloques = []
    bloque_actual = []

    for linea in contenido.splitlines():
        if linea.strip().upper() == "GO":
            texto_bloque = "\n".join(bloque_actual).strip()
            if texto_bloque:
                bloques.append(texto_bloque)
            bloque_actual = []
        else:
            bloque_actual.append(linea)

    texto_bloque = "\n".join(bloque_actual).strip()
    if texto_bloque:
        bloques.append(texto_bloque)

    return bloques

def ejecutar_script():
    carpeta_actual = os.path.dirname(os.path.abspath(__file__))
    ruta_sql = os.path.join(carpeta_actual, "crear_base_hospital_interop.sql")

    print("Leyendo script:", ruta_sql)
    archivo = open(ruta_sql, "r", encoding="utf-8")
    contenido = archivo.read()
    archivo.close()

    bloques = separar_bloques_go(contenido)
    conexion = pyodbc.connect(obtener_cadena_master())
    conexion.autocommit = True
    cursor = conexion.cursor()

    numero = 1
    for bloque in bloques:
        print("Ejecutando bloque", numero, "de", len(bloques))
        cursor.execute(bloque)
        numero = numero + 1

    cursor.close()
    conexion.close()
    print("Base de datos hospital_interop creada o verificada correctamente.")

if __name__ == "__main__":
    ejecutar_script()
