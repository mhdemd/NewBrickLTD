from bs4 import BeautifulSoup
from django import template
from django.utils.html import format_html

register = template.Library()


@register.filter
def add_class_to_paragraphs(value):
    """to add class = "main-slider text-two" to textrich tag"""

    # Check if the input is a string
    if not isinstance(value, str):
        return value

    # Use BeautifulSoup to edit the HTML
    soup = BeautifulSoup(value, "html.parser")

    # Add the class 'main-slider__text-two' to all <p> tags
    for p in soup.find_all("p"):
        p["class"] = p.get("class", []) + ["main-slider__text-two"]

    return str(soup)


@register.filter(name="add_class")
def add_class(field, css_class):
    # Check if the input is a form field (and not a string)
    if hasattr(field, "as_widget"):
        return field.as_widget(attrs={"class": css_class})
    return field  # If it's not a form field, just return it as is
