class Atencion:
    def __init__(self, id_atencion=None, id_historia=None, id_medico=None, id_establecimiento=None, fecha_hora=None, motivo="", diagnostico="", tratamiento="", tipo_atencion="Consulta"):
        self._id_atencion = id_atencion
        self._id_historia = id_historia
        self._id_medico = id_medico
        self._id_establecimiento = id_establecimiento
        self._fecha_hora = fecha_hora
        self._motivo = motivo
        self._diagnostico = diagnostico
        self._tratamiento = tratamiento
        self._tipo_atencion = tipo_atencion