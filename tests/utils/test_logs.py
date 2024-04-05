from blackneedles.utils.logs import replace_repeated_lines


def test_replace_log_lines():
    old_log = [
        "installing operating system",
        "installing necessary packages",
        "fetching framework",
        "starting app",
        "loading caches",
        "adding middlewared",
        "pre-fetching necessary files",
        "listening on port 8080",
        "application is ready",
    ]

    log = [
        "starting app",
        "loading caches",
        "adding middlewared",
        "pre-fetching necessary files",
        "listening on port 8080",
        "application is ready",
        "receiving request #1",
        "receiving request #2",
        "receiving request #3",
    ]

    assert replace_repeated_lines(log, old_log) == [
        "receiving request #1",
        "receiving request #2",
        "receiving request #3",
    ]


def test_same_log():
    old_log = [
        "installing operating system",
        "installing necessary packages",
        "fetching framework",
        "starting app",
        "loading caches",
        "adding middlewared",
        "pre-fetching necessary files",
        "listening on port 8080",
        "application is ready",
    ]
    assert replace_repeated_lines(old_log, old_log) == []
