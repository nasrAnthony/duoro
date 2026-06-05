from django.http import Http404
from django.shortcuts import render


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
