from strpipe.ops.factory import _OpFactory

from strpipe.ops.pad import Pad
from strpipe.ops.token_to_index import TokenToIndexWithUNK

op_factory = _OpFactory()

op_factory.register('Pad', Pad)
op_factory.register('TokenToIndexWithUNK', TokenToIndexWithUNK)
