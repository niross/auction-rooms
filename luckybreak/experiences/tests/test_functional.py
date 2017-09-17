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
        pass


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

    # def test_update_experience_add_auction(self):
        # pass
