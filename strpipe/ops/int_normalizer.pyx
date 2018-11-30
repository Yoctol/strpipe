from .normalizer cimport Normalizer


cdef class IntNormalizer(Normalizer):

    def __init__(self):
        super().__init__(norm_id='int_text_normalizer')
