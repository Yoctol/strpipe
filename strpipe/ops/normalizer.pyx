from text_normalizer.library import *  # noqa
from text_normalizer.collection import *  # noqa

from strpipe.ops.base cimport BaseOp
from strpipe.data.types import STRING


cdef class Normalizer(BaseOp):

    cdef str _norm_id
    cdef object _normalizer

    '''
    ref: https://github.com/Yoctol/text-normalizer
    '''

    def __init__(self, norm_id: str = 'identity_text_normalizer'):
        self.input_type = STRING
        self.output_type = STRING
        self._norm_id = norm_id
        self._normalizer = globals()[self._norm_id]

    def fit(self, input_data):
        return None

    def transform(self, state, input_data):
        output_data = []
        meta_list = []
        for datum in input_data:
            output_datum, meta = self._normalizer.normalize(
                sentence=datum,
            )
            output_data.append(output_datum)
            meta_list.append(meta)
        return output_data, meta_list

    def inverse_transform(self, state, input_data, tx_info):
        output_data = []
        for datum, meta in zip(input_data, tx_info):
            output_datum = self._normalizer.denormalize(
                sentence=datum,
                meta=meta,
            )
            output_data.append(output_datum)
        return output_data
