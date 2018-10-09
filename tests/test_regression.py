import os

from tests.utils import TransformResult, PipeRegressionCase

from strpipe import Pipe

TESTS_FOLDER = os.path.dirname(os.path.abspath(__file__))
SERIALIZED_PIPES_FOLDER = os.path.join(TESTS_FOLDER, 'serialized_pipes')

PATH_KEY = 'PATH_KEY'
TRANSFORM_CASES_KEY = 'TRANSFORM_CASES_KEY'
INVERSE_TRANSFORM_CASES_KEY = 'INVERSE_TRANSFORM_CASES_KEY'

REGRESSION_SUITES = [
    {
        PATH_KEY: 'pad.json',
        TRANSFORM_CASES_KEY: [
            PipeRegressionCase(
                input=[['a', 'b'], ['c'], ['d', 'e', 'f']],
                output=TransformResult(
                    output=[['a', 'b'], ['c', '<PAD>'], ['d', 'e']],
                    tx_info=[
                        [
                            {'sentlen': 2, 'sentence_tail': []},
                            {'sentlen': 1, 'sentence_tail': []},
                            {'sentlen': 3, 'sentence_tail': ['f']},
                        ],
                    ],
                    intermediate=[],
                ),
            )
        ],
        INVERSE_TRANSFORM_CASES_KEY: [
            PipeRegressionCase(
                input=TransformResult(
                    output=[['a', 'b'], ['c', '<PAD>'], ['d', 'e']],
                    tx_info=[
                        [
                            {'sentlen': 2, 'sentence_tail': []},
                            {'sentlen': 1, 'sentence_tail': []},
                            {'sentlen': 3, 'sentence_tail': ['f']},
                        ],
                    ],
                    intermediate=[],
                ),
                output=[['a', 'b'], ['c'], ['d', 'e', 'f']],
            )
        ],
    },
]


def _get_serialized_pipe_path(path):
    return os.path.join(SERIALIZED_PIPES_FOLDER, path)


def test_regression_all_suites():
    for suite in REGRESSION_SUITES:
        p = Pipe.restore_from_json(_get_serialized_pipe_path(suite[PATH_KEY]))

        for case in suite[TRANSFORM_CASES_KEY]:
            actual_output, actual_tx_info, actual_interm = p.transform(case.input)
            assert actual_output == case.output.output
            assert actual_tx_info == case.output.tx_info
            assert actual_interm == case.output.intermediate

        for case in suite[INVERSE_TRANSFORM_CASES_KEY]:
            actual_output = p.inverse_transform(
                case.input.output, case.input.tx_info)
            assert actual_output == case.output
