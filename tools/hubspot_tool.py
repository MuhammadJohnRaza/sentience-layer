"""HubSpot tool for interacting with CRM contacts and deals."""

import os
import requests
from typing import Dict, Any, Optional

class HubSpotTool:
    def __init__(self, access_token: Optional[str] = None):
        self.access_token = access_token or os.environ.get("HUBSPOT_ACCESS_TOKEN")
        self.base_url = "https://api.hubapi.com/crm/v3"
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

    def get_contacts(self, limit: int = 10) -> list:
        """Fetch list of HubSpot contacts."""
        url = f"{self.base_url}/objects/contacts?limit={limit}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json().get("results", [])

    def execute(self, action: str, params: Dict[str, Any]) -> Dict[str, Any]:
        try:
            if action == "get_contacts":
                return {"status": "success", "contacts": self.get_contacts(params.get("limit", 10))}
            else:
                return {"status": "error", "message": f"Unknown action: {action}"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
