import time
from datetime import datetime, timedelta

import pytz
from django.test.utils import override_settings

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from luckybreak.auctions.models import Favourite, Auction, Bid
from luckybreak.common.tests import BaseFunctionalTestCase
from luckybreak.users.models import User


class AddAuctionTestCase(BaseFunctionalTestCase):
    fixtures = ['users.json', 'currencies.json', 'experiences.json']

    def setUp(self):
        super(AddAuctionTestCase, self).setUp()
        self.provider_login()

    @override_settings(DEBUG=True)
    def test_add_auction(self):
        self.client.force_login(self.provider)
        self.selenium.get(self.live_url('auctions:provider-live-auctions'))
        auction_count = self.provider.auctions().count()

        # Open the modal
        self.selenium.execute_script(
            'document.getElementById("provider-add-auction-button").click()'
        )

        # Select an experience
        WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'collection-item'))
        )
        self.selenium.find_element_by_class_name('collection-item').click()

        # Next page
        self.selenium.find_element_by_class_name('next-button').click()

        # Check in date
        self.selenium.find_element_by_id('auction-checkin-date').click()
        WebDriverWait(self.selenium, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'picker--opened'))
        )
        picker = self.selenium.find_element_by_class_name('picker--opened')
        picker.find_element_by_class_name('picker__nav--next').click()
        picker.find_element_by_class_name('picker__nav--next').click()
        picker.find_element_by_class_name('picker__day--infocus').click()

        # Check in time
        WebDriverWait(self.selenium, 10).until(
            EC.element_to_be_clickable((By.ID, 'auction-checkin-time'))
        )
        self.selenium.execute_script('$(\'#auction-checkin-time\').click()')
        WebDriverWait(self.selenium, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'picker--opened'))
        )
        picker = self.selenium.find_element_by_class_name('picker--opened')

        hours = self.selenium.find_element_by_class_name('clockpicker-hours')
        minutes = self.selenium.find_element_by_class_name('clockpicker-minutes')
        hours.find_elements_by_class_name('clockpicker-tick')[14].click()
        minutes.find_elements_by_class_name('clockpicker-tick')[0].click()
        WebDriverWait(picker, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'picker__close'))
        )
        picker.find_elements_by_class_name('picker__close')[1].click()

        # Check out date
        WebDriverWait(self.selenium, 10).until(
            EC.visibility_of_element_located((By.ID, 'auction-checkout-date'))
        )
        self.selenium.find_element_by_id('auction-checkout-date').click()
        WebDriverWait(self.selenium, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'picker--opened'))
        )
        picker = self.selenium.find_element_by_class_name('picker--opened')

        picker.find_element_by_class_name('picker__nav--next').click()
        picker.find_element_by_class_name('picker__nav--next').click()
        picker.find_element_by_class_name('picker__nav--next').click()
        picker.find_element_by_class_name('picker__day--infocus').click()

        # Check out time
        WebDriverWait(self.selenium, 10).until(
            EC.visibility_of_element_located((By.ID, 'auction-checkout-time'))
        )
        self.selenium.execute_script('$(\'#auction-checkout-time\').click()')

        WebDriverWait(self.selenium, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'picker--opened'))
        )
        picker = self.selenium.find_element_by_class_name('picker--opened')
        hours = picker.find_element_by_class_name('clockpicker-hours')
        minutes = picker.find_element_by_class_name('clockpicker-minutes')
        hours.find_elements_by_class_name('clockpicker-tick')[11].click()
        minutes.find_elements_by_class_name('clockpicker-tick')[0].click()
        WebDriverWait(picker, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'picker__close'))
        )
        picker.find_elements_by_class_name('picker__close')[1].click()

        # Next page
        self.selenium.find_element_by_class_name('next-button').click()

        # Start price
        self.selenium.find_element_by_id('auction-starting-price').clear()
        self.selenium.find_element_by_id('auction-starting-price').send_keys('29.99')

        # Reserve price
        self.selenium.find_element_by_id('auction-reserve-price').clear()
        self.selenium.find_element_by_id('auction-reserve-price').send_keys('99.99')

        # Number of lots
        self.selenium.find_element_by_id('auction-lots').clear()
        self.selenium.find_element_by_id('auction-lots').send_keys('3')

        # Submit form
        self.selenium.find_element_by_class_name('next-button').click()

        # Success
        WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'auction-success'))
        )

        # 3 auctions should be created
        self.assertEqual(self.provider.auctions().count(), auction_count + 3)


class ProviderAuctionListTestCase(BaseFunctionalTestCase):
    fixtures = ['users.json', 'currencies.json', 'experiences.json']

    def setUp(self):
        super(ProviderAuctionListTestCase, self).setUp()
        self.provider_login()

    def test_live_auctions(self):
        self.selenium.get(self.live_url('auctions:provider-live-auctions'))
        self.selenium.find_element_by_class_name('provider-auctions').click()

    def test_finished_auctions(self):
        self.selenium.get(self.live_url('auctions:provider-finished-auctions'))
        self.selenium.find_element_by_class_name('provider-auctions').click()


class ProviderAuctionDetailTestCase(BaseFunctionalTestCase):
    fixtures = [
        'users.json', 'currencies.json', 'experiences.json', 'auctions.json'
    ]

    def setUp(self):
        super(ProviderAuctionDetailTestCase, self).setUp()
        self.provider_login()

    def test_page_load(self):
        self.selenium.get(
            self.live_url('auctions:provider-auction', {'pk': 1})
        )
        self.selenium.find_element_by_class_name('provider-auction').click()


class WonAuctionsTestCase(BaseFunctionalTestCase):
    fixtures = [
        'users.json', 'currencies.json', 'experiences.json', 'auctions.json'
    ]

    def test_view_confirm_modal(self):
        self.guest_login()

        auction = Auction.objects.get(pk=1)
        Bid.objects.create(
            user=self.guest,
            auction=auction,
            price=auction.reserve_price + 1
        )
        auction.end_date = datetime.now(pytz.UTC) - timedelta(hours=1)
        auction.mark_complete()

        self.selenium.get(
            self.live_url('auctions:won-auctions')
        )
        self.selenium.find_element_by_class_name('modal-trigger').click()
        WebDriverWait(self.selenium, 10).until(
            EC.visibility_of_element_located(
                (By.CLASS_NAME, 'guest-confirmation-modal')
            )
        )


class AuctionFavouriteTestCase(BaseFunctionalTestCase):
    fixtures = [
        'users.json', 'currencies.json', 'experiences.json', 'auctions.json'
    ]

    def test_guest_signin_add_favourite(self):
        self.selenium.get(self.live_url('browse:homepage'))
        auction = self.selenium.find_element_by_id('auction-1')
        self.selenium.execute_script("arguments[0].scrollIntoView();", auction)
        auction.find_element_by_class_name('auction-favourite').click()
        self.selenium.find_element_by_id('id_login').send_keys(self.guest.email)
        self.selenium.find_element_by_id('id_password').send_keys('password')
        self.selenium.find_element_by_id('signin-submit').click()
        self.wait_for_page_load()
        self.assertEqual(self.guest.favourites.count(), 1)

    def test_provider_signin_add_favourite(self):
        self.selenium.get(self.live_url('browse:homepage'))
        auction = self.selenium.find_element_by_id('auction-1')
        self.selenium.execute_script("arguments[0].scrollIntoView();", auction)
        auction.find_element_by_class_name('auction-favourite').click()
        self.selenium.find_element_by_id('id_login').send_keys(
            self.provider.email
        )
        self.selenium.find_element_by_id('id_password').send_keys('password')
        self.selenium.find_element_by_id('signin-submit').click()
        self.wait_for_page_load()
        self.assertEqual(self.provider.favourites.count(), 1)

    def test_guest_signup_add_favourite(self):
        self.selenium.get(self.live_url('browse:homepage'))
        auction = self.selenium.find_element_by_id('auction-1')
        self.selenium.execute_script("arguments[0].scrollIntoView();", auction)
        auction.find_element_by_class_name('auction-favourite').click()
        self.selenium.find_element_by_class_name('guest-signup-link').click()
        self.selenium.find_element_by_id('id_first_name').send_keys('Felicia')
        self.selenium.find_element_by_id('id_last_name').send_keys('Pearson')
        self.selenium.find_element_by_id('id_email').send_keys(
            'felicia@hotmail.com'
        )
        self.selenium.find_element_by_id('id_password1').send_keys('Adsasf34')
        self.selenium.find_element_by_id('id_password2').send_keys('Adsasf34')
        self.selenium.find_element_by_id('signup-submit').click()
        user = User.objects.get(email='felicia@hotmail.com')
        self.assertEqual(user.favourites.count(), 1)

    def test_provider_signup_add_favourite(self):
        self.selenium.get(self.live_url('browse:homepage'))
        auction = self.selenium.find_element_by_id('auction-1')
        self.selenium.execute_script("arguments[0].scrollIntoView();", auction)
        auction.find_element_by_class_name('auction-favourite').click()
        self.selenium.find_element_by_class_name('provider-signup-link').click()
        self.selenium.find_element_by_id('id_first_name').send_keys('Omar')
        self.selenium.find_element_by_id('id_last_name').send_keys('Little')
        self.selenium.find_element_by_id('id_email').send_keys(
            'omar@hotmail.com'
        )
        self.selenium.find_element_by_id('id_phone').send_keys('1234567890')
        self.selenium.find_element_by_id('id_password1').send_keys('Adsasf34')
        self.selenium.find_element_by_id('id_password2').send_keys('Adsasf34')
        self.selenium.find_element_by_id('signup-submit').click()
        user = User.objects.get(email='omar@hotmail.com')
        self.assertEqual(user.favourites.count(), 1)

    def test_guest_add_favourite(self):
        self.guest_login()
        self.selenium.get(self.live_url('browse:homepage'))
        auction = self.selenium.find_element_by_id('auction-1')
        self.selenium.execute_script("arguments[0].scrollIntoView();", auction)
        auction.find_element_by_class_name('auction-favourite').click()
        WebDriverWait(self.selenium, 10).until(
            lambda driver: driver.execute_script('return jQuery.active == 0')
        )
        self.assertEqual(self.guest.favourites.count(), 1)

    def test_provider_add_favourite(self):
        self.provider_login()
        self.selenium.get(self.live_url('browse:homepage'))
        auction = self.selenium.find_element_by_id('auction-1')
        self.selenium.execute_script("arguments[0].scrollIntoView();", auction)
        auction.find_element_by_class_name('auction-favourite').click()
        WebDriverWait(self.selenium, 10).until(
            lambda driver: driver.execute_script('return jQuery.active == 0')
        )
        self.assertEqual(self.provider.favourites.count(), 1)

    def test_guest_remove_favourite(self):
        self.guest_login()
        Favourite.objects.create(
            auction=Auction.objects.get(pk=1),
            user=self.guest
        )
        self.selenium.get(self.live_url('browse:homepage'))
        self.wait_for_page_load()
        WebDriverWait(self.selenium, 10).until(
            lambda driver: driver.execute_script('return jQuery.active == 0')
        )
        auction = self.selenium.find_element_by_id('auction-1')
        self.selenium.execute_script("arguments[0].scrollIntoView();", auction)
        auction.find_element_by_class_name('auction-favourite').click()
        WebDriverWait(self.selenium, 10).until(
            lambda driver: driver.execute_script('return jQuery.active == 0')
        )
        self.assertEqual(self.guest.favourites.count(), 0)

    def test_provider_remove_favourite(self):
        self.provider_login()
        Favourite.objects.create(
            auction=Auction.objects.get(pk=1),
            user=self.provider
        )
        self.selenium.get(self.live_url('browse:homepage'))
        self.wait_for_page_load()
        auction = self.selenium.find_element_by_id('auction-1')
        self.selenium.execute_script("arguments[0].scrollIntoView();", auction)
        auction.find_element_by_class_name('auction-favourite').click()
        WebDriverWait(self.selenium, 10).until(
            lambda driver: driver.execute_script('return jQuery.active == 0')
        )
        self.assertEqual(self.provider.favourites.count(), 0)


# FIXME: ChannelLiveServerTestCase is too unreliable so there is no
# nice way to test bidding currently
# class PublicAuctionBidTestCase(BaseChannelLiveServerTestCase):
#     fixtures = [
#         'users.json', 'currencies.json', 'experiences.json', 'auctions.json'
#     ]
#
#     def test_favourite_auction_unauthed(self):
#         self.selenium.get(
#             self.live_url('auctions:public-auction', kwargs={'pk': 1})
#         )
#         fav = self.selenium.find_element_by_class_name('favourite')
#         self.scroll_to(fav)
#         fav.click()
#         self.selenium.find_element_by_id('signin-submit')
#
#     def test_favourite_auction(self):
#         pass
#
#     def test_unfavourite_auction(self):
#         pass
#
#     def test_bid_unauthed(self):
#         self.selenium.get(
#             self.live_url('auctions:public-auction', kwargs={'pk': 1})
#         )
#         WebDriverWait(self.selenium, 10).until(
#             EC.element_to_be_clickable((By.CLASS_NAME, 'bid'))
#         )
#         self.selenium.find_element_by_class_name('bid').click()
#         self.selenium.find_element_by_id('signin-submit')
#
#     def test_bid(self):
#         self.guest_login()
#         cur_price = Auction.objects.get(pk=1).current_price()
#         self.selenium.get(
#             self.live_url('auctions:public-auction', kwargs={'pk': 1})
#         )
#         WebDriverWait(self.selenium, 10).until(
#             EC.element_to_be_clickable((By.CLASS_NAME, 'bid'))
#         )
#         self.selenium.find_element_by_class_name('bid').click()
#         WebDriverWait(self.selenium, 10).until(
#             EC.presence_of_element_located((By.ID, 'accept'))
#         )
#         self.selenium.find_element_by_id('accept').click()
#         WebDriverWait(self.selenium, 10).until(
#             EC.invisibility_of_element_located((By.ID, 'accept'))
#         )
#         self.assertEqual(
#             Auction.objects.get(pk=1).current_price(), cur_price + 1
#         )
