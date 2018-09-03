from .default_tokens import DefaultTokens


def add_start_end_token_in_sentences(
        sentences: list[list[str]],
        sos_token: str = DefaultTokens.sos,
        eos_token: str = DefaultTokens.eos,
    ) -> list[list[str]]:
    return add_start_end_token_in_sentences_in_c(
        sentences=sentences,
        sos_token=sos_token,
        eos_token=eos_token,
    )


cdef list add_start_end_token_in_sentences_in_c(  # noqa: E999
        list sentences,
        str sos_token,
        str eos_token,
    ):
    cdef list s_output_list, output_list
    cdef unsigned int i, n_sent

    n_sent = len(sentences)
    output_list = []

    for i in range(n_sent):
        s_output_list = add_start_end_token_in_sentence_in_c(
            sentence=sentences[i],
            sos_token=sos_token,
            eos_token=eos_token,
        )
        output_list.append(s_output_list)
    return output_list


cdef list add_start_end_token_in_sentence_in_c(  # noqa: E999
        list sentence,
        str sos_token,
        str eos_token,
    ):
    cdef list output_list = [sos_token]
    output_list.extend(sentence)
    output_list.extend([eos_token])
    return output_list
