

def join_sentences(
        sentences: list[list[str]],
        by_: str = None,
    ) -> tuple[list[str], list[list[int]]]:

    if by_ is None:
        by_ = ''

    output = join_sentences_in_c(
        sentences=sentences,
        by_=by_,
    )
    meta = join_sentences_meta_in_c(
        sentences=sentences,
        by_=by_,
    )
    return output, meta


def split_strs(
        input_strs: list[str],
        sep: str = None,
        meta: list[list[int]] = None,
    ) -> list[list[str]]:

    if sep is None:
        sep = ''
    if meta is None:
        output = split_strs_in_c(
            input_strs=input_strs,
            sep=sep,
        )
    else:
        output = split_strs_by_meta_in_c(
            input_strs=input_strs,
            sep=sep,
            meta=meta,
        )
    return output


cdef str join_sentence_in_c(list sentence, str by_):
    cdef str output
    output = by_.join(sentence)
    return output


cdef list join_sentences_in_c(list sentences, str by_):
    cdef list input_sent, output_list
    cdef str output_str
    cdef unsigned int i, n_sent

    output_list = []
    n_sent = len(sentences)
    for i in range(n_sent):
        input_sent = sentences[i]
        output_str = join_sentence_in_c(
            sentence=input_sent,
            by_=by_,
         )
        output_list.append(output_str)
    return output_list


cdef list join_sentence_meta_in_c(list sentence, str by_):
    cdef list output
    cdef unsigned int i, n_token, token_len, by_len, cur_len
    cdef str token

    by_len = len(by_)
    n_by = len(sentence) - 1
    output = [0] * n_by
    cur_len = 0
    for i in range(0, n_by):
        token = sentence[i]
        token_len = len(token)
        output[i] = token_len + cur_len
        cur_len = output[i]

    for i in range(1, n_by):
        output[i] = output[i] + by_len * i
    return output


cdef list join_sentences_meta_in_c(list sentences, str by_):
    cdef list output_list, input_sent, output
    cdef unsigned int i, n_sent

    n_sent = len(sentences)
    output_list = []
    for i in range(n_sent):
        input_sent = sentences[i]
        output = join_sentence_meta_in_c(
            sentence=input_sent,
            by_=by_,
        )
        output_list.append(output)
    return output_list


cdef list split_str_in_c(str input_str, str sep):
    cdef list output
    if len(sep) == 0:
        output = list(input_str)
    else:
        output = input_str.split(sep)
    return output


cdef list split_strs_in_c(list input_strs, str sep):
    cdef str input_str
    cdef unsigned int i, n_str
    cdef list output_list, output_sent

    output_list = []
    n_str = len(input_strs)
    for i in range(n_str):
        input_str = input_strs[i]
        output_sent = split_str_in_c(
            input_str=input_str,
            sep=sep,
        )
        output_list.append(output_sent)
    return output_list


cdef list split_str_by_meta_in_c(
        str input_str,
        str sep,
        list meta,
    ):
    cdef list output
    cdef str token
    cdef unsigned int i, n_meta, current_pt, split_pt, sep_len

    current_pt = 0
    output = []
    n_meta = len(meta)
    sep_len = len(sep)

    for i in range(n_meta):
        split_pt = meta[i]
        token = input_str[current_pt: split_pt]
        output.append(token)
        current_pt = split_pt + sep_len

    token = input_str[current_pt:]
    output.append(token)

    return output


cdef list split_strs_by_meta_in_c(
        list input_strs,
        str sep,
        list meta,
    ):
    cdef unsigned int i, n_strs
    cdef str input_str
    cdef list output_list, output, input_meta

    n_strs = len(input_strs)
    output_list = []
    for i in range(n_strs):
        input_str = input_strs[i]
        input_meta = meta[i]
        output = split_str_by_meta_in_c(
            input_str=input_str,
            sep=sep,
            meta=input_meta,
        )
        output_list.append(output)
    return output_list
