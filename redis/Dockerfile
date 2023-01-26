FROM redis:latest

ARG USERNAME=agaitske
ARG USER_UID=1001
ARG USER_GID=1002 ## dm group

# Create the user
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME

RUN chown $USER_UID:$USER_GID /data

USER $USERNAME

EXPOSE 6379
##docker run -p 6379:6379 -d redis
##CMD [ "redis-server", "/usr/local/etc/redis/redis.conf" ]
##CMD [ "redis-server", "--save", "--appendonly yes"]
CMD [ "redis-server", "--save ''", "--appendonly no"]
