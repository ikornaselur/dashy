import mock
import pytest

from dashy.sources.reddit import TopPosts

MOCK_NEWS = [
    (
        154321,
        (
            "Everything You Wanted to Know About LLAMAS "
            "and Were Too Embarrassed to Ask"
        ),
        10,
    ),
    (45231, "Should Fixing LLAMAS Take 60 Steps?", 15),
    (
        35813,
        (
            "Secrets To Getting SHIBA INU To Complete Tasks "
            "Quickly And Efficiently And Correctly"
        ),
        7,
    ),
    (
        24913,
        (
            "Why are all the headlines I generated with some online "
            "generator super clickbaity? Click here and find out!"
        ),
        22,
    ),
]


@pytest.mark.parametrize("width", range(20, 61, 10))
def test_world_news_max_width(width: int) -> None:
    world_news = TopPosts(6, width, subreddit="")

    with mock.patch.object(world_news, "_get_source", return_value=MOCK_NEWS):
        for row in world_news.get_lines():
            assert len(row) <= width, f"Expected {width} length, got {len(row)}"


def test_world_news_word_wrapping_short() -> None:
    world_news = TopPosts(max_lines=6, max_width=28, max_story_lines=5, subreddit="")

    with mock.patch.object(world_news, "_get_source", return_value=MOCK_NEWS):
        news = list(world_news.get_lines())

    assert news == [
        "154k ┬ Everything You Wanted",
        " 10h │ to Know About LLAMAS",
        "     │ and Were Too",
        "     ┴ Embarrassed to Ask",
        " 45k ┬ Should Fixing LLAMAS",
        " 15h ┴ Take 60 Steps?",
    ]


def test_world_news_word_wrapping_long() -> None:
    world_news = TopPosts(max_lines=8, max_width=60, max_story_lines=5, subreddit="")

    with mock.patch.object(world_news, "_get_source", return_value=MOCK_NEWS):
        news = list(world_news.get_lines())

    assert news == [
        "154k ┬ Everything You Wanted to Know About LLAMAS and Were",
        " 10h ┴ Too Embarrassed to Ask",
        " 45k ┬ Should Fixing LLAMAS Take 60 Steps?",
        " 36k ┬ Secrets To Getting SHIBA INU To Complete Tasks",
        "  7h ┴ Quickly And Efficiently And Correctly",
        " 25k ┬ Why are all the headlines I generated with some",
        " 22h │ online generator super clickbaity? Click here and",
        "     ┴ find out!",
    ]


def test_world_news_trimming_individual_stories() -> None:
    world_news = TopPosts(max_lines=5, max_width=45, max_story_lines=2, subreddit="")

    with mock.patch.object(world_news, "_get_source", return_value=MOCK_NEWS):
        news = list(world_news.get_lines())

    assert news == [
        "154k ┬ Everything You Wanted to Know About",
        # Last line below and fits 47 width
        " 10h ┴ LLAMAS and Were Too Embarrassed to Ask",
        " 45k ┬ Should Fixing LLAMAS Take 60 Steps?",
        " 36k ┬ Secrets To Getting SHIBA INU To",
        # Exactly 47 width, but there are more lines, so
        # the last word is cut off and replaced with ..
        "  7h ┴ Complete Tasks Quickly And..",
    ]
