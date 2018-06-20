from django import template


register = template.Library()


@register.filter
def highest_bid(auction, user):
    return auction.bids.filter(user=user).first()
