

def batch_indices_to_tokens(
        indices: list[list[int]],
        index2word: dict,
    ) -> list[list[str]]:

    return batch_indices_to_tokens_in_c(
        indices=indices,
        index2word=index2word,
    )


cdef str index_to_token_in_c(  # noqa: E999
        unsigned int index,
        dict index2word,
    ):
    cdef unsigned int index2word_size
    index2word_size = len(index2word)

    if index2word_size < 1:
        raise ValueError(
            "index to word mapping is empty",
        )

    if index not in index2word:
        raise KeyError(
            "index [{}] is not in index2word mapping".format(index),
        )
    return index2word[index]


cdef list indices_to_tokens_in_c(
        list indices,
        dict index2word,
    ):
    cdef list output_list = []
    cdef unsigned int n_idx, i
    cdef str output_str

    n_idx = len(indices)
    for i in range(n_idx):
        output_str = index_to_token_in_c(
            index=indices[i],
            index2word=index2word,
        )
        output_list.append(output_str)
    return output_list


cdef list batch_indices_to_tokens_in_c(
        list indices,
        dict index2word,
    ):
    cdef list single_indices, out_indices, output_list
    cdef unsigned int n_idx, i

    output_list = []

    n_idx = len(indices)
    for i in range(n_idx):
        single_indices = indices[i]
        out_indices = indices_to_tokens_in_c(
            indices=single_indices,
            index2word=index2word,
        )
        output_list.append(out_indices)
    return output_list
