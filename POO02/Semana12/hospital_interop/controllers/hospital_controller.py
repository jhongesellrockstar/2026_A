from config.conexion import ConexionDB

class HospitalController:
    def __init__(self):
        self.db = ConexionDB()

    def verificar_login_medico(self, cmp, id_establecimiento):
        try:
            con = self.db.obtener_conexion()
            cursor = con.cursor()
            query = """
                SELECT id_medico, nombres, apellidos, especialidad
                FROM medico
                WHERE cmp = ? AND id_establecimiento = ?
            """
            cursor.execute(query, (cmp, id_establecimiento))
            resultado = cursor.fetchone()
            cursor.close()
            return resultado
        except Exception as e:
            print(f"Error: {e}")
            return None

    def buscar_historial_por_dni(self, dni):
        try:
            con = self.db.obtener_conexion()
            cursor = con.cursor()
            query_paciente = """
                SELECT p.id_paciente, p.dni, p.nombres, p.apellidos, p.seguro, h.id_historia
                FROM paciente p
                INNER JOIN historia_clinica h ON p.id_paciente = h.id_paciente
                WHERE p.dni = ?
            """
            cursor.execute(query_paciente, (dni,))
            paciente = cursor.fetchone()

            if not paciente:
                cursor.close()
                return None, []

            id_historia = paciente[5]
            query_atenciones = """
                SELECT a.id_atencion, a.fecha_hora, e.nombre, e.distrito,
                       (m.nombres + ' ' + m.apellidos), a.motivo, a.diagnostico, a.tratamiento
                FROM atencion a
                INNER JOIN establecimiento e ON a.id_establecimiento = e.id_establecimiento
                INNER JOIN medico m ON a.id_medico = m.id_medico
                WHERE a.id_historia = ?
                ORDER BY a.fecha_hora DESC
            """
            cursor.execute(query_atenciones, (id_historia,))
            atenciones = cursor.fetchall()
            cursor.close()
            return paciente, atenciones
        except Exception as e:
            print(f"Error: {e}")
            return None, []

    def existe_paciente_por_dni(self, dni):
        try:
            con = self.db.obtener_conexion()
            cursor = con.cursor()
            cursor.execute("SELECT COUNT(*) FROM paciente WHERE dni = ?", (dni,))
            existe = cursor.fetchone()[0] > 0
            cursor.close()
            return existe
        except Exception as e:
            print(f"Error: {e}")
            return False

    def obtener_paciente_por_dni(self, dni):
        try:
            con = self.db.obtener_conexion()
            cursor = con.cursor()
            query = """
                SELECT p.id_paciente, p.dni, p.nombres, p.apellidos, p.fecha_nacimiento,
                       p.sexo, p.direccion, p.telefono, p.seguro, h.id_historia
                FROM paciente p
                LEFT JOIN historia_clinica h ON p.id_paciente = h.id_paciente
                WHERE p.dni = ?
            """
            cursor.execute(query, (dni,))
            paciente = cursor.fetchone()
            cursor.close()
            return paciente
        except Exception as e:
            print(f"Error: {e}")
            return None

    def registrar_paciente(self, dni, nombres, apellidos, telefono, fecha_nacimiento=None, sexo="", direccion="", seguro="SIS"):
        try:
            if self.existe_paciente_por_dni(dni):
                return False, "Ya existe un paciente con ese DNI."

            sexo = sexo.strip().upper()
            if sexo not in ("M", "F"):
                sexo = None
            if not seguro:
                seguro = "SIS"
            if not fecha_nacimiento:
                fecha_nacimiento = None

            con = self.db.obtener_conexion()
            cursor = con.cursor()
            query_paciente = """
                INSERT INTO paciente (dni, nombres, apellidos, fecha_nacimiento, sexo, direccion, telefono, seguro)
                OUTPUT INSERTED.id_paciente
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """
            cursor.execute(query_paciente, (dni, nombres, apellidos, fecha_nacimiento, sexo, direccion, telefono, seguro))
            id_paciente = cursor.fetchone()[0]

            query_historia = """
                INSERT INTO historia_clinica (id_paciente, estado)
                OUTPUT INSERTED.id_historia
                VALUES (?, 'Activo')
            """
            cursor.execute(query_historia, (id_paciente,))
            id_historia = cursor.fetchone()[0]
            con.commit()
            cursor.close()
            return True, f"Paciente registrado. Historia clinica: {id_historia}."
        except Exception as e:
            print(f"Error: {e}")
            return False, "No se pudo registrar el paciente."

    def registrar_atencion_completa(self, id_historia, id_medico, id_establecimiento, motivo, diagnostico, tratamiento, tipo_atencion):
        try:
            con = self.db.obtener_conexion()
            cursor = con.cursor()
            query = """
                INSERT INTO atencion (id_historia, id_medico, id_establecimiento, motivo, diagnostico, tratamiento, tipo_atencion)
                OUTPUT INSERTED.id_atencion
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """
            cursor.execute(query, (id_historia, id_medico, id_establecimiento, motivo, diagnostico, tratamiento, tipo_atencion))
            id_atencion = cursor.fetchone()[0]
            con.commit()
            cursor.close()
            return id_atencion
        except Exception as e:
            print(f"Error: {e}")
            return None

    def registrar_derivacion(self, id_atencion, id_est_destino, motivo):
        try:
            con = self.db.obtener_conexion()
            cursor = con.cursor()
            query = """
                INSERT INTO derivacion (id_atencion, id_establecimiento_destino, motivo_derivacion)
                VALUES (?, ?, ?)
            """
            cursor.execute(query, (id_atencion, id_est_destino, motivo))
            con.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False

    def registrar_derivacion_por_dni(self, dni, id_establecimiento_destino, especialidad_motivo, id_medico, estado="Pendiente"):
        try:
            paciente = self.obtener_paciente_por_dni(dni)
            if not paciente:
                return False, "No existe un paciente con ese DNI."

            id_historia = paciente[9]
            if not id_historia:
                return False, "El paciente no tiene historia clinica asociada."

            con = self.db.obtener_conexion()
            cursor = con.cursor()
            cursor.execute("SELECT id_establecimiento FROM medico WHERE id_medico = ?", (id_medico,))
            fila_medico = cursor.fetchone()
            if not fila_medico:
                cursor.close()
                return False, "No se encontro el medico responsable."

            id_establecimiento_origen = fila_medico[0]
            motivo_atencion = "Derivacion directa por DNI"
            diagnostico = "Paciente derivado para evaluacion especializada"
            tratamiento = "Pendiente de evaluacion en establecimiento destino"
            tipo_atencion = "Consulta"

            query_atencion = """
                INSERT INTO atencion (id_historia, id_medico, id_establecimiento, motivo, diagnostico, tratamiento, tipo_atencion)
                OUTPUT INSERTED.id_atencion
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """
            cursor.execute(query_atencion, (id_historia, id_medico, id_establecimiento_origen, motivo_atencion, diagnostico, tratamiento, tipo_atencion))
            id_atencion = cursor.fetchone()[0]

            query_derivacion = """
                INSERT INTO derivacion (id_atencion, id_establecimiento_destino, motivo_derivacion, estado)
                OUTPUT INSERTED.id_derivacion
                VALUES (?, ?, ?, ?)
            """
            cursor.execute(query_derivacion, (id_atencion, id_establecimiento_destino, especialidad_motivo, estado or "Pendiente"))
            id_derivacion = cursor.fetchone()[0]
            con.commit()
            cursor.close()
            return True, f"Derivacion registrada. Codigo: {id_derivacion}."
        except Exception as e:
            print(f"Error: {e}")
            return False, "No se pudo registrar la derivacion."

    def listar_derivaciones_por_dni(self, dni):
        try:
            con = self.db.obtener_conexion()
            cursor = con.cursor()
            query = """
                SELECT d.id_derivacion, d.fecha, eo.nombre AS origen, ed.nombre AS destino,
                       d.motivo_derivacion, d.estado
                FROM paciente p
                INNER JOIN historia_clinica h ON p.id_paciente = h.id_paciente
                INNER JOIN atencion a ON h.id_historia = a.id_historia
                INNER JOIN derivacion d ON a.id_atencion = d.id_atencion
                INNER JOIN establecimiento eo ON a.id_establecimiento = eo.id_establecimiento
                INNER JOIN establecimiento ed ON d.id_establecimiento_destino = ed.id_establecimiento
                WHERE p.dni = ?
                ORDER BY d.fecha DESC
            """
            cursor.execute(query, (dni,))
            derivaciones = cursor.fetchall()
            cursor.close()
            return derivaciones
        except Exception as e:
            print(f"Error: {e}")
            return []

    def obtener_establecimientos(self):
        try:
            con = self.db.obtener_conexion()
            cursor = con.cursor()
            cursor.execute("SELECT id_establecimiento, nombre FROM establecimiento")
            lista = cursor.fetchall()
            cursor.close()
            return lista
        except Exception as e:
            print(f"Error: {e}")
            return []
