cdef list sentence_to_indices_with_unk_in_c(
    list sentence,
    dict token2index,
    str unk_token,
)
cdef list sentence_to_indices_with_hash_in_c(
    list sentence,
    dict token2index,
)
cdef dict sentence_to_indices_meta_in_c(
    list sentence,
    dict token2index,
)
cdef list indices_to_sentence_in_c(
    list indices,
    dict index2token,
    dict meta,
)

## batch ##
cdef list sentences_to_indices_with_unk_in_c(
    list sentences,
    dict token2index,
    str unk_token,
)
cdef list sentences_to_indices_with_hash_in_c(
    list sentences,
    dict token2index,
)
cdef list sentences_to_indices_meta_in_c(
    list sentences,
    dict token2index,
)
cdef list indices_to_sentences_in_c(
    list indices,
    dict index2token,
    list meta,
)
