"""GitHub tool for interacting with GitHub repositories and PRs."""

import os
import requests
from typing import Dict, Any, Optional

class GitHubTool:
    def __init__(self, token: Optional[str] = None):
        self.token = token or os.environ.get("GITHUB_TOKEN")
        self.base_url = "https://api.github.com"
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "Authorization": f"token {self.token}" if self.token else ""
        }

    def get_user_repos(self) -> list:
        """List repositories for the authenticated user."""
        response = requests.get(f"{self.base_url}/user/repos", headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_issues(self, owner: str, repo: str) -> list:
        """List issues for a specific repository."""
        response = requests.get(f"{self.base_url}/repos/{owner}/{repo}/issues", headers=self.headers)
        response.raise_for_status()
        return response.json()

    def execute(self, action: str, params: Dict[str, Any]) -> Dict[str, Any]:
        try:
            if action == "get_user_repos":
                return {"status": "success", "repos": self.get_user_repos()}
            elif action == "get_issues":
                return {"status": "success", "issues": self.get_issues(params.get("owner", ""), params.get("repo", ""))}
            else:
                return {"status": "error", "message": f"Unknown action: {action}"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
