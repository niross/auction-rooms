from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class BrowseStaticSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.5

    def items(self):
        return [
            'browse:homepage', 'browse:provider-marketing',
            'browse:search-results'
        ]

    def location(self, item):
        return reverse(item)
