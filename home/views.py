from django.shortcuts import get_object_or_404, render

from .models import HomePage


def about_us(request):
    return render(request, "home/about_us.html")


def contact_us(request):
    return render(request, "home/contact_us.html")


def services(request):
    homepage = get_object_or_404(HomePage, slug="home")
    return homepage.serve_services(request)
