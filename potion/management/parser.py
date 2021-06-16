from typing import Any, Dict, List, Union
from glom import glom

from potion.utilities.type_alias import NotionDatabaseRow, NotionDatabase

DATABASE_PROPERTY_PATHS = {"multi_select": "multi_select.options", "title": "title"}


class Parser:
    def __init__(self) -> None:
        pass

    @staticmethod
    def _parse_properties(data: Dict[str, Any]) -> List[Dict[str, Any]]:
        properties = []
        for property_name, nested_value in data.items():
            result = {}
            type_ = nested_value["type"]
            if type_ in DATABASE_PROPERTY_PATHS.keys():
                spec = DATABASE_PROPERTY_PATHS[type_]
                result["property_name"] = property_name
                result["type"] = type_
                result["value"] = glom(nested_value, spec)
                properties.append(result)
        return properties


class DatabaseParser(Parser):
    def __init__(self) -> None:
        super(DatabaseParser, self).__init__()

    def get_relevant_data(self, data: NotionDatabase) -> NotionDatabase:
        relevant_data_paths = {
            "page_id": "id",
            "database_id": "parent.database_id",
            "database_properties": "properties",
        }
        result = []
        for row in data:
            row_data = self._extract_relevant_data(row, relevant_data_paths)
            row_data["database_properties"] = self._parse_properties(
                row_data["database_properties"]
            )
            result.append(row_data)
        return result

    def get_relevant_meta_data(
        self, data: Dict[str, Any]
    ) -> Dict[str, Union[str, List[Any]]]:
        relevant_data_paths = {
            "database_id": "id",
            "database_name": ("title", (lambda x: x[0], "plain_text")),
            "database_properties": "properties",
        }
        result = self._extract_relevant_data(data, relevant_data_paths)
        result["database_properties"] = self._parse_properties(
            result["database_properties"]
        )
        return result

    @staticmethod
    def _extract_relevant_data(
        data: NotionDatabaseRow, data_paths: Dict[str, Any]
    ) -> Dict[str, Any]:
        result = {}
        for key, spec in data_paths.items():
            result[key] = glom(data, spec)
        return result

    @staticmethod
    def prune_data(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return data
