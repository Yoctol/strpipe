def compute_maxlen(sentences):
    return compute_maxlen_in_c(sentences)


cdef compute_maxlen_in_c(list sentences):  # noqa: E999
    cdef int maxlen = 0
    cdef list sent
    for i in range(len(sentences)):
        sent = sentences[i]
        if len(sent) > maxlen:
            maxlen = len(sent)
    return maxlen
