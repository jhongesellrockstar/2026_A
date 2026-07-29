import csv
import os
import sys
from pathlib import Path
from datetime import datetime

RUTA_PROYECTO = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if RUTA_PROYECTO not in sys.path:
    sys.path.insert(0, RUTA_PROYECTO)

from controllers import HospitalController

DNI_EXISTENTE = "76543210"
DNI_NUEVO_SUGERIDO = "11223344"
DNI_INEXISTENTE = "99999999"
DNI_REGISTRO_TEST = "11335577"
CMP_MEDICO = "123456"
DESTINO = "Centro de Salud Universitario"

def agregar_resultado(resultados, nombre, exito, detalle):
    estado = "OK" if exito else "REVISAR"
    resultados.append([nombre, estado, detalle])
    print(f"{nombre}: {estado} - {detalle}")

def main():
    controller = HospitalController()
    resultados = []

    agregar_resultado(
        resultados,
        "Paciente existente 76543210",
        controller.existe_paciente_por_dni(DNI_EXISTENTE),
        "Debe existir para la demostracion principal."
    )

    agregar_resultado(
        resultados,
        "Paciente inexistente 99999999",
        not controller.existe_paciente_por_dni(DNI_INEXISTENTE),
        "Debe retornar False antes de registrar o derivar."
    )

    if not controller.existe_paciente_por_dni(DNI_REGISTRO_TEST):
        exito, mensaje = controller.registrar_paciente(
            DNI_REGISTRO_TEST,
            "Paciente",
            "Prueba Automatizada",
            "900000001",
            "1992-02-02",
            "M",
            "Direccion de prueba automatizada",
            "SIS"
        )
        agregar_resultado(resultados, "Registro de paciente nuevo", exito, mensaje)
    else:
        agregar_resultado(resultados, "Registro de paciente nuevo", True, "El paciente de prueba ya existia.")

    exito_dup, mensaje_dup = controller.registrar_paciente(
        DNI_NUEVO_SUGERIDO,
        "Luis Alberto",
        "Rojas Medina",
        "987654321",
        "1990-01-01",
        "M",
        "Direccion academica de prueba",
        "SIS"
    )
    agregar_resultado(resultados, "Rechazo de DNI duplicado", not exito_dup, mensaje_dup)

    establecimientos = controller.obtener_establecimientos()
    destino = None
    for est in establecimientos:
        if est[1] == DESTINO:
            destino = est
            break
    agregar_resultado(resultados, "Establecimiento destino disponible", destino is not None, DESTINO)

    medico = controller.verificar_login_medico(CMP_MEDICO, 1)
    if not medico:
        for est in establecimientos:
            medico = controller.verificar_login_medico(CMP_MEDICO, est[0])
            if medico:
                break
    agregar_resultado(resultados, "Medico responsable CMP 123456", medico is not None, "Se usara para la derivacion.")

    if destino and medico:
        existentes = controller.listar_derivaciones_por_dni(DNI_NUEVO_SUGERIDO)
        ya_existe = False
        for derivacion in existentes:
            if derivacion[4] == "Evaluacion por cardiologia - prueba automatizada":
                ya_existe = True
        if ya_existe:
            agregar_resultado(resultados, "Derivacion por DNI existente", True, "La derivacion de prueba ya existia.")
        else:
            exito_der, mensaje_der = controller.registrar_derivacion_por_dni(
                DNI_NUEVO_SUGERIDO,
                destino[0],
                "Evaluacion por cardiologia - prueba automatizada",
                medico[0],
                "Pendiente"
            )
            agregar_resultado(resultados, "Derivacion por DNI existente", exito_der, mensaje_der)
    else:
        agregar_resultado(resultados, "Derivacion por DNI existente", False, "No se pudo ubicar medico o establecimiento destino.")

    if destino and medico:
        exito_no, mensaje_no = controller.registrar_derivacion_por_dni(
            DNI_INEXISTENTE,
            destino[0],
            "Prueba con DNI inexistente",
            medico[0],
            "Pendiente"
        )
        agregar_resultado(resultados, "Rechazo de derivacion DNI inexistente", not exito_no, mensaje_no)

    derivaciones = controller.listar_derivaciones_por_dni(DNI_NUEVO_SUGERIDO)
    agregar_resultado(resultados, "Listado de derivaciones por DNI", len(derivaciones) > 0, f"Derivaciones encontradas: {len(derivaciones)}")

    carpeta = Path(__file__).parent
    ruta_txt = carpeta / "REPORTE_PRUEBAS_PACIENTES_DERIVACION.txt"
    ruta_csv = carpeta / "resumen_pruebas_pacientes_derivacion.csv"

    lineas = [
        "REPORTE DE PRUEBAS - PACIENTES Y DERIVACION",
        "=" * 58,
        f"Fecha y hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "Servidor: localhost\\SQLEXPRESS",
        "Base de datos: hospital_interop",
        "",
    ]
    for nombre, estado, detalle in resultados:
        lineas.append(f"{nombre}: {estado} - {detalle}")

    lineas.append("")
    if all(fila[1] == "OK" for fila in resultados):
        lineas.append("Resultado general: pruebas aprobadas.")
    else:
        lineas.append("Resultado general: revisar elementos marcados como REVISAR.")

    ruta_txt.write_text("\n".join(lineas), encoding="utf-8")
    with ruta_csv.open("w", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(["prueba", "estado", "detalle"])
        escritor.writerows(resultados)

    print("")
    print(f"Reporte TXT generado: {ruta_txt}")
    print(f"Resumen CSV generado: {ruta_csv}")

if __name__ == "__main__":
    main()
