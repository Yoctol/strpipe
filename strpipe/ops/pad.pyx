from .base cimport BaseOp


cdef class Pad(BaseOp):

    cdef __init__(self, maxlen=None):
        pass
