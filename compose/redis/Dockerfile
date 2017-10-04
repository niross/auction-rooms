FROM redis:latest

ADD compose/redis/start-redis.sh /start-redis.sh
RUN chmod -v +x /start-redis.sh

COPY ./compose/redis/redis.conf /usr/local/etc/redis/redis.conf

CMD ["/start-redis.sh"]
