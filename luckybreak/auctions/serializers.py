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


class BidCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Bid
        fields = ('auction', 'user', 'price')

    def validate(self, attrs):
        # Ensure bidder is not auction owner
        if attrs['auction'].experience.user == attrs['user']:
            raise ValidationError({
                'price': 'You cannot bid on your own auctions'
            })

        # Ensure the auction is still live
        if attrs['auction'].end_date < datetime.now(pytz.UTC):
            raise ValidationError({
                'price': 'This auction has finished'
            })

        # Ensure bid price is more than the current price
        if attrs['price'] < attrs['auction'].current_price() + 1:
            raise ValidationError({
                'price': 'Please enter a bid of {} or over'.format(
                    attrs['auction'].current_price() + 1
                )
            })

        # Ensure the user is not already the highest bidder
        highest_bid = attrs['auction'].highest_bid()
        if highest_bid is not None and highest_bid.user == attrs['user']:
            raise ValidationError({
                'price': 'You are already the highest bidder!'
            })
        return attrs


class PublicAuctionSerializer(serializers.ModelSerializer):
    formatted_current_price = serializers.SerializerMethodField()
    current_price = serializers.SerializerMethodField()
    formatted_starting_price = serializers.SerializerMethodField()
    bids = serializers.SerializerMethodField()
    highest_bidder = serializers.SerializerMethodField()

    class Meta:
        model = models.Auction
        fields = (
            'formatted_current_price', 'formatted_starting_price',
            'bids', 'current_price', 'highest_bidder',
        )

    @staticmethod
    def get_current_price(obj):
        return float(obj.current_price())

    @staticmethod
    def get_formatted_current_price(obj):
        return obj.formatted_current_price()

    @staticmethod
    def get_formatted_starting_price(obj):
        return obj.formatted_starting_price()

    @staticmethod
    def get_bids(obj):
        return obj.bids.count()

    @staticmethod
    def get_highest_bidder(obj):
        bid = obj.highest_bid()
        if bid is not None:
            return bid.user.id
        return None


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


class FavouriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Favourite
        fields = ('auction', 'user')
