from strpipe.ops.base cimport BaseOp
from strpipe.toolkit.build_vocabulary cimport(
    build_vocabulary_from_sentences_in_c,
)
from strpipe.toolkit.sentences_to_indices cimport(
    sentences_to_indices_with_unk_in_c,
    indices_to_sentences_in_c,
    sentences_to_indices_meta_in_c,
)
from strpipe.toolkit.invert_dictionary cimport(
    invert_dictionary_in_c,
)
from strpipe.toolkit.tokens_in_sentences cimport(
    is_token_in_sentences_in_c,
)
from strpipe.toolkit.expand_vocabulary cimport(
    expand_vocabulary_in_c,
)
from strpipe.toolkit.default_tokens import DefaultTokens
from strpipe.data.types import STRING_LIST


cdef class TokenToIndex(BaseOp):

    cdef str _unk_token
    cdef dict _token2index, _index2token
    cdef unsigned int _vocab_size
    cdef list _necessary_tokens
    cdef bint _skip_unknown

    def __init__(
            self,
            unk_token: str = DefaultTokens.unk,
            vocab_size: int = 1e+8,
            token2index: dict = None,
            necessary_tokens: list[str] = None,
            _skip_unknown: bool = False,
        ):
        self.input_type = STRING_LIST
        self.output_type = STRING_LIST

        self._unk_token = unk_token
        self._vocab_size = vocab_size
        self._token2index = token2index
        self._necessary_tokens = necessary_tokens
        self._skip_unknown = _skip_unknown
        if self._skip_unknown is True:
            raise NotImplementedError("TokenToIndex has not implemented skip-unknown mode")

        self._index2token = None

        if self._necessary_tokens is None:
            self._necessary_tokens = []

    def fit(self, input_data) -> dict:
        ## whether unk token in sentences or not
        check = is_token_in_sentences_in_c(
            token=self._unk_token,
            sentences=input_data,
        )
        if check:
            raise ValueError(
                f'UNK token [{self._unk_token}] exists in sentences.'
            )

        if self._token2index is None:
            self._token2index = build_vocabulary_from_sentences_in_c(
                sentences=input_data,
                vocab_size=self._vocab_size,
            )
        self._token2index = expand_vocabulary_in_c(
            token2index=self._token2index,
            tokens=[self._unk_token] + self._necessary_tokens,
        )

        self._index2token = invert_dictionary_in_c(
            self._token2index,
            serializable=True,
        )
        return {
            'token2index': self._token2index,
            'index2token': self._index2token,
        }

    def transform(self, state, input_data):
        tx_info = sentences_to_indices_meta_in_c(
            sentences=input_data,
            token2index=state['token2index'],
        )
        indices = sentences_to_indices_with_unk_in_c(
            sentences=input_data,
            token2index=state['token2index'],
            unk_token=self._unk_token,
        )
        return indices, tx_info

    def inverse_transform(self, state, input_data, tx_info):
        return indices_to_sentences_in_c(
            indices=input_data,
            index2token=state['index2token'],
            meta=tx_info,
        )
