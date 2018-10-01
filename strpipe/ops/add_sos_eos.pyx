from strpipe.ops.base cimport BaseOp
from strpipe.toolkit.add_start_end_token cimport (  # noqa: E211
    add_start_end_token_in_sentences_in_c,
    add_start_end_token_in_sentences_meta_in_c,
    remove_start_end_token_in_sentences_in_c,
)
from strpipe.toolkit.tokens_in_sentences cimport (  # noqa: E211
    are_tokens_in_sentences_in_c,
)
from strpipe.toolkit.default_tokens import DefaultTokens
from strpipe.data.types import STRING_LIST


cdef class AddSosEos(BaseOp):
    """Add SOS EOS token to texts.

    Args:
        sos_token (optional): Start of sentence token.
        eos_token (optional): End of sentence token.
        maxlen (optional): The length to pad to. Note that this includes eos, sos tokens as
            part of the length count.
    """

    cdef str _sos_token
    cdef str _eos_token

    def __init__(
            self,
            str sos_token=DefaultTokens.sos,
            str eos_token=DefaultTokens.eos,
        ):
        self.input_type = STRING_LIST
        self.output_type = STRING_LIST

        if sos_token is None:
            sos_token = DefaultTokens.nul
        if eos_token is None:
            eos_token = DefaultTokens.nul

        self._sos_token = sos_token
        self._eos_token = eos_token

    def fit(self, input_data):
        """ Figure out maxlen if not specified in __init__.

        Args:
            input_data: input data
        """
        check_sos, check_eos = are_tokens_in_sentences_in_c(
            tokens=[self._sos_token, self._eos_token],
            sentences=input_data,
        )
        if check_sos:
            raise ValueError('SOS tokens are in input_data')
        if check_eos:
            raise ValueError('EOS tokens are in input_data')

        return None

    def transform(self, state, input_data):
        """Add eos and sos tokens

        Args:
            state
            input_data
        """

        # add start token and end token
        start_end_tx_info = add_start_end_token_in_sentences_meta_in_c(
            sentences=input_data,
            sos_token=self._sos_token,
            eos_token=self._eos_token,
        )
        output_sentences = add_start_end_token_in_sentences_in_c(
            sentences=input_data,
            sos_token=self._sos_token,
            eos_token=self._eos_token,
        )
        return output_sentences, start_end_tx_info

    def inverse_transform(self, state, input_data, tx_info):
        """Remove sos and eos

        Args:
            state:
            input_data:
            tx_info:
        """
        # remove start token and end token
        output_data = remove_start_end_token_in_sentences_in_c(
            sentences=input_data,
            meta=tx_info,
        )
        return output_data
