cdef unsigned int token_to_index_with_unk_in_cpp(
    str token,
    str unk_token,
    dict token2index,
) except -1
cdef unsigned int token_to_index_with_hash_in_cpp(
    str token,
    dict token2index,
)
