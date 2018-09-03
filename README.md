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

data = sp.TextData([
    '你好啊\n',
    '早安',
    '你早上好\n',
])

p.fit(data)
result, tx_info = p.transform(data)  # convention: tx => tranform
back_data = p.inverse_transform(result, tx_info)
```

### Serialization
```python
# Save it
p.save_json('/path/of/pipe')

# Load it
p = Pipe.load_json('/path/of/pipe')
result, meta = p.transform(['你好'])
```

## Test

```
$ make test
```
