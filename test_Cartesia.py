import re


def normalize_string(text: str) -> str:
    without_punctuation = re.sub(r"[.,!$%:@?}{=\-_`~()']", "", text)
    return re.sub(r"\s{2,}", " ", without_punctuation)


def test_normalize_removes_punctuation():
    assert normalize_string("Hello, world!") == "Hello world"


def test_normalize_collapses_multiple_spaces():
    assert normalize_string("Hello    world") == "Hello world"


def test_normalize_handles_both():
    assert normalize_string("Hi!!  there,  friend.") == "Hi there friend"
