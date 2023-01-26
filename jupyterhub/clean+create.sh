uid=1001
gid=1002
subuidSize=$(( $(podman info --format "{{ range \
   .Host.IDMappings.UIDMap }}+{{.Size }}{{end }}" ) - 1 ))
subgidSize=$(( $(podman info --format "{{ range \
   .Host.IDMappings.GIDMap }}+{{.Size }}{{end }}" ) - 1 ))

#--uidmap 0:1:$uid \
#--uidmap $uid:0:1 \
#--uidmap $(($uid+1)):$(($uid+1)):$(($subuidSize-$uid)) \
#--gidmap 0:1:$gid \
#--gidmap $gid:0:1 \
#--gidmap $(($gid+1)):$(($gid+1)):$(($subgidSize-$gid)) \

podman network create jupyter_network

podman pod create \
--name pod-jupyterhub \
--infra-name infra-jupyterhub \
--network jupyter_network \
--publish 8000:8000 --publish 8002:8002 --publish 8080:8080

podman build -t my-jupyterhub-1 .

##-v /HOST-DIR:/CONTAINER-DIR

podman run -dt \
--name jupyterhub \
--pod pod-jupyterhub \
--volume /var/run/docker.sock:///workdir/jupyterhub//.docker/run/docker.sock \
localhost/my-jupyterhub-1:latest

##--volume /var/run/docker.sock:/var/run/docker.sock \
##--volume /opt/dmtools/notebooks:/workdir/notebooks:z \
##--user $uid:$gid \
