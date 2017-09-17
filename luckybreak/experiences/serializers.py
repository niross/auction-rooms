# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import os

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
            'id', 'title', 'description', 'location', 'latitude', 'longitude',
            'terms', 'pax_adults', 'pax_children', 'images', 'inclusions',
            'exclusions', 'user',
        )

    @staticmethod
    def get_latitude(obj):
        return obj.coords.x

    @staticmethod
    def get_longitude(obj):
        return obj.coords.y


class ExperienceCreateSerializer(serializers.ModelSerializer):
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    images = serializers.ListField(child=serializers.ImageField(required=True))
    inclusions = serializers.ListField(child=serializers.CharField(required=True))
    exclusions = serializers.ListField(child=serializers.CharField(required=True))
    default_image = serializers.CharField()

    class Meta:
        model = models.Experience
        fields = (
            'user', 'title', 'description', 'location', 'latitude',
            'longitude', 'terms', 'pax_adults', 'pax_children', 'images',
            'inclusions', 'exclusions', 'default_image'
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
        default_image = validated_data.pop('default_image')
        inclusions = validated_data.pop('inclusions')
        exclusions = validated_data.pop('exclusions')

        experience = super(ExperienceCreateSerializer, self).create(validated_data)
        for image in images:
            image_serializer = ExperienceImageWriteSerializer(
                data={
                    'image': image,
                    'experience': experience.id,
                    'default': image.name == default_image
                }
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


class ExperienceUpdateSerializer(serializers.ModelSerializer):
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    images = serializers.ListField(child=serializers.ImageField(required=True))
    deleted_images = serializers.ListField(child=serializers.PrimaryKeyRelatedField(
        allow_null=True, required=False, queryset=models.ExperienceImage.objects.all()
    ))
    inclusions = serializers.ListField(child=serializers.CharField(required=True))
    exclusions = serializers.ListField(child=serializers.CharField(required=True))
    default_image = serializers.CharField()

    class Meta:
        model = models.Experience
        fields = (
            'user', 'title', 'description', 'location', 'latitude',
            'longitude', 'terms', 'pax_adults', 'pax_children', 'images',
            'deleted_images', 'inclusions', 'exclusions', 'default_image'
        )

    def validate(self, attrs):
        attrs['coords'] = Point(attrs.pop('latitude'), attrs.pop('longitude'))
        return attrs

    def update(self, instance, validated_data):
        images = validated_data.pop('images')
        default_image = validated_data.pop('default_image')
        deleted_images = validated_data.pop('deleted_images')

        inclusions = validated_data.pop('inclusions')
        exclusions = validated_data.pop('exclusions')

        experience = super(ExperienceUpdateSerializer, self).update(
            instance, validated_data
        )

        # Delete any relevant images
        experience.images.filter(pk__in=[d.id for d in deleted_images]).delete()

        # Add any new images
        for image in images:
            image_serializer = ExperienceImageWriteSerializer(
                data={
                    'image': image,
                    'experience': experience.id,
                }
            )
            image_serializer.is_valid(raise_exception=True)
            image_serializer.save()

        # Set the default image
        for image in experience.images.all():
            if default_image == os.path.basename(image.image.name):
                image.default = True
                image.save()
                break

        # Delete any inclusions not included
        experience.inclusions.exclude(name__in=inclusions).delete()

        # Add any new inclusions
        for inclusion in inclusions:
            if not experience.inclusions.filter(name=inclusion).exists():
                inc_serializer = ExperienceInclusionSerializer(
                    data={'name': inclusion, 'experience': experience.id}
                )
                inc_serializer.is_valid(raise_exception=True)
                inc_serializer.save()

        # Delete any exclusions not included
        experience.exclusions.exclude(name__in=exclusions).delete()

        # Add any new exclusions
        for exclusion in exclusions:
            if not experience.exclusions.filter(name=exclusion).exists():
                exc_serializer = ExperienceExclusionSerializer(
                    data={'name': exclusion, 'experience': experience.id}
                )
                exc_serializer.is_valid(raise_exception=True)
                exc_serializer.save()

        return experience
