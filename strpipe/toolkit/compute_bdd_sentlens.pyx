

def compute_bounded_sentlens(
        sentences: list[list[str]],
        maxlen: int = 0,
    ) -> list[int]:
    return compute_bounded_sentlens_in_c(
        sentences=sentences,
        maxlen=maxlen,
    )


cdef list compute_bounded_sentlens_in_c(  # noqa: E999
        list sentences,
        unsigned int maxlen,
    ):
    cdef list sentence, output_list
    cdef int sent_len, n_sent, i

    n_sent = len(sentences)
    output_list = []

    for i in range(n_sent):
        sentence = sentences[i]
        sent_len = compute_bounded_sentlen_in_c(
            sentence=sentence,
            maxlen=maxlen,
        )
        output_list.append(sent_len)
    return output_list


cdef unsigned int compute_bounded_sentlen_in_c(  # noqa: E999
        list sentence,
        unsigned int maxlen,
    ):
    cdef int sent_len = len(sentence)
    if maxlen > 0:
        # maxlen > 0
        return min(maxlen, sent_len)
    else:
        # maxlen = 0 return real length of sentence
        return sent_len
