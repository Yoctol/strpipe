from .default_tokens import DefaultTokens


def add_start_end_token_in_sentences(
        sentences: list[list[str]],
        sos_token: str = DefaultTokens.sos,
        eos_token: str = DefaultTokens.eos,
    ) -> list[list[str]]:

    if sos_token is None:
        sos_token = DefaultTokens.nul

    if eos_token is None:
        eos_token = DefaultTokens.nul

    output_meta = add_start_end_token_in_sentences_meta_in_c(
        sentences=sentences,
        sos_token=sos_token,
        eos_token=eos_token,
    )
    output_sents = add_start_end_token_in_sentences_in_c(
        sentences=sentences,
        sos_token=sos_token,
        eos_token=eos_token,
    )

    return output_sents, output_meta


def remove_start_end_token_in_sentences(
        sentences: list[list[str]],
        meta: list[list[bool, bool]],
    ) -> list[list[str]]:

    return remove_start_end_token_in_sentences_in_c(
        sentences=sentences,
        meta=meta,
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
    cdef list output_list = sentence

    if sos_token != DefaultTokens.nul:
        output_list = [sos_token] + output_list
    if eos_token != DefaultTokens.nul:
        output_list = output_list + [eos_token]
    return output_list


cdef list add_start_end_token_in_sentences_meta_in_c(
        list sentences,
        str sos_token,
        str eos_token,
    ):
    cdef list output_list, output, input_sent
    cdef unsigned int i, n_sent

    output_list = []
    n_sent = len(sentences)
    for i in range(n_sent):
        input_sent = sentences[i]
        output = add_start_end_token_in_sentence_meta_in_c(
            sentence=input_sent,
            sos_token=sos_token,
            eos_token=eos_token,
        )
        output_list.append(output)
    return output_list


cdef list add_start_end_token_in_sentence_meta_in_c(
        list sentence,
        str sos_token,
        str eos_token,
    ):
    cdef list record = [False, False]

    if sos_token != DefaultTokens.nul:
        record[0] = True

    if eos_token != DefaultTokens.nul:
        record[1] = True

    return record


cdef list remove_start_end_token_in_sentences_in_c(
        list sentences,
        list meta,
    ):
    cdef list output_list, output, input_meta, input_sent
    cdef unsigned int i, n_sent

    output_list = []
    n_sent = len(sentences)
    for i in range(n_sent):
        input_sent = sentences[i]
        input_meta = meta[i]
        output = remove_start_end_token_in_sentence_in_c(
            sentence=input_sent,
            meta=input_meta,
        )
        output_list.append(output)
    return output_list


cdef list remove_start_end_token_in_sentence_in_c(
        list sentence,
        list meta,
    ):
    cdef unsigned int start, end

    start = 0
    end = len(sentence)

    if meta[0] is True:
        start = 1
    if meta[1] is True:
        end = end - 1

    return sentence[start: end]
