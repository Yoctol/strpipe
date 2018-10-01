from strpipe.ops.factory import _OpFactory

from strpipe.ops.pad import Pad
from strpipe.ops.token_to_index import TokenToIndex
from strpipe.ops.zhchar_tokenizer import ZhCharTokenizer
from strpipe.ops.normalizer import Normalizer
from strpipe.ops.char_tokenizer import CharTokenizer
from strpipe.ops.add_sos_eos import AddSosEos


op_factory = _OpFactory()

op_factory.register('Pad', Pad)
op_factory.register('TokenToIndex', TokenToIndex)
op_factory.register('ZhCharTokenizer', ZhCharTokenizer)
op_factory.register('Normalizer', Normalizer)
op_factory.register('CharTokenizer', CharTokenizer)
op_factory.register('AddSosEos', AddSosEos)
