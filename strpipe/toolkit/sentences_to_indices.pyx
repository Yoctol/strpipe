from token_to_index cimport(   # noqa: E999
    token_to_index_with_unk_in_cpp,
    token_to_index_with_hash_in_cpp,
)
from .default_tokens import DefaultTokens


def sentences_to_indices_with_unk(
        sentences: list[list[str]],
        token2index: dict,
        unk_token: str = DefaultTokens.unk,
    ) -> tuple[list[list[int]], list[dict]]:

    meta = sentences_to_indices_meta_in_c(
        sentences=sentences,
        token2index=token2index,
    )
    indices = sentences_to_indices_with_unk_in_c(
        sentences=sentences,
        token2index=token2index,
        unk_token=unk_token,
    )
    return indices, meta


def sentences_to_indices_with_hash(
        sentences: list[list[str]],
        token2index: dict,
    ) -> tuple[list[list[int]], list[dict]]:

    meta = sentences_to_indices_meta_in_c(
        sentences=sentences,
        token2index=token2index,
    )
    indices = sentences_to_indices_with_hash_in_c(
        sentences=sentences,
        token2index=token2index,
    )
    return indices, meta


def indices_to_sentences(
        indices: list[list[int]],
        index2token: dict,
        meta: list[dict],
    ) -> list[list[str]]:
    return indices_to_sentences_in_c(
        indices=indices,
        index2token=index2token,
        meta=meta,
    )


cdef list sentence_to_indices_with_unk_in_c(
        list sentence,
        dict token2index,
        str unk_token,
    ):
    cdef unsigned int i, n_token, index
    cdef list output_indices = []
    cdef str token

    n_token = len(sentence)
    for i in range(n_token):
        token = sentence[i]
        index = token_to_index_with_unk_in_cpp(
            token=token,
            token2index=token2index,
            unk_token=unk_token,
        )
        output_indices.append(index)
    return output_indices


cdef list sentence_to_indices_with_hash_in_c(
        list sentence,
        dict token2index,
    ):
    cdef unsigned int i, n_token, index
    cdef list output_indices = []
    cdef str token

    n_token = len(sentence)
    for i in range(n_token):
        token = sentence[i]
        index = token_to_index_with_hash_in_cpp(
            token=token,
            token2index=token2index,
        )
        output_indices.append(index)
    return output_indices


cdef dict sentence_to_indices_meta_in_c(
        list sentence,
        dict token2index,
    ):
    cdef unsigned int i, n_token, index
    cdef str token
    cdef dict meta = {}

    n_token = len(sentence)
    for i in range(n_token):
        token = sentence[i]
        if token not in token2index:
            meta[i] = token
    return meta


cdef list indices_to_sentence_in_c(
        list indices,
        dict index2token,
        dict meta,
    ):
    cdef unsigned int i, n_index, index
    cdef list sentence = []
    cdef str token, key

    n_index = len(indices)
    for i in range(n_index):
        index = indices[i]
        if i in meta:
            token = meta[i]
        else:
            key = str(index)
            token = index2token[key]
        sentence.append(token)
    return sentence


### batch
cdef list sentences_to_indices_with_unk_in_c(
        list sentences,
        dict token2index,
        str unk_token,
    ):
    cdef unsigned int i, n_sent
    cdef list single_output_indices, output_indices, sentence

    n_sent = len(sentences)
    output_indices = []
    for i in range(n_sent):
        sentence = sentences[i]
        single_output_indices = sentence_to_indices_with_unk_in_c(
            sentence=sentence,
            token2index=token2index,
            unk_token=unk_token,
        )
        output_indices.append(single_output_indices)
    return output_indices


cdef list sentences_to_indices_with_hash_in_c(
        list sentences,
        dict token2index,
    ):
    cdef unsigned int i, n_sent
    cdef list single_output_indices, output_indices, sentence

    n_sent = len(sentences)
    output_indices = []
    for i in range(n_sent):
        sentence = sentences[i]
        single_output_indices = sentence_to_indices_with_hash_in_c(
            sentence=sentence,
            token2index=token2index,
        )
        output_indices.append(single_output_indices)
    return output_indices


cdef list sentences_to_indices_meta_in_c(
        list sentences,
        dict token2index,
    ):
    cdef unsigned int i, n_sent
    cdef dict meta
    cdef list sentence, meta_list

    meta_list = []
    n_sent = len(sentences)
    for i in range(n_sent):
        sentence = sentences[i]
        meta = sentence_to_indices_meta_in_c(
            sentence=sentence,
            token2index=token2index,
        )
        meta_list.append(meta)
    return meta_list


cdef list indices_to_sentences_in_c(
        list indices,
        dict index2token,
        list meta,
    ):
    cdef unsigned int i, n_index
    cdef list single_indices, sentences, sentence
    cdef dict single_meta

    sentences = []
    n_index = len(indices)
    for i in range(n_index):
        single_indices = indices[i]
        single_meta = meta[i]
        sentence = indices_to_sentence_in_c(
            indices=single_indices,
            index2token=index2token,
            meta=single_meta,
        )
        sentences.append(sentence)
    return sentences
