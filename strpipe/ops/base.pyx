# distutils: language = c++


cdef class BaseOp:
    '''Base class for Ops

    Sub-classes should implement `fit`, `transform`, and `inverse_transform`.

    Attributes:
        input_type: input type of data to transform
        output_type: output type of transformed data
    '''

    @staticmethod
    cdef fit(input):
        pass

    @staticmethod
    cdef transform(state, input):
        pass

    @staticmethod
    cdef inverse_transfrom(state, input, meta):
        pass
