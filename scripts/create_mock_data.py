import json
import os
import asyncio

from management.parser import DatabaseParser
from management.resource_access import DatabaseRequest
from dotenv import load_dotenv, find_dotenv

PATH = "/data"


async def main():
    load_dotenv(find_dotenv())

    token = os.getenv("NOTION_TOKEN")

    notion_database = DatabaseRequest(token)
    authorized_dbs = await notion_database.fetch_authorized_database_ids()
    database_meta_data = await notion_database.fetch_meta_data(authorized_dbs[0])
    with open(f"{PATH}/initial_database.json", "w") as f:
        json.dump(database_meta_data, f)
    database_parser = DatabaseParser()
    print(database_parser.get_relevant_meta_data(database_meta_data))
    print(authorized_dbs)
    print(database_meta_data)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
