from strpipe.ops.base cimport BaseOp
from strpipe.toolkit.compute_maxlen cimport compute_maxlen_in_c
from strpipe.toolkit.add_start_end_token cimport add_start_end_token_in_sentences_in_c
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

        self._check_tokens(sos_token, eos_token, pad_token)

        self._sos_token = sos_token
        self._eos_token = eos_token

        self._maxlen = maxlen

    def _check_tokens(self, sos_token, eos_token, pad_token):
        if (sos_token == DefaultTokens.nul) and (eos_token == DefaultTokens.nul):
            return True

        if eos_token == DefaultTokens.nul:
            raise ValueError("Only start-of-sentence token was provided."
                             "Should provide corresponding end-of-sentence token.")

        if sos_token == DefaultTokens.nul:
            raise ValueError("Only start-of-sentence token was provided."
                             "Should provide corresponding end-of-sentence token.")

        if sos_token == eos_token:
            raise ValueError("Start-of-sentence token cannot be equal to end-of-sentence token.")
        if sos_token == pad_token:
            raise ValueError("Start-of-sentence token cannot be equal to pad token.")
        if eos_token == pad_token:
            raise ValueError("End-of-sentence token cannot be equal to pad token.")

        return True

    def fit(self, input_data):
        ''' Figure out maxlen if not specified in __init__.

        Args:
            input_data: input data
        '''
        cdef int maxlen
        cdef dict result = {}
        if self._maxlen == -1:
            maxlen = compute_maxlen_in_c(input_data)
            if self._sos_token != DefaultTokens.nul:
                maxlen += 2
                result['sos_token'] = self._sos_token
                result['eos_token'] = self._eos_token
        else:
            maxlen = self._maxlen

        result['maxlen'] = maxlen
        result['pad_token'] = self._pad_token

        return result

    def transform(self, state, input_data):
        '''Add eos and sos tokens if necessary then pads to fixed length.

        Args:
            state
            input_data
        '''
        maxlen = state['maxlen']
        pad_token = state['pad_token']

        cdef str sos_token = DefaultTokens.nul
        cdef str eos_token = DefaultTokens.nul

        if 'sos_token' in state and 'eos_token' in state:
            sos_token = state['sos_token']
            eos_token = state['eos_token']
        elif not ('sos_token' in state or 'eos_token' in state):
            sos_token = self._sos_token
            eos_token = self._eos_token
        else:
            raise ValueError("state must provide both start-of-sentence "
                             "and end-of-sentence token not just one.")
        self._check_tokens(sos_token, eos_token, pad_token)

        if sos_token != DefaultTokens.nul:
            input_data = input_data[: (maxlen - 2)]
            sentences_with_boundary_tokens = add_start_end_token_in_sentences_in_c(
                input_data,
                sos_token,
                eos_token,
            )
            tx_info = pad_sentences_meta_in_c(
                sentences=input_data,
                pad_token=pad_token,
                maxlen=maxlen - 1,
            )
            padded_sentences = pad_sentences_in_c(
                sentences=sentences_with_boundary_tokens,
                pad_token=pad_token,
                maxlen=maxlen,
            )

        else:
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
        '''Remove eos, sos and padding.

        Args:
            state:
            input_data:
            tx_info:
        '''

        cdef str sos_token = DefaultTokens.nul
        cdef str eos_token = DefaultTokens.nul
        cdef str pad_token

        if 'sos_token' in state and 'eos_token' in state:
            sos_token = state['sos_token']
            eos_token = state['eos_token']
        elif not ('sos_token' in state or 'eos_token' in state):
            sos_token = self._sos_token
            eos_token = self._eos_token
        else:
            raise ValueError("state must provide both start-of-sentence "
                             "and end-of-sentence token not just one.")

        pad_token = state['pad_token']
        self._check_tokens(sos_token, eos_token, pad_token)

        cdef list s_list
        cdef unsigned int n_sent

        # Strip SOS
        if sos_token != DefaultTokens.nul:
            s_list = []
            n_sent = len(input_data)
            for i in range(n_sent):
                s_list.append(input_data[i][1:])
            return unpad_sentences_in_c(s_list, tx_info)

        return unpad_sentences_in_c(
            input_data,
            tx_info,
        )
