import json
from typing import List, no_type_check
from urllib import parse

ID_LENGTH_WITHOUT_DASH: int = 32
ID_LENGTH_WITH_DASH: int = 36


def extract_block_id(url: str) -> str:
    split_url = parse.urlsplit(url)
    path_crumb = [x for x in split_url.path.split("/") if x][-1]
    block_id = path_crumb.split("-")[-1]
    return block_id


def format_block_id(block_id: str) -> str:
    if len(block_id) == ID_LENGTH_WITHOUT_DASH:
        block_id = insert_dashes(block_id, [8, 12, 16, 20])
    assert len(block_id) == ID_LENGTH_WITH_DASH
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
            f"Response failed, status code {response.status_code},"
            f" {text['code']}, {text['message']}"
        )

    return wrapper
