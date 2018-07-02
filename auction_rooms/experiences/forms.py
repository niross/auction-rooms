from django import forms

from django.contrib.gis.geos import Point

from auction_rooms.common.widgets.location import LocationWidget
from auction_rooms.experiences.models import Experience


class ExperienceAdminForm(forms.ModelForm):
    latitude = forms.FloatField(widget=forms.HiddenInput())
    longitude = forms.FloatField(widget=forms.HiddenInput())

    class Meta:
        model = Experience
        fields = (
            'title', 'description', 'location', 'pax_adults',
            'pax_children', 'terms',
        )
        widgets = {
            'location': LocationWidget()
        }

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        if instance is not None:
            kwargs.update(initial={
                'latitude': instance.coords.x,
                'longitude': instance.coords.y,
            })

        super(ExperienceAdminForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        experience = super(ExperienceAdminForm, self).save(commit=False)
        experience.coords = Point(
            self.cleaned_data['latitude'],
            self.cleaned_data['longitude']
        )
        experience.save()
        return experience
