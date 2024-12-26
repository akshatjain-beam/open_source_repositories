import unittest
from pokapi.record import FolioRecord

class TestFolioRecord(unittest.TestCase):

    def test_repr_all_fields_present(self):
        """Test __repr__ when all fields are present."""
        record = FolioRecord(
            id="123",
            accession_number="A001",
            title="The Great Book",
            author="John Doe",
            publisher="Big Publisher",
            edition="First",
            year="2020",
            isbn_issn="123-456-789"
        )
        expected_repr = (
            'FolioRecord(accession_number="A001", author="John Doe", edition="First", id="123", isbn_issn="123-456-789", publisher="Big Publisher", title="The Great Book", year="2020")'
        )
        self.assertEqual(repr(record), expected_repr)

    def test_repr_some_fields_missing(self):
        """Test __repr__ when some fields are missing."""
        record = FolioRecord(
            id="123",
            accession_number="A001",
            title="The Great Book",
            publisher="Big Publisher",
            year="2020"
        )
        expected_repr = (
            'FolioRecord(accession_number="A001", author="", edition="", id="123", isbn_issn="", publisher="Big Publisher", title="The Great Book", year="2020")'
        )
        self.assertEqual(repr(record), expected_repr)

    def test_repr_empty_fields(self):
        """Test __repr__ when fields are explicitly set to empty strings."""
        record = FolioRecord(
            id="123",
            accession_number="A001",
            title="The Great Book",
            author="",
            publisher="Big Publisher",
            edition="None",
            year="2020",
            isbn_issn=""
        )
        expected_repr = (
            'FolioRecord(accession_number="A001", author="", edition="None", id="123", isbn_issn="", publisher="Big Publisher", title="The Great Book", year="2020")'
        )
        self.assertEqual(repr(record), expected_repr)

    def test_repr_empty_instance(self):
        """Test __repr__ when creating an empty instance."""
        record = FolioRecord()
        expected_repr = (
            'FolioRecord(accession_number="", author="", edition="", id="", isbn_issn="", publisher="", title="", year="")'
        )
        self.assertEqual(repr(record), expected_repr)
    
    def test_repr_some_fields_none(self):
        """Test __repr__ when some fields are None."""
        record = FolioRecord(
            id=None,
            accession_number="A001",
            title=None,
            author="John Doe",
            publisher=None,
            edition="First",
            year="2020",
            isbn_issn=None
        )
        expected_repr = (
            'FolioRecord(accession_number="A001", author="John Doe", edition="First", id="None", isbn_issn="None", publisher="None", title="None", year="2020")'
        )
        self.assertEqual(repr(record), expected_repr)

if __name__ == '__main__':
    unittest.main()
