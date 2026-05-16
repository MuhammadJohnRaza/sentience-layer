import os
import json
from typing import Any, Dict, List, Optional
from urllib.parse import urljoin


class SlackTool:
    def __init__(self, token: Optional[str] = None, base_url: str = "https://slack.com/api"):
        self.token = token or os.getenv("SLACK_BOT_TOKEN")
        self.base_url = base_url.rstrip("/")
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json; charset=utf-8",
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
        result = response.json()
        if not result.get("ok"):
            error = result.get("error", "unknown_error")
            raise Exception(f"Slack API error: {error}")
        return result

    def post_message(
        self,
        channel: str,
        text: str,
        blocks: Optional[List[Dict[str, Any]]] = None,
        thread_ts: Optional[str] = None,
        unfurl_links: bool = False,
    ) -> Dict[str, Any]:
        payload = {
            "channel": channel,
            "text": text,
            "unfurl_links": unfurl_links,
        }
        if blocks:
            payload["blocks"] = blocks
        if thread_ts:
            payload["thread_ts"] = thread_ts
        return self._request("POST", "/chat.postMessage", payload)

    def update_message(
        self,
        channel: str,
        ts: str,
        text: Optional[str] = None,
        blocks: Optional[List[Dict[str, Any]]] = None,
    ) -> Dict[str, Any]:
        payload = {
            "channel": channel,
            "ts": ts,
        }
        if text:
            payload["text"] = text
        if blocks:
            payload["blocks"] = blocks
        return self._request("POST", "/chat.update", payload)

    def delete_message(self, channel: str, ts: str) -> Dict[str, Any]:
        payload = {
            "channel": channel,
            "ts": ts,
        }
        return self._request("POST", "/chat.delete", payload)

    def get_conversation_history(
        self,
        channel: str,
        limit: int = 100,
        cursor: Optional[str] = None,
        oldest: Optional[str] = None,
        latest: Optional[str] = None,
    ) -> Dict[str, Any]:
        params = {
            "channel": channel,
            "limit": min(limit, 200),
        }
        if cursor:
            params["cursor"] = cursor
        if oldest:
            params["oldest"] = oldest
        if latest:
            params["latest"] = latest
        return self._request("GET", "/conversations.history", params=params)

    def get_thread_replies(
        self,
        channel: str,
        thread_ts: str,
        limit: int = 100,
    ) -> Dict[str, Any]:
        params = {
            "channel": channel,
            "ts": thread_ts,
            "limit": min(limit, 200),
        }
        return self._request("GET", "/conversations.replies", params=params)

    def list_channels(
        self,
        types: str = "public_channel,private_channel",
        exclude_archived: bool = True,
        limit: int = 200,
    ) -> List[Dict[str, Any]]:
        params = {
            "types": types,
            "exclude_archived": exclude_archived,
            "limit": limit,
        }
        result = self._request("GET", "/conversations.list", params=params)
        return result.get("channels", [])

    def get_channel_info(self, channel: str) -> Dict[str, Any]:
        params = {"channel": channel}
        return self._request("GET", "/conversations.info", params=params)

    def join_channel(self, channel: str) -> Dict[str, Any]:
        payload = {"channel": channel}
        return self._request("POST", "/conversations.join", payload)

    def leave_channel(self, channel: str) -> Dict[str, Any]:
        payload = {"channel": channel}
        return self._request("POST", "/conversations.leave", payload)

    def invite_to_channel(
        self,
        channel: str,
        users: List[str],
    ) -> Dict[str, Any]:
        payload = {
            "channel": channel,
            "users": ",".join(users),
        }
        return self._request("POST", "/conversations.invite", payload)

    def upload_file(
        self,
        channels: List[str],
        file_path: Optional[str] = None,
        content: Optional[str] = None,
        filename: Optional[str] = None,
        title: Optional[str] = None,
        initial_comment: Optional[str] = None,
    ) -> Dict[str, Any]:
        import requests

        url = urljoin(self.base_url + "/", "/files.upload")
        data = {
            "channels": ",".join(channels),
        }
        if initial_comment:
            data["initial_comment"] = initial_comment
        if title:
            data["title"] = title

        files = None
        if file_path:
            files = {"file": open(file_path, "rb")}
            if filename:
                data["filename"] = filename
        elif content:
            data["content"] = content
            if filename:
                data["filename"] = filename

        response = requests.post(
            url,
            headers={"Authorization": f"Bearer {self.token}"},
            data=data,
            files=files,
            timeout=60,
        )
        result = response.json()
        if not result.get("ok"):
            raise Exception(f"Slack upload error: {result.get('error')}")
        return result

    def get_user_info(self, user: str) -> Dict[str, Any]:
        params = {"user": user}
        return self._request("GET", "/users.info", params=params)

    def list_users(
        self,
        cursor: Optional[str] = None,
        limit: int = 200,
        team_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        params = {"limit": limit}
        if cursor:
            params["cursor"] = cursor
        if team_id:
            params["team_id"] = team_id
        return self._request("GET", "/users.list", params=params)

    def set_user_status(
        self,
        user: str,
        text: str,
        emoji: str,
        expiration: Optional[int] = None,
    ) -> Dict[str, Any]:
        profile = {
            "status_text": text,
            "status_emoji": emoji,
        }
        if expiration:
            profile["status_expiration"] = expiration
        payload = {
            "user": user,
            "profile": json.dumps(profile),
        }
        return self._request("POST", "/users.profile.set", payload)

    def schedule_message(
        self,
        channel: str,
        text: str,
        post_at: int,
        blocks: Optional[List[Dict[str, Any]]] = None,
    ) -> Dict[str, Any]:
        payload = {
            "channel": channel,
            "text": text,
            "post_at": post_at,
        }
        if blocks:
            payload["blocks"] = blocks
        return self._request("POST", "/chat.scheduleMessage", payload)

    def search_messages(
        self,
        query: str,
        sort: str = "score",
        sort_dir: str = "desc",
        count: int = 20,
    ) -> Dict[str, Any]:
        params = {
            "query": query,
            "sort": sort,
            "sort_dir": sort_dir,
            "count": count,
        }
        return self._request("GET", "/search.messages", params=params)

    def react_to_message(
        self,
        channel: str,
        timestamp: str,
        name: str,
    ) -> Dict[str, Any]:
        payload = {
            "channel": channel,
            "timestamp": timestamp,
            "name": name,
        }
        return self._request("POST", "/reactions.add", payload)

    def open_modal(
        self,
        trigger_id: str,
        view: Dict[str, Any],
    ) -> Dict[str, Any]:
        payload = {
            "trigger_id": trigger_id,
            "view": view,
        }
        return self._request("POST", "/views.open", payload)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "authenticated": self.token is not None,
        }