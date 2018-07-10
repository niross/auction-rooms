Auction Rooms
=============

Hotel Room Auctions!

This project was written by me as a proof of concept and a way to get aquainted with django-channels. The idea was to allow hotels to auction off spare rooms as a way to generate leads and boost their occupancy rates.

The backend uses Django (GeoDjango specifically) with postgres and makes use of django-channels for websocket support for live auctions.

The front end is built using a mixture of standard django templates interspersed with various react components.


Demo
^^^^

You can view the live demo by visiting https://auction-rooms.sonick.co.uk/.

Note that all auctions are for testing purposes only and do not represent actual products/services.

All auctions have a reserve price set to £99,999.00, feel free to bid away.


Getting up and running locally
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

    $ git clone git@github.com:niross/auction-rooms.git
    $ cd auction-rooms
    $ docker-compose -f local.yml build
    $ docker-compose -f local.yml up
    $ gulp --cwd auction_rooms/static/js/apps/ hotload

URL for testing is http://localhost:8000

Emails sent by the system will be viewable at http://localhost:8025/


Testing
^^^^^^^

To run the unit and functional tests, follow the steps above to get up and running locally.

::

    $ run manage.py test --settings config.settings.test


Deployment
----------

TODO
