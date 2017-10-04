# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from datetime import datetime, timedelta

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

import pytz

from luckybreak.experiences.models import Experience
from luckybreak.experiences.serializers import ExperienceReadSerializer
from luckybreak.users.serializers import PublicUserSerializer
from . import models


class AuctionImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AuctionImage
        fields = ('id', 'auction', 'image', 'default')


class AuctionInclusionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AuctionInclusion
        fields = ('id', 'auction', 'name')


class AuctionExclusionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AuctionExclusion
        fields = ('id', 'auction', 'name')


class BidSerializer(serializers.ModelSerializer):
    user = PublicUserSerializer()
    formatted_price = serializers.SerializerMethodField()

    class Meta:
        model = models.Bid
        fields = ('id', 'user', 'price', 'formatted_price', 'created')

    @staticmethod
    def get_formatted_price(obj):
        return obj.formatted_price()


class AuctionReadSerializer(serializers.ModelSerializer):
    latitude = serializers.SerializerMethodField()
    longitude = serializers.SerializerMethodField()
    images = AuctionImageSerializer(many=True)
    inclusions = AuctionInclusionSerializer(many=True)
    exclusions = AuctionExclusionSerializer(many=True)
    experience = ExperienceReadSerializer()
    bids = BidSerializer(many=True)
    formatted_current_price = serializers.SerializerMethodField()
    formatted_starting_price = serializers.SerializerMethodField()

    class Meta:
        model = models.Auction
        fields = (
            'id', 'title', 'description', 'location', 'latitude', 'longitude',
            'terms', 'pax_adults', 'pax_children', 'images', 'inclusions',
            'exclusions', 'check_in', 'check_out', 'starting_price',
            'reserve_price', 'experience', 'bids', 'formatted_current_price',
            'formatted_starting_price', 'created',
        )

    @staticmethod
    def get_latitude(obj):
        return obj.coords.x

    @staticmethod
    def get_longitude(obj):
        return obj.coords.y

    @staticmethod
    def get_formatted_current_price(obj):
        return obj.formatted_current_price()

    @staticmethod
    def get_formatted_starting_price(obj):
        return obj.formatted_starting_price()


class AuctionCreateSerializer(serializers.ModelSerializer):
    _DURATION_CHOICES = (
        (1, '1 Day'),
        (3, '3 Days'),
        (5, '5 Days'),
        (7, '7 Days'),
    )
    experience = serializers.PrimaryKeyRelatedField(
        queryset=Experience.objects.live()
    )
    duration_days = serializers.ChoiceField(choices=_DURATION_CHOICES)
    lots = serializers.IntegerField()

    class Meta:
        model = models.Auction
        fields = (
            'experience', 'check_in', 'check_out', 'starting_price',
            'reserve_price', 'duration_days', 'lots',
        )

    def validate(self, attrs):
        duration = attrs.pop('duration_days')
        attrs['end_date'] = datetime.now(pytz.UTC) + timedelta(days=duration)

        # Check that check out is after check in
        if attrs['check_out'] <= attrs['check_in']:
            raise ValidationError({
                'check_out': 'Check out must be after check in'
            })

        # Check the check in date is after auction completion
        if attrs['check_in'] <= attrs['end_date']:
            raise ValidationError({
                'check_in': 'Check in cannot be before auction end date'
            })

        return attrs

    def create(self, validated_data):
        lots = validated_data.pop('lots')
        auctions = []
        for _ in range(lots):
            auctions.append(models.Auction.objects.create_auction(**validated_data))
        return auctions
