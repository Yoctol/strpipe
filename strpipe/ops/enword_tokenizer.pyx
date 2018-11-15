from strpipe.ops.base cimport BaseOp

from nltk.tokenize import WordPunctTokenizer

from strpipe.data.types import STRING_LIST, STRING


cdef class EnWordTokenizer(BaseOp):

    cdef unsigned int _num_jobs
    cdef object _tokenizer

    def __init__(
            self,
            num_jobs: int = 1,
            punct: bool = True,
        ):
        self.input_type = STRING
        self.output_type = STRING_LIST
        self._tokenizer = WordPunctTokenizer()
        self._num_jobs = num_jobs

    def fit(self, input_data):
        return None

    def transform(self, state, input_data):
        output_data = []
        lens = []
        spans = []
        for input_datum in input_data:
            output_datum = self._tokenizer.tokenize(input_datum)
            annotation = self._tokenizer.span_tokenize(input_datum)
            output_data.append(output_datum)
            lens.append(len(input_datum))
            spans.append(list(annotation))
        tx_info = {'lens': lens, 'spans': spans}
        return output_data, tx_info

    def inverse_transform(self, state, input_data, tx_info):
        output_data = []
        for input_datum, span, len_ in zip(
            input_data, tx_info['spans'], tx_info['lens']):
            output_list = [' '] * len_
            for (start, end), token in zip(span, input_datum):
                output_list[start: end] = list(token)
            output_data.append(''.join(output_list))
        return output_data
