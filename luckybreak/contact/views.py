from django.views.generic import CreateView
from django.urls import reverse
from django.contrib import messages

from luckybreak.contact.forms import ContactForm


class ContactView(CreateView):
    template_name = 'contact/contact.html'
    form_class = ContactForm

    def get_form_kwargs(self):
        kwargs = super(ContactView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        messages.success(
            self.request,
            'Thanks for your message, We\'ll be in touch asap.'
        )
        return super(ContactView, self).form_valid(form)

    def get_success_url(self):
        return reverse('contact:contact')
