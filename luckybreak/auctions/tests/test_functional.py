from django.test.utils import override_settings

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from luckybreak.common.tests import BaseFunctionalTestCase


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
        self.selenium.find_element_by_id('provider-add-auction-button').click()

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
