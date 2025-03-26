from django.shortcuts import render

# Create your views here.


def home(request):
    return render(request, "website/home.html")


def about(request):
    return render(request, "website/about.html")


def contact(request):
    return render(request, "website/contact.html")


def terms(request):
    return render(request, "website/terms.html")


def privacy(request):
    return render(request, "website/privacy.html")


def faq(request):
    return render(request, "website/faq.html")
