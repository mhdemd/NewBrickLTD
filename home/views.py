from django.shortcuts import get_object_or_404, render

from .models import HomePage


def about_us(request):
    return render(request, "home/about_us.html")


def contact_us(request):
    homepage = get_object_or_404(HomePage, slug="maintenance-services-london")
    return homepage.serve(request, template_name="home/contact_us.html")


def services(request):
    homepage = get_object_or_404(HomePage, slug="maintenance-services-london")
    return homepage.serve_services(request)


def service_detail(request, service_name):
    homepage = get_object_or_404(HomePage, slug="maintenance-services-london")
    return homepage.serve_service_detail(request, service_name)
