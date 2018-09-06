from strpipe.ops.factory import _OpFactory

from strpipe.ops.pad import Pad
from strpipe.ops.token_to_index import TokenToIndexWithUNK
from strpipe.ops.zhchar_tokenizer import ZhCharTokenizer


op_factory = _OpFactory()

op_factory.register('Pad', Pad)
op_factory.register('TokenToIndexWithUNK', TokenToIndexWithUNK)
op_factory.register('ZhCharTokenizer', ZhCharTokenizer)
