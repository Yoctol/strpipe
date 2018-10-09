from collections import namedtuple


TransformResult = namedtuple('TransformResult', ['output', 'tx_info', 'intermediate'])
PipeRegressionCase = namedtuple('PipeRegressionCase', ['input', 'output'])
