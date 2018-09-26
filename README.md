# strpipe

[![Build Status](https://travis-ci.org/Yoctol/strpipe.svg?branch=master)](https://travis-ci.org/Yoctol/strpipe) [![PyPI version](https://badge.fury.io/py/strpipe.svg)](https://badge.fury.io/py/strpipe)


Reversible string processing pipe. Featuring reproducibility, serializability and performance.

## Installation

```
pip install strpipe
```

## Usage

```python
import strpipe as sp

p = sp.Pipe()
p.add_step_by_op_name(
    op_name='Trim',
    op_kwargs={'tokens': ['\n', '\r']},
)
p.add_step_by_op_name('CharTokenize')
p.add_step_by_op_name(
    op_name='MapStringToIndex',
    state={'你': 0, '好': 1, '早': 2},  # if provided, the p.fit won't change it
)

data = [
    '你好啊\n',
    '早安',
    '你早上好\n',
]

p.fit(data)
result, tx_info = p.transform(data)  # convention: tx => tranform
back_data = p.inverse_transform(result, tx_info)
```

### Serialization
```python
# Save it
p.save_json('/path/of/pipe')

# Load it
p = sp.Pipe.restore_from_json('/path/of/pipe')
result, meta = p.transform(['你好'])
```

## Test

```
$ make test
```

## Docs

```
$ make docs

Docs will be built in the `docs/build/html` folder. (Note: this also reinstalls the package because we
need Cython code to be rebuilt.)
```

## Extend Ops

1. Extend the new ops with `BaseOp`
2. Define `input_type`, `output_type`
3. Implement op creation
4. Implement fit, transform, inverse_transform. If the op is stateless, the `fit` method should return None.

> Note: It is expected that an ops's functionality will often be able to be decomposed into several functions. These functions should be written into (or imported from) the toolkit package for easy reuse.
Ops in the ops package will, for the most part, be wrappers for functions in toolkit.

5. Write tests
6. Register to `op_factory`
