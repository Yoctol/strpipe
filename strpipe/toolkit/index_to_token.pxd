cdef str index_to_token_in_c(
    unsigned int index,
    dict index2word,
)
cdef list indices_to_tokens_in_c(
    list indices,
    dict index2word,
)
cdef list batch_indices_to_tokens_in_c(
    list indices,
    dict index2word,
)
