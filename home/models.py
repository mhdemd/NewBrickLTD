import re
from datetime import timedelta

import bleach
from django.core.mail import send_mail
from django.db import models
from django.http import Http404
from django.template.response import TemplateResponse
from django.utils import timezone
from django.utils.text import slugify
from modelcluster.fields import ParentalKey
from wagtail import blocks
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.blocks import RichTextBlock
from wagtail.fields import RichTextField, StreamField
from wagtail.images import get_image_model_string
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Orderable, Page
from wagtail.snippets.models import register_snippet

from .forms import ContactForm


################################## HomePage's Models
class HomePageSlide(Orderable):
    id = models.BigAutoField(primary_key=True)
    page = ParentalKey("HomePage", related_name="slides", on_delete=models.CASCADE)

    # Home slide
    image_desktop = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Slide image for desktop (size 1320x845)",
    )
    image_mobile = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Slide image for mobile (size 340x800)",
    )
    text_slide_1 = models.CharField(blank=True, max_length=255, help_text="Line 1")
    text_slide_2 = RichTextField(blank=True, max_length=255, help_text="Line 2 & 3")
    text_slide_3 = models.CharField(blank=True, max_length=255, help_text="Line 4")
    text_slide_4 = RichTextField(
        blank=True,
        features=["bold", "italic", "link", "ul", "ol", "blockquote"],
        help_text="Line 4",
    )
    text_slide_5 = RichTextField(
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
        # Home slide
        FieldPanel("image_desktop"),
        FieldPanel("image_mobile"),
        FieldPanel("text_slide_1"),
        FieldPanel("text_slide_2"),
        FieldPanel("text_slide_3"),
        FieldPanel("text_slide_4"),
        FieldPanel("text_slide_5"),
        FieldPanel("hero_cta"),
        FieldPanel("hero_cta_link"),
        FieldPanel("badge_image"),
    ]


class ServiceMemberBlock(blocks.StructBlock):
    slug = blocks.CharBlock(
        required=False,
        help_text="Slug for the service",
    )

    name = RichTextBlock(
        required=True,
        help_text="Name of the service",
    )
    image = ImageChooserBlock(required=True, help_text="Image of the service")
    second_image = ImageChooserBlock(required=True, help_text="Image of the service")

    description = blocks.TextBlock(
        required=True,
        help_text="Description of the service above the checkmarks",
        max_length=1000,
    )

    second_description = blocks.TextBlock(
        required=True,
        help_text="Description of the service below the checkmarks",
        max_length=1000,
    )

    # Three checkmark items as separate CharBlocks
    checkmark_one = blocks.CharBlock(required=True, help_text="First checkmark item")
    checkmark_two = blocks.CharBlock(required=True, help_text="Second checkmark item")
    checkmark_three = blocks.CharBlock(required=True, help_text="Third checkmark item")

    # Meta fields
    meta_title = blocks.CharBlock(
        required=False, help_text="Meta title for the service page"
    )
    meta_description = blocks.TextBlock(
        required=False, help_text="Meta description for the service page"
    )
    meta_h1 = blocks.CharBlock(required=False, help_text="Meta H1 for the service page")
    meta_keywords = blocks.TextBlock(
        required=False, help_text="Meta keywords for the service page"
    )

    def clean(self, value):
        # First, let the parent class do its validation
        cleaned_data = super().clean(value)

        # Get the user-supplied slug (may be blank or something typed)
        raw_slug = cleaned_data.get("slug", "").strip()

        if raw_slug:
            # The user typed something, so let's slugify it.
            # This ensures no matter what the user entered, we store a proper slug.
            cleaned_data["slug"] = slugify(bleach.clean(raw_slug, tags=[], strip=True))
        else:
            # The user left it blank, so we auto-generate from the 'name' field
            raw_name = cleaned_data.get("name", "").strip()
            slug_from_name = slugify(bleach.clean(raw_name, tags=[], strip=True))
            cleaned_data["slug"] = slug_from_name

        return cleaned_data

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
    # Services
    body = StreamField(
        [
            ("service_group", ServiceGroupBlock()),
        ],
        default=[],
        verbose_name="Services",
    )

    # Why choose us
    why_choose_us = RichTextField(
        blank=True,
        features=["bold", "italic", "link", "ul", "ol", "blockquote"],
        help_text="Paragraph for why choose us",
    )

    # Change the service name to slug-friendly format
    def slugify(self, text):
        return re.sub(r"[\W_]+", "-", text).lower()

    # Form service and email sending
    def serve(self, request, template_name="home/home_page.html"):
        form = ContactForm(request.POST or None)
        context = self.get_context(request)
        context["message_limit_reached"] = False  # Add a flag for message limit

        if request.method == "POST" and form.is_valid():
            # Get user information from the form
            user_name = form.cleaned_data["name"]
            user_email = form.cleaned_data["email"]
            user_phone = form.cleaned_data["phone"]
            user_message = form.cleaned_data["message"]

            # Get the IP address of the user
            user_ip = request.META.get("HTTP_X_FORWARDED_FOR")
            if user_ip:
                # If there are multiple IPs in X-Forwarded-For, take the first one (client's IP)
                user_ip = user_ip.split(",")[0].strip()
            else:
                user_ip = request.META.get("REMOTE_ADDR")

            # Check if there are already 3 or more messages from this IP in the last 24 hours
            last_24_hours = timezone.now() - timedelta(hours=24)
            recent_messages_count = ContactMessage.objects.filter(
                ip_address=user_ip, submitted_at__gte=last_24_hours
            ).count()

            # If the message limit has been reached, set the flag to True
            if recent_messages_count >= 3:
                context["message_limit_reached"] = True
            else:
                # Proceed with saving and sending the email
                email_subject = f"New Contact Request from {user_name}"
                email_message = f"""
                Name: {user_name}
                Email: {user_email}
                Phone: {user_phone}
                
                Message:
                {user_message}
                """

                send_mail(
                    subject=email_subject,
                    message=email_message,
                    from_email="info@newbrickltd.co.uk",
                    recipient_list=["info@newbrickltd.co.uk"],
                )

                # Save message to the database
                ContactMessage.objects.create(
                    name=user_name,
                    email=user_email,
                    phone=user_phone,
                    message=user_message,
                    ip_address=user_ip,  # Store IP address
                )

                # Delete messages older than one month
                one_month_ago = timezone.now() - timedelta(days=30)
                ContactMessage.objects.filter(submitted_at__lt=one_month_ago).delete()

            context["form"] = form
            return TemplateResponse(request, template_name, context)

        context["form"] = form
        return TemplateResponse(request, template_name, context)

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [InlinePanel("slides", label="Slides")],
            heading="Main slider",
        ),
        FieldPanel("body", heading="Services"),
        FieldPanel("why_choose_us", heading="Why choose us"),
    ]


################################## About Us's Models
class AboutUsPage(Page):
    main_title = models.CharField(max_length=255, blank=True)
    subtitle = models.CharField(max_length=255, blank=True)
    description = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("main_title"),
        FieldPanel("subtitle"),
        FieldPanel("description"),
    ]


################################## Services's Models
class ServicesPage(Page):
    main_title = models.CharField(max_length=255, blank=True)
    description = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("main_title"),
        FieldPanel("description"),
    ]

    def get_context(self, request, *args, **kwargs):
        # دریافت کانتکست پایه
        context = super().get_context(request, *args, **kwargs)

        # دریافت صفحه والد
        homepage = self.get_parent().specific

        # اضافه کردن body والد به کانتکست
        if hasattr(homepage, "body"):
            context["parent_body"] = homepage.body

        return context


################################## Contact Us's Models
class ContactUsPage(Page):
    main_title = models.CharField(max_length=255, blank=True)
    description = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("main_title"),
        FieldPanel("description"),
    ]

    # Form service and email sending (Copied from HomePage)
    def serve(self, request, template_name="home/contact_us_page.html"):
        form = ContactForm(request.POST or None)
        context = self.get_context(request)
        context["message_limit_reached"] = False  # Add a flag for message limit

        if request.method == "POST" and form.is_valid():
            # Get user information from the form
            user_name = form.cleaned_data["name"]
            user_email = form.cleaned_data["email"]
            user_phone = form.cleaned_data["phone"]
            user_message = form.cleaned_data["message"]

            # Get the IP address of the user
            user_ip = request.META.get("HTTP_X_FORWARDED_FOR")
            if user_ip:
                # If there are multiple IPs in X-Forwarded-For, take the first one (client's IP)
                user_ip = user_ip.split(",")[0].strip()
            else:
                user_ip = request.META.get("REMOTE_ADDR")

            # Check if there are already 3 or more messages from this IP in the last 24 hours
            last_24_hours = timezone.now() - timedelta(hours=24)
            recent_messages_count = ContactMessage.objects.filter(
                ip_address=user_ip, submitted_at__gte=last_24_hours
            ).count()

            # If the message limit has been reached, set the flag to True
            if recent_messages_count >= 3:
                context["message_limit_reached"] = True
            else:
                # Proceed with saving and sending the email
                email_subject = f"New Contact Request from {user_name}"
                email_message = f"""
                Name: {user_name}
                Email: {user_email}
                Phone: {user_phone}
                
                Message:
                {user_message}
                """

                send_mail(
                    subject=email_subject,
                    message=email_message,
                    from_email="info@newbrickltd.co.uk",
                    recipient_list=["info@newbrickltd.co.uk"],
                )

                # Save message to the database
                ContactMessage.objects.create(
                    name=user_name,
                    email=user_email,
                    phone=user_phone,
                    message=user_message,
                    ip_address=user_ip,  # Store IP address
                )

                # Delete messages older than one month
                one_month_ago = timezone.now() - timedelta(days=30)
                ContactMessage.objects.filter(submitted_at__lt=one_month_ago).delete()

            context["form"] = form
            return TemplateResponse(request, template_name, context)

        context["form"] = form
        return TemplateResponse(request, template_name, context)


################################## Contact form's Model (to store messages in database)
class ContactMessage(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(
        null=True, blank=True
    )  # New field for IP address

    def __str__(self):
        return f"Message from {self.name} ({self.email})"


################################## Company info's models
@register_snippet  # This decorator registers the model as a Snippet
class CompanyInfo(models.Model):
    phone = models.CharField(max_length=20, help_text="Company phone number")
    whatsapp = models.CharField(max_length=20, blank=True, help_text="WhatsApp number")
    address = models.TextField(help_text="Company address")
    postal_code = models.CharField(blank=True, max_length=10, help_text="Postal code")
    email = models.EmailField(help_text="Company email address")
    facebook = models.URLField(blank=True, help_text="Facebook link")
    twitter = models.URLField(blank=True, help_text="Twitter link")
    linkedin = models.URLField(blank=True, help_text="LinkedIn link")
    instagram = models.URLField(blank=True, help_text="Instagram link")
    telegram = models.URLField(blank=True, help_text="Telegram link")

    def __str__(self):
        return f"Company Info ({self.email})"
