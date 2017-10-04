from channels.generic.websockets import JsonWebsocketConsumer


class ProviderAuctionConsumer(JsonWebsocketConsumer):
    http_user = True

    # Automatically add/remove this connection from these groups
    def connection_groups(self, **kwargs):
        return ['provider-auction-{}'.format(kwargs['pk'])]

    # Perform actions on connection start
    def connect(self, message, **kwargs):
        print("*"*89)
        print("Connection start")
        message.reply_channel.send({'accept': True})

    # Called when a message is received
    def receive(self, content, **kwargs):
        http_user = True
        print("*"*89)
        print("Received a message")

    # Perform actions on connection close
    def disconnect(self, message, **kwargs):
        print("*"*89)
        print("Ive disconected")
