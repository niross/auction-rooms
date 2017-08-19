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
        'experience', 'check_in', 'check_out', 'starting_price',
        'reserve_price', 'end_date', 'view_count', 'search_appearance_count',
    )

    inlines = (BidAdmin,)

    @staticmethod
    def formatted_name(auction):
        return '{} Auction: {}'.format(
            auction.status(), auction.experience.title
        )
    formatted_name.short_description = 'Auction'

    @staticmethod
    def formatted_current_price(auction):
        return auction.formatted_current_price
    formatted_current_price.short_description = 'Current Price'

    @staticmethod
    def bids(auction):
        return auction.bids.count()

    @staticmethod
    def experience_link(auction):
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
