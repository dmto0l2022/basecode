# podman run -it --userns=keep-id registry.access.redhat.com/rhel7/rhel /bin/bash

podman rmi $(podman images -qa) -f
podman system reset

podman pod stop pod_main_backend
podman pod rm pod_main_backend

uid=${ENV_UID} ##1001
gid=${ENV_GID} ##1002
#uid=1001
#gid=1002
#env_username=${ENV_USERNAME}
#env_groupname=${ENV_GROUPNAME}

subuidSize=$(( $(podman info --format "{{ range \
   .Host.IDMappings.UIDMap }}+{{.Size }}{{end }}" ) - 1 ))
subgidSize=$(( $(podman info --format "{{ range \
   .Host.IDMappings.GIDMap }}+{{.Size }}{{end }}" ) - 1 ))

# as root inside

#podman pod create \
#--name pod_main_backend \
#--infra-name infra_main_backend \
#--network bridge \
#--publish 8002:8002 \
#--publish 8004:8004 \
#--publish 8006:8006 \
#--publish 8008:8008 \
#--publish 3306:3306 \
#--publish 6379:6379

#podman pod create \
#--name pod_main_backend \
#--infra-name infra_main_backend \
#--network bridge \
#--userns=keep-id \
#--publish 8002:8002 \
#--publish 8004:8004 \
#--publish 8006:8006 \
#--publish 8008:8008 \
#--publish 3306:3306 \
#--publish 6379:6379


#### DEVELOPMENT ###
#podman pod create \
#--name pod_main_backend \
#--infra-name infra_main_backend \
#--network bridge \
#--uidmap 0:1:$uid \
#--uidmap $uid:0:1 \
#--uidmap $(($uid+1)):$(($uid+1)):$(($subuidSize-$uid)) \
#--gidmap 0:1:$gid \
#--gidmap $gid:0:1 \
#--gidmap $(($gid+1)):$(($gid+1)):$(($subgidSize-$gid)) \
#--publish 8002:8002 \
#--publish 8004 \
#--publish 8006 \
#--publish 8008:8008 \
#--publish 8010:8010 \
#--publish 8012:8012 \
#--publish 8014:8014 \
#--publish 8016:8016 \
#--publish 3306:3306 \
#--publish 6379


### PRODUCTION ###
podman pod create \
--name pod_main_backend \
--infra-name infra_main_backend \
--network bridge \
--uidmap 0:1:$uid \
--uidmap $uid:0:1 \
--uidmap $(($uid+1)):$(($uid+1)):$(($subuidSize-$uid)) \
--gidmap 0:1:$gid \
--gidmap $gid:0:1 \
--gidmap $(($gid+1)):$(($gid+1)):$(($subgidSize-$gid)) \
--publish 8010:8010 \
--publish 8014:8014 \
--publish 8016:8016 \
--publish 3306:3306 \
--publish 6379

