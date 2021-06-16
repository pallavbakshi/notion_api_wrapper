import pytest

from potion.utilities import utilities


@pytest.mark.parametrize(
    "url, expected",
    [
        ("https://www.notion.so/Get-Started-232/", "232"),
        ("www.notion.so/Get-Started-232/", "232"),
        ("www.notion.so/workspace/Get-Started-232/", "232"),
        ("www.notion.so/workspace/232/", "232"),
        ("www.notion.so/workspace/232?v=999", "232"),
        ("https://www.notion.so/Get-Started-232?v=999", "232"),
        ("https://www.notion.so/workspace/Get-Started-232?v=999", "232"),
    ],
)
def test_extract_block_id(url, expected):
    result = utilities.extract_block_id(url)
    assert result == expected


@pytest.mark.parametrize(
    "block_id, expected",
    [
        ("a" * 32, f"{'a' * 8}-{'a' * 4}-{'a' * 4}-{'a' * 4}-{'a' * 12}"),
    ],
)
def test_format_block_id(block_id, expected):
    result = utilities.format_block_id(block_id)
    assert result == expected


@pytest.mark.parametrize(
    "block_id, dash_scheme, expected",
    [
        (
            "aaa",
            [
                1,
            ],
            "a-aa",
        ),
        ("aaaaaa", [2, 4], "aa-aa-aa"),
    ],
)
def test_insert_dashes(block_id, dash_scheme, expected):
    result = utilities.insert_dashes(block_id, dash_scheme)
    assert result == expected
