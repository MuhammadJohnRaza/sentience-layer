import os
import json
import base64
from typing import Any, Dict, List, Optional
from urllib.parse import urljoin


class JiraTool:
    def __init__(
        self,
        base_url: Optional[str] = None,
        email: Optional[str] = None,
        token: Optional[str] = None,
    ):
        self.base_url = (base_url or os.getenv("JIRA_BASE_URL", "")).rstrip("/")
        self.email = email or os.getenv("JIRA_EMAIL")
        self.token = token or os.getenv("JIRA_API_TOKEN")
        
        credentials = f"{self.email}:{self.token}"
        encoded = base64.b64encode(credentials.encode()).decode()
        self.headers = {
            "Authorization": f"Basic {encoded}",
            "Content-Type": "application/json",
            "Accept": "application/json",
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
        if response.status_code == 204:
            return {"success": True}
        return response.json()

    def get_issue(self, issue_key: str, fields: Optional[List[str]] = None) -> Dict[str, Any]:
        params = {}
        if fields:
            params["fields"] = ",".join(fields)
        return self._request("GET", f"/rest/api/3/issue/{issue_key}", params=params)

    def search_issues(
        self,
        jql: str,
        start_at: int = 0,
        max_results: int = 50,
        fields: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        payload = {
            "jql": jql,
            "startAt": start_at,
            "maxResults": max_results,
        }
        if fields:
            payload["fields"] = fields
        return self._request("POST", "/rest/api/3/search", payload)

    def create_issue(
        self,
        project_key: str,
        summary: str,
        issue_type: str = "Task",
        description: Optional[str] = None,
        priority: Optional[str] = None,
        assignee: Optional[str] = None,
        labels: Optional[List[str]] = None,
        components: Optional[List[str]] = None,
        parent: Optional[str] = None,
    ) -> Dict[str, Any]:
        fields = {
            "project": {"key": project_key},
            "summary": summary,
            "issuetype": {"name": issue_type},
        }
        
        if description:
            fields["description"] = {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [{"type": "text", "text": description}],
                    }
                ],
            }
        
        if priority:
            fields["priority"] = {"name": priority}
        if assignee:
            fields["assignee"] = {"id": assignee} if assignee.startswith("5") else {"name": assignee}
        if labels:
            fields["labels"] = labels
        if components:
            fields["components"] = [{"name": c} for c in components]
        if parent:
            fields["parent"] = {"key": parent}

        return self._request("POST", "/rest/api/3/issue", {"fields": fields})

    def update_issue(
        self,
        issue_key: str,
        summary: Optional[str] = None,
        description: Optional[str] = None,
        priority: Optional[str] = None,
        assignee: Optional[str] = None,
        status: Optional[str] = None,
        labels: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        fields = {}
        if summary:
            fields["summary"] = summary
        if description:
            fields["description"] = {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [{"type": "text", "text": description}],
                    }
                ],
            }
        if priority:
            fields["priority"] = {"name": priority}
        if assignee:
            fields["assignee"] = {"id": assignee} if assignee.startswith("5") else {"name": assignee}
        if labels:
            fields["labels"] = labels

        result = self._request("PUT", f"/rest/api/3/issue/{issue_key}", {"fields": fields})

        if status:
            transitions = self.get_transitions(issue_key)
            for t in transitions:
                if t.get("name", "").lower() == status.lower():
                    self._request(
                        "POST",
                        f"/rest/api/3/issue/{issue_key}/transitions",
                        {"transition": {"id": t["id"]}},
                    )
                    break

        return result

    def delete_issue(self, issue_key: str) -> Dict[str, Any]:
        return self._request("DELETE", f"/rest/api/3/issue/{issue_key}")

    def get_transitions(self, issue_key: str) -> List[Dict[str, Any]]:
        result = self._request("GET", f"/rest/api/3/issue/{issue_key}/transitions")
        return result.get("transitions", [])

    def transition_issue(self, issue_key: str, transition_id: str, comment: Optional[str] = None) -> Dict[str, Any]:
        payload = {"transition": {"id": transition_id}}
        if comment:
            payload["update"] = {
                "comment": [{"add": {"body": comment}}]
            }
        return self._request("POST", f"/rest/api/3/issue/{issue_key}/transitions", payload)

    def add_comment(self, issue_key: str, body: str) -> Dict[str, Any]:
        payload = {
            "body": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [{"type": "text", "text": body}],
                    }
                ],
            }
        }
        return self._request("POST", f"/rest/api/3/issue/{issue_key}/comment", payload)

    def get_comments(self, issue_key: str) -> List[Dict[str, Any]]:
        result = self._request("GET", f"/rest/api/3/issue/{issue_key}/comment")
        return result.get("comments", [])

    def get_projects(self, expand: Optional[str] = None) -> List[Dict[str, Any]]:
        params = {}
        if expand:
            params["expand"] = expand
        result = self._request("GET", "/rest/api/3/project", params=params)
        return result if isinstance(result, list) else []

    def get_project(self, project_key: str) -> Dict[str, Any]:
        return self._request("GET", f"/rest/api/3/project/{project_key}")

    def get_boards(self, project_key: Optional[str] = None) -> List[Dict[str, Any]]:
        params = {}
        if project_key:
            params["projectKeyOrId"] = project_key
        result = self._request("GET", "/rest/agile/1.0/board", params=params)
        return result.get("values", [])

    def get_sprints(self, board_id: int, state: str = "active,future") -> List[Dict[str, Any]]:
        params = {"state": state}
        result = self._request("GET", f"/rest/agile/1.0/board/{board_id}/sprint", params=params)
        return result.get("values", [])

    def get_sprint_issues(self, sprint_id: int) -> List[Dict[str, Any]]:
        result = self._request("GET", f"/rest/agile/1.0/sprint/{sprint_id}/issue")
        return result.get("issues", [])

    def get_user(self, account_id: str) -> Dict[str, Any]:
        params = {"accountId": account_id}
        return self._request("GET", "/rest/api/3/user", params=params)

    def get_current_user(self) -> Dict[str, Any]:
        return self._request("GET", "/rest/api/3/myself")

    def get_worklog(self, issue_key: str) -> List[Dict[str, Any]]:
        result = self._request("GET", f"/rest/api/3/issue/{issue_key}/worklog")
        return result.get("worklogs", [])

    def add_worklog(
        self,
        issue_key: str,
        time_spent: str,
        started: Optional[str] = None,
        comment: Optional[str] = None,
    ) -> Dict[str, Any]:
        payload = {"timeSpent": time_spent}
        if started:
            payload["started"] = started
        if comment:
            payload["comment"] = comment
        return self._request("POST", f"/rest/api/3/issue/{issue_key}/worklog", payload)

    def get_filters(self, favorites: bool = False) -> List[Dict[str, Any]]:
        params = {"favorites": str(favorites).lower()}
        result = self._request("GET", "/rest/api/3/filter/search", params=params)
        return result.get("values", [])

    def get_issue_types(self, project_key: Optional[str] = None) -> List[Dict[str, Any]]:
        if project_key:
            result = self._request("GET", f"/rest/api/3/issue/createmeta/{project_key}/issuetypes")
            return result.get("values", [])
        result = self._request("GET", "/rest/api/3/issuetype")
        return result if isinstance(result, list) else []

    def get_fields(self) -> List[Dict[str, Any]]:
        return self._request("GET", "/rest/api/3/field")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "base_url": self.base_url,
            "authenticated": self.email is not None and self.token is not None,
        }