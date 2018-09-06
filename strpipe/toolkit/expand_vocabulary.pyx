

def expand_vocabulary(
        token2index: dict,
        tokens: list[str],
    ) -> dict:
    return expand_vocabulary_in_c(
        token2index=token2index,
        tokens=tokens,
    )


cdef dict expand_vocabulary_in_c(
        dict token2index,
        list tokens,
    ):
    cdef unsigned int n_token, vocab_size, i
    cdef str token
    cdef list extra_tokens = []

    vocab_size = len(token2index)
    n_token = len(tokens)
    for i in range(n_token):
        token = tokens[i]
        if token not in token2index:
            token2index[token] = vocab_size
            vocab_size = vocab_size + 1

    return token2index
