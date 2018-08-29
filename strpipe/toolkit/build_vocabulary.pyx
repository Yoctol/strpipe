import operator
from .default_tokens import DefaultTokens


def build_vocabulary_from_sentences(
        sentences: list[list[str]],
        vocab_size: int = 1e+8,
        sos_token: str = DefaultTokens.sos_token,
        eos_token: str = DefaultTokens.eos_token,
        unk_token: str = DefaultTokens.unk_token,
        pad_token: str = DefaultTokens.pad_token,
    ):
        return build_vocabulary_from_sentences_in_c(
            sentences=sentences,
            vocab_size=vocab_size,
            sos_token=sos_token,
            eos_token=eos_token,
            unk_token=unk_token,
            pad_token=pad_token,
        )


cdef dict build_vocabulary_from_sentences_in_c(  # noqa: E999
        list sentences,
        long int vocab_size,
        str sos_token,
        str eos_token,
        str unk_token,
        str pad_token,
    ):
    cdef set default_tokens = set(
        [
            sos_token, eos_token,
            unk_token, pad_token,
        ],
    )
    cdef unsigned int max_len = 0
    cdef unsigned int n_sents = len(sentences)
    cdef str token
    cdef list sentence, trim_counter
    cdef unsigned int i, j, vocab_count, n_tokens, n_counter
    cdef dict output_dict, counter

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
    )[0: vocab_size + 10]

    output_dict = {}
    vocab_count = 0
    for token in default_tokens:
        output_dict[token] = vocab_count
        vocab_count += 1

    n_counter = len(trim_counter)
    for idx in range(n_counter):
        key = trim_counter[idx][0]
        if key not in output_dict:
            output_dict[key] = vocab_count
            vocab_count += 1
        if vocab_count > vocab_size - 1:
            break

    return output_dict
