class HistoriaClinica:
    def __init__(self, id_historia=None, id_paciente=None, fecha_creacion=None, estado="Activo"):
        self._id_historia = id_historia
        self._id_paciente = id_paciente
        self._fecha_creacion = fecha_creacion
        self._estado = estado

    def get_id(self): return self._id_historia