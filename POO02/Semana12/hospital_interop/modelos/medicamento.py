class Medicamento:
    def __init__(self, id_medicamento=None, nombre="", presentacion="", concentracion=""):
        self._id_medicamento = id_medicamento
        self._nombre = nombre
        self._presentacion = presentacion
        self._concentracion = concentracion