# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import logging

from django.contrib.gis.geos import Point
from rest_framework import serializers

from . import models


class ExperienceImageReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ExperienceImage
        fields = ('image')

class ExperienceInclusionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ExperienceInclusion
        fields = ('name',)


class ExperienceExclusionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ExperienceExclusion
        fields = ('name',)


class ExperienceReadSerializer(serializers.ModelSerializer):
    latitude = serializers.SerializerMethodField()
    longitude = serializers.SerializerMethodField()
    images = ExperienceImageReadSerializer(many=True)
    inclusions = ExperienceInclusionSerializer(many=True)
    exclusions = ExperienceExclusionSerializer(many=True)

    class Meta:
        model = models.Experience
        fields = (
            'title', 'description', 'location', 'latitude', 'longitude',
            'terms', 'pax_adults', 'pax_children', 'images', 'inclusions',
            'exclusions',
        )

    def get_latitude(self, obj):
        return obj.coords.x

    def get_longitude(self, obj):
        return obj.coords.y
