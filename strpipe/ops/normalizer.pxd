from .base cimport BaseOp


cdef class Normalizer(BaseOp):

    cdef str _norm_id
    cdef object _normalizer
