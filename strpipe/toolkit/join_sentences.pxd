cdef list join_sentences_in_c(
    list sentences,
    str by_,
)


cdef str join_sentence_in_c(
    list sentence,
    str by_,
)


cdef list join_sentence_meta_in_c(
    list sentence,
    str by_,
)


cdef list join_sentences_meta_in_c(
    list sentences,
    str by_,
)


cdef list split_str_in_c(
    str input_str,
    str sep,
)


cdef list split_strs_in_c(
    list input_strs,
    str sep,
)


cdef list split_str_by_meta_in_c(
    str input_str,
    str sep,
    list meta,
)


cdef list split_strs_by_meta_in_c(
    list input_strs,
    str sep,
    list meta,
)
