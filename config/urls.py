from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.views import defaults as default_views
from django.views.generic import TemplateView

from auction_rooms.auctions.sitemaps import AuctionStaticSitemap
from auction_rooms.browse.sitemaps import BrowseStaticSitemap

sitemaps = {
    'browse': BrowseStaticSitemap,
    'auctions': AuctionStaticSitemap,
}

urlpatterns = [
    # Django Admin, use {% url 'admin:index' %}
    url(settings.ADMIN_URL, admin.site.urls),

    # User management
    url(r'^', include('auction_rooms.users.urls', namespace='users')),
    url(r'^accounts/', include('allauth.urls')),

    # App Views
    url(r'', include('auction_rooms.browse.urls', namespace='browse')),
    url(
        r'^contact/',
        include('auction_rooms.contact.urls', namespace='contact')
    ),
    url(
        r'^experiences/',
        include('auction_rooms.experiences.urls', namespace='experiences')
    ),
    url(
        r'^auctions/',
        include('auction_rooms.auctions.urls', namespace='auctions')
    ),

    # API
    url(
        r'^api/',
        include(
            'auction_rooms.experiences.api_urls',
            namespace='experience-api'
        )
    ),
    url(
        r'^api/',
        include('auction_rooms.auctions.api_urls', namespace='auction-api')
    ),

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
        url(
            r'^400/$',
            default_views.bad_request,
            kwargs={'exception': Exception('Bad Request!')}
        ),
        url(
            r'^403/$',
            default_views.permission_denied,
            kwargs={'exception': Exception('Permission Denied')}
        ),
        url(
            r'^404/$',
            default_views.page_not_found,
            kwargs={'exception': Exception('Page not Found')}
        ),
        url(r'^500/$', default_views.server_error),
    ]
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar
        urlpatterns = [
            url(r'^__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns
