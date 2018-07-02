Auction Rooms
==========

Hotel Room Auctions!


Getting up and running locally
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

    $ git clone git@github.com:niross/auction-rooms.git
    $ cd auction-rooms
    $ docker-compose -f local.yml build
    $ docker-compose -f local.yml up

URL for testing is http://localhost:8000

Emails sent by the system will be viewable at http://localhost:8025/


Test coverage
^^^^^^^^^^^^^

To run the tests, check your test coverage, and generate an HTML coverage report::

    $ coverage run manage.py test
    $ coverage html
    $ open htmlcov/index.html

Running tests with py.test
~~~~~~~~~~~~~~~~~~~~~~~~~~

::

  $ py.test


Deployment
----------

TODO


