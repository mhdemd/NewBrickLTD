import re

import bleach
from django.core.mail import send_mail
from django.db import models
from django.http import Http404
from django.template.response import TemplateResponse
from django.utils.text import slugify
from modelcluster.fields import ParentalKey
from wagtail import blocks
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.blocks import RichTextBlock
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
    name = RichTextBlock(required=True, help_text="Name of the service")
    image = ImageChooserBlock(required=True, help_text="Image of the service")
    # profile_link = blocks.URLBlock(required=False, help_text="Link to service")
    description = blocks.TextBlock(
        required=True, help_text="Description of the service", max_length=1000
    )

    class Meta:
        template = "blocks/service_member.html"
        label = "Service Member"


class ServiceGroupBlock(blocks.StructBlock):
    members = blocks.ListBlock(
        ServiceMemberBlock(), max_num=4, help_text="Maximum 3 members per service group"
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

    # Change the service name to slug-friendly format
    def slugify(self, text):
        return re.sub(r"[\W_]+", "-", text).lower()

    # Form service and email sending
    def serve(self, request, template_name="home/home_page.html"):
        form = ContactForm(request.POST or None)
        context = self.get_context(request)

        if request.method == "POST" and form.is_valid():
            send_mail(
                subject=f"New Contact: {form.cleaned_data['name']}",
                message=form.cleaned_data["message"],
                from_email=form.cleaned_data["email"],
                recipient_list=["mahdi.emadi@yahoo.com"],
            )
            context["form"] = form
            return TemplateResponse(request, template_name, context)

        context["form"] = form
        return TemplateResponse(request, template_name, context)

    # Service to display the services page
    def serve_services(self, request):
        context = self.get_context(request)
        context["page"] = self

        return TemplateResponse(request, "home/services.html", context)

    # Service Show details of each service
    def serve_service_detail(self, request, service_name):
        service_group = None

        # جستجو در block برای پیدا کردن سرویس
        for block in self.body:
            if block.block_type == "service_group":
                for member in block.value.get("members", []):
                    # اگر نام سرویس RichText است، از source آن استفاده کنید
                    service_name_raw = (
                        member.get("name").source
                        if hasattr(member.get("name"), "source")
                        else str(member.get("name"))
                    )

                    # حذف تگ‌های HTML از نام سرویس، جایگزینی <br/> و &amp; با فضای مناسب
                    cleaned_service_name = bleach.clean(
                        service_name_raw, tags=[], strip=True
                    )
                    cleaned_service_name = (
                        cleaned_service_name.replace("&amp;", "amp-")
                        .replace("&", "")
                        .replace("\n", " ")
                        .replace("\r", " ")
                    )

                    # اضافه کردن فاصله به جای <br/> و تگ‌های حذف‌شده
                    cleaned_service_name = cleaned_service_name.replace(
                        "  ", " "
                    )  # حذف فاصله‌های مضاعف

                    # تبدیل نام سرویس به اسلاگ برای مقایسه صحیح
                    slugified_name = slugify(cleaned_service_name)

                    # چاپ مقادیر برای دیباگ
                    print(
                        f"Original name: {service_name_raw}, Cleaned name: {cleaned_service_name}, Slugified name: {slugified_name}"
                    )
                    print(f"Requested service name: {service_name}")

                    # بررسی تطابق
                    if slugified_name == service_name:
                        service_group = member
                        break

        # اگر سرویس پیدا نشد
        if not service_group:
            raise Http404("Service not found")

        context = self.get_context(request)
        context["service"] = service_group

        return TemplateResponse(request, "home/service_details.html", context)

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [InlinePanel("slides", label="Slides")],
            heading="Main slider",
        ),
        FieldPanel("body", heading="Services"),
    ]
