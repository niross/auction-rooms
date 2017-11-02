from datetime import datetime, timedelta

import pytz
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance
from django.db.models import Sum, F
from django.views.generic import TemplateView, ListView

from luckybreak.auctions.models import Auction
from luckybreak.auctions.tasks import increment_search_appearance_count


class HomepageView(TemplateView):
    template_name = 'browse/homepage.html'

    def get_context_data(self, **kwargs):
        context = super(HomepageView, self).get_context_data(**kwargs)

        context['featured'] = Auction.objects.live().filter(
            featured=True
        ).order_by('created')[:6]

        context['ending'] = Auction.objects.live().filter(
            end_date__lt=datetime.now() + timedelta(days=1)
        ).order_by('end_date')[:6]

        context['latest'] = Auction.objects.live().order_by('-created')[:6]

        return context


class ProviderMarketingView(TemplateView):
    template_name = 'browse/provider_marketing.html'


class SearchResultsView(ListView):
    template_name = 'browse/search_results.html'
    queryset = Auction.objects.live().filter(check_in__gte=datetime.today())
    context_object_name = 'auctions'
    paginate_by = 18
    ordering = ['end_date']

    def get_queryset(self):
        qs = super(SearchResultsView, self).get_queryset()

        # Location
        if 'coords' in self.request.GET and self.request.GET['coords'] != '':
            try:
                pnt = Point(
                    *list(map(float, self.request.GET['coords'].split(',')))
                )
                qs = qs.filter(
                    coords__distance_lte=(pnt, D(mi=200))
                ).annotate(
                    distance=Distance('coords', pnt)
                ).order_by('distance', 'end_date')
            except TypeError:
                pass
            except ValueError:
                pass

        # Pax
        if 'pax' in self.request.GET and self.request.GET['pax'] != '':
            try:
                qs = qs.annotate(
                    pax=Sum(F('pax_adults') + F('pax_children'))
                ).filter(pax__gte=int(self.request.GET['pax']))
            except ValueError:
                pass

        # Date
        if 'date' in self.request.GET and self.request.GET['date'] != '':
            # Show results for 1 day before and 1 day after specified date.
            # Because reasons.
            try:
                date = datetime.strptime(
                    self.request.GET['date'], '%d %B, %Y'
                ).replace(tzinfo=pytz.utc)
                start = date - timedelta(days=2)
                end = date + timedelta(days=2)
                qs = qs.filter(check_in__range=(start, end))
            except ValueError:
                pass

        return qs

    def get_context_data(self, **kwargs):
        context = super(SearchResultsView, self).get_context_data(**kwargs)
        if not self.request.user.is_authenticated() or \
                not self.request.user.is_staff:
            increment_search_appearance_count.delay(
                [x.id for x in context['object_list']]
            )
            pass
        return context
