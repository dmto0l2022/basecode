xport DOCKER_HOST=unix:///workdir/jupyterhub//.docker/run/docker.sock


notebook_dir = os.environ.get('DOCKER_NOTEBOOK_DIR') or '/home/jovyan'
c.DockerSpawner.notebook_dir = notebook_dir
c.DockerSpawner.volumes = {
'jupyterhub-user-{username}': notebook_dir ,
'jupyterhub-shared': '/home/jovyan/sh

# WARNING: systemd not found. You have to remove XDG_RUNTIME_DIR manually on every logout.
export XDG_RUNTIME_DIR=/workdir/jupyterhub//.docker/run
export PATH=/usr/bin:$PATH
Some applications may require the following environment variable too:
export DOCKER_HOST=unix:///workdir/jupyterhub//.docker/run/docker.sock


https://github.com/jupyterhub/jupyterhub/tree/main/singleuser

https://github.com/jupyter/docker-stacks/tree/main/docker-stacks-foundation

