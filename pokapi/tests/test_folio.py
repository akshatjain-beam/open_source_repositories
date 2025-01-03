#!/usr/bin/env python3

from   os.path import dirname, join, abspath, exists
import pytest
import sys
import warnings
import uritemplate
import unittest

this_dir = dirname(abspath(__file__))
sys.path.append(join(this_dir, '..'))

data_dir = join(this_dir, 'data')

from pokapi import Folio, FolioRecord
from pokapi.folio import pub_authors

# In the tests that follow, we don't contact a live Folio server because we
# would have to hardwire a specific server's credentials in here (e.g.,
# Caltech), which would be bad.  So instead, we will saved JSON files in the
# calls, and create a Folio object with fake credential values.

folio = Folio(okapi_url     = "unused url",
              okapi_token   = "unused token",
              tenant_id     = "unused tenant id",
              an_prefix     = 'clc')

# Right, then, let's get on with testing.

def test_folio_field_empty_value():
    r = folio.record(barcode = "")
    assert r == FolioRecord()


def test_saved_json_barcode1():
    with open(join(data_dir, 'barcode-35047019077817.json'), 'r') as f:
        raw_json = f.read()
    r = folio.record(raw_json = raw_json)
    assert r.accession_number == "clc.4f114d62.90b8.4b2b.befb.5d81be6963cc"
    assert r.id               == "4f114d62-90b8-4b2b-befb-5d81be6963cc"
    assert r.title            == "Marbles : mania, depression, Michelangelo, and me : a graphic memoir"
    assert r.author           == "Ellen Forney"
    assert r.edition          == ""
    assert r.publisher        == "Gotham Books"
    assert r.isbn_issn        == "9781592407323"


def test_saved_json_barcode2():
    with open(join(data_dir, 'barcode-35047015251580.json'), 'r') as f:
        raw_json = f.read()
    r = folio.record(raw_json = raw_json)
    assert r.accession_number == "clc.ada3b101.eb41.40ed.b553.4467da58245e"
    assert r.id               == "ada3b101-eb41-40ed-b553-4467da58245e"
    assert r.title            == "Spacetime physics : introduction to special relativity"
    assert r.author           == "Edwin F. Taylor, John Archibald Wheeler"
    assert r.edition          == "2nd ed"
    assert r.publisher        == "W.H. Freeman"
    assert r.isbn_issn        == "0716723271"
    assert r.year             == "1992"


def test_saved_json_barcode3():
    with open(join(data_dir, 'barcode-35047019547967.json'), 'r') as f:
        raw_json = f.read()
    r = folio.record(raw_json = raw_json)
    assert r.accession_number == "clc.6b2826e0.e5b2.406e.9b95.398418136fbd"
    assert r.id               == "6b2826e0-e5b2-406e-9b95-398418136fbd"
    assert r.title            == "Principles of neural science"
    assert r.author           == "Eric R. Kandel ... [et al.] ; art editor, Sarah Mack"
    assert r.edition          == "5th ed"
    assert r.publisher        == "McGraw-Hill"
    assert r.isbn_issn        == "0071390111"
    assert r.year             == "2013"


def test_saved_json_barcode4():
    with open(join(data_dir, 'barcode-35047019621192.json'), 'r') as f:
        raw_json = f.read()
    r = folio.record(raw_json = raw_json)
    assert r.accession_number == "clc.a56d6be1.3e59.4133.9228.515fb2dead2d"
    assert r.id               == "a56d6be1-3e59-4133-9228-515fb2dead2d"
    assert r.title            == "Principles of cognitive neuroscience"
    assert r.author           == "Dale Purves ... [et al.]"
    assert r.edition          == "2nd ed"
    assert r.publisher        == "Sinauer Associates"
    assert r.isbn_issn        == "0878935738"
    assert r.year             == "2013"


def test_saved_json_an1():
    with open(join(data_dir, 'instanceid-a6a62669-6d1a-4e90-b9e0-2a029505b2ad.json'), 'r') as f:
        raw_json = f.read()
    r = folio.record(raw_json = raw_json)
    assert r.accession_number == "clc.a6a62669.6d1a.4e90.b9e0.2a029505b2ad"
    assert r.id               == "a6a62669-6d1a-4e90-b9e0-2a029505b2ad"
    assert r.title            == "Investments"
    assert r.author           == "Zvi Bodie, Boston University, Alex Kane, University of California, San Diego, Alan J. Marcus, Boston College"
    assert r.edition          == "Eleventh edition"
    assert r.publisher        == "McGraw-Hill Education"
    assert r.isbn_issn        == "9781259277177"
    assert r.year             == "2018"


def test_raw_json_field():
    with open(join(data_dir, 'instanceid-a6a62669-6d1a-4e90-b9e0-2a029505b2ad.json'), 'r') as f:
        raw_json = f.read()
    r1 = folio.record(raw_json = raw_json)
    r2 = folio.record(raw_json = r1._raw_data)
    assert r1 == r2


import unittest
from pokapi.folio import cleaned
class TestCleanedFunction(unittest.TestCase):
    
    def test_cleaned_with_normal_text(self):
        """Test with normal text."""
        self.assertEqual(cleaned("  Hello World!  "), "Hello World!")

    def test_cleaned_with_trailing_periods(self):
        """Test with trailing periods."""
        self.assertEqual(cleaned("File name..."), "File name")
    
    def test_cleaned_with_trailing_slashes(self):
        """Test with trailing slashes."""
        self.assertEqual(cleaned("path/to/directory//"), "path/to/directory")
    
    
    def test_cleaned_with_only_spaces(self):
        """Test with a string that only has spaces."""
        self.assertEqual(cleaned("    "), "")
    
    def test_cleaned_with_empty_string(self):
        """Test with an empty string."""
        self.assertEqual(cleaned(""), "")
    
    def test_cleaned_with_none(self):
        """Test with None as input."""
        self.assertEqual(cleaned(None), None)

    def test_cleaned_with_text_with_no_trailing_chars(self):
        """Test with text that has no trailing characters."""
        self.assertEqual(cleaned("No trailing characters"), "No trailing characters")

if __name__ == "__main__":
    unittest.main()
import regex
import unittest

class TestExtractedName(unittest.TestCase):
    """Unit tests for the pub_authors function to validate author name extraction and formatting."""
    
    def test_single_primary_author(self):
        """Test that a single primary author returns correctly without modifications."""
        result = pub_authors([{'name': 'Alice Wonderland', 'primary': True}])
        self.assertEqual(result, 'Alice Wonderland')

    def test_single_primary_author_with_hyphens(self):
        """Test that a single primary author with hyphens is returned correctly after stripping whitespace."""
        result = pub_authors([{'name': '   Emily - A.  ', 'primary': True}])
        self.assertEqual(result, 'Emily - A.')

    def test_invalid_name(self):
        """Test that an invalid name returns correctly (in this case, a name in Chinese)."""
        result = pub_authors([{'name': '王小明', 'primary': True}])
        self.assertEqual(result, '王小明')

    def test_only_spaces(self):
        """Test that a name with only spaces returns an empty string."""
        result = pub_authors([{'name': '    ', 'primary': True}])
        self.assertEqual(result, '')

    def test_chinese_name(self):
        """Test that a valid Chinese name is returned correctly after stripping whitespace."""
        result = pub_authors([{'name': '  张伟  ', 'primary': True}])
        self.assertEqual(result, '张伟')

    def test_spanish_name(self):
        """Test that a valid Spanish name is returned correctly after stripping whitespace."""
        result = pub_authors([{'name': '  Juan Carlos  ', 'primary': True}])
        self.assertEqual(result, 'Juan Carlos')

    def test_french_name(self):
        """Test that a valid French name is returned correctly after stripping whitespace."""
        result = pub_authors([{'name': '  Marie Curie  ', 'primary': True}])
        self.assertEqual(result, 'Marie Curie')

    def test_russian_name(self):
        """Test that a valid Russian name is returned correctly after stripping whitespace."""
        result = pub_authors([{'name': '  Анна Каренина  ', 'primary': True}])
        self.assertEqual(result, 'Анна Каренина')

    def test_arabic_name(self):
        """Test that a valid Arabic name is returned correctly after stripping whitespace."""
        result = pub_authors([{'name': '  أحمد  ', 'primary': True}])
        self.assertEqual(result, 'أحمد')
