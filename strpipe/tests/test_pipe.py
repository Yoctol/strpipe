from unittest.mock import MagicMock, Mock

import pytest

from strpipe.pipe import Pipe
from strpipe.ops import _OpFactory, op_factory as default_op_factory
from strpipe.data import STRING, STRING_LIST


class FakeStatefulOp:

    input_type = STRING
    output_type = STRING

    @staticmethod
    def fit(data):
        return 'SOME_STATE'

    @staticmethod
    def transform(state, data):
        return data, {'a': 1}

    @staticmethod
    def inverse_transfrom(state, data, meta):
        return data


class FakeStatelessOp:

    input_type = STRING
    output_type = STRING_LIST

    @staticmethod
    def fit(data):
        return None

    @staticmethod
    def transform(state, data):
        return data, {'b': 2}

    @staticmethod
    def inverse_transfrom(state, data, meta):
        return data


@pytest.fixture
def fake_factory():
    test_factory = _OpFactory()
    test_factory.register('StatefulOp',  # noqa: E128
        FakeStatefulOp,
    )
    test_factory.register('StatelessOp',  # noqa: E128
        FakeStatelessOp,
    )
    return test_factory


def test_pipe_init_use_correct_factory(fake_factory):
    p = Pipe()
    assert p.op_factory == default_op_factory
    p_custom = Pipe(op_factory=fake_factory)
    assert p_custom.op_factory == fake_factory


def test_add_step_by_op_name_correctly_create_op(mocker):
    MockOp = Mock()
    mock_op_name = 'MockOp'
    mock_factory = _OpFactory()
    mock_factory.register(mock_op_name,  # noqa: E128
        MockOp
    )
    p = Pipe(op_factory=mock_factory)

    p.add_steps_by_op_name(mock_op_name)
    MockOp.assert_called_once_with(**{})


def test_add_step_by_op_name_correctly_create_op_with_kwargs(mocker):
    MockOp = Mock()
    mock_op_name = 'MockOp'
    mock_factory = _OpFactory()
    mock_factory.register(mock_op_name,  # noqa: E128
        MockOp,
    )
    expected_kwargs = {'a': 1, '2': 'b'}
    p = Pipe(op_factory=mock_factory)

    p.add_steps_by_op_name(
        mock_op_name,
        op_kwargs=expected_kwargs,
    )
    MockOp.assert_called_once_with(**expected_kwargs)


def test_add_step_by_op_name_raise_if_type_wrong():
    mock_op_1 = MagicMock(inpur_type=STRING, output_type=STRING)
    mock_op_2 = MagicMock(inpur_type=STRING_LIST, output_type=STRING)
    MockOp1 = Mock(return_value=mock_op_1)
    MockOp2 = Mock(return_value=mock_op_2)

    mock_factory = _OpFactory()
    mock_factory.register('MockOp1',  # noqa: E128
        MockOp1,
    )
    mock_factory.register('MockOp2',  # noqa: E128
        MockOp2,
    )
    p = Pipe(op_factory=mock_factory)

    p.add_steps_by_op_name('MockOp1')
    with pytest.raises(TypeError):
        p.add_steps_by_op_name('MockOp2')
