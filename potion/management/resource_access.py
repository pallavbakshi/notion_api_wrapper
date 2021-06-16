import json
from typing import Any, Dict, List

import aiohttp

from potion.utilities.constants import NOTION_VERSION, DATABASE_URL
from potion.utilities.utilities import format_block_id
from potion.utilities.type_alias import PageID, DatabaseID


class InvalidNotionToken(Exception):
    pass


class InvalidBlockID(Exception):
    pass


class NotionRequestException(Exception):
    pass


class NotionDatabaseException(Exception):
    pass


class ResourceRequest:
    def __init__(self, token: str) -> None:
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Notion-Version": NOTION_VERSION,
            "Content-Type": "application/json",
        }

    async def get(self, endpoint: str) -> Dict[str, Any]:
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.get(endpoint) as resp:
                return await self.validate_response(resp, endpoint)

    @staticmethod
    async def validate_response(resp: Any, endpoint: str) -> Dict[str, Any]:
        resp_data = json.loads(await resp.text())
        if resp.status != 200:
            raise NotionRequestException(
                f"Request to {endpoint} failed with {resp.status} "
                f"- {resp_data['code']} - {resp_data['message']}"
            )
        return {"resp": resp, "data": resp_data}

    async def post(self, endpoint: str) -> Dict[str, Any]:
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.post(endpoint) as resp:
                return await self.validate_response(resp, endpoint)


class DatabaseRequest(ResourceRequest):
    def __init__(self, token: str) -> None:
        super(DatabaseRequest, self).__init__(token)

    async def fetch_authorized_database_ids(self) -> List[DatabaseID]:
        reply = await self.get(DATABASE_URL)
        data = reply["data"]
        if len(data["results"]) == 0:
            raise NotionRequestException("No databases shared with the integration.")
        return [elem["id"] for elem in data["results"]]

    async def fetch_page_ids_within(self, database_id: str) -> List[PageID]:
        database_id = format_block_id(database_id)
        endpoint = f"{DATABASE_URL}/{database_id}/query"
        response = await self.post(endpoint)
        results = response["data"]["results"]
        return [elem["id"] for elem in results]

    async def fetch_meta_data(self, database_id: str) -> Dict[str, Any]:
        database_id = format_block_id(database_id)
        endpoint = f"{DATABASE_URL}/{database_id}"
        response = await self.get(endpoint)
        data = response["data"]
        return data

    # TODO Add vulture
    async def create_row_within(self, database_id: str, data: Dict[str, Any]) -> None:
        print(data, database_id)
