from strpipe.ops.factory import _OpFactory

from strpipe.ops.pad import Pad
from strpipe.ops.token_to_index import TokenToIndexWithUNK
from strpipe.ops.zhchar_tokenizer import ZhCharTokenizer
from strpipe.ops.normalizer import Normalizer


op_factory = _OpFactory()

op_factory.register('Pad', Pad)
op_factory.register('TokenToIndexWithUNK', TokenToIndexWithUNK)
op_factory.register('ZhCharTokenizer', ZhCharTokenizer)
op_factory.register('Normalizer', Normalizer)
