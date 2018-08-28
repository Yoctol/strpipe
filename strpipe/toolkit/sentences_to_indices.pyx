from token_to_index cimport(   # noqa: E999
    token_to_index_with_unk_in_c,
    token_to_index_with_hash_in_c,
)


def sentence_to_indices(
        sentence: list,
        word2index: dict[str, int],
        use_hash: bint = False,
        unk_token: str = "<UNK>",
    ) -> list[int]:
    return sentence_to_indices_in_c(
        sentence=sentence,
        word2index=word2index,
        use_hash=use_hash,
        unk_token=unk_token,
    )


def batch_sentences_to_indices(
        sentences: list[str],
        word2index: dict[str, int],
        use_hash: bint = False,
        unk_token: str = "<UNK>",
    ):
    return batch_sentences_to_indices_in_c(
        sentences=sentences,
        word2index=word2index,
        use_hash=use_hash,
        unk_token=unk_token,
    )


cdef list batch_sentences_to_indices_in_c(  # noqa: E999
        list sentences,
        dict word2index,
        bint use_hash,
        str unk_token,
    ):
    cdef int i, n_sent
    cdef list sentence, indices, output_list
    n_sent = len(sentences)
    output_list = []

    for i in range(n_sent):
        sentence = sentences[i]
        indices = sentence_to_indices_in_c(
            sentence=sentence,
            word2index=word2index,
            use_hash=use_hash,
            unk_token=unk_token,
        )
        output_list.append(indices)
    return output_list


cdef list sentence_to_indices_in_c(  # noqa: E999
        list sentence,
        dict word2index,
        bint use_hash,
        str unk_token,
    ):
    cdef int i, n_token
    cdef list output_list = []
    cdef bint unk_in_word2index

    unk_in_word2index = check_unk_in_word2index_in_c(
        unk_token=unk_token,
        word2index=word2index,
    )
    n_token = len(sentence)

    for i in range(n_token):
        token = sentence[i]
        if use_hash:
            index = token_to_index_with_hash_in_c(
                token=token,
                word2index=word2index,
            )
        elif unk_in_word2index:
            index = token_to_index_with_unk_in_c(
                unk_token=unk_token,
                token=token,
                word2index=word2index,
            )
        else:
            raise ValueError(
                "OOV handling support (1) hash (2) UNK token only",
            )
        output_list.append(index)
    return output_list


cdef bint check_unk_in_word2index_in_c(  # noqa: E999
        str unk_token,
        dict word2index,
    ):
    if unk_token in word2index:
        return True
    else:
        return False
