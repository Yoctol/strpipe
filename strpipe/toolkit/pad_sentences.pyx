from default_tokens import DefaultTokens


def pad_sentences(
        sentences: list[list[str]],
        maxlen: int,
        pad_token: str = DefaultTokens.pad,
    ) -> tuple[list[list[str]], dict]:
    '''
    transform
    '''

    meta = pad_sentences_meta_in_c(
        sentences=sentences,
        pad_token=pad_token,
        maxlen=maxlen,
    )
    padded_sentences = pad_sentences_in_c(
        sentences=sentences,
        pad_token=pad_token,
        maxlen=maxlen,
    )
    return padded_sentences, meta


def unpad_sentences(
        sentences: list[list[str]],
        meta: list[dict],
    ) -> list[list[str]]:
    '''
    inverse transform
    '''
    return unpad_sentences_in_c(
        sentences=sentences,
        meta=meta,
    )


cdef list pad_sentence_in_c(
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


cdef dict pad_sentence_meta_in_c(
        list sentence,
        str pad_token,
        unsigned int maxlen,
    ):
    cdef dict output_meta_dict = {}
    cdef list sentence_tail
    cdef unsigned int sentlen = len(sentence)
    output_meta_dict['sentlen'] = sentlen
    if maxlen >= sentlen:
        output_meta_dict['sentence_tail'] = []
    else:
        sentence_tail = sentence[maxlen:]
        output_meta_dict['sentence_tail'] = sentence_tail
    return output_meta_dict


cdef list unpad_sentence_in_c(
        list sentence,
        dict meta,
    ):
    cdef int padded_sentlen, sentlen
    cdef list sentence_tail, output_sentence

    sentlen = meta['sentlen']
    sentence_tail = meta['sentence_tail']
    padded_sentlen = len(sentence)
    if padded_sentlen >= sentlen:
        output_sentence = sentence[:sentlen]
    else:
        output_sentence = sentence + sentence_tail

    return output_sentence


### batch versions ###
cdef list pad_sentences_in_c(
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


cdef list pad_sentences_meta_in_c(
        list sentences,
        str pad_token,
        unsigned int maxlen,
    ):
    cdef unsigned int i, n_sent
    cdef list output_meta_list = []
    cdef dict meta_dict

    n_sent = len(sentences)
    for i in range(n_sent):
        meta_dict = pad_sentence_meta_in_c(
            sentence=sentences[i],
            pad_token=pad_token,
            maxlen=maxlen,
        )
        output_meta_list.append(meta_dict)
    return output_meta_list


cdef list unpad_sentences_in_c(
        list sentences,
        list meta,
    ):
    cdef list output_sentence, output_sentences
    cdef unsigned int i, n_sent

    n_sent = len(sentences)
    output_sentences = []
    for i in range(n_sent):
        output_sentence = unpad_sentence_in_c(
            sentence=sentences[i],
            meta=meta[i],
        )
        output_sentences.append(output_sentence)
    return output_sentences
