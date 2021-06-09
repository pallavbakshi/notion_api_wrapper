import os

import pytest
from dotenv import load_dotenv, find_dotenv

from potion.client import InvalidNotionToken
from potion.utilities import format_block_id

load_dotenv(find_dotenv())


@pytest.fixture()
def token():
    tok = os.getenv("NOTION_TOKEN")
    if tok is None:
        raise InvalidNotionToken("Set NOTION_TOKEN within your environment to fix it.")
    return tok


@pytest.fixture()
def database_id():
    database_id = os.getenv("NOTION_DATABASE")
    if database_id is None:
        raise InvalidNotionToken(
            "Set NOTION_DATABASE within your environment to fix it."
        )
    return format_block_id(database_id)
