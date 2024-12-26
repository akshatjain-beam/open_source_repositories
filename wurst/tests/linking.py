import unittest
from wurst.linking import link_internal, InvalidLink  # Replace 'your_module' with the actual module name


class TestLinkInternal(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures for unit tests."""
        self.maxDiff = None
        self.basic_data = [
            {
                "database": "db1",
                "code": "act1",
                "exchanges": [
                    {
                        "name": "steel",
                        "product": "hot rolled",
                        "location": "GLO",
                        "unit": "kg",
                        "type": "technosphere",
                        "amount": 1.0
                    },
                    {
                        "name": "product1",
                        "product": "main",
                        "location": "GLO",
                        "unit": "kg",
                        "type": "production",
                        "amount": 1.0
                    }
                ]
            },
            {
                "database": "db1",
                "code": "act2",
                "exchanges": [
                    {
                        "name": "steel",
                        "product": "hot rolled",
                        "location": "GLO",
                        "unit": "kg",
                        "type": "production",
                        "amount": 1.0
                    }
                ]
            }
        ]

    def test_successful_linking(self):
        """Test basic successful linking of exchanges.
        
        This test verifies that the 'input' field of the first exchange in
        the first activity is correctly linked to the corresponding activity
        ('act2') in the dataset based on matching fields.
        """
        result = link_internal(self.basic_data)
        self.assertEqual(
            tuple(result[0]["exchanges"][0]["input"]),
            ("db1", "act2")
        )

    def test_already_linked_exchange(self):
        """Test that already linked exchanges are not modified.
        
        This test ensures that if an exchange already has an 'input' field,
        it should not be altered by the linking process.
        """
        data = [x.copy() for x in self.basic_data]
        data[0]["exchanges"] = [x.copy() for x in data[0]["exchanges"]]
        data[0]["exchanges"][0]["input"] = ["db1", "existing"]
        result = link_internal(data)
        self.assertEqual(
            data[0]["exchanges"][0]["input"],
            ["db1", "existing"]
        )

    def test_biosphere_exchange_error(self):
        """Test that unlinked biosphere exchanges raise ValueError.
        
        This test checks that if an exchange of type 'biosphere' is present
        and cannot be linked, the function raises a ValueError with the
        appropriate message.
        """
        data = [x.copy() for x in self.basic_data]
        data[0]["exchanges"] = [x.copy() for x in data[0]["exchanges"]]
        data[0]["exchanges"][0]["type"] = "biosphere"
        with self.assertRaises(ValueError) as context:
            link_internal(data)
        self.assertIn("Unlinked biosphere exchange", str(context.exception))

    def test_custom_fields(self):
        """Test linking with custom fields.
        
        This test verifies that the function can correctly link exchanges
        using a custom field instead of the standard fields. The linking
        should still create the correct 'input' based on the custom field values.
        """
        data = [
            {
                "database": "db1",
                "code": "act1",
                "exchanges": [
                    {
                        "custom_field": "value1",
                        "type": "technosphere",
                        "amount": 1.0
                    },
                    {
                        "custom_field": "value2",
                        "type": "production",
                        "amount": 1.0
                    }
                ]
            },
            {
                "database": "db1",
                "code": "act2",
                "exchanges": [
                    {
                        "custom_field": "value1",
                        "type": "production",
                        "amount": 1.0
                    }
                ]
            }
        ]
        result = link_internal(data, fields=("custom_field",))
        self.assertEqual(
            tuple(result[0]["exchanges"][0]["input"]),
            ("db1", "act2")
        )

    def test_multiple_exchanges(self):
        """Test linking multiple exchanges in a single activity.
        
        This test ensures that multiple exchanges within a single activity
        are linked correctly to their respective activities. Each exchange
        should be able to find a match based on the specified fields.
        """
        data = [
            {
                "database": "db1",
                "code": "act1",
                "exchanges": [
                    {
                        "name": "steel",
                        "product": "hot rolled",
                        "location": "GLO",
                        "unit": "kg",
                        "type": "technosphere",
                        "amount": 1.0
                    },
                    {
                        "name": "aluminum",
                        "product": "cast",
                        "location": "GLO",
                        "unit": "kg",
                        "type": "technosphere",
                        "amount": 1.0
                    },
                    {
                        "name": "product1",
                        "product": "main",
                        "location": "GLO",
                        "unit": "kg",
                        "type": "production",
                        "amount": 1.0
                    }
                ]
            },
            {
                "database": "db1",
                "code": "act2",
                "exchanges": [
                    {
                        "name": "steel",
                        "product": "hot rolled",
                        "location": "GLO",
                        "unit": "kg",
                        "type": "production",
                        "amount": 1.0
                    }
                ]
            },
            {
                "database": "db1",
                "code": "act3",
                "exchanges": [
                    {
                        "name": "aluminum",
                        "product": "cast",
                        "location": "GLO",
                        "unit": "kg",
                        "type": "production",
                        "amount": 1.0
                    }
                ]
            }
        ]
        result = link_internal(data)
        self.assertEqual(tuple(result[0]["exchanges"][0]["input"]), ("db1", "act2"))
        self.assertEqual(tuple(result[0]["exchanges"][1]["input"]), ("db1", "act3"))

    def test_missing_field(self):
        """Test handling of missing fields in exchanges.
        
        This test checks that if a necessary field for linking is missing
        in an exchange, a KeyError is raised, indicating that the linking
        activity cannot be found.
        """
        data = [x.copy() for x in self.basic_data]
        data[0]["exchanges"] = [x.copy() for x in data[0]["exchanges"]]
        del data[0]["exchanges"][0]["location"]
        with self.assertRaises(KeyError) as context:
            link_internal(data)
        self.assertIn("Can't find linking activity", str(context.exception))

    def test_empty_data(self):
        """Test handling of empty dataset.
        
        This test ensures that when the input dataset is empty, the
        function returns an empty list without errors.
        """
        result = link_internal([])
        self.assertEqual(result, [])

    def test_no_exchanges(self):
        """Test handling of activities with no exchanges.
        
        This test verifies that if an activity has no exchanges defined,
        the function simply returns the original activity unchanged.
        """
        data = [
            {
                "database": "db1",
                "code": "act1",
                "exchanges": [
                    {
                        "name": "product1",
                        "product": "main",
                        "location": "GLO",
                        "unit": "kg",
                        "type": "production",
                        "amount": 1.0
                    }
                ]
            }
        ]
        result = link_internal(data)
        self.assertEqual(result, data)

if __name__ == '__main__':
    unittest.main()
