from channels.generic.websockets import JsonWebsocketConsumer

from luckybreak.auctions.models import Auction


class ProviderAuctionConsumer(JsonWebsocketConsumer):
    http_user = True

    # Automatically add/remove this connection from these groups
    def connection_groups(self, **kwargs):
        return ['provider-auction-{}'.format(kwargs['pk'])]

    # Perform actions on connection start
    def connect(self, message, **kwargs):
        if not message.user.is_authenticated():
            message.reply_channel.send({'accept': False})
            return

        # Ensure the current user owns the auction
        try:
            Auction.objects.get(
                pk=kwargs['pk'],
                experience__user=message.user
            )
        except Auction.DoesNotExist:
            message.reply_channel.send({'accept': False})
            return

        message.reply_channel.send({'accept': True})


class PublicAuctionConsumer(JsonWebsocketConsumer):
    http_user = True

    # Automatically add/remove this connection from these groups
    def connection_groups(self, **kwargs):
        return ['public-auction-{}'.format(kwargs['pk'])]

    # Perform actions on connection start
    def connect(self, message, **kwargs):
        message.reply_channel.send({'accept': True})
