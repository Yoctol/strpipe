from strpipe.ops.factory import _OpFactory

from strpipe.ops.pad import Pad


op_factory = _OpFactory()

op_factory.register('Pad',
    Pad,
)
