from bs4 import BeautifulSoup
from django import template

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
