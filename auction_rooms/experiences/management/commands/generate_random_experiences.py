import random

import os
from django.contrib.gis.geos import Point
from django.core.files.base import ContentFile
from django.core.management import BaseCommand
from django.conf import settings
from loremipsum import get_sentences, get_paragraphs, get_sentence

from auction_rooms.experiences.models import Experience, ExperienceInclusion, \
    ExperienceExclusion, ExperienceImage
from auction_rooms.users.models import User

CITIES = (
    ('Manchester', 53.480759, -2.242631),
    ('Birmingham', 52.486243, -1.890401),
    ('Brighton', 50.827932, -0.168749),
    ('Bristol', 51.454513, -2.587910),
    ('Oxford', 51.752021, -1.257726),
    ('Cambridge', 52.204267, 0.114908),
    ('Southampton', 50.909700, -1.404351),
    ('Liverpool', 53.408371, -2.991573),
    ('London', 51.507351, -0.127758),
)


class Command(BaseCommand):

    def __init__(self, stdout=None, stderr=None, no_color=False):
        super(Command, self).__init__(
            stdout=stdout, stderr=stderr, no_color=no_color
        )

    def add_arguments(self, parser):
        parser.add_argument(
            '--amount',
            type=int,
            help='How many experiences to create',
            default=5
        )

    @staticmethod
    def _get_images():
        image_dir = str(settings.APPS_DIR('static', 'images', 'demo'))
        return [
            os.path.join(image_dir, x) for x in os.listdir(image_dir)
        ]

    def handle(self, *args, **kwargs):
        provider = User.objects.get(pk=1)
        for i in range(0, kwargs['amount']):
            location = CITIES[random.randint(0, len(CITIES) - 1)]
            experience = Experience.objects.create(
                user=provider,
                title=' '.join(
                    get_sentence().split()[:random.randint(2, 5)]
                ).title(),
                description='\n\n'.join(get_paragraphs(random.randint(1, 3))),
                location=location[0],
                coords=Point(location[1], location[2]),
                terms='\n'.join(get_paragraphs(random.randint(1, 2))),
                pax_adults=random.randint(1, 4),
                pax_children=random.randint(0, 3),
            )

            for inc in get_sentences(random.randint(1, 4)):
                ExperienceInclusion.objects.create(
                    experience=experience,
                    name=' '.join(inc.split()[:random.randint(2, 4)]).title()
                )

            for exc in get_sentences(random.randint(1, 4)):
                ExperienceExclusion.objects.create(
                    experience=experience,
                    name=' '.join(exc.split()[:random.randint(2, 4)]).title()
                )

            images = self._get_images()
            num_images = random.randint(2, 6)
            for i in range(0, num_images):
                image = images.pop(random.randint(0, len(images) - 1))
                with open(image, 'r') as fh:
                    path = os.path.join(
                        settings.MEDIA_ROOT,
                        ExperienceImage.image.field.upload_to,
                        os.path.basename(image)
                    )
                    ei = ExperienceImage(experience=experience, default=i == 0)
                    ei.image.save(path, ContentFile(fh.read()), True)
                    ei.image.name = os.path.join(
                        ExperienceImage.image.field.upload_to,
                        os.path.basename(image)
                    )
                    ei.save()

        print 'Finished creating {} experiences'.format(kwargs['amount'])


