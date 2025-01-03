import pytest

from dfmt import reformat, split_regions, get_prefix


def test_get_prefix():
    """
    Test if the correct prefix is identified from various types of lines.
    """
    assert get_prefix("# ") == "# "
    assert get_prefix(" * ") == " * "
    assert get_prefix(" > ") == " > "
    assert get_prefix(">> ") == ">> "


class TestRegions:
    @staticmethod
    def test_one_line():
        """
        Test that a single line without any prefix is correctly identified as a single region.
        """
        text = "hello"
        regions = split_regions(text)
        assert len(regions) == 1
        actual = regions[0]
        assert actual.prefix == ""
        assert actual.text == "hello\n"

    @staticmethod
    def test_two_lines():
        """
        Test that two lines without any prefix are correctly identified as a single region.
        """
        text = "hello\nworld"
        regions = split_regions(text)
        assert len(regions) == 1
        actual = regions[0]
        assert actual.prefix == ""
        assert actual.text == "hello\nworld\n"

    @staticmethod
    def test_one_indented_paragraph():
        """
        Test that an indented paragraph is correctly identified with its prefix.
        """
        text = """\
  hello
  world
"""
        regions = split_regions(text)
        assert len(regions) == 1
        actual = regions[0]
        assert actual.prefix == "  "
        assert actual.text == "  hello\n  world\n"

    @staticmethod
    def test_two_indented_paragraphs():
        """
        Test that two separate indented paragraphs are correctly identified as separate regions.
        """
        text = """\
  hello
  world

  goodbye
  world
"""
        regions = split_regions(text)
        one, two, three = regions
        assert two.prefix == ""
        assert two.text == "\n"

    @staticmethod
    def test_two_paragraphs_in_pound_comment():
        """
        Test that two separate paragraphs in pound comments are correctly identified as separate regions.
        """
        text = """\
  # this is the
  # first paragraph
  #
  # this is the
  # second paragraph
"""
        regions = split_regions(text)
        one, two, three = regions
        assert two.prefix == "  "
        assert two.text == "  #\n"


def test_empty_selection():
    """
    Test reformatting of an empty string should return a newline.
    """
    assert reformat("") == "\n"


def test_empty_line():
    """
    Test reformatting of a single empty line should return a newline.
    """
    assert reformat("\n") == "\n"


def test_blank_line():
    """
    Test reformatting of a line with spaces only should return a newline.
    """
    assert reformat("   \n") == "\n"


def test_keep_small_lines():
    """
    Test that lines shorter than the specified width are not wrapped.
    """
    assert reformat("this is small", width=20) == "this is small\n"


def test_keep_long_words():
    """
    Test that long words that exceed the specified width are not broken.
    """
    assert (
        reformat(
            "this is a very big url: https://a.very.long.domain.tld/a/very/long/path",
            width=40,
        )
        == "this is a very big url:\nhttps://a.very.long.domain.tld/a/very/long/path\n"
    )


def test_into_two_lines():
    """
    Test that a short string is wrapped into two lines given a small width.
    """
    assert reformat("aaa bbb", width=3) == "aaa\nbbb\n"


def test_into_three_lines():
    """
    Test that a string is wrapped into three lines given a small width.
    """
    assert reformat("aaa bb ccc", width=3) == "aaa\nbb\nccc\n"


def test_long_sentence():
    """
    Test wrapping a long sentence into multiple lines based on the specified width.
    """
    assert (
        reformat("this is a pretty big sentence in two pretty big parts", width=12)
        == "this is a\npretty big\nsentence in\ntwo pretty\nbig parts\n"
    )


def test_pound_comment_1_to_2():
    """
    Test wrapping a pound comment into multiple lines based on the specified width.
    """
    assert (
        reformat("# this is a pretty big comment, isn't it?", width=20)
        == "# this is a pretty\n# big comment, isn't\n# it?\n"
    )


def test_pound_comment_2_to_3():
    """
    Test wrapping a pound comment into three lines based on the specified width.
    """
    text = """\
# aaa bbb
# ccc
"""
    expected = """\
# aaa
# bbb
# ccc
"""
    actual = reformat(text, width=5)
    if actual != expected:
        pytest.fail(actual)


def test_doxygen():
    """
    Test wrapping a doxygen comment into multiple lines based on the specified width.
    """
    text = """\
 * this is a pretty big line in a doxygen comment
"""
    expected = """\
 * this is a pretty
 * big line in a
 * doxygen comment
"""
    actual = reformat(text, width=20)
    if actual != expected:
        pytest.fail(actual)


def test_preserve_leading_indent():
    """
    Test that leading indent is preserved when wrapping lines.
    """
    text = " aaa bbb"
    assert reformat(text, width=4) == " aaa\n bbb\n"


def test_indented_pound_comment():
    """
    Test wrapping an indented pound comment into multiple lines based on the specified width.
    """
    text = """\
    # this is a pretty big line in a Python comment that is indented
"""
    expected = """\
    # this is a pretty big line in a
    # Python comment that is indented
"""
    actual = reformat(text, width=40)
    if actual != expected:
        pytest.fail(actual)


def test_pound_paragraphs():
    """
    Test wrapping multiple paragraphs of pound comments, ensuring blank lines are preserved.
    """
    text = """\
    # this is a pretty big line in a Python comment that is indented
    #
    # and this is a second big line in a Python comment that is indented
"""
    expected = """\
    # this is a pretty big line in a
    # Python comment that is indented
    #
    # and this is a second big line in a
    # Python comment that is indented
"""
    actual = reformat(text, width=40)
    if actual != expected:
        pytest.fail(actual)


def test_empty_line_between_regions():
    """
    Test that an empty line between regions is preserved after reformatting.
    """
    text = """\
# first line

# second line
"""
    expected = """\
# first line

# second line
"""
    actual = reformat(text, width=20)
    if actual != expected:
        pytest.fail(actual)


def test_quoting_simple():
    """
    Test wrapping a simple quoted line into multiple lines based on the specified width.
    """
    text = """\
> Inline comment by a third party which wraps onto multiple lines
"""
    expected = """\
> Inline comment by a third
> party which wraps onto
> multiple lines
"""
    actual = reformat(text, width=30)
    if actual != expected:
        pytest.fail(actual)


def test_quoting_nested():
    """
    Test wrapping nested quoted lines into multiple lines based on the specified width.
    """
    text = """\
> Inline commentary by a third party which also wraps onto multiple lines

> > Some kind of very long text that's being quoted by somebody else.
"""

    expected = """\
> Inline commentary by a third party which also
> wraps onto multiple lines

> > Some kind of very long text that's being
> > quoted by somebody else.
"""
    actual = reformat(text, width=50)
    if actual != expected:
        pytest.fail(actual)
