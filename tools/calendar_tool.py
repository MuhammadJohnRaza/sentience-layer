import os
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional


class CalendarTool:
    def __init__(self, credentials_path: Optional[str] = None, token_path: Optional[str] = None):
        self.credentials_path = credentials_path or os.getenv("GOOGLE_CREDENTIALS_PATH")
        self.token_path = token_path or os.getenv("GOOGLE_TOKEN_PATH", "calendar_token.json")
        self.service = None
        self._authenticate()

    def _authenticate(self) -> None:
        try:
            from google.oauth2.credentials import Credentials
            from google_auth_oauthlib.flow import InstalledAppFlow
            from google.auth.transport.requests import Request
            from googleapiclient.discovery import build

            SCOPES = ["https://www.googleapis.com/auth/calendar"]

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

            self.service = build("calendar", "v3", credentials=creds)
        except ImportError:
            raise ImportError("Install google-api-python-client and google-auth-oauthlib")

    def list_calendars(self, min_access_role: str = "owner") -> List[Dict[str, Any]]:
        result = (
            self.service.calendarList()
            .list(minAccessRole=min_access_role)
            .execute()
        )
        return result.get("items", [])

    def get_calendar(self, calendar_id: str = "primary") -> Dict[str, Any]:
        return self.service.calendarList().get(calendarId=calendar_id).execute()

    def create_calendar(self, summary: str, description: Optional[str] = None, timezone: str = "UTC") -> Dict[str, Any]:
        body = {
            "summary": summary,
            "timeZone": timezone,
        }
        if description:
            body["description"] = description
        return self.service.calendars().insert(body=body).execute()

    def delete_calendar(self, calendar_id: str) -> None:
        self.service.calendars().delete(calendarId=calendar_id).execute()

    def list_events(
        self,
        calendar_id: str = "primary",
        time_min: Optional[datetime] = None,
        time_max: Optional[datetime] = None,
        max_results: int = 250,
        query: Optional[str] = None,
        single_events: bool = True,
        order_by: str = "startTime",
    ) -> List[Dict[str, Any]]:
        params = {
            "calendarId": calendar_id,
            "maxResults": max_results,
            "singleEvents": single_events,
            "orderBy": order_by,
        }
        if time_min:
            params["timeMin"] = time_min.isoformat()
        if time_max:
            params["timeMax"] = time_max.isoformat()
        if query:
            params["q"] = query

        result = self.service.events().list(**params).execute()
        return result.get("items", [])

    def get_event(self, event_id: str, calendar_id: str = "primary") -> Dict[str, Any]:
        return self.service.events().get(calendarId=calendar_id, eventId=event_id).execute()

    def create_event(
        self,
        summary: str,
        start: datetime,
        end: datetime,
        calendar_id: str = "primary",
        description: Optional[str] = None,
        location: Optional[str] = None,
        attendees: Optional[List[str]] = None,
        recurrence: Optional[List[str]] = None,
        reminders: Optional[Dict[str, Any]] = None,
        color_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        body = {
            "summary": summary,
            "start": {"dateTime": start.isoformat()},
            "end": {"dateTime": end.isoformat()},
        }
        if description:
            body["description"] = description
        if location:
            body["location"] = location
        if attendees:
            body["attendees"] = [{"email": e} for e in attendees]
        if recurrence:
            body["recurrence"] = recurrence
        if reminders:
            body["reminders"] = reminders
        if color_id:
            body["colorId"] = color_id

        return self.service.events().insert(calendarId=calendar_id, body=body).execute()

    def update_event(
        self,
        event_id: str,
        calendar_id: str = "primary",
        **kwargs: Any,
    ) -> Dict[str, Any]:
        event = self.get_event(event_id, calendar_id)
        for key, value in kwargs.items():
            if value is not None:
                event[key] = value
        return self.service.events().update(
            calendarId=calendar_id, eventId=event_id, body=event
        ).execute()

    def delete_event(self, event_id: str, calendar_id: str = "primary") -> None:
        self.service.events().delete(calendarId=calendar_id, eventId=event_id).execute()

    def quick_add(self, text: str, calendar_id: str = "primary") -> Dict[str, Any]:
        return (
            self.service.events()
            .quickAdd(calendarId=calendar_id, text=text)
            .execute()
        )

    def get_free_busy(
        self,
        time_min: datetime,
        time_max: datetime,
        calendar_ids: List[str],
        timezone: str = "UTC",
    ) -> Dict[str, Any]:
        body = {
            "timeMin": time_min.isoformat(),
            "timeMax": time_max.isoformat(),
            "timeZone": timezone,
            "items": [{"id": cid} for cid in calendar_ids],
        }
        return self.service.freebusy().query(body=body).execute()

    def list_colors(self) -> Dict[str, Any]:
        return self.service.colors().get().execute()

    def create_recurring_event(
        self,
        summary: str,
        start_time: datetime,
        duration_minutes: int,
        recurrence_rule: str,
        calendar_id: str = "primary",
        description: Optional[str] = None,
    ) -> Dict[str, Any]:
        end_time = start_time + timedelta(minutes=duration_minutes)
        return self.create_event(
            summary=summary,
            start=start_time,
            end=end_time,
            calendar_id=calendar_id,
            description=description,
            recurrence=[recurrence_rule],
        )

    def find_free_slot(
        self,
        duration_minutes: int,
        calendar_ids: Optional[List[str]] = None,
        search_start: Optional[datetime] = None,
        search_end: Optional[datetime] = None,
        work_start: int = 9,
        work_end: int = 17,
    ) -> Optional[datetime]:
        if not calendar_ids:
            calendar_ids = ["primary"]
        if not search_start:
            search_start = datetime.now()
        if not search_end:
            search_end = search_start + timedelta(days=7)

        busy_result = self.get_free_busy(search_start, search_end, calendar_ids)
        busy_periods = []
        for cal_id, cal_data in busy_result.get("calendars", {}).items():
            for period in cal_data.get("busy", []):
                busy_periods.append(
                    (
                        datetime.fromisoformat(period["start"].replace("Z", "+00:00")),
                        datetime.fromisoformat(period["end"].replace("Z", "+00:00")),
                    )
                )

        busy_periods.sort()
        current = search_start.replace(hour=work_start, minute=0, second=0, microsecond=0)
        if current < search_start:
            current = search_start

        while current < search_end:
            slot_end = current + timedelta(minutes=duration_minutes)
            if slot_end.hour > work_end or (slot_end.hour == work_end and slot_end.minute > 0):
                current = current.replace(hour=work_start, minute=0) + timedelta(days=1)
                continue

            is_free = True
            for start, end in busy_periods:
                if current < end and slot_end > start:
                    is_free = False
                    current = end
                    break

            if is_free:
                return current

            current = slot_end

        return None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "authenticated": self.service is not None,
        }