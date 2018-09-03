import pytest

from strpipe.ops.factory import _OpFactory


class FakeOp:
    pass


def test_factory_register():
    factory = _OpFactory()
    factory.register('Fake', FakeOp)
    assert 'Fake' in factory._factory
    assert factory['Fake'] == FakeOp

    with pytest.raises(KeyError):
        factory['WrongName']


def test_factory_register_same_op_name():
    factory = _OpFactory()
    factory.register('Fake', FakeOp)
    with pytest.raises(KeyError):
        factory.register('Fake', FakeOp)
