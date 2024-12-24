import bleach
from django.http import Http404
from django.shortcuts import render
from django.utils.text import slugify

from .models import HomePage


def service_detail(request, service_name):
    """
    A function-based view that finds the 'service_name' slug in the HomePage's body
    and renders the service_details.html template.
    """
    # 1) Retrieve the HomePage containing the service blocks.
    #    (Assuming you have only ONE HomePage; adjust if needed.)
    homepage = HomePage.objects.live().first()
    if not homepage:
        raise Http404("No HomePage found.")

    # 2) Search through homepage.body for a matching slug
    service_block = None

    # 'body' is a StreamValue; each item is a StreamBlock with block_type + value
    for block in homepage.body:
        if block.block_type == "service_group":
            for member in block.value.get("members", []):
                raw_slug = member.get("slug", "")
                cleaned_slug = (
                    bleach.clean(raw_slug, tags=[], strip=True)
                    .replace("\n", " ")
                    .replace("\r", " ")
                    .strip()
                )

                if cleaned_slug == service_name:
                    service_block = member
                    break
            if service_block:
                break

    if not service_block:
        raise Http404("Service not found")

    # 3) Render the service details template
    context = {
        "service": service_block,
        # Add anything else you want to pass to the template
    }
    return render(request, "home/service_details.html", context)
