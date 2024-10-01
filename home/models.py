from django.core.mail import send_mail
from django.db import models
from django.http import JsonResponse
from django.template.response import TemplateResponse
from modelcluster.fields import ParentalKey
from wagtail import blocks
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.images import get_image_model_string
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Orderable, Page

from .forms import ContactForm


class HomePageSlide(Orderable):
    id = models.BigAutoField(primary_key=True)
    page = ParentalKey("HomePage", related_name="slides", on_delete=models.CASCADE)
    image = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Slide image",
    )
    text_1 = models.CharField(blank=True, max_length=255, help_text="Line 1")
    text_2 = models.CharField(blank=True, max_length=255, help_text="Line 2 & 3")
    text_3 = models.CharField(blank=True, max_length=255, help_text="Line 4")
    text_4 = RichTextField(
        blank=True,
        features=["bold", "italic", "link", "ul", "ol", "blockquote"],
        help_text="Line 4",
    )
    text_5 = RichTextField(
        blank=True,
        features=["bold", "italic", "link", "ul", "ol", "blockquote"],
        help_text="Line 5",
    )
    hero_cta = models.CharField(
        blank=False,
        verbose_name="Hero CTA",
        max_length=255,
        help_text="Text to display on Call to Action",
    )
    hero_cta_link = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Hero CTA link",
        help_text="Choose a page to link to for the Call to Action",
    )
    badge_image = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Badge image",
    )

    panels = [
        FieldPanel("image"),
        FieldPanel("text_1"),
        FieldPanel("text_2"),
        FieldPanel("text_3"),
        FieldPanel("text_4"),
        FieldPanel("text_5"),
        FieldPanel("hero_cta"),
        FieldPanel("hero_cta_link"),
        FieldPanel("badge_image"),
    ]


class ServiceMemberBlock(blocks.StructBlock):
    name = blocks.CharBlock(
        required=True, max_length=100, help_text="Name of the team member"
    )
    job_title = blocks.CharBlock(
        required=True, max_length=100, help_text="Job title of the team member"
    )
    image = ImageChooserBlock(required=True, help_text="Image of the team member")
    profile_link = blocks.URLBlock(
        required=False, help_text="Link to team member's profile"
    )

    class Meta:
        template = "blocks/service_member.html"
        label = "Service Member"


class ServiceGroupBlock(blocks.StructBlock):
    members = blocks.ListBlock(
        ServiceMemberBlock(), max_num=4, help_text="Maximum 4 members per service group"
    )

    class Meta:
        template = "blocks/service_group.html"
        label = "Service Group"


class HomePage(Page):
    body = StreamField(
        [
            ("service_group", ServiceGroupBlock()),
        ],
        default=[],
        verbose_name="Services",
    )

    def serve(self, request):
        form = ContactForm(request.POST or None)
        context = self.get_context(request)

        if request.method == "POST":
            if form.is_valid():
                send_mail(
                    subject=f"New Contact: {form.cleaned_data['name']}",
                    message=form.cleaned_data["message"],
                    from_email=form.cleaned_data["email"],
                    recipient_list=["mahdi.emadi@yahoo.com"],
                )
                context["form"] = form
                return TemplateResponse(request, "home/home_page.html", context)

        context["form"] = form
        return TemplateResponse(request, "home/home_page.html", context)

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [InlinePanel("slides", label="Slides")],
            heading="Main slider",
        ),
        FieldPanel("body", heading="Services"),
    ]
