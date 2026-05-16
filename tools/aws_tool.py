"""AWS tool for interacting with AWS services."""

import boto3
from typing import Dict, Any, Optional

class AWSTool:
    def __init__(self, region_name: str = "us-east-1"):
        self.region_name = region_name
        # Note: Relies on standard boto3 credential resolution (env vars, IAM roles)
        self.s3_client = boto3.client("s3", region_name=self.region_name)
        self.ec2_client = boto3.client("ec2", region_name=self.region_name)

    def list_s3_buckets(self) -> list:
        """List all S3 buckets."""
        response = self.s3_client.list_buckets()
        return [bucket["Name"] for bucket in response.get("Buckets", [])]

    def describe_ec2_instances(self) -> list:
        """Describe EC2 instances."""
        response = self.ec2_client.describe_instances()
        instances = []
        for reservation in response.get("Reservations", []):
            instances.extend(reservation.get("Instances", []))
        return instances

    def execute(self, action: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a specific AWS action."""
        try:
            if action == "list_buckets":
                return {"status": "success", "buckets": self.list_s3_buckets()}
            elif action == "describe_instances":
                return {"status": "success", "instances": self.describe_ec2_instances()}
            else:
                return {"status": "error", "message": f"Unknown action: {action}"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
