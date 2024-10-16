import logging

from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.utils import timezone
from wagtail.models import Page

# تنظیمات برای لاگ
logger = logging.getLogger(__name__)


class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = "daily"

    def items(self):
        return ["about_us", "contact_us", "services"]

    def location(self, item):
        return reverse(item)

    def lastmod(self, obj):
        return timezone.now()


class WagtailSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.8

    def items(self):
        pages = Page.objects.live().public().specific()
        valid_pages = []
        for page in pages:
            site = page.get_site()
            if site:
                relative_url = page.relative_url(site)
                # بررسی دقیق‌تر صفحه‌های مشکل‌دار
                if (
                    relative_url
                    and not relative_url.startswith("http://")
                    and not relative_url.startswith("https://")
                    and relative_url != "/"
                ):
                    valid_pages.append(page)
                else:
                    logger.warning(
                        f"Page with issue: {page.title} - Relative URL: {relative_url}"
                    )
        return valid_pages

    def lastmod(self, obj):
        return obj.last_published_at

    def location(self, obj):
        site = obj.get_site()
        if site:
            relative_url = obj.relative_url(site)
            if relative_url and not relative_url.startswith("http"):
                # بررسی می‌کنیم که آیا ترکیب صحیح است و URL به درستی ساخته می‌شود
                return f"{site.root_url.rstrip('/')}/{relative_url.lstrip('/')}"
            elif relative_url and relative_url.startswith("http"):
                return relative_url
        logger.warning(f"Invalid URL for page: {obj.title}")
        return None
