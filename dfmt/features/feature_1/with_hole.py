import argparse
from dataclasses import dataclass
import re
import sys
import textwrap

SIMPLE_PREFIX_RE = r"""
	(\s*) # Some blanks, then either:
	(
	  \#  # Pound comments
	  |
	  //  # C-style comments
	  |
	  /// # Rust doc comments
	  |
	  //! # Doxygen
	  |
	  \*  # Bullet point (star)
	  |
	  -   # Bullet point (dash)
    )?
	[ \t]   # Exactly one space or tab
"""


BLOCKQUOTE_RE = r"\s*(>\s*)+\s+"

FULL_RE = re.compile(f"{BLOCKQUOTE_RE}|{SIMPLE_PREFIX_RE}", re.VERBOSE)


def get_prefix(text):
    match = FULL_RE.match(text)
    if match is None:
        return ""
    else:
        return match.group()


def is_blank(line):
    return all(x == " " for x in line[:-1])


@dataclass
class Region:
    text: str
    prefix: str


"""
Implement a funcion `split_regions` that splits the input text 
into regions based on line prefixes.

As the function processes each line, it tracks the current prefix. 
When lines share the same prefix, they are combined into a single 
region; otherwise, a new region is created.

Args:
    text (str): The input text

Returns:
    list: A list of Region objects

Note:
    Include the new line for the last line
"""
$PlaceHolder$


def reformat_region(region, *, width):
    text = region.text
    prefix = region.prefix
    if is_blank(text):
        return "\n"
    lines = text.splitlines()
    prefix_length = len(prefix)
    to_wrap = "\n".join(x[prefix_length:] for x in text.splitlines())
    wrapped = textwrap.wrap(
        to_wrap, width=width - prefix_length, break_long_words=False
    )
    res = ""
    for line in wrapped:
        res += prefix + line + "\n"
    return res


def reformat(text, *, width=80):
    if text in ("", "\n"):
        return "\n"
    regions = split_regions(text)
    res = ""
    for region in regions:
        res += reformat_region(region, width=width)
    return res


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-w", "--width", default=80, type=int)
    args = parser.parse_args()
    text = sys.stdin.read()
    wrapped = reformat(text, width=args.width)
    sys.stdout.write(wrapped)