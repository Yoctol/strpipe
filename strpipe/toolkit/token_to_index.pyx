# distutils: language = c++
from consistent_hash cimport consistent_hash_in_c  # noqa: E999
from default_tokens import DefaultTokens


def token_to_index_with_unk(
        token: str,
        token2index: dict,
        unk_token: str = DefaultTokens.unk,
    ) -> int:
    return token_to_index_with_unk_in_cpp(
        token=token,
        unk_token=unk_token,
        token2index=token2index,
    )


cdef unsigned int token_to_index_with_unk_in_cpp(  # noqa: E999
        str token,
        str unk_token,
        dict token2index,
    ) except -1:
    cdef unsigned int index

    if unk_token not in token2index:
        raise KeyError(
            'unk token [{}] is not in token2index'.format(
                unk_token,
            ),
        )

    if token not in token2index:
        # assign unk index
        index = token2index[unk_token]
    else:
        index = token2index[token]
    return index


def token_to_index_with_hash(
        token: str,
        token2index: dict,
    ) -> int:
    return token_to_index_with_hash_in_cpp(
        token=token,
        token2index=token2index,
    )


cdef unsigned int token_to_index_with_hash_in_cpp(  # noqa: E999
        str token,
        dict token2index,
    ):
    cdef unsigned int index, vocab_size
    vocab_size = len(token2index)

    if token not in token2index:
        index = consistent_hash_in_c(
            input_str=token,
            mod_int=vocab_size,
            seed=0,
        )
    else:
        index = token2index[token]
    return index
