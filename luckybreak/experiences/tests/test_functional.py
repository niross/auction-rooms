import os
import time

from django.test.utils import override_settings

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from PIL import Image

from luckybreak.common.tests import BaseFunctionalTestCase
from luckybreak.experiences.models import Experience


class AddExperienceTestCase(BaseFunctionalTestCase):
    fixtures = ['currencies.json']

    def setUp(self):
        super(AddExperienceTestCase, self).setUp()
        self.selenium.get(self.live_url('account_login'))
        self.selenium.find_element_by_id('id_login').send_keys(self.provider.email)
        self.selenium.find_element_by_id('id_password').send_keys('password')
        self.selenium.find_element_by_id('signin-submit').click()

        # Save a temporary image for uploading during tests
        self.tmp_image_path = '/tmp/tmpimg-{}.jpg'.format(int(time.time()))
        with open(self.tmp_image_path, 'wb') as fh:
            Image.new('RGB', (10, 10)).save(fh, 'jpeg')

    def tearDown(self):
        super(AddExperienceTestCase, self).tearDown()

        # Delete the temporary image
        os.remove(self.tmp_image_path)

    @override_settings(DEBUG=True)
    def test_add_experience(self):
        self.client.force_login(self.provider)
        self.selenium.get(self.live_url('users:dashboard'))
        self.selenium.find_element_by_id('add-experience-button').click()

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
        self.selenium.find_element_by_class_name('experience-success')

        # Ensure the model was created
        experience = Experience.objects.last()
        self.assertEqual(experience.images.count(), 1)
        self.assertEqual(experience.inclusions.count(), 3)
        self.assertEqual(experience.exclusions.count(), 2)


    def test_add_experience_and_auction(self):
        pass
