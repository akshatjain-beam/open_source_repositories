'''
record.py: the FolioRecord object class for Pokapi

Authors
-------

Michael Hucka <mhucka@caltech.edu> -- Caltech Library

Copyright
---------

Copyright (c) 2021 by the California Institute of Technology.  This code
is open-source software released under a 3-clause BSD license.  Please see the
file "LICENSE" for more information.
'''

if __debug__:
    from sidetrack import log

from .exceptions import DataMismatchError


# Class definitions.
# .............................................................................

class FolioRecord():
    '''Object class for representing a record returned by FOLIO/Okapi.

    This object is at the level of abstraction corresponding to FOLIO's
    "instance" records. The "id" is the instance id.

    Some field values may be empty strings, depending on the record. For
    example, journals will not have a "year" value, so the value of that field
    will be '' for journals.
    '''

    # The reason for an explicit list of fields here is so that we can use it
    # in the definition of __repr__().
    __fields = {
        'id'               : str,          # id of Folio instance record
        'accession_number' : str,          # accession number
        'title'            : str,          # extracted from instance "title" field
        'author'           : str,          # string concatenated from contributors
        'publisher'        : str,          # publication.publisher
        'edition'          : str,          # editions[0]
        'year'             : str,          # publication.year
        'isbn_issn'        : str,          #
    }


    def __init__(self, **kwargs):
        # Internal variables.  Need to set these first.
        self._raw_data = None

        # Always first initialize every field.
        for field, field_type in self.__fields.items():
            setattr(self, field, ([] if field_type == list else ''))
        # Set values if given arguments.
        for field, value in kwargs.items():
            setattr(self, field, value)

    """
    Create a function `__repr__` that returns a string representation of the FolioRecord instance.

    The representation is formatted with the class name followed by
    each field and its corresponding value in the instance. Fields are sorted alphabetically in the output  
    and their values are formatted as follows:
    - If the value is a list, it is represented as is.
    - If the value is not a list, it is enclosed in double quotes.
    If the attribute does not exist, handle missing attributes by None

    Returns:
        str: A string representation of the FolioRecord instance.
              If an instance has the following values:
        
    Example:    
        - id: '123'
        - accession_number: 'A001'
        - title: 'The Great Book'
        - author: 'John Doe'
        - publisher: 'Big Publisher'
        - edition: 'First'
        - year: '2020'
        - isbn_issn: '123-456-789'

        The output of this method would be:
        'FolioRecord(accession_number="A001", author="John Doe", edition="First",
        id="123", isbn_issn="123-456-789", publisher="Big Publisher",
        title="The Great Book", year="2020")'
    """
    $PlaceHolder$   


    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.__dict__ == other.__dict__
        return NotImplemented


    def __ne__(self, other):
        # Based on lengthy Stack Overflow answer by user "Maggyero" posted on
        # 2018-06-02 at https://stackoverflow.com/a/50661674/743730
        eq = self.__eq__(other)
        if eq is not NotImplemented:
            return not eq
        return NotImplemented


    def __lt__(self, other):
        return self.id < other.id


    def __gt__(self, other):
        if isinstance(other, type(self)):
            return other.id < self.id
        return NotImplemented


    def __le__(self, other):
        if isinstance(other, type(self)):
            return not other.id < self.id
        return NotImplemented


    def __ge__(self, other):
        if isinstance(other, type(self)):
            return not self.id < other.id
        return NotImplemented
