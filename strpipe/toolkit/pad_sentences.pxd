cdef list pad_sentence_in_c(
    list sentence,
    str pad_token,
    unsigned int maxlen,
)


cdef dict pad_sentence_meta_in_c(
    list sentence,
    str pad_token,
    unsigned int maxlen,
)


cdef list unpad_sentence_in_c(
    list sentence,
    dict meta,
)


cdef list pad_sentences_in_c(
    list sentences,
    str pad_token,
    unsigned int maxlen,
)


cdef list pad_sentences_meta_in_c(
    list sentences,
    str pad_token,
    unsigned int maxlen,
)


cdef list unpad_sentences_in_c(
    list sentences,
    list meta,
)
