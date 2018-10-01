cdef list add_start_end_token_in_sentences_in_c(
    list sentences,
    str sos_token,
    str eos_token
)


cdef list add_start_end_token_in_sentence_in_c(
    list sentence,
    str sos_token,
    str eos_token
)


cdef list add_start_end_token_in_sentences_meta_in_c(
    list sentences,
    str sos_token,
    str eos_token,
)


cdef list add_start_end_token_in_sentence_meta_in_c(
    list sentence,
    str sos_token,
    str eos_token,
)


cdef list remove_start_end_token_in_sentences_in_c(
    list sentences,
    list meta,
)


cdef list remove_start_end_token_in_sentence_in_c(
    list sentence,
    list meta,
)
