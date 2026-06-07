import json
from io import BytesIO
from unittest.mock import patch
from urllib.error import HTTPError

from django.test import TestCase, override_settings
from django.urls import reverse

from .views import GraphEmailError, post_request


class FakeResponse:
    def __init__(self, body):
        self.body = body

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return False

    def read(self):
        return self.body


@override_settings(
    MICROSOFT_TENANT_ID="tenant-id",
    MICROSOFT_CLIENT_ID="client-id",
    MICROSOFT_CLIENT_SECRET="client-secret",
    MICROSOFT_GRAPH_SCOPE="https://graph.microsoft.com/.default",
    MICROSOFT_GRAPH_SENDER="info@duoro.ca",
    MICROSOFT_GRAPH_SAVE_TO_SENT_ITEMS=True,
    CONTACT_EMAIL_RECIPIENTS=["info@duoro.ca"],
    CONTACT_EMAIL_SUBJECT_PREFIX="[Duoro]",
)
class ContactFormTests(TestCase):
    @patch("duoro.views.urlopen")
    def test_valid_contact_submission_sends_graph_email(self, mock_urlopen):
        mock_urlopen.side_effect = [
            FakeResponse(json.dumps({"access_token": "access-token"}).encode("utf-8")),
            FakeResponse(b""),
        ]

        response = self.client.post(
            reverse("contact"),
            {
                "name": "Tony",
                "email": "tony@example.com",
                "company": "Duoro",
                "details": "I need a new website.",
            },
        )

        self.assertRedirects(response, "/contact/#contact-form", fetch_redirect_response=False)
        self.assertEqual(mock_urlopen.call_count, 2)

        token_request = mock_urlopen.call_args_list[0].args[0]
        self.assertEqual(
            token_request.full_url,
            "https://login.microsoftonline.com/tenant-id/oauth2/v2.0/token",
        )
        self.assertIn(b"grant_type=client_credentials", token_request.data)

        send_request = mock_urlopen.call_args_list[1].args[0]
        self.assertEqual(
            send_request.full_url,
            "https://graph.microsoft.com/v1.0/users/info%40duoro.ca/sendMail",
        )

        payload = json.loads(send_request.data.decode("utf-8"))
        self.assertEqual(payload["message"]["toRecipients"][0]["emailAddress"]["address"], "info@duoro.ca")
        self.assertEqual(payload["message"]["replyTo"][0]["emailAddress"]["address"], "tony@example.com")
        self.assertIn("New inquiry from Tony", payload["message"]["subject"])
        self.assertIn("I need a new website.", payload["message"]["body"]["content"])

    @patch("duoro.views.urlopen")
    def test_invalid_contact_submission_does_not_send_email(self, mock_urlopen):
        response = self.client.post(
            reverse("contact"),
            {
                "name": "",
                "email": "not-an-email",
                "details": "",
            },
        )

        self.assertEqual(response.status_code, 200)
        mock_urlopen.assert_not_called()

    @patch("duoro.views.urlopen")
    def test_graph_http_error_includes_response_body(self, mock_urlopen):
        mock_urlopen.side_effect = HTTPError(
            url="https://login.microsoftonline.com/tenant-id/oauth2/v2.0/token",
            code=401,
            msg="Unauthorized",
            hdrs={},
            fp=BytesIO(b'{"error":"invalid_client"}'),
        )

        with self.assertRaisesMessage(GraphEmailError, "invalid_client"):
            post_request("https://example.com", b"", {})
