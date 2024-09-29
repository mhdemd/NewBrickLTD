from django.db import models

# import MultiFieldPanel:
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Page


class HomePage(Page):
    # add the Hero section of HomePage:
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Homepage image",
    )
    text_1 = models.CharField(blank=True, max_length=255, help_text="Line 1")
    text_2 = models.CharField(blank=True, max_length=255, help_text="Line 2 & 3")
    text_3 = models.CharField(blank=True, max_length=255, help_text="Line 4")
    text_4 = RichTextField(
        blank=True, features=["bold", "italic", "link", "ul", "ol"], help_text="Line 4"
    )
    text_5 = RichTextField(
        blank=True, features=["bold", "italic", "link", "ul", "ol"], help_text="Line 5"
    )

    hero_cta = models.CharField(
        blank=True,
        verbose_name="Hero CTA",
        max_length=255,
        help_text="Text to display on Call to Action",
    )
    hero_cta_link = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Hero CTA link",
        help_text="Choose a page to link to for the Call to Action",
    )

    body = RichTextField(blank=True)

    # modify your content_panels:
    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("image"),
                FieldPanel("text_1"),
                FieldPanel("text_2"),
                FieldPanel("text_3"),
                FieldPanel("text_4"),
                FieldPanel("text_5"),
                FieldPanel("hero_cta"),
                FieldPanel("hero_cta_link"),
            ],
            heading="Main slider",
        ),
        FieldPanel("body"),
    ]
