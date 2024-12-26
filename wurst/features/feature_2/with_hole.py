from .errors import InvalidLink, NonuniqueCode
from .searching import reference_product
from pprint import pformat


get_input_databases = lambda data: {ds["database"] for ds in data}


def link_internal(data, fields=("name", "product", "location", "unit")):
    """

    Write lines of code to Link internal exchanges in a dataset based on specified fields.

    1. This will iterates through the provided dataset of activities.
    2. And links internal exchanges by creating an 'input' field for each exchange that matches the specified fields. 
    

    Args:
    data (list[dict]): A list of activity datasets. Each dataset is expected to be a 
    dictionary containing:
    - database (str): The name of the database.
    - code (str): A unique identifier for the activity.
    - exchanges (list[dict]): A list of exchanges, where each exchange is expected to 
    contain keys defined in the `fields` argument.  

    fields (tuple): A tuple of strings representing the keys in the exchanges that will be 
    used to create a unique identifier for linking. Defaults to ("name", "product", 
    "location", "unit").

    Returns:
    list[dict]: The updated list of activity datasets, where each internal exchange has 
    an 'input' field populated with a tuple containing the database and code of the linked activity.

    Raises:
    ValueError: If an exchange of type 'biosphere' is found that cannot be linked to any activity.
    KeyError: If an exchange cannot be linked to an existing activity based on the specified fields.

    """
    $PlaceHolder$

def check_internal_linking(data):
    """Check that each internal link is to an actual activity"""
    names = get_input_databases(data)
    keys = {(ds["database"], ds["code"]) for ds in data}
    for ds in data:
        for exc in ds["exchanges"]:
            if exc.get("input") and exc["input"][0] in names:
                if exc["input"] not in keys:
                    raise InvalidLink(
                        "Exchange links to non-existent activity:\n{}".format(
                            pformat(exc)
                        )
                    )

   


def change_db_name(data, name):
    """Change the database of all datasets in ``data`` to ``name``.

    Raises errors if each dataset does not have exactly one reference production exchange."""
    old_names = get_input_databases(data)
    for ds in data:
        ds["database"] = name
        for exc in ds["exchanges"]:
            if exc.get("input") and exc["input"][0] in old_names:
                exc["input"] = (name, exc["input"][1])
    return data


def check_duplicate_codes(data):
    """Check that there won't be duplicate codes when activities are merged to new, common database"""
    seen = set()
    for ds in data:
        if ds["code"] in seen:
            raise NonuniqueCode("Code {} seen at least twice".format(ds["code"]))
        seen.add(ds["code"])
