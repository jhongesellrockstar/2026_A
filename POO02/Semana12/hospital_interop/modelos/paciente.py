class Paciente:
    def __init__(self, id_paciente=None, dni="", nombres="", apellidos="", fecha_nacimiento=None, sexo="", direccion="", telefono="", seguro=""):
        self._id_paciente = id_paciente
        self._dni = dni
        self._nombres = nombres
        self._apellidos = apellidos
        self._fecha_nacimiento = fecha_nacimiento
        self._sexo = sexo
        self._direccion = direccion
        self._telefono = telefono
        self._seguro = seguro

    def get_id(self): return self._id_paciente
    def get_dni(self): return self._dni
    def get_nombres(self): return self._nombres
    def get_apellidos(self): return self._apellidos
    def get_telefono(self): return self._telefono
    def get_nombre_completo(self): return f"{self._nombres} {self._apellidos}"
    def get_datos_completos(self):
        return (self._dni, self._nombres, self._apellidos, self._fecha_nacimiento, self._sexo, self._direccion, self._telefono, self._seguro)
