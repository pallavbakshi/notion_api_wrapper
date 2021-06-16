import os

import pytest
from dotenv import load_dotenv, find_dotenv

from potion.management.parser import DatabaseParser
from potion.management.resource_access import (
    ResourceRequest,
    InvalidNotionToken,
    DatabaseRequest,
)
from potion.utilities.constants import API_URL
from potion.utilities.utilities import format_block_id

load_dotenv(find_dotenv())


@pytest.fixture(autouse=True)
def token():
    tok = os.getenv("NOTION_TOKEN")
    if tok is None:
        raise InvalidNotionToken("Set NOTION_TOKEN within your environment to fix it.")
    return tok


@pytest.fixture(autouse=True)
def database_id():
    database_id = os.getenv("NOTION_DATABASE")
    if database_id is None:
        raise InvalidNotionToken(
            "Set NOTION_DATABASE within your environment to fix it."
        )
    return format_block_id(database_id)


@pytest.fixture
def notion_request(token):
    nr = ResourceRequest(token)
    return nr


@pytest.fixture
def database_request(token):
    nd = DatabaseRequest(token)
    return nd


@pytest.fixture
def database_endpoint(database_id):
    endpoint = f"{API_URL}/databases/{database_id}"
    return endpoint


# TODO fix
@pytest.fixture
def page_endpoint(page_id):
    endpoint = f"{API_URL}/databases/{database_id}"
    return endpoint


@pytest.fixture
def data_parser():
    dc = DatabaseParser()
    return dc
