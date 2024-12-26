import unittest
import warnings
from unittest import TestCase
import pandas as pd

from py2mappr._builder.build_dataset import build_datapoints, build_attr_descriptor

# Suppress all warnings
warnings.filterwarnings("ignore")



class BuildDatapointTestCase(TestCase):
    def test_string_text_is_converted_from_md(self):
        datapoint_dict = {
            "id": "test",
            "description": "This is a **test**.",
        }

        datapoint = pd.Series(datapoint_dict)
        dpAttribTypes = {"id": "string", "description": "string"}
        dpRenderTypes = {"id": "default", "description": "text"}
        expected = "<p>This is a <strong>test</strong>.</p>"

        result = build_datapoints(
            pd.DataFrame([datapoint], index=["description"]),
            dpAttribTypes,
            dpRenderTypes,
        )

        self.assertEqual(expected, result[0]["attr"]["description"])

    def test_string_default_not_converted_from_md(self):
        datapoint_dict = {
            "id": "test",
            "description": "This is a **test**.",
        }

        datapoint = pd.Series(datapoint_dict)
        dpAttribTypes = {"id": "string", "description": "string"}
        dpRenderTypes = {"id": "default", "description": "default"}
        expected = "This is a **test**."

        result = build_datapoints(
            pd.DataFrame([datapoint], index=["description"]),
            dpAttribTypes,
            dpRenderTypes,
        )

        self.assertEqual(expected, result[0]["attr"]["description"])


class TestBuildAttrDescriptor(unittest.TestCase):

    def test_basic_functionality(self):
        """
        Test the basic functionality of the build_attr_descriptor function.
        Ensures that when provided with a column name and an empty override,
        the function returns the default descriptor dictionary with the column
        name correctly set.
        """
        column = 'example_column'
        override = pd.Series()

        result = build_attr_descriptor(column, override)
        expected = {
            "id": 'example_column',
            "title": 'example_column',
            "visible": True,
            "visibleInProfile": True,
            "searchable": True,
            "attrType": "string",
            "renderType": "default",
            "metadata": {"descr": "", "maxLabel": "", "minLabel": ""},
            "overlayAnchor": "",
            "priority": "medium",
            "axis": "none",
            "tooltip": "",
            "colorSelectable": False,
            "sizeSelectable": False,
        }
        self.assertEqual(result, expected)

    def test_empty_title(self):
        """
        Test the function with a different column name but still an empty override.
        This ensures that the function correctly handles different input column names
        while producing the default descriptor output.
        """
        column = 'another_column'
        override = pd.Series()

        result = build_attr_descriptor(column, override)
        expected = {
            "id": 'another_column',
            "title": 'another_column',
            "visible": True,
            "visibleInProfile": True,
            "searchable": True,
            "attrType": "string",
            "renderType": "default",
            "metadata": {"descr": "", "maxLabel": "", "minLabel": ""},
            "overlayAnchor": "",
            "priority": "medium",
            "axis": "none",
            "tooltip": "",
            "colorSelectable": False,
            "sizeSelectable": False,
        }
        self.assertEqual(result, expected)

    def test_with_override(self):
        """
        Test the function with an override that changes some of the default attributes.
        This ensures that the function correctly merges the override values with the
        default descriptor dictionary.
        """
        column = 'my_column'
        override = pd.Series({
            'title': 'My Custom Title',
            'visible': False,
            'priority': 'high'
        })

        result = build_attr_descriptor(column, override)
        expected = {
            "id": 'my_column',
            "title": 'My Custom Title',
            "visible": False,
            "visibleInProfile": True,
            "searchable": True,
            "attrType": "string",
            "renderType": "default",
            "metadata": {"descr": "", "maxLabel": "", "minLabel": ""},
            "overlayAnchor": "",
            "priority": 'high',
            "axis": "none",
            "tooltip": "",
            "colorSelectable": False,
            "sizeSelectable": False,
        }
        self.assertEqual(result, expected)

    def test_with_partial_override(self):
        """
        Test the function with an override that partially modifies the descriptor.
        Ensures that the function handles partial overrides correctly, preserving the
        default values for attributes not specified in the override.
        """
        column = 'partial_column'
        override = pd.Series({
            'title': None,  # Should not change the title
            'other_attr': 'new_value'  # Not in the original config
        })

        result = build_attr_descriptor(column, override)
        expected = {
            "id": 'partial_column',
            "title": None,
            "visible": True,
            "visibleInProfile": True,
            "searchable": True,
            "attrType": "string",
            "renderType": "default",
            "metadata": {"descr": "", "maxLabel": "", "minLabel": ""},
            "overlayAnchor": "",
            "priority": "medium",
            "axis": "none",
            "tooltip": "",
            "colorSelectable": False,
            "sizeSelectable": False,
        }
        self.assertEqual(result, expected)

    def test_with_none_override(self):
        """
        Test the function with a None override. Ensures that the function correctly
        handles a None value for the override, producing the default descriptor dictionary.
        """
        column = 'none_override_column'
        override = None

        result = build_attr_descriptor(column, override)
        expected = {
            "id": 'none_override_column',
            "title": 'none_override_column',
            "visible": True,
            "visibleInProfile": True,
            "searchable": True,
            "attrType": "string",
            "renderType": "default",
            "metadata": {"descr": "", "maxLabel": "", "minLabel": ""},
            "overlayAnchor": "",
            "priority": "medium",
            "axis": "none",
            "tooltip": "",
            "colorSelectable": False,
            "sizeSelectable": False,
        }
        self.assertEqual(result, expected)