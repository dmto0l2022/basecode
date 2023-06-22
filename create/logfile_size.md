logfile

Create or edit /etc/containers/containers.conf for podman running as root, or $HOME/.config/container/containers.conf for root-less containers, to contain "log_size_max=SIZE" in the [containers] section, with SIZE being the maximum size in bytes for the log files. For example:

[containers]
log_size_max=10485760
