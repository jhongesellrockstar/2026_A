class Establecimiento:
    def __init__(self, id_establecimiento=None, nombre="", tipo="", distrito="", region="", telefono=""):
        self._id_establecimiento = id_establecimiento
        self._nombre = nombre
        self._tipo = tipo
        self._distrito = distrito
        self._region = region
        self._telefono = telefono

    def get_id(self): return self._id_establecimiento
    def get_nombre(self): return self._nombre