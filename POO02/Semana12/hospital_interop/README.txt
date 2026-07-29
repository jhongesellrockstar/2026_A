Sistema de Interoperabilidad Hospitalaria
=========================================

Tecnologias:
- Python
- tkinter
- pyodbc
- SQL Server Express

Requisitos:
- Python instalado.
- SQL Server Express con instancia SQLEXPRESS.
- ODBC Driver 17 o 18 for SQL Server.
- Dependencias indicadas en requirements.txt.

Instalacion:
python -m pip install -r requirements.txt

Crear o actualizar base:
python sql\ejecutar_script_sql.py
python sql\ejecutar_actualizacion_pacientes_derivaciones.py

Ejecutar:
python main.py

Datos de prueba:
Establecimiento: Hospital Academico Lima Callao
CMP: 123456
DNI existente: 76543210
DNI nuevo sugerido: 11223344

Pruebas:
python tests\probar_tablas_hospital_interop.py
python tests\probar_pacientes_derivacion.py
