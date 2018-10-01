from strpipe.ops.base cimport BaseOp
from strpipe.toolkit.compute_maxlen cimport compute_maxlen_in_c
from strpipe.toolkit.pad_sentences cimport (  # noqa: E211
    pad_sentences_in_c,
    pad_sentences_meta_in_c,
    unpad_sentences_in_c,
)
from strpipe.toolkit.tokens_in_sentences cimport (  # noqa: E211
    is_token_in_sentences_in_c,
)
from strpipe.toolkit.default_tokens import DefaultTokens
from strpipe.data.types import STRING_LIST


cdef class Pad(BaseOp):
    """Pad texts so that they are the same size.

    Args:
        pad_token (optional): Padding token. Default: :obj:`DefaultTokens.pad`
        maxlen (optional): The length to pad to. Note that this includes eos, sos tokens as
            part of the length count.
    """

    cdef str _pad_token
    cdef int _maxlen

    def __init__(
            self,
            str pad_token=DefaultTokens.pad,
            int maxlen=-1,
        ):
        self.input_type = STRING_LIST
        self.output_type = STRING_LIST

        self._pad_token = pad_token
        self._maxlen = maxlen

    def fit(self, input_data):
        """ Figure out maxlen if not specified in __init__.

        Args:
            input_data: input data
        """
        check = is_token_in_sentences_in_c(
            token=self._pad_token,
            sentences=input_data,
        )
        if check:
            raise ValueError(f'Pad token [{self._pad_token}] is in input_data')

        cdef int maxlen
        cdef dict result = {}
        if self._maxlen == -1:
            maxlen = compute_maxlen_in_c(input_data)
        else:
            maxlen = self._maxlen

        result['maxlen'] = maxlen

        return result

    def transform(self, state, input_data):
        """Add eos and sos tokens if necessary then pads to fixed length.

        Args:
            state
            input_data
        """
        maxlen = state['maxlen']

        # pad sentences
        pad_tx_info = pad_sentences_meta_in_c(
            sentences=input_data,
            pad_token=self._pad_token,
            maxlen=maxlen,
        )
        padded_sentences = pad_sentences_in_c(
            sentences=input_data,
            pad_token=self._pad_token,
            maxlen=maxlen,
        )

        return padded_sentences, pad_tx_info

    def inverse_transform(self, state, input_data, tx_info):
        """Remove eos, sos and padding.

        Args:
            state:
            input_data:
            tx_info:
        """

        # unpad sentences
        output_data = unpad_sentences_in_c(
            input_data,
            meta=tx_info,
        )
        return output_data
