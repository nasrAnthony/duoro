import logging
import json
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen

from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ImproperlyConfigured
from django.http import Http404
from django.shortcuts import redirect, render

from .forms import ContactForm


logger = logging.getLogger(__name__)


PROJECTS = [
    {
        "slug": "ka-security",
        "label": "Project 1",
        "title": "K&A Solutions",
        "category": "Security Services",
        "summary": (
            "A professional website designed to present security services with clarity, "
            "authority, and a straightforward path to inquiry."
        ),
        "outcome": "Built to create trust quickly and make the service offer easy to understand.",
        "services": ["Web Design", "Development", "Business Presence"],
        "stack": ["Responsive UI", "Clear Service Structure", "Lead-focused Layout"],
        "live_url": "https://kasecurity.ca/",
        "image": "images/portfolio-entry-1/portfolio1.png",
        "image_alt": "Homepage preview for K&A Solutions",
        "combined_image": "images/portfolio-entry-1/combined-entry-1.png",
        "combined_image_alt": "Desktop and mobile website previews for K&A Solutions",
        "detail_image": "images/portfolio-entry-1/portfolio1-full-web-page.png",
        "detail_image_alt": "Full page website snapshot for K&A Solutions",
        "detail_note_title": "Support behind the scenes.",
        "detail_features": [
            "Fully Custom CRM",
            "Automated Tools",
            "Client Portal",
            "Inventory Tracking",
        ],
    },
    {
        "slug": "family-first-insurances",
        "label": "Project 2",
        "title": "Family First Insurances",
        "category": "Insurance Agency",
        "summary": (
            "A clean and reassuring insurance website shaped to feel approachable, "
            "organized, and easy for visitors to navigate."
        ),
        "outcome": "Designed to make a detail-heavy business feel simpler and more trustworthy.",
        "services": ["Web Design", "Content Structure", "Development"],
        "stack": ["Responsive Design", "Service-led Pages", "Conversion-minded Layout"],
        "live_url": "https://familyfirstinsurances.ca/",
        "image": "images/portfolio-entry-2/portfolio2.png",
        "image_alt": "Homepage preview for Family First Insurances",
        "combined_image": "images/portfolio-entry-2/combined-entry-2.png",
        "combined_image_alt": "Desktop and mobile website previews for Family First Insurances",
        "detail_image": "images/portfolio-entry-2/portfolio2-full-web-page.png",
        "detail_image_alt": "Full page website snapshot for Family First Insurances",
        "detail_note_title": "Built for trust and clarity.",
        "detail_features": [
            "Insurance Intake Flow",
            "Service-led Navigation",
            "Advisor Contact Paths",
            "Conversion-focused Layout",
        ],
    },
    {
        "slug": "inner-wheel-ottawa",
        "label": "Project 3",
        "title": "Inner Wheel Ottawa",
        "category": "Community Organization",
        "summary": (
            "A community-focused website created to share the organization's mission, "
            "activities, and public presence in a polished, easy-to-navigate way."
        ),
        "outcome": "Built with a calm, readable presentation suited to an organization audience.",
        "services": ["Web Design", "Development", "Organization Presence"],
        "stack": ["Responsive Layout", "Information Design", "Accessible Structure"],
        "live_url": "https://innerwheelottawa.com/",
        "image": "images/portfolio-entry-3/portfolio3.png",
        "image_alt": "Homepage preview for Inner Wheel Ottawa",
        "combined_image": "images/portfolio-entry-3/combined-entry-3.png",
        "combined_image_alt": "Desktop and mobile website previews for Inner Wheel Ottawa",
        "detail_image": "images/portfolio-entry-3/portfolio3-full-web-page.png",
        "detail_image_alt": "Full page website snapshot for Inner Wheel Ottawa",
        "detail_note_title": "Designed for communication.",
        "detail_features": [
            "Community-first Structure",
            "Readable Information Flow",
            "Event-friendly Layout",
            "Accessible Presentation",
        ],
    },
    {
        "slug": "mmg-contracting",
        "label": "Project 4",
        "title": "MMG Contracting",
        "category": "Contracting",
        "summary": (
            "A contracting website created to present the business clearly and give the brand "
            "a stronger, more polished online presence."
        ),
        "outcome": "Designed to showcase the company professionally and make the service offering easy to understand.",
        "services": ["Web Design", "Development", "Business Presence"],
        "stack": ["Responsive Layout", "Service-led Structure", "Clean Presentation"],
        "live_url": "",
        "image": "images/portfolio-entry-4/portfolio4.png",
        "image_alt": "Homepage preview for MMG Contracting",
        "combined_image": "images/portfolio-entry-4/combined-entry-4.png",
        "combined_image_alt": "Desktop and mobile website previews for MMG Contracting",
        "detail_image": "images/portfolio-entry-4/portfolio4-full-web-page.png",
        "detail_image_alt": "Full page website snapshot for MMG Contracting",
        "detail_note_title": "Built to present the brand professionally.",
        "detail_features": [
            "Service-focused Structure",
            "Responsive Build",
            "Clean Visual System",
            "Business-ready Presence",
        ],
    },
]


def portfolio(request):
    return render(request, "portfolio.html", {"projects": PROJECTS})


def portfolio_detail(request, slug):
    project = next((item for item in PROJECTS if item["slug"] == slug), None)
    if not project:
        raise Http404("Project not found")
    return render(request, "portfolio_detail.html", {"project": project})


def contact(request):
    form = ContactForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            if send_contact_email(form.cleaned_data):
                messages.success(request, "Thanks. Your inquiry has been sent.")
                return redirect("/contact/#contact-form")

            messages.error(
                request,
                "Sorry, the message could not be sent right now. Please email info@duoro.ca directly.",
            )
        else:
            messages.error(request, "Please check the form and try again.")
    else:
        form = ContactForm()

    return render(request, "contact.html", {"form": form})


def send_contact_email(data):
    recipients = settings.CONTACT_EMAIL_RECIPIENTS

    if not recipients:
        logger.error("Contact form email attempted without CONTACT_EMAIL_RECIPIENTS.")
        return False

    try:
        access_token = get_graph_access_token()
        send_graph_contact_email(access_token, data, recipients)
    except (ImproperlyConfigured, GraphEmailError, URLError, OSError) as error:
        logger.exception("Contact form email failed: %s", error)
        return False

    return True


class GraphEmailError(Exception):
    pass


def get_graph_access_token():
    required_settings = {
        "MICROSOFT_TENANT_ID": settings.MICROSOFT_TENANT_ID,
        "MICROSOFT_CLIENT_ID": settings.MICROSOFT_CLIENT_ID,
        "MICROSOFT_CLIENT_SECRET": settings.MICROSOFT_CLIENT_SECRET,
    }
    missing_settings = [name for name, value in required_settings.items() if not value]

    if missing_settings:
        raise ImproperlyConfigured(
            "Missing Microsoft Graph setting(s): " + ", ".join(missing_settings)
        )

    token_url = (
        "https://login.microsoftonline.com/"
        f"{quote(settings.MICROSOFT_TENANT_ID, safe='')}/oauth2/v2.0/token"
    )
    payload = urlencode(
        {
            "client_id": settings.MICROSOFT_CLIENT_ID,
            "client_secret": settings.MICROSOFT_CLIENT_SECRET,
            "scope": settings.MICROSOFT_GRAPH_SCOPE,
            "grant_type": "client_credentials",
        }
    ).encode("utf-8")
    response_data = post_request(
        token_url,
        payload,
        {"Content-Type": "application/x-www-form-urlencoded"},
    )
    token = response_data.get("access_token")

    if not token:
        raise GraphEmailError("Microsoft token response did not include access_token.")

    return token


def send_graph_contact_email(access_token, data, recipients):
    sender = settings.MICROSOFT_GRAPH_SENDER

    if not sender:
        raise ImproperlyConfigured("MICROSOFT_GRAPH_SENDER must be set.")

    subject = f"{settings.CONTACT_EMAIL_SUBJECT_PREFIX} New inquiry from {data['name']}"
    company = data.get("company") or "Not provided"
    body = (
        "New Duoro website inquiry\n\n"
        f"Name: {data['name']}\n"
        f"Email: {data['email']}\n"
        f"Company: {company}\n\n"
        "Project details:\n"
        f"{data['details']}\n"
    )
    payload = {
        "message": {
            "subject": subject,
            "body": {
                "contentType": "Text",
                "content": body,
            },
            "toRecipients": email_recipients(recipients),
            "replyTo": email_recipients([data["email"]]),
        },
        "saveToSentItems": settings.MICROSOFT_GRAPH_SAVE_TO_SENT_ITEMS,
    }
    send_url = f"https://graph.microsoft.com/v1.0/users/{quote(sender, safe='')}/sendMail"

    post_request(
        send_url,
        json.dumps(payload).encode("utf-8"),
        {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        },
        expect_json=False,
    )


def email_recipients(addresses):
    return [
        {
            "emailAddress": {
                "address": address,
            },
        }
        for address in addresses
    ]


def post_request(url, data, headers, expect_json=True):
    request = Request(url, data=data, headers=headers, method="POST")

    try:
        with urlopen(request, timeout=20) as response:
            response_body = response.read().decode("utf-8")
    except HTTPError as error:
        response_body = error.read().decode("utf-8", errors="replace")
        raise GraphEmailError(
            f"Microsoft request failed with HTTP {error.code}: {response_body}"
        ) from error

    if not expect_json:
        return {}

    try:
        return json.loads(response_body)
    except json.JSONDecodeError as error:
        raise GraphEmailError("Microsoft Graph response was not valid JSON.") from error
