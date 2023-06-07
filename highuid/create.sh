#podman \
#   run \
#    --privileged \
#    --rm \
#    --uidmap=0:0:10000 \
#    --uidmap=65534:10000:1 \
#    --uidmap=7200720:10001:1 \
#     quay.io/buildah/stable buildah bud -t img1
     
     
podman build -f Dockerfile -t highuid_image .

##-v /HOST-DIR:/CONTAINER-DIR

podman run -dt \
--name highuid_container \
--uidmap=0:0:10000 \
--uidmap=65534:10000:1 \
-v /opt/dmtools/code/basecode/:/workdir \
localhost/highuid_image:latest

#--uidmap=7200720:10001:1 \
