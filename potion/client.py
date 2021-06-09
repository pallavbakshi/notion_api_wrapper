import json
from functools import partial
from typing import List, Dict, Callable, Optional, Any

import requests
from requests import Response

from potion.constants import NOTION_VERSION, BLOCK_LIMIT
from potion.utilities import validate_response


class InvalidNotionToken(Exception):
    pass


class NotionRequests:
    def __init__(self, token: str) -> None:
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Notion-Version": NOTION_VERSION,
            "Content-Type": "application/json",
        }

    def post(self, url: str, query: str = "") -> List[Dict]:
        post_request = partial(self._post, url, query=query)
        return self._paginate(post_request)

    @validate_response
    def _post(
        self,
        url: str,
        cursor: Optional[str] = None,
        query: Optional[str] = None,
        sort: Optional[str] = None,
    ) -> Response:
        data: Dict[str, Any] = {
            "filter": query or {},
            "sorts": sort or {},
            "start_cursor": cursor,
        }
        response = requests.post(url, headers=self.headers, data=data)
        return response

    def get(self, url: str, block_limit: int = BLOCK_LIMIT) -> List[Dict]:
        get_request = partial(self._get, url, block_limit=block_limit)
        return self._paginate(get_request)

    @validate_response
    def _get(
        self, url: str, cursor: Optional[str] = None, block_limit: int = BLOCK_LIMIT
    ) -> Response:
        params = {"page_size": f"{block_limit}", "cursor": cursor}
        response = requests.get(url, headers=self.headers, params=params)
        return response

    @staticmethod
    def _paginate(request: Callable) -> List[Dict[Any, Any]]:
        result = []
        cursor = None
        has_more = True
        while has_more:
            response = request(cursor=cursor)
            response = json.loads(response.text)
            has_more = response["has_more"]
            cursor = response["next_cursor"]
            result.extend(response["results"])
        return result


class NotionClient(NotionRequests):
    def __init__(self, token: str) -> None:
        super(NotionClient, self).__init__(token)
        self.token: str = self._ensure_valid_token(token)

    def _ensure_valid_token(self, token: str) -> str:
        if self._is_valid(token):
            return token
        raise InvalidNotionToken(
            f"Token {token[:4]}... is invalid. Check Notion integration."
        )

    @staticmethod
    def _is_valid(token: str) -> bool:
        print(token)
        print(8)
        return True
