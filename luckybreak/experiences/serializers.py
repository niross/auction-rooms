# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.contrib.gis.geos import Point

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from . import models


class ExperienceImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ExperienceImage
        fields = ('id', 'experience', 'image', 'default')


class ExperienceImageWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ExperienceImage
        fields = ('experience', 'image', 'default')


class ExperienceInclusionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ExperienceInclusion
        fields = ('id', 'experience', 'name')


class ExperienceInclusionWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ExperienceInclusion
        fields = ('experience', 'name')


class ExperienceExclusionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ExperienceExclusion
        fields = ('id', 'experience', 'name',)


class ExperienceExclusionWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ExperienceExclusion
        fields = ('experience', 'name')


class ExperienceReadSerializer(serializers.ModelSerializer):
    latitude = serializers.SerializerMethodField()
    longitude = serializers.SerializerMethodField()
    images = ExperienceImageSerializer(many=True)
    inclusions = ExperienceInclusionSerializer(many=True)
    exclusions = ExperienceExclusionSerializer(many=True)

    class Meta:
        model = models.Experience
        fields = (
            'title', 'description', 'location', 'latitude', 'longitude',
            'terms', 'pax_adults', 'pax_children', 'images', 'inclusions',
            'exclusions', 'banner_image',
        )

    @staticmethod
    def get_latitude(obj):
        return obj.coords.x

    @staticmethod
    def get_longitude(obj):
        return obj.coords.y


class TestImageSerializer(serializers.Serializer):
    image = serializers.ImageField(required=True)
    default = serializers.BooleanField(default=False)


class ExperienceWriteSerializer(serializers.ModelSerializer):
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    images = serializers.ListField(child=serializers.ImageField(required=True))
    inclusions = serializers.ListField(child=serializers.CharField(required=True))
    exclusions = serializers.ListField(child=serializers.CharField(required=True))

    class Meta:
        model = models.Experience
        fields = (
            'user', 'title', 'description', 'location', 'latitude',
            'longitude', 'terms', 'pax_adults', 'pax_children', 'images',
            'inclusions', 'exclusions', 'banner_image'
        )

    def validate_images(self, images):
        if not images:
            raise ValidationError('Please provide at least one image')
        return images

    def validate(self, attrs):
        attrs['coords'] = Point(attrs.pop('latitude'), attrs.pop('longitude'))
        return attrs

    def create(self, validated_data):
        images = validated_data.pop('images')
        inclusions = validated_data.pop('inclusions')
        exclusions = validated_data.pop('exclusions')

        experience = super(ExperienceWriteSerializer, self).create(validated_data)
        for image in images:
            image_serializer = ExperienceImageWriteSerializer(
                data={'image': image, 'experience': experience.id}
            )
            image_serializer.is_valid(raise_exception=True)
            image_serializer.save()

        for inclusion in inclusions:
            inc_serializer = ExperienceInclusionSerializer(
                data={'name': inclusion, 'experience': experience.id}
            )
            inc_serializer.is_valid(raise_exception=True)
            inc_serializer.save()

        for exclusion in exclusions:
            exc_serializer = ExperienceExclusionSerializer(
                data={'name': exclusion, 'experience': experience.id}
            )
            exc_serializer.is_valid(raise_exception=True)
            exc_serializer.save()

        return experience
