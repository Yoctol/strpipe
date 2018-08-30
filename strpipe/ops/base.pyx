cdef class BaseOp:

    cdef public str input_type
    cdef public str output_type

    @staticmethod
    def fit(input):
        pass

    @staticmethod
    def transform(state, input):
        pass

    @staticmethod
    def inverse_transfrom(state, input, meta):
        pass
