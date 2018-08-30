cdef class BaseOp:

    @staticmethod
    cdef fit(input):
        pass

    @staticmethod
    cdef transform(state, input):
        pass

    @staticmethod
    cdef inverse_transfrom(state, input, meta):
        pass
