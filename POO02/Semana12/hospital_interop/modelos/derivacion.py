class Derivacion:
    def __init__(self, id_derivacion=None, id_atencion=None, id_establecimiento_destino=None, motivo_derivacion="", estado="Pendiente", fecha=None):
        self._id_derivacion = id_derivacion
        self._id_atencion = id_atencion
        self._id_establecimiento_destino = id_establecimiento_destino
        self._motivo_derivacion = motivo_derivacion
        self._estado = estado
        self._fecha = fecha