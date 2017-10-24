# -*- coding: utf-8 -*-
import logging

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template

from luckybreak.emailer.models import EmailLog
from luckybreak.users.models import User

log = logging.getLogger(__name__)


class BaseEmail(object):
    """
    Base class for emails sent to customers
    """
    def __init__(self, **kwargs):
        self.params = kwargs
        self.params['site'] = Site.objects.get_current()
        self.params['recipient'] = User.objects.get(pk=kwargs['recipient_id'])

    def add_attachments(self, msg):
        """
        Overridden by child classes to add extra attachments
        :param EmailMultiAlternatives msg:
        :return EmailMultiAlternatives:
        """
        pass

    def send(self):
        log.info('Sending {} email to {}'.format(
            self.template_name, self.params['recipient'].email
        ))
        html_template = get_template('emailer/{}/{}.html'.format(
            self.template_name, self.template_name
        ))
        text_template = get_template('emailer/{}/{}.txt'.format(
            self.template_name, self.template_name
        ))

        msg = EmailMultiAlternatives(
            self.subject,
            text_template.render(self.params),
            settings.DEFAULT_FROM_EMAIL,
            [self.params['recipient'].email]
        )
        msg.attach_alternative(
            html_template.render(self.params), 'text/html'
        )
        msg.mixed_subtype = 'related'

        self.add_attachments(msg)

        msg.send()

        EmailLog.objects.create(
            recipient=self.params['recipient'],
            name=self.name,
            subject=self.subject,
            content=html_template.render(self.params)
        )


class ProviderAuctionFinished(BaseEmail):
    name = 'Provider Auction Finished'
    template_name = 'provider_auction_finished'
    subject = 'Your auction has finished'

    def __init__(self, **kwargs):
        super(ProviderAuctionFinished, self).__init__(**kwargs)
        from luckybreak.auctions.models import Auction
        self.params['auction'] = Auction.objects.get(pk=kwargs['auction_id'])


class GuestAuctionWon(BaseEmail):
    name = 'Guest Auction Won'
    template_name = 'guest_auction_won'
    subject = 'You\'re a Winner!'

    def __init__(self, **kwargs):
        super(GuestAuctionWon, self).__init__(**kwargs)
        from luckybreak.auctions.models import Auction
        self.params['auction'] = Auction.objects.get(pk=kwargs['auction_id'])