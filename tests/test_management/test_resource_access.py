import pytest

from potion.management.resource_access import NotionRequestException
from tests.utilities import all_object_types_are_page, all_id_of_appropriate_length

INITIAL_LENGTH_OF_NOTION_DATABASE = 3
INITIAL_AUTHORIZED_DATABASES = 1


@pytest.mark.asyncio
async def test_get_request(notion_request, database_endpoint, database_id):
    reply = await notion_request.get(database_endpoint)
    resp = reply["resp"]
    data = reply["data"]
    assert resp.status == 200
    assert data["id"] == database_id
    assert "title" in data.keys()
    assert "properties" in data.keys()


@pytest.mark.asyncio
async def test_get_request_fail(notion_request, database_endpoint, database_id):
    invalid_url = database_endpoint.replace("v1", "v2")
    with pytest.raises(NotionRequestException) as e:
        await notion_request.get(invalid_url)
    assert "invalid_request_url" in str(e.value)


@pytest.mark.asyncio
async def test_get_authorized_databases(database_request):
    result = await database_request.fetch_authorized_databases()
    assert len(result) == INITIAL_AUTHORIZED_DATABASES

    database_ids = [database_id for database_id, _ in result]
    assert all_id_of_appropriate_length(database_ids)


@pytest.mark.asyncio
async def test_get_rows_within_database_id(database_request, database_id):
    data = await database_request.fetch_meta_data(database_id)
    assert "object" in data.keys()


@pytest.mark.asyncio
async def test_get_data_from_database(database_request, database_id):
    results = await database_request.fetch_data_from(database_id)
    assert len(results) == INITIAL_LENGTH_OF_NOTION_DATABASE
    assert all_object_types_are_page(results)


@pytest.mark.asyncio
async def test_get_page_ids_within_database_id(database_request, database_id):
    page_ids = await database_request.fetch_page_ids_within(database_id)
    assert len(page_ids) == INITIAL_LENGTH_OF_NOTION_DATABASE
    assert all_id_of_appropriate_length(page_ids)


@pytest.mark.asyncio
async def test_fetch_database_name(database_request, database_id):
    name = await database_request.fetch_database_name(database_id)
    assert name == "Notion Testing"
