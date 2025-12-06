from django.urls import path
from . import views

app_name = "website"

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("terms/", views.terms, name="terms"),
    path("privacy/", views.privacy, name="privacy"),
    path("faq/", views.faq, name="faq"),
    path(
        "newsletter/subscribe/", views.newsletter_subscribe, name="newsletter_subscribe"
    ),
]
