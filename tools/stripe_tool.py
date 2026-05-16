"""Stripe tool for fetching payments, customers, and subscriptions."""

import os
import stripe
from typing import Dict, Any, Optional

class StripeTool:
    def __init__(self, api_key: Optional[str] = None):
        stripe.api_key = api_key or os.environ.get("STRIPE_API_KEY")

    def list_customers(self, limit: int = 10) -> list:
        """List Stripe customers."""
        return stripe.Customer.list(limit=limit).get('data', [])

    def list_charges(self, limit: int = 10) -> list:
        """List recent charges."""
        return stripe.Charge.list(limit=limit).get('data', [])

    def execute(self, action: str, params: Dict[str, Any]) -> Dict[str, Any]:
        try:
            if action == "list_customers":
                return {"status": "success", "customers": self.list_customers(params.get("limit", 10))}
            elif action == "list_charges":
                return {"status": "success", "charges": self.list_charges(params.get("limit", 10))}
            else:
                return {"status": "error", "message": f"Unknown action: {action}"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
