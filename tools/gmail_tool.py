import os
import base64
import json
from typing import Any, Dict, List, Optional
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders


class GmailTool:
    def __init__(self, credentials_path: Optional[str] = None, token_path: Optional[str] = None):
        self.credentials_path = credentials_path or os.getenv("GMAIL_CREDENTIALS_PATH")
        self.token_path = token_path or os.getenv("GMAIL_TOKEN_PATH", "token.json")
        self.service = None
        self._authenticate()

    def _authenticate(self) -> None:
        try:
            from google.oauth2.credentials import Credentials
            from google_auth_oauthlib.flow import InstalledAppFlow
            from google.auth.transport.requests import Request
            from googleapiclient.discovery import build

            SCOPES = [
                "https://www.googleapis.com/auth/gmail.modify",
                "https://www.googleapis.com/auth/gmail.readonly",
            ]

            creds = None
            if os.path.exists(self.token_path):
                creds = Credentials.from_authorized_user_file(self.token_path, SCOPES)

            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        self.credentials_path, SCOPES
                    )
                    creds = flow.run_local_server(port=0)
                with open(self.token_path, "w") as token:
                    token.write(creds.to_json())

            self.service = build("gmail", "v1", credentials=creds)
        except ImportError:
            raise ImportError("Install google-api-python-client and google-auth-oauthlib")

    def list_messages(
        self,
        query: str = "",
        max_results: int = 100,
        label_ids: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        params = {"userId": "me", "q": query, "maxResults": max_results}
        if label_ids:
            params["labelIds"] = label_ids
        result = self.service.users().messages().list(**params).execute()
        return result.get("messages", [])

    def get_message(self, message_id: str, format: str = "full") -> Dict[str, Any]:
        return (
            self.service.users()
            .messages()
            .get(userId="me", id=message_id, format=format)
            .execute()
        )

    def get_thread(self, thread_id: str) -> Dict[str, Any]:
        return self.service.users().threads().get(userId="me", id=thread_id).execute()

    def send_message(
        self,
        to: str,
        subject: str,
        body: str,
        html: Optional[str] = None,
        cc: Optional[List[str]] = None,
        bcc: Optional[List[str]] = None,
        attachments: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        message = MIMEMultipart("alternative") if html else MIMEMultipart()
        message["to"] = to
        message["subject"] = subject
        if cc:
            message["cc"] = ", ".join(cc)
        if bcc:
            message["bcc"] = ", ".join(bcc)

        message.attach(MIMEText(body, "plain"))
        if html:
            message.attach(MIMEText(html, "html"))

        if attachments:
            for file_path in attachments:
                with open(file_path, "rb") as f:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header(
                    "Content-Disposition",
                    f'attachment; filename="{os.path.basename(file_path)}"',
                )
                message.attach(part)

        raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
        body = {"raw": raw}
        return self.service.users().messages().send(userId="me", body=body).execute()

    def draft_message(
        self,
        to: str,
        subject: str,
        body: str,
        html: Optional[str] = None,
    ) -> Dict[str, Any]:
        message = MIMEText(html or body, "html" if html else "plain")
        message["to"] = to
        message["subject"] = subject
        raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
        draft = {"message": {"raw": raw}}
        return self.service.users().drafts().create(userId="me", body=draft).execute()

    def modify_labels(
        self,
        message_id: str,
        add_labels: Optional[List[str]] = None,
        remove_labels: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        body = {}
        if add_labels:
            body["addLabelIds"] = add_labels
        if remove_labels:
            body["removeLabelIds"] = remove_labels
        return (
            self.service.users()
            .messages()
            .modify(userId="me", id=message_id, body=body)
            .execute()
        )

    def trash_message(self, message_id: str) -> Dict[str, Any]:
        return self.service.users().messages().trash(userId="me", id=message_id).execute()

    def untrash_message(self, message_id: str) -> Dict[str, Any]:
        return self.service.users().messages().untrash(userId="me", id=message_id).execute()

    def delete_message(self, message_id: str) -> None:
        self.service.users().messages().delete(userId="me", id=message_id).execute()

    def list_labels(self) -> List[Dict[str, Any]]:
        result = self.service.users().labels().list(userId="me").execute()
        return result.get("labels", [])

    def create_label(
        self,
        name: str,
        label_list_visibility: str = "labelShow",
        message_list_visibility: str = "show",
    ) -> Dict[str, Any]:
        body = {
            "name": name,
            "labelListVisibility": label_list_visibility,
            "messageListVisibility": message_list_visibility,
        }
        return self.service.users().labels().create(userId="me", body=body).execute()

    def get_profile(self) -> Dict[str, Any]:
        return self.service.users().getProfile(userId="me").execute()

    def search_threads(self, query: str = "", max_results: int = 100) -> List[Dict[str, Any]]:
        result = (
            self.service.users()
            .threads()
            .list(userId="me", q=query, maxResults=max_results)
            .execute()
        )
        return result.get("threads", [])

    def batch_modify(
        self,
        message_ids: List[str],
        add_labels: Optional[List[str]] = None,
        remove_labels: Optional[List[str]] = None,
    ) -> None:
        body = {"ids": message_ids}
        if add_labels:
            body["addLabelIds"] = add_labels
        if remove_labels:
            body["removeLabelIds"] = remove_labels
        self.service.users().messages().batchModify(userId="me", body=body).execute()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "authenticated": self.service is not None,
        }