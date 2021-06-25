import pytest


@pytest.mark.asyncio
async def test_get_data(notion_client, database_id):
    result = await notion_client.get_data(database_id)
    print(result)
    assert True


@pytest.mark.asyncio
async def test_get_data_verbose(notion_client, database_id):
    result = await notion_client.get_data(database_id, verbose=True)
    print(result)
    assert True


@pytest.mark.asyncio
async def test_get_data_dump(notion_client, database_id):
    result = await notion_client.get_data(database_id, data_dump=True)
    print(result)
    assert True
