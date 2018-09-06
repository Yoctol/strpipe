import operator
from .default_tokens import DefaultTokens


def build_vocabulary_from_sentences(
        sentences: list[list[str]],
        vocab_size: int = 1e+8,
    ):
    return build_vocabulary_from_sentences_in_c(
        sentences=sentences,
        vocab_size=vocab_size,
    )


cdef dict build_vocabulary_from_sentences_in_c(  # noqa: E999
        list sentences,
        unsigned int vocab_size,
    ):
    cdef str token
    cdef list sentence, trim_counter
    cdef unsigned int i, j, idx, n_tokens, n_counter, n_sents
    cdef dict output_dict, counter

    n_sents = len(sentences)
    counter = {}
    for i in range(n_sents):
        sentence = sentences[i]
        n_tokens = len(sentence)
        for j in range(n_tokens):
            token = sentence[j]
            if token in counter:
                counter[token] += 1
            else:
                counter[token] = 1

    trim_counter = sorted(
        counter.items(),
        key=operator.itemgetter(1),
        reverse=True,
    )[0: vocab_size]

    n_counter = len(trim_counter)
    output_dict = {}
    for idx in range(n_counter):
        key = trim_counter[idx][0]
        output_dict[key] = idx
    return output_dict
