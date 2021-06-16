from typing import List
from urllib import parse

from potion.utilities.constants import ID_LENGTH_WITHOUT_DASH, ID_LENGTH_WITH_DASH


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
