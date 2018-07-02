from django import forms
from django.forms import widgets

from auction_rooms.contact.models import ContactMessage

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ('name', 'email', 'message', 'user')
        widgets = {
            'message': widgets.Textarea(attrs={
                'class': 'materialize-textarea'
            }),
            'user': widgets.HiddenInput()
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(ContactForm, self).__init__(*args, **kwargs)
        if self.user.is_authenticated:
            self.fields['name'].initial = self.user.get_full_name()
            self.fields['email'].initial = self.user.email
            self.fields['user'].initial = self.user

