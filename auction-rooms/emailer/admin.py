# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import EmailLog


class EmailLogAdmin(admin.ModelAdmin):
    list_display = ('name', 'recipient', 'subject', 'created')
    fields = ('name', 'recipient', 'created', 'subject', 'content_as_html')
    readonly_fields = (
        'name', 'recipient', 'created', 'subject', 'content_as_html'
    )

    def content_as_html(self, obj):
        return mark_safe(obj.content)
    content_as_html.short_description = 'Content'


admin.site.register(EmailLog, EmailLogAdmin)
