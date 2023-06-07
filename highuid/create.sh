podman \
   run \
    --privileged \
    --rm \
    --uidmap=0:0:10000 \
    --uidmap=65534:10000:1 \
    --uidmap=7200720:10001:1 \
     quay.io/buildah/stable buildah bud -t img1
     
     
