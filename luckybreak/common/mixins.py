from detective.auctions.models import AuctionSite, FeaturedCategory
from detective.forces.models import PoliceForce


class NavContextMixin(object):
    def get_context_data(self, **kwargs):
        context = super(NavContextMixin, self).get_context_data(**kwargs)
        context.update({
            'forces': PoliceForce.objects.live(),
            'auction_sites': AuctionSite.objects.live(),
            'categories': FeaturedCategory.objects.live(),
            'featured_categories': FeaturedCategory.objects.live().filter(
                show_on_homepage=True
            ),
        })
        return context
