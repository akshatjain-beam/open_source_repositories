#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `socials` package."""

import pytest

from click.testing import CliRunner

import socials
from socials import cli


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert 'socials.cli.main' in result.output
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert '--help  Show this message and exit.' in help_result.output


def test_extract():
    """Test the extract method."""
    urls = [
        'http://google.de',
        'http://facebook.com',
        'http://facebook.com/peterparker',
        'http://facebook.com/peter_parker',
        'http://facebook.com/peter[parker',  # Invalid character
        'https://www.facebook.com/profile.php?id=4',
        'mailto:bill@microsoft.com',
        'steve@microsoft.com',
        'https://www.linkedin.com/company/google/',
        'https://www.linkedin.com/comp^any/google/',  # Invalid character
        'http://www.twitter.com/Some_Company/',
        'http://www.twitter.com/Some_\\Company',  # Invalid character
        'https://www.instagram.com/instagram/',
        'https://www.instagram.com/instag-ram/',  # Invalid character
        'http://instagr.am/instagram',
        'http://youtube.com/this/is/too/long',
        'http://www.youtube.com/user/Some_1',
        'http://youtube.com/c/your-custom-name',
        'http://youtube.com/your.custom.name',
    ]
    extraction = socials.extract(urls)
    matches = extraction.get_matches_per_platform()
    assert 'facebook' in matches
    assert len(matches['facebook']) == 3
    assert 'http://facebook.com/peterparker' in matches['facebook']
    assert 'http://facebook.com/peter_parker' in matches['facebook']
    assert 'https://www.facebook.com/profile.php?id=4' in matches['facebook']

    assert 'email' in matches
    assert len(matches['email']) == 2
    assert 'bill@microsoft.com' in matches['email']
    assert 'steve@microsoft.com' in matches['email']

    assert 'linkedin' in matches
    assert len(matches['linkedin']) == 1
    assert 'https://www.linkedin.com/company/google/' in matches['linkedin']

    assert 'twitter' in matches
    assert len(matches['twitter']) == 1
    assert 'http://www.twitter.com/Some_Company/' in matches['twitter']

    assert 'instagram' in matches
    assert len(matches['instagram']) == 2
    assert 'https://www.instagram.com/instagram/' in matches['instagram']
    assert 'http://instagr.am/instagram' in matches['instagram']

    assert 'youtube' in matches
    assert len(matches['youtube']) == 3
    assert 'http://www.youtube.com/user/Some_1' in matches['youtube']
    assert 'http://youtube.com/c/your-custom-name' in matches['youtube']
    assert 'http://youtube.com/your.custom.name' in matches['youtube']


def test_extract_linkedin():
    """Test the extract method."""

    valid_urls = [
        # LinkedIn private profiles (valid)
        'https://www.linkedin.com/in/john-doe',
        'https://linkedin.com/in/jane_doe',
        'https://www.linkedin.com/pub/john-doe/12/34/567/',
        'http://linkedin.com/pub/jane_doe/ab/cd/efg/',
        'http://linkedin.com/pub/jane_doe/ab/cd/ef/',
        'https://www.linkedin.com/in/johndoe123/',
        # LinkedIn company profiles (valid)
        'https://www.linkedin.com/company/microsoft/',
        'http://linkedin.com/company/google',
        'https://www.linkedin.com/company/micro_soft/',
    ]

    invalid_urls = [
        # LinkedIn private profiles (invalid)
        'https://www.linkedin.com/in/john_doe@',  # Invalid character
        'https://linkedin.com/in/jane^doe',  # Invalid character
        'http://linkedin.com/pub/jane_doe/ab/cd/efg/hij/',  # More than 3 segments
        # LinkedIn company profiles (invalid)
        'http://linkedin.com/company/google!',  # Invalid character
        'https://www.linkedin.com/company/microsoft//',  # Double trailing slash
    ]

    urls = valid_urls + invalid_urls

    extraction = socials.extract(urls)
    matches_all = extraction.get_matches_per_platform()

    assert 'linkedin' in matches_all
    matches_linkedin = matches_all['linkedin']

    # Ensure valid LinkedIn URLs are matched
    assert len(matches_linkedin) == 9
    for url in valid_urls:
        assert url in matches_linkedin

def test_extract_facebook():
    """Test the extract method for Facebook URLs."""

    valid_urls = [
        # Facebook profiles (valid)
        'https://www.facebook.com/john_doe',
        'https://www.facebook.com/john-doe',
        'https://www.facebook.com/john.doe',
        'https://facebook.com/johndoe123',
        'https://www.facebook.com/profile.php?id=1234567890',
        'https://facebook.com/profile.php?id=9876543210',
    ]

    invalid_urls = [
        # Facebook profiles (invalid)
        'https://www.facebook.com/john_doe!',  # Invalid character
        'https://facebook.com/john^doe',  # Invalid character
        'https://www.facebook.com/profile.php?id=1234567890&extra=1',  # Extra query parameter
    ]

    urls = valid_urls + invalid_urls

    extraction = socials.extract(urls)
    matches_all = extraction.get_matches_per_platform()
    
    assert 'facebook' in matches_all
    matches_facebook = matches_all['facebook']

    # Ensure valid Facebook URLs are matched
    assert len(matches_facebook) == len(valid_urls)
    for url in valid_urls:
        assert url in matches_facebook
