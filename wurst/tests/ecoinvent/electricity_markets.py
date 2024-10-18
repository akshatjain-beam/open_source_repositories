from unittest.mock import Mock
from wurst.ecoinvent.electricity_markets import *


def test_empty_low_voltage_markets():
    given = [
        {
            "exchanges": [
                {
                    "name": "market for transmission network, electricity, low voltage",
                    "unit": "kilowatt hour",
                },
                {
                    "name": "market for sulfur hexafluoride, liquid",
                    "unit": "kilowatt hour",
                },
                {
                    "amount": 0.0096,
                    "name": "market for electricity, low voltage",
                    "type": "technosphere",
                    "unit": "kilowatt hour",
                },
                {
                    "amount": 1.0,
                    "name": "market for electricity, low voltage",
                    "type": "production",
                    "unit": "kilowatt hour",
                },
                {
                    "amount": 0.2,
                    "name": "electricity voltage transformation from medium to low voltage",
                    "unit": "kilowatt hour",
                },
                {
                    "name": "electricity production, photovoltaic, 3kWp slanted-roof installation, a-Si, panel, mounted",
                    "unit": "kilowatt hour",
                },
                {"name": "burnt shale production", "unit": "kilowatt hour"},
                {"name": "petroleum refinery operation", "unit": "kilowatt hour"},
            ],
            "name": "market for electricity, low voltage",
        }
    ]
    expected = [
        {
            "exchanges": [
                {
                    "name": "market for transmission network, electricity, low voltage",
                    "unit": "kilowatt hour",
                },
                {
                    "name": "market for sulfur hexafluoride, liquid",
                    "unit": "kilowatt hour",
                },
                {
                    "amount": 0.0096,
                    "name": "market for electricity, low voltage",
                    "type": "technosphere",
                    "unit": "kilowatt hour",
                },
                {
                    "amount": 1.0,
                    "name": "market for electricity, low voltage",
                    "type": "production",
                    "unit": "kilowatt hour",
                },
                {
                    "amount": 1.0,
                    "name": "electricity voltage transformation from medium to low voltage",
                    "unit": "kilowatt hour",
                },
            ],
            "name": "market for electricity, low voltage",
        }
    ]
    assert empty_low_voltage_markets(given) == expected


def test_empty_medium_voltage_markets():
    given = [
        {
            "exchanges": [
                {
                    "name": "market for transmission network, electricity, medium voltage",
                    "unit": "kilowatt hour",
                },
                {
                    "name": "market for sulfur hexafluoride, liquid",
                    "unit": "kilowatt hour",
                },
                {
                    "amount": 0.0096,
                    "name": "market for electricity, medium voltage",
                    "type": "technosphere",
                    "unit": "kilowatt hour",
                },
                {
                    "amount": 1.0,
                    "name": "market for electricity, medium voltage",
                    "type": "production",
                    "unit": "kilowatt hour",
                },
                {
                    "amount": 0.2,
                    "name": "electricity voltage transformation from high to medium voltage",
                    "unit": "kilowatt hour",
                },
                {
                    "name": "electricity production, photovoltaic, 3kWp slanted-roof installation, a-Si, panel, mounted",
                    "unit": "kilowatt hour",
                },
                {"name": "burnt shale production", "unit": "kilowatt hour"},
                {"name": "petroleum refinery operation", "unit": "kilowatt hour"},
            ],
            "name": "market for electricity, medium voltage",
        }
    ]
    expected = [
        {
            "exchanges": [
                {
                    "name": "market for transmission network, electricity, medium voltage",
                    "unit": "kilowatt hour",
                },
                {
                    "name": "market for sulfur hexafluoride, liquid",
                    "unit": "kilowatt hour",
                },
                {
                    "amount": 0.0096,
                    "name": "market for electricity, medium voltage",
                    "type": "technosphere",
                    "unit": "kilowatt hour",
                },
                {
                    "amount": 1.0,
                    "name": "market for electricity, medium voltage",
                    "type": "production",
                    "unit": "kilowatt hour",
                },
                {
                    "amount": 1.0,
                    "name": "electricity voltage transformation from high to medium voltage",
                    "unit": "kilowatt hour",
                },
            ],
            "name": "market for electricity, medium voltage",
        }
    ]
    assert empty_medium_voltage_markets(given) == expected


def test_empty_high_voltage_markets():
    given = [
        {
            "exchanges": [
                {
                    "name": "market for transmission network, electricity, high voltage",
                    "unit": "kilowatt hour",
                },
                {
                    "name": "market for sulfur hexafluoride, liquid",
                    "unit": "kilowatt hour",
                },
                {
                    "amount": 0.0096,
                    "name": "market for electricity, high voltage",
                    "type": "technosphere",
                    "unit": "kilowatt hour",
                },
                {
                    "amount": 1.0,
                    "name": "market for electricity, high voltage",
                    "type": "production",
                    "unit": "kilowatt hour",
                },
                {
                    "name": "electricity, high voltage, import from CA-AB",
                    "unit": "kilowatt hour",
                },
                {
                    "name": "electricity, high voltage, import from WECC, US only",
                    "unit": "kilowatt hour",
                },
                {
                    "name": "electricity production, photovoltaic, 3kWp slanted-roof installation, a-Si, panel, mounted",
                    "unit": "kilowatt hour",
                },
                {"name": "burnt shale production", "unit": "kilowatt hour"},
                {"name": "petroleum refinery operation", "unit": "kilowatt hour"},
            ],
            "name": "market for electricity, high voltage",
        }
    ]
    expected = [
        {
            "exchanges": [
                {
                    "name": "market for transmission network, electricity, high voltage",
                    "unit": "kilowatt hour",
                },
                {
                    "name": "market for sulfur hexafluoride, liquid",
                    "unit": "kilowatt hour",
                },
                {
                    "amount": 0.0096,
                    "name": "market for electricity, high voltage",
                    "type": "technosphere",
                    "unit": "kilowatt hour",
                },
                {
                    "amount": 1.0,
                    "name": "market for electricity, high voltage",
                    "type": "production",
                    "unit": "kilowatt hour",
                },
            ],
            "name": "market for electricity, high voltage",
        }
    ]
    assert empty_high_voltage_markets(given) == expected


def test_move_all_generation_to_high_voltage():
    given = [
        {
            "location": "CZ",
            "name": "market for electricity, low voltage",
            "unit": "kilowatt hour",
            "exchanges": [
                {
                    "uncertainty type": 0,
                    "loc": 1.0,
                    "amount": 1.0,
                    "type": "production",
                    "name": "market for electricity, low voltage",
                    "unit": "kilowatt hour",
                    "location": "CZ",
                },
                {
                    "amount": 6,
                    "type": "technosphere",
                    "name": "market for sulfur hexafluoride, liquid",
                    "unit": "kilogram",
                    "location": "RER",
                },
                {
                    "uncertainty type": 0,
                    "amount": 0.02,
                    "type": "technosphere",
                    "name": "electricity production, photovoltaic, 3kWp slanted-roof installation, multi-Si, panel, mounted",
                    "unit": "kilowatt hour",
                    "location": "CZ",
                },
                {
                    "uncertainty type": 0,
                    "amount": 0.01,
                    "type": "technosphere",
                    "name": "electricity production, photovoltaic, 3kWp slanted-roof installation, single-Si, panel, mounted",
                    "unit": "kilowatt hour",
                    "location": "CZ",
                },
                {
                    "uncertainty type": 0,
                    "amount": 0.9,
                    "type": "technosphere",
                    "name": "electricity voltage transformation from medium to low voltage",
                    "unit": "kilowatt hour",
                    "location": "CZ",
                },
                {
                    "uncertainty type": 0,
                    "amount": 0.05,
                    "type": "technosphere",
                    "product": "electricity, low voltage",
                    "name": "market for electricity, low voltage",
                    "unit": "kilowatt hour",
                    "location": "CZ",
                },
                {
                    "uncertainty type": 2,
                    "amount": 9,
                    "type": "biosphere",
                    "name": "Sulfur hexafluoride",
                    "unit": "kilogram",
                    "location": None,
                    "categories": ("air",),
                },
            ],
        },
        {
            "location": "CZ",
            "name": "market for electricity, medium voltage",
            "unit": "kilowatt hour",
            "exchanges": [
                {
                    "uncertainty type": 2,
                    "amount": 1.8,
                    "type": "technosphere",
                    "name": "market for transmission network, electricity, medium voltage",
                    "unit": "kilometer",
                    "location": "GLO",
                },
                {
                    "uncertainty type": 0,
                    "amount": 1.0,
                    "type": "production",
                    "product": "electricity, medium voltage",
                    "name": "market for electricity, medium voltage",
                    "unit": "kilowatt hour",
                    "location": "CZ",
                },
                {
                    "uncertainty type": 0,
                    "amount": 0.9,
                    "type": "technosphere",
                    "name": "electricity voltage transformation from high to medium voltage",
                    "unit": "kilowatt hour",
                    "location": "CZ",
                },
                {
                    "uncertainty type": 0,
                    "amount": 0.1,
                    "type": "technosphere",
                    "name": "electricity, from municipal waste incineration to generic market for electricity, medium voltage",
                    "unit": "kilowatt hour",
                    "location": "CZ",
                },
                {
                    "uncertainty type": 0,
                    "amount": 0.1234,
                    "type": "technosphere",
                    "name": "market for electricity, medium voltage",
                    "unit": "kilowatt hour",
                    "location": "CZ",
                },
            ],
        },
        {
            "location": "CZ",
            "name": "market for electricity, high voltage",
            "unit": "kilowatt hour",
            "exchanges": [
                {
                    "uncertainty type": 2,
                    "amount": 3,
                    "type": "technosphere",
                    "name": "market for transmission network, long-distance",
                    "unit": "kilometer",
                    "location": "GLO",
                },
                {
                    "uncertainty type": 0,
                    "loc": 1.0,
                    "amount": 1.0,
                    "type": "production",
                    "name": "market for electricity, high voltage",
                    "unit": "kilowatt hour",
                    "location": "CZ",
                },
                {
                    "uncertainty type": 0,
                    "amount": 0.4,
                    "type": "technosphere",
                    "name": "electricity production, hard coal",
                    "unit": "kilowatt hour",
                    "location": "CZ",
                },
                {
                    "uncertainty type": 0,
                    "amount": 0.3,
                    "type": "technosphere",
                    "name": "electricity production, wind, 1-3MW turbine, onshore",
                    "unit": "kilowatt hour",
                    "location": "CZ",
                },
                {
                    "uncertainty type": 0,
                    "amount": 0.05,
                    "type": "technosphere",
                    "name": "electricity, high voltage, import from AT",
                    "unit": "kilowatt hour",
                    "location": "CZ",
                },
                {
                    "uncertainty type": 0,
                    "amount": 0.05,
                    "type": "technosphere",
                    "name": "electricity, high voltage, import from DE",
                    "unit": "kilowatt hour",
                    "location": "CZ",
                },
            ],
        },
    ]
    expected = [
        {
            "location": "CZ",
            "name": "market for electricity, low voltage",
            "unit": "kilowatt hour",
            "exchanges": [
                {
                    "uncertainty type": 0,
                    "loc": 1.0,
                    "amount": 1.0,
                    "type": "production",
                    "name": "market for electricity, low voltage",
                    "unit": "kilowatt hour",
                    "location": "CZ",
                },
                {
                    "amount": 6,
                    "type": "technosphere",
                    "name": "market for sulfur hexafluoride, liquid",
                    "unit": "kilogram",
                    "location": "RER",
                },
                {
                    "uncertainty type": 0,
                    "amount": 1.0,
                    "type": "technosphere",
                    "name": "electricity voltage transformation from medium to low voltage",
                    "unit": "kilowatt hour",
                    "location": "CZ",
                },
                {
                    "uncertainty type": 0,
                    "amount": 0.05,
                    "type": "technosphere",
                    "product": "electricity, low voltage",
                    "name": "market for electricity, low voltage",
                    "unit": "kilowatt hour",
                    "location": "CZ",
                },
                {
                    "uncertainty type": 2,
                    "amount": 9,
                    "type": "biosphere",
                    "name": "Sulfur hexafluoride",
                    "unit": "kilogram",
                    "location": None,
                    "categories": ("air",),
                },
            ],
        },
        {
            "location": "CZ",
            "name": "market for electricity, medium voltage",
            "unit": "kilowatt hour",
            "exchanges": [
                {
                    "uncertainty type": 2,
                    "amount": 1.8,
                    "type": "technosphere",
                    "name": "market for transmission network, electricity, medium voltage",
                    "unit": "kilometer",
                    "location": "GLO",
                },
                {
                    "uncertainty type": 0,
                    "amount": 1.0,
                    "type": "production",
                    "product": "electricity, medium voltage",
                    "name": "market for electricity, medium voltage",
                    "unit": "kilowatt hour",
                    "location": "CZ",
                },
                {
                    "uncertainty type": 0,
                    "amount": 1.0,
                    "type": "technosphere",
                    "name": "electricity voltage transformation from high to medium voltage",
                    "unit": "kilowatt hour",
                    "location": "CZ",
                },
                {
                    "uncertainty type": 0,
                    "amount": 0.1234,
                    "type": "technosphere",
                    "name": "market for electricity, medium voltage",
                    "unit": "kilowatt hour",
                    "location": "CZ",
                },
            ],
        },
        {
            "location": "CZ",
            "name": "market for electricity, high voltage",
            "unit": "kilowatt hour",
            "exchanges": [
                {
                    "uncertainty type": 2,
                    "amount": 3,
                    "type": "technosphere",
                    "name": "market for transmission network, long-distance",
                    "unit": "kilometer",
                    "location": "GLO",
                },
                {
                    "uncertainty type": 0,
                    "loc": 1.0,
                    "amount": 1.0,
                    "type": "production",
                    "name": "market for electricity, high voltage",
                    "unit": "kilowatt hour",
                    "location": "CZ",
                },
                {
                    "uncertainty type": 0,
                    "amount": 0.4 * 0.9 * 0.9,
                    "loc": 0.4 * 0.9 * 0.9,
                    "type": "technosphere",
                    "name": "electricity production, hard coal",
                    "unit": "kilowatt hour",
                    "location": "CZ",
                },
                {
                    "uncertainty type": 0,
                    "amount": 0.243,  # 0.3 * 0.9 * 0.9,
                    "loc": 0.243,  # 0.3 * 0.9 * 0.9,
                    "type": "technosphere",
                    "name": "electricity production, wind, 1-3MW turbine, onshore",
                    "unit": "kilowatt hour",
                    "location": "CZ",
                },
                {
                    "uncertainty type": 0,
                    "amount": 0.05 * 0.9 * 0.9,
                    "loc": 0.05 * 0.9 * 0.9,
                    "type": "technosphere",
                    "name": "electricity, high voltage, import from AT",
                    "unit": "kilowatt hour",
                    "location": "CZ",
                },
                {
                    "uncertainty type": 0,
                    "amount": 0.05 * 0.9 * 0.9,
                    "loc": 0.05 * 0.9 * 0.9,
                    "type": "technosphere",
                    "name": "electricity, high voltage, import from DE",
                    "unit": "kilowatt hour",
                    "location": "CZ",
                },
                {
                    "uncertainty type": 0,
                    "amount": 0.1 * 0.9,
                    "loc": 0.1 * 0.9,
                    "type": "technosphere",
                    "name": "electricity, from municipal waste incineration to generic market for electricity, medium voltage",
                    "unit": "kilowatt hour",
                    "location": "CZ",
                },
                {
                    "uncertainty type": 0,
                    "amount": 0.02,
                    "type": "technosphere",
                    "name": "electricity production, photovoltaic, 3kWp slanted-roof installation, multi-Si, panel, mounted",
                    "unit": "kilowatt hour",
                    "location": "CZ",
                },
                {
                    "uncertainty type": 0,
                    "amount": 0.01,
                    "type": "technosphere",
                    "name": "electricity production, photovoltaic, 3kWp slanted-roof installation, single-Si, panel, mounted",
                    "unit": "kilowatt hour",
                    "location": "CZ",
                },
            ],
        },
    ]
    assert move_all_generation_to_high_voltage(given) == expected


def test_remove_electricity_trade():
    given = [
        {
            "location": "CZ",
            "name": "market for electricity, high voltage",
            "unit": "kilowatt hour",
            "exchanges": [
                {
                    "uncertainty type": 2,
                    "amount": 3,
                    "type": "technosphere",
                    "name": "market for transmission network, long-distance",
                    "unit": "kilometer",
                    "location": "GLO",
                },
                {
                    "uncertainty type": 0,
                    "loc": 1.0,
                    "amount": 1.0,
                    "type": "production",
                    "name": "market for electricity, high voltage",
                    "unit": "kilowatt hour",
                    "location": "CZ",
                },
                {
                    "uncertainty type": 0,
                    "amount": 0.4,
                    "type": "technosphere",
                    "name": "electricity production, hard coal",
                    "unit": "kilowatt hour",
                    "location": "CZ",
                },
                {
                    "uncertainty type": 0,
                    "amount": 0.3,
                    "type": "technosphere",
                    "name": "electricity production, wind, 1-3MW turbine, onshore",
                    "unit": "kilowatt hour",
                    "location": "CZ",
                },
                {
                    "uncertainty type": 0,
                    "amount": 0.05,
                    "type": "technosphere",
                    "name": "electricity, high voltage, import from AT",
                    "unit": "kilowatt hour",
                    "location": "CZ",
                },
                {
                    "uncertainty type": 0,
                    "amount": 0.05,
                    "type": "technosphere",
                    "name": "electricity, high voltage, import from DE",
                    "unit": "kilowatt hour",
                    "location": "CZ",
                },
            ],
        }
    ]
    expected = [
        {
            "location": "CZ",
            "name": "market for electricity, high voltage",
            "unit": "kilowatt hour",
            "exchanges": [
                {
                    "uncertainty type": 2,
                    "amount": 3,
                    "type": "technosphere",
                    "name": "market for transmission network, long-distance",
                    "unit": "kilometer",
                    "location": "GLO",
                },
                {
                    "uncertainty type": 0,
                    "loc": 1.0,
                    "amount": 1.0,
                    "type": "production",
                    "name": "market for electricity, high voltage",
                    "unit": "kilowatt hour",
                    "location": "CZ",
                },
                {
                    "uncertainty type": 0,
                    "amount": 0.4,
                    "type": "technosphere",
                    "name": "electricity production, hard coal",
                    "unit": "kilowatt hour",
                    "location": "CZ",
                },
                {
                    "uncertainty type": 0,
                    "amount": 0.3,
                    "type": "technosphere",
                    "name": "electricity production, wind, 1-3MW turbine, onshore",
                    "unit": "kilowatt hour",
                    "location": "CZ",
                },
            ],
        }
    ]
    assert remove_electricity_trade(given) == expected


"""Tests for get_generators_in_mix function which retrieves electricity mix inputs."""

import pytest


class MockExchange:
    """Mock class for database exchanges."""
    def __init__(self, input_data):
        self.input = input_data
    
    def __getitem__(self, key):
        return getattr(self, key)

class MockActivity:
    """Mock class for database activities."""
    def __init__(self, name, exchanges):
        self._name = name
        self._exchanges = exchanges

    def __getitem__(self, key):
        if key == "name":
            return self._name
        raise KeyError(f"Key {key} not found")

    def technosphere(self):
        """Return list of technosphere exchanges."""
        return self._exchanges


class MockDatabase:
    """Mock class for database."""
    def __init__(self, activities):
        self.activities = activities

    def __iter__(self):
        return iter(self.activities)


@pytest.fixture
def sample_db():
    """Create a sample database with electricity activities."""
    # Create some producer activities
    solar = {"name": "electricity production, solar", "unit": "kilowatt hour"}
    wind = {"name": "electricity production, wind", "unit": "kilowatt hour"}
    coal = {"name": "electricity production, coal", "unit": "kilowatt hour"}
    transport = {"name": "transport service", "unit": "ton kilometer"}

    # Create exchanges
    exchanges = [
        MockExchange(solar),
        MockExchange(wind),
        MockExchange(coal),
        MockExchange(transport)  # Non-electricity exchange
    ]

    # Create activities
    activities = [
        MockActivity("market for electricity, high voltage", exchanges),
        MockActivity("market for electricity, medium voltage", exchanges),
    ]

    return MockDatabase(activities)


def test_basic_electricity_mix(sample_db):
    """
    Test basic functionality with the default electricity mix name.

    This test verifies that the `get_generators_in_mix` function 
    correctly retrieves the names of input generators associated 
    with the default electricity mix, which is "market for electricity, high voltage".
    
    The expected output includes:
        - "electricity production, solar"
        - "electricity production, wind"
        - "electricity production, coal"

    It checks whether the actual result matches the expected set of generator names.
    """
    result = get_generators_in_mix(sample_db)
    expected = {
        "electricity production, solar",
        "electricity production, wind",
        "electricity production, coal"
    }
    assert result == expected


def test_different_mix_name(sample_db):
    """
    Test function with a different electricity mix name.

    This test checks whether the `get_generators_in_mix` function can 
    successfully retrieve the names of input generators when provided 
    with a different electricity mix name, specifically 
    "market for electricity, medium voltage".

    The expected output remains the same:
        - "electricity production, solar"
        - "electricity production, wind"
        - "electricity production, coal"

    The test verifies that the function handles different mix names correctly,
    even if the underlying generators are the same.
    """
    result = get_generators_in_mix(sample_db, "market for electricity, medium voltage")
    expected = {
        "electricity production, solar",
        "electricity production, wind",
        "electricity production, coal"
    }
    assert result == expected


def test_non_existent_mix(sample_db):
    """
    Test function with a mix name that doesn't exist in the database.

    This test ensures that when the `get_generators_in_mix` function 
    is called with a mix name that does not exist in the database, 
    it returns an empty set.

    The specific mix name tested is "non-existent mix", and since there 
    are no matching entries in the sample database, the expected output 
    is an empty set.
    """
    result = get_generators_in_mix(sample_db, "non-existent mix")
    assert result == set()


@pytest.fixture
def empty_db():
    """Create an empty database."""
    return MockDatabase([])


def test_empty_database(empty_db):
    """
    Test function with an empty database.

    This test verifies the behavior of the `get_generators_in_mix` 
    function when provided with an empty database. It expects the 
    function to return an empty set, as there are no input generators 
    to retrieve in this case.
    """
    result = get_generators_in_mix(empty_db)
    assert result == set()


@pytest.fixture
def db_with_empty_mix():
    """Create a database with an electricity mix that has no exchanges."""
    activities = [
        MockActivity("market for electricity, high voltage", [])
    ]
    return MockDatabase(activities)


def test_mix_with_no_exchanges(db_with_empty_mix):
    """
    Test function with an electricity mix that has no exchanges.

    This test checks that the `get_generators_in_mix` function returns 
    an empty set when called with a database entry that has no associated 
    exchanges. Since there are no input generators in this mix, 
    the expected output is an empty set.
    """
    result = get_generators_in_mix(db_with_empty_mix)
    assert result == set()


@pytest.fixture
def db_with_only_non_electricity():
    """Create a database with only non-electricity exchanges."""
    transport = {"name": "transport service", "unit": "ton kilometer"}
    exchanges = [MockExchange(transport)]
    activities = [
        MockActivity("market for electricity, high voltage", exchanges)
    ]
    return MockDatabase(activities)


def test_mix_with_only_non_electricity(db_with_only_non_electricity):
    """
    Test function with a mix containing only non-electricity exchanges.

    This test ensures that when the `get_generators_in_mix` function 
    is called with a mix that has only non-electricity exchanges, 
    it correctly returns an empty set. Since there are no relevant 
    input generators in this case, the expected output is an empty set.
    """
    result = get_generators_in_mix(db_with_only_non_electricity)
    assert result == set()