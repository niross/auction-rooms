from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.views import defaults as default_views
from django.views.generic import TemplateView

from luckybreak.auctions.sitemaps import AuctionStaticSitemap
from luckybreak.browse.sitemaps import BrowseStaticSitemap

sitemaps = {
    'browse': BrowseStaticSitemap,
    'auctions': AuctionStaticSitemap,
}

urlpatterns = [
    # Django Admin, use {% url 'admin:index' %}
    url(settings.ADMIN_URL, admin.site.urls),

    # User management
    url(r'^', include('luckybreak.users.urls', namespace='users')),
    url(r'^accounts/', include('allauth.urls')),

    # App Views
    url(r'', include('luckybreak.browse.urls', namespace='browse')),
    url(r'^contact/', include('luckybreak.contact.urls', namespace='contact')),
    url(r'^experiences/', include('luckybreak.experiences.urls', namespace='experiences')),
    url(r'^auctions/', include('luckybreak.auctions.urls', namespace='auctions')),

    # API
    url(r'^api/', include('luckybreak.experiences.api_urls', namespace='experience-api')),
    url(r'^api/', include('luckybreak.auctions.api_urls', namespace='auction-api')),

    url(r'^robots.txt$', TemplateView.as_view(
        template_name="robots.txt",
        content_type="text/plain"
    ), name="robots"),

    url(
        r'^sitemap\.xml$',
        sitemap,
        {'sitemaps': sitemaps},
        name='sitemap'
    ),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        url(r'^400/$', default_views.bad_request, kwargs={'exception': Exception('Bad Request!')}),
        url(r'^403/$', default_views.permission_denied, kwargs={'exception': Exception('Permission Denied')}),
        url(r'^404/$', default_views.page_not_found, kwargs={'exception': Exception('Page not Found')}),
        url(r'^500/$', default_views.server_error),
    ]
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar
        urlpatterns = [
            url(r'^__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns
