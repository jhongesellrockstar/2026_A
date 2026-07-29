import csv
import os
import sys
from datetime import datetime

RUTA_PROYECTO = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if RUTA_PROYECTO not in sys.path:
    sys.path.insert(0, RUTA_PROYECTO)

from config.conexion import ConexionDB

TABLAS = [
    "establecimiento",
    "medico",
    "paciente",
    "historia_clinica",
    "atencion",
    "derivacion",
    "medicamento",
    "prescripcion",
]

RELACIONES = [
    (
        "medico con establecimiento",
        """
        SELECT COUNT(*)
        FROM medico m
        INNER JOIN establecimiento e
            ON m.id_establecimiento = e.id_establecimiento
        """,
    ),
    (
        "paciente con historia_clinica",
        """
        SELECT COUNT(*)
        FROM paciente p
        INNER JOIN historia_clinica h
            ON p.id_paciente = h.id_paciente
        """,
    ),
    (
        "historia_clinica con atencion",
        """
        SELECT COUNT(*)
        FROM historia_clinica h
        INNER JOIN atencion a
            ON h.id_historia = a.id_historia
        """,
    ),
    (
        "atencion con medico",
        """
        SELECT COUNT(*)
        FROM atencion a
        INNER JOIN medico m
            ON a.id_medico = m.id_medico
        """,
    ),
    (
        "atencion con establecimiento",
        """
        SELECT COUNT(*)
        FROM atencion a
        INNER JOIN establecimiento e
            ON a.id_establecimiento = e.id_establecimiento
        """,
    ),
    (
        "derivacion con atencion",
        """
        SELECT COUNT(*)
        FROM derivacion d
        INNER JOIN atencion a
            ON d.id_atencion = a.id_atencion
        """,
    ),
    (
        "derivacion con establecimiento destino",
        """
        SELECT COUNT(*)
        FROM derivacion d
        INNER JOIN establecimiento e
            ON d.id_establecimiento_destino = e.id_establecimiento
        """,
    ),
    (
        "prescripcion con atencion",
        """
        SELECT COUNT(*)
        FROM prescripcion p
        INNER JOIN atencion a
            ON p.id_atencion = a.id_atencion
        """,
    ),
    (
        "prescripcion con medicamento",
        """
        SELECT COUNT(*)
        FROM prescripcion p
        INNER JOIN medicamento m
            ON p.id_medicamento = m.id_medicamento
        """,
    ),
]

def contar_registros(cursor, tabla):
    cursor.execute(f"SELECT COUNT(*) FROM {tabla}")
    return cursor.fetchone()[0]

def ejecutar_consulta_conteo(cursor, consulta):
    cursor.execute(consulta)
    return cursor.fetchone()[0]

def guardar_reporte_txt(ruta, lineas):
    with open(ruta, "w", encoding="utf-8") as archivo:
        archivo.write("\n".join(lineas))

def guardar_resumen_csv(ruta, filas):
    with open(ruta, "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(["tipo", "elemento", "cantidad", "estado"])
        for fila in filas:
            escritor.writerow(fila)

def main():
    carpeta_tests = os.path.dirname(__file__)
    ruta_reporte = os.path.join(carpeta_tests, "REPORTE_PRUEBAS_TABLAS.txt")
    ruta_csv = os.path.join(carpeta_tests, "resumen_pruebas_tablas.csv")

    lineas = []
    filas_csv = []

    lineas.append("REPORTE DE PRUEBAS DE TABLAS - hospital_interop")
    lineas.append("=" * 58)
    lineas.append(f"Fecha y hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lineas.append("Servidor: localhost\\SQLEXPRESS")
    lineas.append("Base de datos: hospital_interop")
    lineas.append("")

    conexion_db = ConexionDB()
    conexion = conexion_db.obtener_conexion()
    cursor = conexion.cursor()

    lineas.append("1. Conteo de registros por tabla")
    lineas.append("-" * 58)
    for tabla in TABLAS:
        cantidad = contar_registros(cursor, tabla)
        estado = "OK" if cantidad > 0 else "REVISAR"
        mensaje = f"{tabla}: {cantidad} registro(s) - {estado}"
        print(mensaje)
        lineas.append(mensaje)
        filas_csv.append(["tabla", tabla, cantidad, estado])

    lineas.append("")
    lineas.append("2. Verificacion de relaciones principales")
    lineas.append("-" * 58)
    for nombre, consulta in RELACIONES:
        cantidad = ejecutar_consulta_conteo(cursor, consulta)
        estado = "OK" if cantidad > 0 else "REVISAR"
        mensaje = f"{nombre}: {cantidad} relacion(es) encontrada(s) - {estado}"
        print(mensaje)
        lineas.append(mensaje)
        filas_csv.append(["relacion", nombre, cantidad, estado])

    cursor.close()
    conexion_db.cerrar()

    lineas.append("")
    lineas.append("Resultado general:")
    if all(fila[3] == "OK" for fila in filas_csv):
        lineas.append("Todas las tablas principales tienen datos y relaciones verificables.")
    else:
        lineas.append("Existen tablas o relaciones sin datos. Revisar los elementos marcados como REVISAR.")

    guardar_reporte_txt(ruta_reporte, lineas)
    guardar_resumen_csv(ruta_csv, filas_csv)

    print("")
    print(f"Reporte TXT generado: {ruta_reporte}")
    print(f"Resumen CSV generado: {ruta_csv}")

if __name__ == "__main__":
    main()
