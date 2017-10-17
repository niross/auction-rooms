from channels.routing import route_class

from . import consumers


channel_routing = [
    route_class(
        consumers.ProviderAuctionConsumer,
        path=r'^/provider/auctions/(?P<pk>[0-9]+)/stream/'
    ),
    route_class(
        consumers.PublicAuctionConsumer,
        path=r'^/public/auctions/(?P<pk>[0-9]+)/stream/'
    ),
]
