# run container as current user

podman run -it --userns=keep-id registry.access.redhat.com/rhel7/rhel /bin/bash
