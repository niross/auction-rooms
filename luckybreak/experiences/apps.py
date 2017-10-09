from __future__ import unicode_literals

from django.apps import AppConfig


class ExperiencesConfig(AppConfig):
    name = 'luckybreak.experiences'

    def ready(self):
        super(ExperiencesConfig, self).ready()
        from . import signals  # noqa
