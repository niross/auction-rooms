from django.views.generic import TemplateView


class HomepageView(TemplateView):
    template_name = 'browse/homepage.html'

    def get_context_data(self, **kwargs):
        context = super(HomepageView, self).get_context_data(**kwargs)
        return context
