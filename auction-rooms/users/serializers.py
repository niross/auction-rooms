from rest_framework import serializers

from auctioneer.users import models


class PublicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ('first_name', 'last_name')
