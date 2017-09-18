# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url, include
from rest_framework import routers

from . import api_views


router = routers.DefaultRouter()
router.register(
    r'auctions/provider',
    api_views.ProviderAuctionViewSet,
    base_name='provider-auction'
)

urlpatterns = [
    url(r'^', include(router.urls)),
]
