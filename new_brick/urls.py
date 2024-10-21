from django.conf import settings
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.contrib.sitemaps.views import sitemap
from wagtail.documents import urls as wagtaildocs_urls

from home import views as home_views
from home.sitemaps import StaticViewSitemap, WagtailSitemap
from search import views as search_views

sitemaps = {
    "static": StaticViewSitemap,  # نقشه سایت برای view های ثابت
    "wagtail": WagtailSitemap,  # نقشه سایت برای صفحات Wagtail
}

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("new-admin-brick/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("search/", search_views.search, name="search"),
    path("contact-us/", home_views.contact_us, name="contact_us"),
    path(
        "service/<str:service_name>/", home_views.service_detail, name="service_detail"
    ),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = urlpatterns + [
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    path("", include(wagtail_urls)),
    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    path("pages/", include(wagtail_urls)),
]
