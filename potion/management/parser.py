from typing import Any, Dict, List, Union
from glom import glom

DATABASE_PROPERTY_PATHS = {"multi_select": "multi_select.options", "title": "title"}


class Parser:
    def __init__(self) -> None:
        pass

    def parse_properties(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
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

    def get_relevant_meta_data(
        self, data: Dict[str, Any]
    ) -> Dict[str, Union[str, List[Any]]]:
        relevant_data_paths = {
            "database_id": "id",
            "database_name": ("title", (lambda x: x[0], "plain_text")),
            "database_properties": "properties",
        }
        result = {}
        for key, spec in relevant_data_paths.items():
            result[key] = glom(data, spec)
        result["database_properties"] = self.parse_properties(
            result["database_properties"]
        )
        return result
