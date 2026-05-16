import os
from typing import Any, Dict, List, Optional
from urllib.parse import urljoin


class NotionTool:
    def __init__(self, token: Optional[str] = None, base_url: str = "https://api.notion.com/v1"):
        self.token = token or os.getenv("NOTION_TOKEN")
        self.base_url = base_url.rstrip("/")
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28",
        }

    def _request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        import requests

        url = urljoin(self.base_url + "/", endpoint.lstrip("/"))
        response = requests.request(
            method=method,
            url=url,
            headers=self.headers,
            json=data,
            params=params,
            timeout=30,
        )
        response.raise_for_status()
        return response.json()

    def search(
        self,
        query: str = "",
        filter_type: Optional[str] = None,
        page_size: int = 100,
    ) -> Dict[str, Any]:
        payload = {"page_size": page_size}
        if query:
            payload["query"] = query
        if filter_type:
            payload["filter"] = {"value": filter_type, "property": "object"}
        return self._request("POST", "/search", payload)

    def get_page(self, page_id: str) -> Dict[str, Any]:
        return self._request("GET", f"/pages/{page_id}")

    def create_page(
        self,
        parent: Dict[str, Any],
        properties: Dict[str, Any],
        children: Optional[List[Dict[str, Any]]] = None,
        icon: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        payload = {
            "parent": parent,
            "properties": properties,
        }
        if children:
            payload["children"] = children
        if icon:
            payload["icon"] = icon
        return self._request("POST", "/pages", payload)

    def update_page(
        self,
        page_id: str,
        properties: Dict[str, Any],
        archived: Optional[bool] = None,
        icon: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        payload = {"properties": properties}
        if archived is not None:
            payload["archived"] = archived
        if icon:
            payload["icon"] = icon
        return self._request("PATCH", f"/pages/{page_id}", payload)

    def get_database(self, database_id: str) -> Dict[str, Any]:
        return self._request("GET", f"/databases/{database_id}")

    def query_database(
        self,
        database_id: str,
        filter_obj: Optional[Dict[str, Any]] = None,
        sorts: Optional[List[Dict[str, Any]]] = None,
        page_size: int = 100,
        start_cursor: Optional[str] = None,
    ) -> Dict[str, Any]:
        payload = {"page_size": page_size}
        if filter_obj:
            payload["filter"] = filter_obj
        if sorts:
            payload["sorts"] = sorts
        if start_cursor:
            payload["start_cursor"] = start_cursor
        return self._request("POST", f"/databases/{database_id}/query", payload)

    def create_database(
        self,
        parent: Dict[str, Any],
        title: List[Dict[str, Any]],
        properties: Dict[str, Any],
    ) -> Dict[str, Any]:
        payload = {
            "parent": parent,
            "title": title,
            "properties": properties,
        }
        return self._request("POST", "/databases", payload)

    def update_database(
        self,
        database_id: str,
        title: Optional[List[Dict[str, Any]]] = None,
        properties: Optional[Dict[str, Any]] = None,
        description: Optional[List[Dict[str, Any]]] = None,
    ) -> Dict[str, Any]:
        payload = {}
        if title:
            payload["title"] = title
        if properties:
            payload["properties"] = properties
        if description:
            payload["description"] = description
        return self._request("PATCH", f"/databases/{database_id}", payload)

    def get_block_children(
        self,
        block_id: str,
        page_size: int = 100,
        start_cursor: Optional[str] = None,
    ) -> Dict[str, Any]:
        params = {"page_size": page_size}
        if start_cursor:
            params["start_cursor"] = start_cursor
        return self._request("GET", f"/blocks/{block_id}/children", params=params)

    def append_block_children(
        self,
        block_id: str,
        children: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        payload = {"children": children}
        return self._request("PATCH", f"/blocks/{block_id}/children", payload)

    def delete_block(self, block_id: str) -> Dict[str, Any]:
        return self._request("DELETE", f"/blocks/{block_id}")

    def get_user(self, user_id: str) -> Dict[str, Any]:
        return self._request("GET", f"/users/{user_id}")

    def list_users(
        self,
        page_size: int = 100,
        start_cursor: Optional[str] = None,
    ) -> Dict[str, Any]:
        params = {"page_size": page_size}
        if start_cursor:
            params["start_cursor"] = start_cursor
        return self._request("GET", "/users", params=params)

    def get_self(self) -> Dict[str, Any]:
        return self._request("GET", "/users/me")

    def rich_text(
        self,
        content: str,
        link: Optional[str] = None,
        bold: bool = False,
        italic: bool = False,
        code: bool = False,
    ) -> Dict[str, Any]:
        text = {"content": content}
        if link:
            text["link"] = {"url": link}
        annotations = {
            "bold": bold,
            "italic": italic,
            "strikethrough": False,
            "underline": False,
            "code": code,
            "color": "default",
        }
        return {"type": "text", "text": text, "annotations": annotations}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "authenticated": self.token is not None,
        }