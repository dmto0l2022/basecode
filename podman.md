# run container as current user

podman run -it --userns=keep-id registry.access.redhat.com/rhel7/rhel /bin/bash

# keepy groups

podman run --privileged --userns=keep-id --group-add keep-groups 
--net=host --cgroups=disabled

podman run -it --userns=keep-id --group-add keep-groups registry.access.redhat.com/rhel7/rhel /bin/bash

podman run -it --userns=keep-id --group-add keep-groups --group-add dmtools registry.access.redhat.com/rhel7/rhel /bin/bash


--group-add strings 
