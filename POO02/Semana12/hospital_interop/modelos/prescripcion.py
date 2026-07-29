class Prescripcion:
    def __init__(self, id_prescripcion=None, id_atencion=None, id_medicamento=None, dosis="", frecuencia="", duracion_dias=0):
        self._id_prescripcion = id_prescripcion
        self._id_atencion = id_atencion
        self._id_medicamento = id_medicamento
        self._dosis = dosis
        self._frecuencia = frecuencia
        self._duracion_dias = duracion_dias