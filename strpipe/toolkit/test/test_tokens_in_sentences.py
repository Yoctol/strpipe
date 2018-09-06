from ..tokens_in_sentences import (
    are_tokens_in_sentences,
    is_token_in_sentences,
)


def test_are_tokens_in_sentences():
    output = are_tokens_in_sentences(
        tokens=["蛋白質", "蒼蠅"],
        sentences=[
            ["蔣勤彥", "只吃", "甲殼類"],
            ["不吃", "蒼蠅"],
        ],
    )
    assert output == [False, True]

    output = are_tokens_in_sentences(
        tokens=["蒼蠅", "蔣勤彥"],
        sentences=[
            ["蔣勤彥", "只吃", "甲殼類"],
            ["不吃", "蒼蠅"],
        ],
    )
    assert output == [True, True]


def test_is_token_in_sentences():
    output = is_token_in_sentences(
        token="蛋白質",
        sentences=[
            ["蔣勤彥", "只吃", "甲殼類"],
            ["不吃", "蒼蠅"],
        ],
    )
    assert output is False

    output = is_token_in_sentences(
        token="蒼蠅",
        sentences=[
            ["蔣勤彥", "只吃", "甲殼類"],
            ["不吃", "蒼蠅"],
        ],
    )
    assert output is True
