import io
from django.core.files.uploadedfile import SimpleUploadedFile

from django.urls import reverse

from rest_framework import status
from PIL import Image

from luckybreak.common.tests import BaseAPITestCase
from luckybreak.experiences.models import Experience


class ExperienceAPITestCase(BaseAPITestCase):
    def test_unauthed_create_experience(self):
        """
        Unauthenticated users cannot create experiences
        """
        response = self.client.post(
            reverse('experience-api:experience-list'),
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_guest_create_experience(self):
        """
        Guests cannot create experiences
        """
        self.client.force_authenticate(user=self.guest)
        response = self.client.post(
            reverse('experience-api:experience-list'),
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_provider_create_experience(self):
        self.client.force_authenticate(user=self.provider)
        fp = io.BytesIO()
        Image.new('RGB', (10, 100)).save(fp, 'jpeg')
        fp.seek(0)
        image1 = SimpleUploadedFile('image1.jpg', fp.read(), content_type='image/jpeg')
        fp.seek(0)
        image2 = SimpleUploadedFile('image1.jpg', fp.read(), content_type='image/jpeg')

        count = Experience.objects.all().count()
        response = self.client.post(
            reverse('experience-api:experience-list'),
            format='multipart',
            data={
                'title': 'Test Experience',
                'description': 'A test experience. For testing things...',
                'location': 'Nashville, Tennessee',
                'latitude': 0,
                'longitude': 50,
                'images': [image1],
                'inclusions': ['wifi', 'breakfast'],
                'exclusions': ['parking'],
                'banner_image': image2,
                'pax_adults': 10,
                'pax_children': 0,
            }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Experience.objects.all().count(), count + 1)
        experience = Experience.objects.last()
        self.assertEqual(experience.images.count(), 1)
        self.assertEqual(experience.inclusions.count(), 2)
        self.assertEqual(experience.exclusions.count(), 1)

    # def test_unauthed_update_experience(self):
    #     """
    #     Unauthenticated users cannot update experiences
    #     """
    #     response = self.client.post(
    #         reverse('experience-api:experience-detail'),
    #     )
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # def test_guest_update_experience(self):
    #     """
    #     Guests cannot update experiences
    #     """
    #     self.client.force_authenticate(user=self.guest)
    #     response = self.client.post(
    #         reverse('experience-api:experience-detail'),
    #     )
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # def test_update_invalid_experience(self):
    #     """
    #     Provider cannot update an experience that they don't own
    #     """
    #     self.client.force_authenticate(user=self.guest)
    #     response = self.client.post(
    #         reverse('experience-api:experience-detail'),
    #     )
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # def test_provider_update_experience(self):
    #     self.client.force_authenticate(user=self.provider)
    #     fp = io.BytesIO()
    #     Image.new('RGB', (10, 100)).save(fp, 'jpeg')
    #     fp.seek(0)
    #     image1 = SimpleUploadedFile('image1.jpg', fp.read(), content_type='image/jpeg')
    #     fp.seek(0)
    #     image2 = SimpleUploadedFile('image1.jpg', fp.read(), content_type='image/jpeg')

    #     count = Experience.objects.all().count()
    #     response = self.client.post(
    #         reverse('experience-api:experience-detail'),
    #         format='multipart',
    #         data={
    #             'title': 'Test Experience',
    #             'description': 'A test experience. For testing things...',
    #             'location': 'Nashville, Tennessee',
    #             'latitude': 0,
    #             'longitude': 50,
    #             'images': [image1],
    #             'inclusions': ['wifi', 'breakfast'],
    #             'exclusions': ['parking'],
    #             'banner_image': image2
    #         }
    #     )
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(Experience.objects.all().count(), count + 1)
    #     experience = Experience.objects.last()
    #     self.assertEqual(experience.images.count(), 1)
    #     self.assertEqual(experience.inclusions.count(), 2)
    #     self.assertEqual(experience.exclusions.count(), 1)
