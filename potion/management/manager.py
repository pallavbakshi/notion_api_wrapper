from potion.management.parser import DatabaseParser
from potion.management.resource_access import DatabaseRequest
from potion.utilities.type_alias import DatabaseID, NotionDatabase
from potion.utilities.utilities import format_block_id


class PotionManagerException(Exception):
    pass


class Manager:
    def __init__(self, token: str) -> None:
        self.token = token
        self.database_request: DatabaseRequest = DatabaseRequest(token)
        self.database_parser: DatabaseParser = DatabaseParser()

    async def _check_database_authorization(self, database_id: DatabaseID) -> None:
        databases = await self.database_request.fetch_authorized_databases()
        if database_id not in [id_ for id_, _ in databases]:  # type: ignore
            raise PotionManagerException(
                f"{database_id} doesn't have authorization for project. "
                f"Following databases are authorized for this project - "
                f"{databases}."
            )

    async def get_data_from_database(
        self, database_id: DatabaseID, verbose: bool = False
    ) -> NotionDatabase:
        database_id = format_block_id(database_id)
        await self._check_database_authorization(database_id)
        response = await self.database_request.fetch_data_from(database_id)
        database_name = await self.database_request.fetch_database_name(database_id)
        data = self.database_parser.get_relevant_data(response, database_name)

        if verbose:
            return self.database_parser.prune_data(data)

        return data
