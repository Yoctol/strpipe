from collections import namedtuple


TransformResult = namedtuple('TransformResult', ['output', 'tx_info'])
PipeRegressionCase = namedtuple('PipeRegressionCase', ['input', 'output'])
