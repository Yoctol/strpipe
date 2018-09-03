cdef class BaseOp:

    cdef public str input_type
    cdef public str output_type

    @staticmethod
    cdef fit(input)

    @staticmethod
    cdef transform(state, input)

    @staticmethod
    cdef inverse_transfrom(state, input, tx_info)
