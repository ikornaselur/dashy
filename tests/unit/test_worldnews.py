import mock
import pytest

from dashy.sources.reddit.worldnews import WorldNews


MOCK_NEWS = [
    (
        54321,
        (
            "Everything You Wanted to Know About LLAMAS "
            "and Were Too Embarrassed to Ask"
        ),
    ),
    (45231, "Should Fixing LLAMAS Take 60 Steps?"),
    (
        35813,
        (
            "Secrets To Getting SHIBA INU To Complete Tasks "
            "Quickly And Efficiently And Correctly"
        ),
    ),
    (
        24913,
        (
            "Why are all the headlines I generated with some online "
            "generator super clickbaity? Click here and find out!"
        ),
    ),
]


@pytest.mark.parametrize("width", range(20, 61, 10))
def test_world_news_max_width(width: int) -> None:
    world_news = WorldNews(6, width)

    with mock.patch.object(world_news, "_get_source", return_value=MOCK_NEWS):
        for row in world_news.get_lines():
            assert len(row) <= width, f"Expected {width} length, got {len(row)}"


def test_world_news_word_wrapping_short() -> None:
    world_news = WorldNews(max_lines=6, max_width=30, max_story_lines=5)

    with mock.patch.object(world_news, "_get_source", return_value=MOCK_NEWS):
        news = list(world_news.get_lines())

    assert news == [
        "54,321 | Everything You Wanted",
        "       | to Know About LLAMAS",
        "       | and Were Too",
        "       | Embarrassed to Ask",
        "45,231 | Should Fixing LLAMAS",
        "       | Take 60 Steps?",
    ]


def test_world_news_word_wrapping_long() -> None:
    world_news = WorldNews(max_lines=8, max_width=60, max_story_lines=5)

    with mock.patch.object(world_news, "_get_source", return_value=MOCK_NEWS):
        news = list(world_news.get_lines())

    assert news == [
        "54,321 | Everything You Wanted to Know About LLAMAS and Were",
        "       | Too Embarrassed to Ask",
        "45,231 | Should Fixing LLAMAS Take 60 Steps?",
        "35,813 | Secrets To Getting SHIBA INU To Complete Tasks",
        "       | Quickly And Efficiently And Correctly",
        "24,913 | Why are all the headlines I generated with some",
        "       | online generator super clickbaity? Click here and",
        "       | find out!",
    ]


def test_world_news_trimming_individual_stories() -> None:
    world_news = WorldNews(max_lines=5, max_width=47, max_story_lines=2)

    with mock.patch.object(world_news, "_get_source", return_value=MOCK_NEWS):
        news = list(world_news.get_lines())

    assert news == [
        "54,321 | Everything You Wanted to Know About",
        # Last line below and fits 47 width
        "       | LLAMAS and Were Too Embarrassed to Ask",
        "45,231 | Should Fixing LLAMAS Take 60 Steps?",
        "35,813 | Secrets To Getting SHIBA INU To",
        # Exactly 47 width, but there are more lines, so
        # the last word is cut off and replaced with ..
        "       | Complete Tasks Quickly And..",
    ]
