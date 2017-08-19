from django.forms.utils import flatatt
from django.forms.widgets import Input
from django.utils.encoding import force_text
from django.utils.html import format_html
from django.conf import settings


class LocationWidget(Input):
    input_type = 'text'

    class Media:
        js = (
            'https://cdnjs.cloudflare.com/ajax/libs/jquery/3.1.1/jquery.js',
            'https://maps.googleapis.com/maps/api/js?v=3.exp&sensor=false&'
            'libraries=places&key={}'.format(settings.GOOGLE_MAPS_KEY),
            'js/location-typeahead.js',
            'js/admin/location-widget.js',
        )

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        if value != '':
            # Only add the 'value' attribute if a value is non-empty.
            final_attrs['value'] = force_text(self._format_value(value))

        return format_html(u'<input{} />', flatatt(final_attrs))
