from strpipe.ops.base cimport BaseOp

from tokenizer_hub import ChineseCharTokenizer

from strpipe.data.types import STRING_LIST, STRING


cdef class ZhCharTokenizer(BaseOp):

    cdef unsigned int _num_jobs
    cdef object _tokenizer

    def __init__(self, num_jobs: int = 1):
        self.input_type = STRING
        self.output_type = STRING_LIST
        self._tokenizer = ChineseCharTokenizer()
        self._num_jobs = num_jobs

    def fit(self, input_data):
        return None

    def transform(self, state, input_data):
        output_data = self._tokenizer.lcut_sentences(
            sentences=input_data,
            num_jobs=self._num_jobs,
        )
        meta = None
        return output_data, meta

    def inverse_transform(self, state, input_data, tx_info):
        output_data = []
        for sent in input_data:
            output_sent = ''.join(sent)
            output_data.append(output_sent)
        return output_data
