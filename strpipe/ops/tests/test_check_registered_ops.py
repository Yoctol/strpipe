"""Test all registered ops to behave.

- all ops should be able to initialize wo kwargs
- all ops should support fit, transform and inverse_transform
- With the given input type, and output type, the op should work correctly
"""

from strpipe.ops import op_factory
from strpipe.data.types import (
    STRING,
    STRING_LIST,
    INT_LIST,
)


TEST_INPUT_DATA = {
    STRING: [
        'What a beautiful day!',
        'My email is 123@yoctol.com',
    ],
    STRING_LIST: [
        ['what', 'a', 'beautiful', 'day', '!'],
        ['My', 'email', 'is', '123@yoctol.com'],
    ],
    INT_LIST: [
        [1, 3, 5],
        [2, 4, 6, 8],
    ],
}


def test_all_can_be_created_without_kwargs():
    for _Op in op_factory._factory.values():
        op = _Op()
        assert op
        assert hasattr(op, 'input_type')
        assert hasattr(op, 'output_type')


def test_all_has_fit_transform_inverse_transform():
    for _Op in op_factory._factory.values():
        op = _Op()
        assert op
        assert hasattr(op, 'fit')
        assert callable(getattr(op, 'fit'))
        assert hasattr(op, 'transform')
        assert callable(getattr(op, 'transform'))
        assert hasattr(op, 'inverse_transform')
        assert callable(getattr(op, 'inverse_transform'))


def test_all_correctly_processed():
    for _Op in op_factory._factory.values():
        op = _Op()
        input_data = TEST_INPUT_DATA[op.input_type]
        state = op.fit(input_data)
        output_data, meta = op.transform(state, input_data)
        # assert output_data.type = op.output_type
        op.inverse_transform(state, output_data, meta)
        # tx_data = op.inverse_transform(state, output_data, meta)
        # assert tx_data.type == input_data.type

        # TODO: if recoverable, the input and tx should be the same
        # if op.is_recoverable:
        #     assert input_data == tx_data
