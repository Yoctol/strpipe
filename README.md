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
p.add_step(sp.Step('Lower'))
p.add_step(sp.Step('JiebaTokenize'))

data = TextData([
    '你好啊',
    '早安',
    '',
])
p.fit(data)
p.transform()
p.inverse_transform()
```

### Serialization
```python
# Save it
p.save('/path/of/pipe')

# Load it
p = Pipe.load('/path/of/pipe')
result, meta = p.transform(['你好'])
```

## Test

```
$ make test
```
