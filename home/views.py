from django.shortcuts import get_object_or_404, render

from .models import HomePage


def service_detail(request, service_name):
    homepage = get_object_or_404(HomePage, slug="maintenance-services-london")
    return homepage.serve_service_detail(request, service_name)
