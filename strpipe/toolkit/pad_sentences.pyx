from default_tokens import DefaultTokens


def pad_sentences(
        sentences: list[list[str]],
        maxlen: int,
        pad_token: str = DefaultTokens.pad,
    ) -> list[list[str]]:

    return pad_sentences_in_c(
        sentences=sentences,
        pad_token=pad_token,
        maxlen=maxlen,
    )


cdef list pad_sentence_in_c(  # noqa: E999
        list sentence,
        str pad_token,
        unsigned int maxlen,
    ):
    cdef unsigned int sent_len, diff_len
    cdef list padded_sentence, diff_sentence

    sent_len = len(sentence)

    if sent_len >= maxlen:
        padded_sentence = sentence[: maxlen]
    else:
        diff_len = maxlen - sent_len
        diff_sentence = [pad_token] * diff_len
        padded_sentence = sentence
        padded_sentence.extend(diff_sentence)
    return padded_sentence


cdef list pad_sentences_in_c(  # noqa: E999
        list sentences,
        str pad_token,
        unsigned int maxlen,
    ):
    cdef unsigned int n_sent, i
    cdef list sentence, padded_sentence, output_list

    output_list = []
    n_sent = len(sentences)

    for i in range(n_sent):
        sentence = sentences[i]
        padded_sentence = pad_sentence_in_c(
            sentence=sentence,
            pad_token=pad_token,
            maxlen=maxlen,
        )
        output_list.append(padded_sentence)
    return output_list
