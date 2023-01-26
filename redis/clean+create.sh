podman stop container_redis_1
podman pod stop pod_redis
podman pod rm pod_redis
podman rmi image_redis

cd /opt/dmtools/code/flask-mariadb-nginx/redis

uid=1001
gid=1002
subuidSize=$(( $(podman info --format "{{ range \
   .Host.IDMappings.UIDMap }}+{{.Size }}{{end }}" ) - 1 ))
subgidSize=$(( $(podman info --format "{{ range \
   .Host.IDMappings.GIDMap }}+{{.Size }}{{end }}" ) - 1 ))

podman pod create \
--name pod_redis \
--infra-name infra_redis \
--network bridge \
--uidmap 0:1:$uid \
--uidmap $uid:0:1 \
--uidmap $(($uid+1)):$(($uid+1)):$(($subuidSize-$uid)) \
--gidmap 0:1:$gid \
--gidmap $gid:0:1 \
--gidmap $(($gid+1)):$(($gid+1)):$(($subgidSize-$gid)) \
--publish 6379:6379

podman build -f Dockerfile -t image_redis_1 .
##-v /HOST-DIR:/CONTAINER-DIR

## docker run --name some-redis -d redis redis-server --save 60 1 --loglevel warning

podman run -dt \
--name container_redis_1 \
--pod pod_redis \
--user $uid:$gid \
localhost/image_redis_1:latest
