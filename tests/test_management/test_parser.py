import json

import pytest

from tests.utilities import contains_desired_fields

PATH = "./data"


@pytest.fixture
def database_meta_data():
    meta_data_filename = "initial_database_meta_data.json"
    with open(f"{PATH}/{meta_data_filename}", "r") as f:
        meta_data = json.load(f)
    return meta_data


def test_get_relevant_meta_data(data_parser, database_meta_data):
    result = data_parser.get_relevant_meta_data(database_meta_data)
    desired_fields = ["database_id", "database_name", "database_properties"]
    assert contains_desired_fields(result, desired_fields)

    desired_properties = ["property_name", "property_type", "property_value"]
    assert contains_desired_fields(result["database_properties"], desired_properties)
