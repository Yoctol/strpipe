

def are_tokens_in_sentences(
        tokens: list[str],
        sentences: list[list[str]],
    ):
    return are_tokens_in_sentences_in_c(
        tokens=tokens,
        sentences=sentences,
    )


def is_token_in_sentences(
        token: str,
        sentences: list[list[str]],
    ):
    return is_token_in_sentences_in_c(
        token=token,
        sentences=sentences,
    )


cdef list are_tokens_in_sentences_in_c(
        list tokens,
        list sentences,
    ):
    cdef bint check
    cdef unsigned int i, n_token
    cdef str token
    cdef list output_check = []

    n_token = len(tokens)
    for i in range(n_token):
        token = tokens[i]
        check = is_token_in_sentences_in_c(
            token=token,
            sentences=sentences,
        )
        output_check.append(check)
    return output_check


cdef bint is_token_in_sentences_in_c(
        str token,
        list sentences,
    ):
    cdef bint single_check
    cdef unsigned int i, n_sent
    cdef list sentence

    n_sent = len(sentences)
    for i in range(n_sent):
        sentence = sentences[i]
        single_check = is_token_in_sentence_in_c(
            token=token,
            sentence=sentence,
        )
        if single_check > 0:
            return 1
    return 0


cdef bint is_token_in_sentence_in_c(
        str token,
        list sentence,
    ):
    return token in sentence
