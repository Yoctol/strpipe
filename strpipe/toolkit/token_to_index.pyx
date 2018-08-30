# distutils: language = c++
from consistent_hash cimport consistent_hash_in_c  # noqa: E999
from default_tokens import DefaultTokens


def token_to_index_with_unk(
        token: str,
        word2index: dict,
        unk_token: str = DefaultTokens.unk,
    ) -> int:
    return token_to_index_with_unk_in_c(
        token=token,
        unk_token=unk_token,
        word2index=word2index,
    )


cdef unsigned int token_to_index_with_unk_in_c(  # noqa: E999
        str token,
        str unk_token,
        dict word2index,
    ):
    cdef unsigned int index

    if token not in word2index:
        # assign unk index
        index = word2index[unk_token]
    else:
        index = word2index[token]
    return index


def token_to_index_with_hash(
        token: str,
        word2index: dict,
    ) -> int:
    return token_to_index_with_hash_in_c(
        token=token,
        word2index=word2index,
    )


cdef unsigned int token_to_index_with_hash_in_c(  # noqa: E999
        str token,
        dict word2index,
    ):
    cdef unsigned int index

    if token not in word2index:
        index = consistent_hash_in_c(
            input_str=token,
            mod_int=len(word2index),
            seed=0,
        )
    else:
        index = word2index[token]
    return index
