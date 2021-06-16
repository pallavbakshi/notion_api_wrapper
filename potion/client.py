import asyncio
import os
from dataclasses import dataclass
from typing import Union, Dict, Any

from dotenv import find_dotenv, load_dotenv

from potion.utilities.type_alias import (
    NotionDatabaseRow,
    NotionPage,
    DatabaseID,
    PageID,
)

load_dotenv(find_dotenv())


@dataclass(frozen=True)
class NotionDataClass:
    data_type: Union[NotionDatabaseRow, NotionPage]
    data_id: Union[DatabaseID, PageID]
    data: Dict[str, Any]


class NotionClient:
    def __init__(self, token: str) -> None:
        self.token = token

    def get_data(
        self, data_id: Union[DatabaseID, PageID], verbose: bool = False
    ) -> NotionDataClass:
        pass

    def get_data_dump(self, data_id: Union[DatabaseID, PageID]) -> NotionDataClass:
        pass


async def main() -> None:
    await asyncio.sleep(4)
    token = os.getenv("NOTION_TOKEN") or ""
    database_id = os.getenv("NOTION_DATABASE")
    # client = NotionClient(token)
    print("Hello", token, database_id)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
