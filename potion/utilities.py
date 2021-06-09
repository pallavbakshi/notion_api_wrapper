import json
from typing import Any, Tuple, List, Dict, no_type_check

ID_LENGTH_WITHOUT_DASH: int = 32
NOTION_PLATFORM: str = "notion"
NOTION_WORKSPACE: str = "pallavtech"


def extract_block_id(url: str) -> str:
    start_idx = url.find(NOTION_WORKSPACE) + len(NOTION_WORKSPACE) + len("/")
    end_idx = start_idx + ID_LENGTH_WITHOUT_DASH
    return url[start_idx:end_idx]


def get_notion_secrets(project_name: str, block_id: str) -> Tuple[str, str]:
    projects = get_secrets(NOTION_PLATFORM)["projects"]
    token, blocks = _get_project_details(project_name, projects)
    block_id = _get_complete_block_id(block_id, blocks)
    return token, block_id


def _get_project_details(
    project_name: str, projects: List[Dict[str, Any]]
) -> Tuple[str, List[Dict[str, str]]]:
    for project in projects:
        if project["name"] == project_name:
            return project["token"], project["blocks"]
    else:
        raise RuntimeError(
            f"No project with name {project_name} found in configuration."
        )


def _get_complete_block_id(block_id: str, blocks: List[Dict[str, str]]) -> str:
    for block in blocks:
        if block["block_id"].startswith(block_id):
            full_block_id = format_block_id(extract_block_id(block["block_url"]))
            return full_block_id
    else:
        raise RuntimeError(f"No block id found matching {block_id} in configuration.")


def get_secrets(platform: "str") -> Any:
    with open("config.json", "r") as f:
        data = json.load(f)
    return data[platform]


def format_block_id(block_id: str) -> str:
    if len(block_id) == ID_LENGTH_WITHOUT_DASH:
        return insert_dashes(block_id, [8, 12, 16, 20])
    return block_id


def insert_dashes(text: str, indices: List[int]) -> str:
    last_index = len(text)
    parts = [text[i:j] for i, j in zip([0] + indices, indices + [last_index])]
    return "-".join(parts)


@no_type_check
def validate_response(fn):
    def wrapper(*args, **kwargs):
        response = fn(*args, **kwargs)
        if response.status_code == 200:
            return response
        text = json.loads(response.text)
        raise RuntimeError(
            f"Response failed, status code {response.status_code}, {text['code']}, {text['message']}"
        )

    return wrapper
