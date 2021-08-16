import mock
import pytest

from dashy.sources.reddit.worldnews import get_top_news


MOCK_NEWS = [
    (
        54321,
        (
            "Everything You Wanted to Know About LLAMAS "
            "and Were Too Embarrassed to Ask"
        ),
    ),
    (45231, "Should Fixing LLAMAS Take 60 Steps?"),
    (35813, "Secrets To Getting SHIBA INU To Complete Tasks Quickly And Efficiently"),
    (
        24913,
        (
            "Why are all the headlines I generated with some online "
            "generator super clickbaity? Click here and find out!"
        ),
    ),
]


@pytest.mark.parametrize("width", range(20, 61, 10))
def test_top_news_max_width(width: int) -> None:
    with mock.patch(
        "dashy.sources.reddit.worldnews._get_source", return_value=MOCK_NEWS
    ):
        for row in get_top_news(width):
            assert len(row) <= width, f"Expected {width} length, got {len(row)}"


def test_top_news_word_wrapping_short() -> None:
    with mock.patch(
        "dashy.sources.reddit.worldnews._get_source", return_value=MOCK_NEWS[:2]
    ):
        news = list(get_top_news(30))

    assert news == [
        "54,321 | Everything You Wanted",
        "       | to Know About LLAMAS",
        "       | and Were Too",
        "       | Embarrassed to Ask",
        "45,231 | Should Fixing LLAMAS",
        "       | Take 60 Steps?",
    ]


def test_top_news_word_wrapping_long() -> None:
    with mock.patch(
        "dashy.sources.reddit.worldnews._get_source", return_value=MOCK_NEWS
    ):
        news = list(get_top_news(60))

    assert news == [
        "54,321 | Everything You Wanted to Know About LLAMAS and Were",
        "       | Too Embarrassed to Ask",
        "45,231 | Should Fixing LLAMAS Take 60 Steps?",
        "35,813 | Secrets To Getting SHIBA INU To Complete Tasks",
        "       | Quickly And Efficiently",
        "24,913 | Why are all the headlines I generated with some",
        "       | online generator super clickbaity? Click here and",
        "       | find out!",
    ]
