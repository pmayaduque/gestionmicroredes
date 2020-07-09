
class Generator():

    def __init__(self, id_gen, va_op):
        self.id_gen = id_gen
        self.va_op = va_op


class Solar(Generator):
    def __init__(self, id_gen, va_op, ef, A):
        self.ef = ef
        self.A = A
        self.tec = 0
        super(Solar, self).__init__(id_gen, va_op)

class Eolica(Generator):
    def __init__(self, id_gen, va_op, ef, s, p, w_min, w_a, w_max):
        self.ef = ef
        self.s = s
        self.p = p
        self.w_min = w_min
        self.w_a = w_a
        self.w_max = w_max
        self.tec = 1
        super(Eolica, self).__init__(id_gen, va_op)

class Hidraulica(Generator):
    def __init__(self, id_gen, va_op, ef, ht, p):
        self.ef = ef
        self.ht = ht
        self.p = p
        super(Hidraulica, self).__init__(id_gen, va_op)

class Diesel(Generator):
    def __init__(self, id_gen, va_op, ef, g_max):
        self.ef = ef
        self.g_max = g_max
        super(Diesel, self).__init__(id_gen, va_op)

class Bateria():
    def __init__(self, id_bat, ef, o, ef_inv):
        """
        Crea los objetos que son unidades de almacenamiento de energía.
        Args:
            id_bateria (char) id o nombre de la batería.
            ef (float) eficiencia de la batería.
            o (float) tasa de autodescarga.
            ef_inv (float) eficiencia del inversor.
        """
        self.id_bateria = id_bat
        self.ef = ef
        self.o = o
        self.ef_inv = ef_inv