import asyncio
import os
from typing import Union, Dict, Any

from dotenv import find_dotenv, load_dotenv

from potion.management.manager import Manager
from potion.utilities.type_alias import (
    DatabaseID,
    PageID,
)

load_dotenv(find_dotenv())


class NotionClient:
    def __init__(self, token: str) -> None:
        self.token = token

    async def get_data(
        self,
        block_id: Union[DatabaseID, PageID],
        verbose: bool = False,
        data_dump: bool = False,
    ) -> Dict[str, Any]:
        assert not (verbose and data_dump)
        nm = Manager(self.token)
        result = await nm.get_data(block_id, verbose, data_dump)
        return result


async def main() -> None:
    await asyncio.sleep(4)
    token = os.getenv("NOTION_TOKEN") or ""
    database_id = os.getenv("NOTION_DATABASE")
    # client = NotionClient(token)
    print("Hello", token, database_id)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
