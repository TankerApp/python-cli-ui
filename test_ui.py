import io

import ui

import pytest

RED = "\x1b[31;1m"
GREEN = "\x1b[32;1m"
RESET = "\x1b[0m"
BOLD = "\x1b[1m"
BEGIN_TITLE = "\x1b]0;"
END_TITLE = "\x07"


def assert_equal_strings(a, b):
    return a.split() == b.split()


@pytest.fixture
def smart_tty():
    res = io.StringIO()
    res.isatty = lambda: True
    return res


@pytest.fixture
def dumb_tty():
    res = io.StringIO()
    res.isatty = lambda: True
    return res


def test_info_stdout_is_a_tty(smart_tty):
    ui.info(ui.red, "this is red", ui.reset,
            ui.green, "this is green",
            fileobj=smart_tty)
    expected = (RED + "this is red " + RESET +
                GREEN + "this is green" + RESET + "\n")
    actual = smart_tty.getvalue()
    assert_equal_strings(actual, expected)


def test_update_title(smart_tty):
    ui.info("Something", ui.bold, "bold", fileobj=smart_tty, update_title=True)
    expected = (BEGIN_TITLE + "Something bold" + END_TITLE +
                "Something " + BOLD + "bold" + RESET + "\n")
    actual = smart_tty.getvalue()
    assert_equal_strings(actual, expected)


def test_info_stdout_is_not_a_tty(dumb_tty):
    ui.info(ui.red, "this is red", ui.reset,
            ui.green, "this is green",
            fileobj=dumb_tty)
    expected = "this is red this is green\n"
    actual = dumb_tty.getvalue()
    assert_equal_strings(actual, expected)


def test_info_characters(smart_tty):
    ui.info("Doing stuff", ui.ellipsis, "sucess", ui.check, fileobj=smart_tty)
    actual = smart_tty.getvalue()
    expected = "Doing stuff " + RESET + "…" + " sucess " + GREEN + "✓"
    assert_equal_strings(actual, expected)


def test_record_message(messages):
    ui.info_1("This is foo")
    assert messages.find("foo")
    messages.reset()
    ui.info_1("This is bar")
    assert not messages.find("foo")
