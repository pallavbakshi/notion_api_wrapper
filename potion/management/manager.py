from typing import Union, Dict, Any

from potion.management.parser import DatabaseParser
from potion.management.resource_access import DatabaseRequest
from potion.utilities.type_alias import DatabaseID, PageID
from potion.utilities.utilities import format_block_id


class PotionManagerException(Exception):
    pass


class Manager:
    def __init__(self, token: str) -> None:
        self.token = token
        self.database_request: DatabaseRequest = DatabaseRequest(token)
        self.database_parser: DatabaseParser = DatabaseParser()

    async def _is_database_authorized(self, database_id: DatabaseID) -> None:
        databases = await self.database_request.fetch_authorized_databases()
        return database_id in [id_ for id_, _ in databases]  # type: ignore

    async def get_data(
        self,
        block_id: Union[DatabaseID, PageID],
        verbose: bool = False,
        data_dump: bool = False,
    ) -> Dict[str, Any]:
        block_id = format_block_id(block_id)
        if await self._is_database_authorized(block_id):
            database_id = block_id
            return await self.get_data_from_database(
                database_id, verbose=verbose, data_dump=data_dump
            )
        page_id = block_id
        return await self.get_data_from_page(
            page_id, verbose=verbose, data_dump=data_dump
        )

    async def get_data_from_page(
        self, page_id: PageID, verbose: bool = False, data_dump: bool = False
    ) -> Dict[str, Any]:

        # TODO - Fix
        return {"hello": 2}

    async def get_data_from_database(
        self, database_id: DatabaseID, verbose: bool = False, data_dump: bool = False
    ) -> Dict[str, Any]:
        database_id = format_block_id(database_id)
        if not await self._is_database_authorized(database_id):
            raise PotionManagerException(
                f"Incorrect database id or database id {database_id} not authorized."
            )
        response = await self.database_request.fetch_data_from(database_id)
        database_name = await self.database_request.fetch_database_name(database_id)
        data = self.database_parser.get_relevant_data(response, database_name)

        result = {
            "block_id": database_id,
            "verbose": verbose,
            "data_dump": data_dump,
            "object": "database",
        }

        if not verbose:
            result["data"] = self.database_parser.prune_data(data)

        if data_dump:
            result["data"] = data

        return result
