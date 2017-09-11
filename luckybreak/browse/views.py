from django.views.generic import TemplateView


class HomepageView(TemplateView):
    template_name = 'browse/homepage.html'

    def get_context_data(self, **kwargs):
        context = super(HomepageView, self).get_context_data(**kwargs)
        # TODO: Add tests for contexts added here
        return context


class ProviderMarketingView(TemplateView):
    template_name = 'browse/provider_marketing.html'
