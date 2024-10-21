from django.shortcuts import get_object_or_404, render

from .models import HomePage


def contact_us(request):
    homepage = get_object_or_404(HomePage, slug="maintenance-services-london")
    return homepage.serve(request, template_name="home/contact_us.html")


def service_detail(request, service_name):
    homepage = get_object_or_404(HomePage, slug="maintenance-services-london")
    return homepage.serve_service_detail(request, service_name)
