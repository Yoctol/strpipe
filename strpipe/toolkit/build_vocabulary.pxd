cdef dict build_vocabulary_from_sentences_in_c(
    list sentences,
    unsigned int vocab_size,
    str sos_token,
    str eos_token,
    str unk_token,
    str pad_token,
)
