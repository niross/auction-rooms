import os
import time

from django.test.utils import override_settings

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from PIL import Image

from auctioneer.common.tests import BaseFunctionalTestCase
from auctioneer.experiences.models import Experience


class BaseExperienceTestCase(BaseFunctionalTestCase):
    fixtures = ['users.json', 'currencies.json', 'experiences.json']

    def setUp(self):
        super(BaseExperienceTestCase, self).setUp()
        self.provider_login()

        # Save a temporary image for uploading during tests
        self.tmp_image_path = '/tmp/tmpimg-{}.jpg'.format(int(time.time()))
        with open(self.tmp_image_path, 'wb') as fh:
            Image.new('RGB', (10, 10)).save(fh, 'jpeg')

    def tearDown(self):
        super(BaseExperienceTestCase, self).tearDown()

        # Delete the temporary image
        os.remove(self.tmp_image_path)


class AddExperienceTestCase(BaseExperienceTestCase):
    @override_settings(DEBUG=True)
    def test_add_experience(self):
        self.client.force_login(self.provider)
        self.selenium.get(self.live_url('experiences:experiences'))
        self.selenium.execute_script('document.getElementById("add-experience-button").click()')

        # Basic
        self.selenium.find_element_by_id('experience-title').send_keys('Test Experience')

        self.selenium.find_element_by_id('experience-location').send_keys('b')
        WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.ID, 'PlacesAutocomplete__autocomplete-container'))
        )
        self.selenium.find_element_by_id('experience-location').send_keys(Keys.ARROW_DOWN)
        self.selenium.find_element_by_id('experience-location').send_keys(Keys.ENTER)


        self.selenium.find_element_by_id('experience-pax-adults').send_keys('3')
        self.selenium.find_element_by_id('experience-pax-children').send_keys('2')
        self.selenium.find_element_by_id('experience-description').send_keys(
            'Test description for a test experience.'
        )

        self.selenium.find_element_by_class_name('next-button').click()

        # Images
        WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.XPATH, '//input[@type=\'file\']'))
        )
        dz = self.selenium.find_element_by_xpath("//input[@type='file']")
        dz.send_keys(self.tmp_image_path)
        self.selenium.find_element_by_class_name('next-button').click()

        # Extra details
        self.selenium.find_element_by_id('experience-inclusions').send_keys(
            'inclusion1\ninclusion2\ninclusion3'
        )
        self.selenium.find_element_by_id('experience-exclusions').send_keys(
            'exclusion1\nexclusion2'
        )
        self.selenium.find_element_by_id('experience-terms').send_keys(
            'Some terms and conditions'
        )
        self.selenium.find_element_by_class_name('next-button').click()

        # Success
        WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'experience-success'))
        )

        # Ensure the model was created
        experience = Experience.objects.latest('created')
        self.assertEqual(experience.images.count(), 1)
        self.assertEqual(experience.inclusions.count(), 3)
        self.assertEqual(experience.inclusions.filter(name='inclusion1').count(), 1)
        self.assertEqual(experience.inclusions.filter(name='inclusion2').count(), 1)
        self.assertEqual(experience.inclusions.filter(name='inclusion3').count(), 1)
        self.assertEqual(experience.exclusions.count(), 2)
        self.assertEqual(experience.exclusions.filter(name='exclusion1').count(), 1)
        self.assertEqual(experience.exclusions.filter(name='exclusion2').count(), 1)

    def test_add_experience_and_auction(self):
        self.client.force_login(self.provider)
        auction_count = self.provider.auctions().count()
        self.selenium.get(self.live_url('experiences:experiences'))
        self.selenium.execute_script(
            'document.getElementById("add-experience-button").click()'
        )

        # Basic
        self.selenium.find_element_by_id('experience-title').send_keys('Test Experience')

        self.selenium.find_element_by_id('experience-location').send_keys('b')
        WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.ID, 'PlacesAutocomplete__autocomplete-container'))
        )
        self.selenium.find_element_by_id('experience-location').send_keys(Keys.ARROW_DOWN)
        self.selenium.find_element_by_id('experience-location').send_keys(Keys.ENTER)


        self.selenium.find_element_by_id('experience-pax-adults').send_keys('3')
        self.selenium.find_element_by_id('experience-pax-children').send_keys('2')
        self.selenium.find_element_by_id('experience-description').send_keys(
            'Test description for a test experience.'
        )

        self.selenium.find_element_by_class_name('next-button').click()

        # Images
        WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.XPATH, '//input[@type=\'file\']'))
        )
        dz = self.selenium.find_element_by_xpath("//input[@type='file']")
        dz.send_keys(self.tmp_image_path)
        self.selenium.find_element_by_class_name('next-button').click()

        # Extra details
        self.selenium.find_element_by_id('experience-inclusions').send_keys(
            'inclusion1\ninclusion2\ninclusion3'
        )
        self.selenium.find_element_by_id('experience-exclusions').send_keys(
            'exclusion1\nexclusion2'
        )
        self.selenium.find_element_by_id('experience-terms').send_keys(
            'Some terms and conditions'
        )
        self.selenium.find_element_by_class_name('next-button').click()

        # Success
        WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'experience-success'))
        )
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

        # Ensure the model was created
        experience = Experience.objects.latest('created')
        self.assertEqual(experience.images.count(), 1)
        self.assertEqual(experience.inclusions.count(), 3)
        self.assertEqual(experience.inclusions.filter(name='inclusion1').count(), 1)
        self.assertEqual(experience.inclusions.filter(name='inclusion2').count(), 1)
        self.assertEqual(experience.inclusions.filter(name='inclusion3').count(), 1)
        self.assertEqual(experience.exclusions.count(), 2)
        self.assertEqual(experience.exclusions.filter(name='exclusion1').count(), 1)
        self.assertEqual(experience.exclusions.filter(name='exclusion2').count(), 1)


class UpdateExperienceTestCase(BaseExperienceTestCase):
    @override_settings(DEBUG=True)
    def test_update_experience(self):
        self.client.force_login(self.provider)
        self.selenium.get(self.live_url('experiences:experiences'))

        experience = Experience.objects.last()
        self.selenium.find_element_by_id(
            'edit-experience-button-{}'.format(experience.id)
        ).click()

        modal = self.selenium.find_element_by_id('experience-modal-{}'.format(experience.id))

        # Basic
        WebDriverWait(modal, 10).until(
            EC.element_to_be_clickable((By.NAME, 'experience-title'))
        )
        modal.find_element_by_name('experience-title').clear()
        modal.find_element_by_name('experience-title').send_keys('Updated Experience')

        modal.find_element_by_id('experience-location').clear()
        modal.find_element_by_id('experience-location').send_keys('z')
        WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.ID, 'PlacesAutocomplete__autocomplete-container'))
        )
        modal.find_element_by_id('experience-location').send_keys(Keys.ARROW_DOWN)
        modal.find_element_by_id('experience-location').send_keys(Keys.ENTER)

        modal.find_element_by_id('experience-pax-adults').clear()
        modal.find_element_by_id('experience-pax-adults').send_keys('1')

        modal.find_element_by_id('experience-pax-children').clear()
        modal.find_element_by_id('experience-pax-children').send_keys('1')

        modal.find_element_by_id('experience-description').clear()
        modal.find_element_by_id('experience-description').send_keys(
            'Updated Description.'
        )

        modal.find_element_by_class_name('next-button').click()

        # Images
        WebDriverWait(modal, 10).until(
            EC.presence_of_element_located((By.XPATH, '//input[@type=\'file\']'))
        )
        dz = modal.find_element_by_xpath("//input[@type='file']")
        dz.send_keys(self.tmp_image_path)
        modal.find_element_by_class_name('next-button').click()

        # Extra details
        modal.find_element_by_id('experience-inclusions').clear()
        modal.find_element_by_id('experience-inclusions').send_keys(
            'Inclusion 1\nInclusion 2\nInclusion 3'
        )
        modal.find_element_by_id('experience-exclusions').clear()
        modal.find_element_by_id('experience-exclusions').send_keys(
            'Exclusion 1\nExclusion 2\nExclusion 3'
        )
        modal.find_element_by_id('experience-terms').clear()
        modal.find_element_by_id('experience-terms').send_keys(
            'Updated terms and conditions'
        )
        modal.find_element_by_class_name('next-button').click()

        # Success
        WebDriverWait(modal, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'experience-success'))
        )

        # Ensure the model was created
        experience = Experience.objects.last()
        self.assertEqual(experience.images.count(), 3)
        self.assertEqual(experience.inclusions.count(), 3)
        self.assertEqual(experience.inclusions.filter(name='Inclusion 1').count(), 1)
        self.assertEqual(experience.inclusions.filter(name='Inclusion 2').count(), 1)
        self.assertEqual(experience.inclusions.filter(name='Inclusion 3').count(), 1)
        self.assertEqual(experience.exclusions.count(), 3)
        self.assertEqual(experience.exclusions.filter(name='Exclusion 1').count(), 1)
        self.assertEqual(experience.exclusions.filter(name='Exclusion 2').count(), 1)
        self.assertEqual(experience.exclusions.filter(name='Exclusion 3').count(), 1)

    def test_update_experience_add_auction(self):
        self.client.force_login(self.provider)
        auction_count = self.provider.auctions().count()
        self.selenium.get(self.live_url('experiences:experiences'))

        experience = Experience.objects.last()
        self.selenium.find_element_by_id(
            'edit-experience-button-{}'.format(experience.id)
        ).click()
        self.selenium.execute_script(
            'document.getElementById("edit-experience-button-{}")'
            '.click()'.format(
                experience.id
            )
        )

        modal = self.selenium.find_element_by_id('experience-modal-{}'.format(experience.id))

        # Basic
        WebDriverWait(modal, 10).until(
            EC.element_to_be_clickable((By.NAME, 'experience-title'))
        )
        modal.find_element_by_name('experience-title').clear()
        modal.find_element_by_name('experience-title').send_keys('Updated Experience')

        modal.find_element_by_id('experience-location').clear()
        modal.find_element_by_id('experience-location').send_keys('z')
        WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.ID, 'PlacesAutocomplete__autocomplete-container'))
        )
        modal.find_element_by_id('experience-location').send_keys(Keys.ARROW_DOWN)
        modal.find_element_by_id('experience-location').send_keys(Keys.ENTER)

        modal.find_element_by_id('experience-pax-adults').clear()
        modal.find_element_by_id('experience-pax-adults').send_keys('1')

        modal.find_element_by_id('experience-pax-children').clear()
        modal.find_element_by_id('experience-pax-children').send_keys('1')

        modal.find_element_by_id('experience-description').clear()
        modal.find_element_by_id('experience-description').send_keys(
            'Updated Description.'
        )

        modal.find_element_by_class_name('next-button').click()

        # Images
        WebDriverWait(modal, 10).until(
            EC.presence_of_element_located((By.XPATH, '//input[@type=\'file\']'))
        )
        dz = modal.find_element_by_xpath("//input[@type='file']")
        dz.send_keys(self.tmp_image_path)
        modal.find_element_by_class_name('next-button').click()

        # Extra details
        modal.find_element_by_id('experience-inclusions').clear()
        modal.find_element_by_id('experience-inclusions').send_keys(
            'Inclusion 1\nInclusion 2\nInclusion 3'
        )
        modal.find_element_by_id('experience-exclusions').clear()
        modal.find_element_by_id('experience-exclusions').send_keys(
            'Exclusion 1\nExclusion 2\nExclusion 3'
        )
        modal.find_element_by_id('experience-terms').clear()
        modal.find_element_by_id('experience-terms').send_keys(
            'Updated terms and conditions'
        )
        modal.find_element_by_class_name('next-button').click()

        # Success
        WebDriverWait(modal, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'experience-success'))
        )

        WebDriverWait(modal, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'next-button'))
        )

        modal.find_element_by_class_name('next-button').click()

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
        modal.find_element_by_class_name('next-button').click()

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
        modal.find_element_by_class_name('next-button').click()

        # Success
        WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'auction-success'))
        )

        # 3 auctions should be created
        self.assertEqual(self.provider.auctions().count(), auction_count + 3)

        # Ensure the model was created
        experience = Experience.objects.last()
        self.assertEqual(experience.images.count(), 3)
        self.assertEqual(experience.inclusions.count(), 3)
        self.assertEqual(experience.inclusions.filter(name='Inclusion 1').count(), 1)
        self.assertEqual(experience.inclusions.filter(name='Inclusion 2').count(), 1)
        self.assertEqual(experience.inclusions.filter(name='Inclusion 3').count(), 1)
        self.assertEqual(experience.exclusions.count(), 3)
        self.assertEqual(experience.exclusions.filter(name='Exclusion 1').count(), 1)
        self.assertEqual(experience.exclusions.filter(name='Exclusion 2').count(), 1)
        self.assertEqual(experience.exclusions.filter(name='Exclusion 3').count(), 1)
