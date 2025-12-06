from django.shortcuts import render, redirect
from notes.models import Note
from django.db.models import Count
from django.contrib import messages
from .forms import ContactForm, NewsletterForm
from .models import ContactSubmission, NewsletterSubscription


def home(request):
    """
    Home page view with responsive optimizations and enhanced context.
    """
    context = {}

    # Handle newsletter subscription form
    if request.method == "POST" and "newsletter_submit" in request.POST:
        form = NewsletterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            # Check if already subscribed
            subscription, created = NewsletterSubscription.objects.get_or_create(
                email=email, defaults={"is_active": True}
            )

            if created:
                messages.success(
                    request, "Thank you for subscribing to our newsletter!"
                )
            else:
                if not subscription.is_active:
                    subscription.is_active = True
                    subscription.save()
                    messages.success(request, "Your subscription has been reactivated!")
                else:
                    messages.info(
                        request, "You're already subscribed to our newsletter."
                    )

            return redirect("website:home")
    else:
        form = NewsletterForm()

    context["newsletter_form"] = form

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

        # Add following information for follow buttons
        from accounts.models import Follow

        following_ids = Follow.objects.filter(follower=request.user).values_list(
            "followed_id", flat=True
        )
        context["following_ids"] = list(following_ids)

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
    # Handle newsletter subscription form
    if request.method == "POST" and "newsletter_submit" in request.POST:
        form = NewsletterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            # Check if already subscribed
            subscription, created = NewsletterSubscription.objects.get_or_create(
                email=email, defaults={"is_active": True}
            )

            if created:
                messages.success(
                    request, "Thank you for subscribing to our newsletter!"
                )
            else:
                if not subscription.is_active:
                    subscription.is_active = True
                    subscription.save()
                    messages.success(request, "Your subscription has been reactivated!")
                else:
                    messages.info(
                        request, "You're already subscribed to our newsletter."
                    )

            return redirect("website:about")
    else:
        form = NewsletterForm()

    context = {
        "newsletter_form": form,
        "meta": {
            "title": "About Notes App",
            "description": "Learn about our note-taking app",
            "mobile_app": True,
        },
    }

    return render(request, "website/about.html", context)


def contact(request):
    """
    Contact page with form handling.

    Processes contact form submissions and displays success/error messages.
    """
    if request.method == "POST":
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            # Save the contact submission
            ContactSubmission.objects.create(
                name=contact_form.cleaned_data["name"],
                email=contact_form.cleaned_data["email"],
                subject=contact_form.cleaned_data["subject"],
                message=contact_form.cleaned_data["message"],
                status="new",
            )

            messages.success(
                request,
                "Thank you! Your message has been sent successfully. We'll get back to you soon.",
            )
            return redirect("website:contact")
    else:
        contact_form = ContactForm()

    # Handle newsletter subscription form
    if request.method == "POST" and "newsletter_submit" in request.POST:
        newsletter_form = NewsletterForm(request.POST)
        if newsletter_form.is_valid():
            email = newsletter_form.cleaned_data["email"]
            # Check if already subscribed
            subscription, created = NewsletterSubscription.objects.get_or_create(
                email=email, defaults={"is_active": True}
            )

            if created:
                messages.success(
                    request, "Thank you for subscribing to our newsletter!"
                )
            else:
                if not subscription.is_active:
                    subscription.is_active = True
                    subscription.save()
                    messages.success(request, "Your subscription has been reactivated!")
                else:
                    messages.info(
                        request, "You're already subscribed to our newsletter."
                    )

            return redirect("website:contact")
    else:
        newsletter_form = NewsletterForm()

    context = {
        "contact_form": contact_form,
        "newsletter_form": newsletter_form,
        "meta": {
            "title": "Contact Us",
            "description": "Get in touch with Notes App support",
            "mobile_app": True,
        },
    }

    return render(request, "website/contact.html", context)


def terms(request):
    """Terms page with mobile view."""
    # Handle newsletter subscription form
    if request.method == "POST" and "newsletter_submit" in request.POST:
        form = NewsletterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            # Check if already subscribed
            subscription, created = NewsletterSubscription.objects.get_or_create(
                email=email, defaults={"is_active": True}
            )

            if created:
                messages.success(
                    request, "Thank you for subscribing to our newsletter!"
                )
            else:
                if not subscription.is_active:
                    subscription.is_active = True
                    subscription.save()
                    messages.success(request, "Your subscription has been reactivated!")
                else:
                    messages.info(
                        request, "You're already subscribed to our newsletter."
                    )

            return redirect("website:terms")
    else:
        form = NewsletterForm()

    context = {
        "newsletter_form": form,
        "meta": {
            "title": "Terms of Service",
            "description": "Notes App terms and conditions",
            "mobile_app": True,
        },
    }

    return render(request, "website/terms.html", context)


def privacy(request):
    """Privacy policy with mobile optimization."""
    # Handle newsletter subscription form
    if request.method == "POST" and "newsletter_submit" in request.POST:
        form = NewsletterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            # Check if already subscribed
            subscription, created = NewsletterSubscription.objects.get_or_create(
                email=email, defaults={"is_active": True}
            )

            if created:
                messages.success(
                    request, "Thank you for subscribing to our newsletter!"
                )
            else:
                if not subscription.is_active:
                    subscription.is_active = True
                    subscription.save()
                    messages.success(request, "Your subscription has been reactivated!")
                else:
                    messages.info(
                        request, "You're already subscribed to our newsletter."
                    )

            return redirect("website:privacy")
    else:
        form = NewsletterForm()

    context = {
        "newsletter_form": form,
        "meta": {
            "title": "Privacy Policy",
            "description": "How we protect your data",
            "mobile_app": True,
        },
    }

    return render(request, "website/privacy.html", context)


def faq(request):
    """FAQ page with mobile-friendly layout."""
    # Handle newsletter subscription form
    if request.method == "POST" and "newsletter_submit" in request.POST:
        form = NewsletterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            # Check if already subscribed
            subscription, created = NewsletterSubscription.objects.get_or_create(
                email=email, defaults={"is_active": True}
            )

            if created:
                messages.success(
                    request, "Thank you for subscribing to our newsletter!"
                )
            else:
                if not subscription.is_active:
                    subscription.is_active = True
                    subscription.save()
                    messages.success(request, "Your subscription has been reactivated!")
                else:
                    messages.info(
                        request, "You're already subscribed to our newsletter."
                    )

            return redirect("website:faq")
    else:
        form = NewsletterForm()

    context = {
        "newsletter_form": form,
        "meta": {
            "title": "Frequently Asked Questions",
            "description": "Get answers about Notes App",
            "mobile_app": True,
        },
    }

    return render(request, "website/faq.html", context)


def newsletter_subscribe(request):
    """
    Handle newsletter subscription form submissions from any page.

    This view processes AJAX and non-AJAX requests for newsletter subscriptions.
    """
    if request.method == "POST":
        form = NewsletterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            # Check if already subscribed
            subscription, created = NewsletterSubscription.objects.get_or_create(
                email=email, defaults={"is_active": True}
            )

            if created:
                messages.success(
                    request, "Thank you for subscribing to our newsletter!"
                )
            else:
                if not subscription.is_active:
                    subscription.is_active = True
                    subscription.save()
                    messages.success(request, "Your subscription has been reactivated!")
                else:
                    messages.info(
                        request, "You're already subscribed to our newsletter."
                    )
        else:
            messages.error(request, "Please enter a valid email address.")

    # Redirect back to the referring page or home
    referer = request.META.get("HTTP_REFERER")
    if referer:
        return redirect(referer)
    return redirect("website:home")
