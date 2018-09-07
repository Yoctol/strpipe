from strpipe.ops.base cimport BaseOp
from strpipe.toolkit.compute_maxlen cimport compute_maxlen_in_c
from strpipe.toolkit.tokens_in_sentences cimport are_tokens_in_sentences_in_c
from strpipe.toolkit.compute_bdd_sentlens cimport compute_bounded_sentlens_in_c
from strpipe.toolkit.pad_sentences cimport (  # noqa: E211
    pad_sentences_in_c,
    pad_sentences_meta_in_c,
    unpad_sentences_in_c,
)

from strpipe.toolkit.default_tokens import DefaultTokens
from strpipe.data.types import STRING_LIST


cdef class Pad(BaseOp):
    '''Pad texts so that they are the same size.

    Args:
        pad_token (optional): Padding token. Default: :obj:`DefaultTokens.pad`
        sos_token (optional): Start of sentence token.
        eos_token (optional): End of sentence token.
        maxlen (optional): The length to pad to. Note that this includes eos, sos tokens as
            part of the length count.
    '''

    cdef str _pad_token
    cdef str _sos_token
    cdef str _eos_token
    cdef int _maxlen

    def __init__(
        self,
        str sos_token=DefaultTokens.nul,
        str eos_token=DefaultTokens.nul,
        str pad_token=DefaultTokens.pad,
        int maxlen=-1):
        self.input_type = STRING_LIST
        self.output_type = STRING_LIST
        self._pad_token = pad_token
        self._sos_token = sos_token
        self._eos_token = eos_token
        self._maxlen = maxlen

    def fit(self, input_data):
        ''' Figure out maxlen if not specified in __init__.

        Args:
            input_data: input data
        '''
        cdef list tokens = [self._pad_token]
        if self._sos_token != DefaultTokens.nul:
            tokens.append(self._sos_token)
        if self._eos_token != DefaultTokens.nul:
            tokens.append(self._eos_token)
        token_check = are_tokens_in_sentences_in_c(tokens,
                                                   input_data)
        if any(token_check):
            raise ValueError("Detected input_data already has tokens matching given pad/eos/sos!")

        cdef int maxlen
        if self._maxlen == -1:
            maxlen = compute_maxlen_in_c(input_data)
        else:
            maxlen = self._maxlen

        state = {
            'maxlen': maxlen,
            'pad_token': self._pad_token,
        }

        if self._sos_token != DefaultTokens.nul:
            state['sos_token'] = self._sos_token
            state['maxlen'] += 1
        if self._eos_token != DefaultTokens.nul:
            state['eos_token'] = self._eos_token
            state['maxlen'] += 1

        return state

    def transform(self, state, input_data):
        '''Add eos and sos tokens if necessary then pads to fixed length.

        Args:
            state
            input_data
        '''
        maxlen = state['maxlen']
        pad_token = state['pad_token']
        sos_token = state.get('sos_token', DefaultTokens.nul)
        eos_token = state.get('eos_token', DefaultTokens.nul)

        cdef list tokens = [pad_token]
        if sos_token != DefaultTokens.nul:
            tokens.append(self._sos_token)
        if eos_token != DefaultTokens.nul:
            tokens.append(self._eos_token)
        token_check = are_tokens_in_sentences_in_c(tokens,
                                                   input_data)
        if any(token_check):
            raise ValueError("Detected input_data already has tokens matching given pad/eos/sos!")

        tx_info = pad_sentences_meta_in_c(
            sentences=input_data,
            pad_token=pad_token,
            sos_token=sos_token,
            eos_token=eos_token,
            maxlen=maxlen,
        )
        padded_sentences = pad_sentences_in_c(
            sentences=input_data,
            pad_token=pad_token,
            sos_token=sos_token,
            eos_token=eos_token,
            maxlen=maxlen,
        )
        return padded_sentences, tx_info

    def inverse_transform(self, state, input_data, tx_info):
        '''Remove eos, sos and padding.

        Args:
            state:
            input_data:
            tx_info:
        '''
        return unpad_sentences_in_c(
            input_data,
            tx_info,
        )
