podman pod stop pod-upload-backend
podman pod rm pod-upload-backend
cd /opt/dmtools/code/flask-mariadb-nginx/flask_dash_upload

uid=1001
gid=1002
subuidSize=$(( $(podman info --format "{{ range \
   .Host.IDMappings.UIDMap }}+{{.Size }}{{end }}" ) - 1 ))
subgidSize=$(( $(podman info --format "{{ range \
   .Host.IDMappings.GIDMap }}+{{.Size }}{{end }}" ) - 1 ))

podman pod create \
--name pod-upload-backend \
--infra-name infra-upload-backend \
--network bridge \
--uidmap 0:1:$uid \
--uidmap $uid:0:1 \
--uidmap $(($uid+1)):$(($uid+1)):$(($subuidSize-$uid)) \
--gidmap 0:1:$gid \
--gidmap $gid:0:1 \
--gidmap $(($gid+1)):$(($gid+1)):$(($subgidSize-$gid)) \
--publish 8002:8002

podman build -t my-dashupload-1 .

##-v /HOST-DIR:/CONTAINER-DIR

podman run -dt \
--name upload_backend-1 \
--pod pod-upload-backend \
--volume /opt/dmtools/uploads:/uploads:z \
--user $uid:$gid \
localhost/my-dashupload-1:latest

