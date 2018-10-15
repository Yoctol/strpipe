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
p.add_step_by_op_name('ZhCharTokenizer')
p.add_step_by_op_name('AddSosEos')
p.add_checkpoint()
p.add_step_by_op_name('Pad')
p.add_step_by_op_name('TokenToIndex')

data = [
    '你好啊',
    '早安',
    '你早上好',
]

p.fit(data)
result, tx_info, intermediates = p.transform(data)  # convention: tx => tranform
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
