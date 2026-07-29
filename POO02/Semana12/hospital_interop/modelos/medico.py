class Medico:
    def __init__(self, id_medico=None, cmp="", nombres="", apellidos="", especialidad="", id_establecimiento=None):
        self._id_medico = id_medico
        self._cmp = cmp
        self._nombres = nombres
        self._apellidos = apellidos
        self._especialidad = especialidad
        self._id_establecimiento = id_establecimiento

    def get_id(self): return self._id_medico
    def get_cmp(self): return self._cmp
    def get_nombre_completo(self): return f"{self._nombres} {self._apellidos}"