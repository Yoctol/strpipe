import hashlib


def token_to_index_with_unk(
        token: str,
        word2index: dict,
        unk_token: str = "<UNK>",
    ) -> int:
    return token_to_index_with_unk_in_c(
        token=token,
        unk_token=unk_token,
        word2index=word2index,
    )


cdef int token_to_index_with_unk_in_c(  # noqa
        str token,
        str unk_token,
        dict word2index,
    ):
    cdef long int index

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


cdef int token_to_index_with_hash_in_c(
        str token,
        dict word2index,
    ):
    cdef long int index

    if token not in word2index:
        index = hashlib.sha1(token) % len(word2index)
    else:
        index = word2index[token]
    return index
