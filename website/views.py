from django.shortcuts import render
from notes.models import Note
from django.db.models import Count


def home(request):
    """
    Home page view with responsive optimizations and enhanced context.
    """
    context = {}

    # Get public notes with user info and engagement metrics
    context["public_notes"] = (
        Note.objects.select_related("user")
        .filter(is_public=True)
        .order_by("-created_at")[:6]
    )

    # Get user's notes with stats if logged in
    if request.user.is_authenticated:
        user_notes = Note.objects.filter(user=request.user)
        context["user_notes"] = user_notes.order_by("-created_at")[:10]
        context["stats"] = {
            "total_notes": user_notes.count(),
            "public_notes": user_notes.filter(is_public=True).count(),
            "private_notes": user_notes.filter(is_public=False).count(),
        }

    # Add PWA and mobile-specific metadata
    context["meta"] = {
        "title": "Notes App - Capture Your Thoughts",
        "description": "Access your notes anywhere, anytime",
        "viewport": "width=device-width, initial-scale=1, maximum-scale=5",
        "theme_color": "#0d6efd",  # Bootstrap primary color
        "mobile_app": True,
    }

    return render(request, "website/home.html", context)


def about(request):
    """About page with app info."""
    return render(
        request,
        "website/about.html",
        {
            "meta": {
                "title": "About Notes App",
                "description": "Learn about our note-taking app",
                "mobile_app": True,
            }
        },
    )


def contact(request):
    """Mobile-optimized contact page."""
    return render(
        request,
        "website/contact.html",
        {
            "meta": {
                "title": "Contact Us",
                "description": "Get in touch with Notes App support",
                "mobile_app": True,
            }
        },
    )


def terms(request):
    """Terms page with mobile view."""
    return render(
        request,
        "website/terms.html",
        {
            "meta": {
                "title": "Terms of Service",
                "description": "Notes App terms and conditions",
                "mobile_app": True,
            }
        },
    )


def privacy(request):
    """Privacy policy with mobile optimization."""
    return render(
        request,
        "website/privacy.html",
        {
            "meta": {
                "title": "Privacy Policy",
                "description": "How we protect your data",
                "mobile_app": True,
            }
        },
    )


def faq(request):
    """FAQ page with mobile-friendly layout."""
    return render(
        request,
        "website/faq.html",
        {
            "meta": {
                "title": "Frequently Asked Questions",
                "description": "Get answers about Notes App",
                "mobile_app": True,
            }
        },
    )
