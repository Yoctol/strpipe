cdef class BaseOp:

    cdef public str input_type
    cdef public str output_type

    def __init__(self):
        pass

    cdef fit(self, input)
    cdef transform(self, state, input)
    cdef inverse_transfrom(self, state, input, meta)
