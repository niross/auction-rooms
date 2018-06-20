from __future__ import unicode_literals

from django.contrib import admin

from auctioneer.experiences import models
from auctioneer.experiences.forms import ExperienceAdminForm


class ExperienceImageAdmin(admin.StackedInline):
    model = models.ExperienceImage
    extra = 1


class ExperienceInclusionAdmin(admin.StackedInline):
    model = models.ExperienceInclusion
    extra = 1


class ExperienceExclusionAdmin(admin.StackedInline):
    model = models.ExperienceInclusion
    extra = 1


class ExperienceAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'location', 'pax_adults', 'pax_children',
        'created', 'modified', 'deleted'
    )
    list_editable = ('deleted',)
    search_fields = ('title', 'description', 'location', 'terms')
    form = ExperienceAdminForm

    inlines = (
        ExperienceImageAdmin, ExperienceInclusionAdmin,
        ExperienceExclusionAdmin
    )

admin.site.register(models.Experience, ExperienceAdmin)
