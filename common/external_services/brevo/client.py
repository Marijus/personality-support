import logging
from urllib.parse import quote

import requests


class BrevoClient:
    api_key: str

    def __init__(self, api_key: str):
        self.api_key = api_key

    def create_contact(self, email: str, attributes, list_id: str | None = None):
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "api-key": self.api_key,
        }

        data = {
            "email": email,
        }
        if list_id:
            data["listIds"] = [list_id]

        if attributes:
            data["attributes"] = attributes

        response = requests.post("https://api.brevo.com/v3/contacts", json=data, headers=headers, timeout=5)
        self._handle_response(response)

    def remove_contact_from_list(self, list_id: int, email: str):
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "api-key": self.api_key,
        }
        payload = {"emails": [email]}
        response = requests.post(
            f"https://api.brevo.com/v3/contacts/lists/{list_id}/contacts/remove",
            json=payload,
            headers=headers,
        )
        self._handle_response(response)

    def add_contact_to_list(self, list_id: int, email: str):
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "api-key": self.api_key,
        }
        payload = {"emails": [email]}

        response = requests.post(
            f"https://api.brevo.com/v3/contacts/lists/{list_id}/contacts/add",
            json=payload,
            headers=headers,
            timeout=5,
        )
        self._handle_response(response)

    def update_brevo_contact_attribute(self, email: str, attribute: str, value):
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "api-key": self.api_key,
        }
        identifier = quote(email, safe="")
        url = f"https://api.brevo.com/v3/contacts/{identifier}"

        payload = {
            "attributes": {
                attribute: value
            }
        }

        response = requests.put(url, json=payload, headers=headers, timeout=5)
        self._handle_response(response)

    def send_email(self, from_email: str, emails: list[str], subject: str, email_html: str, reply_to=None, in_reply_to=None, attachments=None):
        url = "https://api.brevo.com/v3/smtp/email"

        domain = from_email.split("@")[1]

        data = {
            "sender": {
                "name": f"{domain} support",
                "email": from_email
            },
            "to": [{"email": email} for email in emails],
            "subject": subject,
            "htmlContent": email_html,
        }
        if reply_to:
            data["replyTo"] = {
                "email": reply_to,
            }
        if in_reply_to:
            data["headers"] = {
                "In-Reply-To": in_reply_to,
                "References": in_reply_to
            }
        if attachments:
            data["attachment"] = attachments

        headers = {
            'accept': 'application/json',
            'api-key': self.api_key,
            'content-type': 'application/json'
        }

        email_timeout = 30 if attachments else 5
        response = requests.request("POST", url, headers=headers, json=data, timeout=email_timeout)
        self._handle_response(response)

    def _handle_response(self, response: requests.Response):
        if not response.ok:
            raise requests.HTTPError(
                f"HTTP {response.status_code}: {response.text}",
                response=response
            )
