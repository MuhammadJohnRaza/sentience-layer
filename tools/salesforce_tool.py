"""Salesforce tool for interacting with leads, contacts, and opportunities."""

import os
from simple_salesforce import Salesforce
from typing import Dict, Any, Optional

class SalesforceTool:
    def __init__(self, username: Optional[str] = None, password: Optional[str] = None, security_token: Optional[str] = None):
        self.username = username or os.environ.get("SF_USERNAME")
        self.password = password or os.environ.get("SF_PASSWORD")
        self.security_token = security_token or os.environ.get("SF_SECURITY_TOKEN")
        
        if self.username and self.password and self.security_token:
            self.sf = Salesforce(username=self.username, password=self.password, security_token=self.security_token)
        else:
            self.sf = None

    def get_recent_leads(self, limit: int = 10) -> list:
        if not self.sf:
            raise ValueError("Salesforce credentials not provided.")
        return self.sf.query(f"SELECT Id, Name, Company, Email FROM Lead ORDER BY CreatedDate DESC LIMIT {limit}")['records']

    def execute(self, action: str, params: Dict[str, Any]) -> Dict[str, Any]:
        try:
            if action == "get_recent_leads":
                return {"status": "success", "leads": self.get_recent_leads(params.get("limit", 10))}
            else:
                return {"status": "error", "message": f"Unknown action: {action}"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
