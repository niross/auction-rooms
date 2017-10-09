from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from luckybreak.auctions import models


class BidAdmin(admin.TabularInline):
    model = models.Bid
    fields = ('user', 'price')
    readonly_fields = ('user', 'price')
    extra = 0
    can_delete = False
    max_num = 0


class AuctionAdmin(admin.ModelAdmin):
    list_display = (
        'formatted_name', 'bids', 'formatted_current_price',
        'experience_link', 'end_date'
    )
    readonly_fields = (
        'experience', 'view_count', 'search_appearance_count'
    )
    fields = (
        'experience', 'check_in', 'check_out', 'currency',
        'starting_price', 'reserve_price', 'end_date', 'featured',
        'view_count', 'search_appearance_count',
    )

    inlines = (BidAdmin,)

    def formatted_name(self, auction):  # pylint: disable=no-self-use
        return '{} Auction: {}'.format(
            auction.get_status_display(), auction.experience.title
        )
    formatted_name.short_description = 'Auction'

    def formatted_current_price(self, auction):  # pylint: disable=no-self-use
        return auction.formatted_current_price()
    formatted_current_price.short_description = 'Current Price'

    def bids(self, auction):  # pylint: disable=no-self-use
        return auction.bids.count()

    def experience_link(self, auction):  # pylint: disable=no-self-use
        return format_html(
            '<a href="{}">{}</a>',
            reverse(
                'admin:experiences_experience_change',
                args=(auction.experience.id,)
            ),
            auction.experience.title
        )
    experience_link.short_description = 'Experience'


admin.site.register(models.Auction, AuctionAdmin)
