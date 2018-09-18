from strpipe.ops.base cimport BaseOp
from strpipe.toolkit.join_sentences cimport split_strs_in_c, join_sentences_in_c
from strpipe.data.types import STRING_LIST, STRING


cdef class CharTokenizer(BaseOp):

    def __init__(self, num_jobs: int = 1):
        self.input_type = STRING
        self.output_type = STRING_LIST

    def fit(self, input_data):
        return None

    def transform(self, state, input_data):
        output_data = split_strs_in_c(
            input_strs=input_data,
            sep='',
        )
        tx_info = None
        return output_data, tx_info

    def inverse_transform(self, state, input_data, tx_info):
        output_data = join_sentences_in_c(
            sentences=input_data,
            by_='',
        )
        return output_data
