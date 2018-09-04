from strpipe.ops.base cimport BaseOp
from strpipe.toolkit.compute_maxlen cimport compute_maxlen_in_c
from strpipe.toolkit.compute_bdd_sentlens cimport compute_bounded_sentlens_in_c
from strpipe.toolkit.pad_sentences cimport (  # noqa: E211
    pad_sentences_in_c,
    pad_sentences_meta_in_c,
    unpad_sentences_in_c,
)

from strpipe.toolkit.default_tokens import DefaultTokens
from strpipe.data.types import STRING_LIST


cdef class Pad(BaseOp):

    cdef str _pad_token
    cdef int _maxlen

    def __init__(self, str pad_token=DefaultTokens.pad, int maxlen=-1):
        self.input_type = STRING_LIST
        self.output_type = STRING_LIST
        self._pad_token = pad_token
        self._maxlen = maxlen

    def fit(self, input_data):
        cdef int maxlen
        if self._maxlen == -1:
            maxlen = compute_maxlen_in_c(input_data)
        else:
            maxlen = self._maxlen
        return {
            'maxlen': maxlen,
            'pad_token': self._pad_token,
        }

    def transform(self, state, input_data):
        maxlen = state['maxlen']
        pad_token = state['pad_token']
        tx_info = pad_sentences_meta_in_c(
            sentences=input_data,
            pad_token=pad_token,
            maxlen=maxlen,
        )
        padded_sentences = pad_sentences_in_c(
            sentences=input_data,
            pad_token=pad_token,
            maxlen=maxlen,
        )
        return padded_sentences, tx_info

    def inverse_transform(self, state, input_data, tx_info):
        return unpad_sentences_in_c(
            input_data,
            tx_info,
        )
