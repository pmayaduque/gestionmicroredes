
class Generator():

    def __init__(self, id_gen, va_op):
        self.id_gen = id_gen
        self.va_op = va_op


class Solar(Generator):
    def __init__(self, id_gen, tec, va_op, ef, A):
        self.ef = ef
        self.A = A
        self.tec = tec
        super(Solar, self).__init__(id_gen, va_op)

class Eolica(Generator):
    def __init__(self, id_gen, tec, va_op, ef, s, p, w_min, w_a, w_max):
        self.ef = ef
        self.s = s
        self.p = p
        self.w_min = w_min
        self.w_a = w_a
        self.w_max = w_max
        self.tec = tec
        super(Eolica, self).__init__(id_gen, va_op)

class Hidraulica(Generator):
    def __init__(self, id_gen, tec, va_op, ef, ht, p):
        self.ef = ef
        self.ht = ht
        self.p = p
        self.tec = tec
        super(Hidraulica, self).__init__(id_gen, va_op)

class Diesel(Generator):
    def __init__(self, id_gen,tec, va_op, ef, g_min, g_max):
        self.ef = ef
        self.g_min = g_min
        self.g_max = g_max
        self.tec = tec
        super(Diesel, self).__init__(id_gen, va_op)

class Bateria():
    def __init__(self, id_bat, ef, o, ef_inv, eb_zero):
        """
        Crea los objetos que son unidades de almacenamiento de energía.
        Args:
            id_bateria (char) id o nombre de la batería.
            ef (float) eficiencia de la batería.
            o (float) tasa de autodescarga.
            ef_inv (float) eficiencia del inversor.
        """
        self.id_bat = id_bat
        self.ef = ef
        self.o = o
        self.ef_inv = ef_inv
        self.eb_zero = eb_zero