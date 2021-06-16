import json

import pytest

from tests.utilities import contains_desired_fields

PATH = "./data"


@pytest.fixture
def database_data():
    meta_data_filename = "initial_database_data.json"
    with open(f"{PATH}/{meta_data_filename}", "r") as f:
        meta_data = json.load(f)
    return meta_data


@pytest.mark.asyncio
async def test_get_data_from_database(notion_manager, database_id):
    result = await notion_manager.get_data_from_database(database_id)
    desired_keys = ["page_id", "database_id", "database_properties", "database_name"]
    assert contains_desired_fields(result, desired_keys)
