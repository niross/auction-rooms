from django.views.generic import TemplateView

from luckybreak.auctions.models import Auction


class HomepageView(TemplateView):
    template_name = 'browse/homepage.html'

    def get_context_data(self, **kwargs):
        context = super(HomepageView, self).get_context_data(**kwargs)
        context['featured'] = Auction.objects.live().filter(
            featured=True
        ).order_by('created')[:6]
        context['ending'] = Auction.objects.live().filter().order_by(
            'end_date'
        )[:6]
        return context


class ProviderMarketingView(TemplateView):
    template_name = 'browse/provider_marketing.html'
