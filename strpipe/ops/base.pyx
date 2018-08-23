cdef class BaseOp:

    cdef public str input_type
    cdef public str output_type

    def __init__(self):
        pass

    @staticmethod
    def fit(input) -> state:
        pass

    @staticmethod
    def transform(state, input):
        pass

    @staticmethod
    def inverse_transfrom(state, input, meta) -> Data:
        pass
