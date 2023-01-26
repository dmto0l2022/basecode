import os

#pathtofile = '/srv/jupyterhub/notebooks'


#pathtofile = '/srv/jupyterhub/home/jupyterhub'

pathtofile = '/workdir/notebooks'

c.JupyterHub.authenticator_class = 'jupyterhub.auth.PAMAuthenticator'

##c.LocalAuthenticator.create_system_users = True

c.JupyterHub.bind_url = 'http://0.0.0.0:8000/'

#c.JupyterHub.bind_url = 'http://0.0.0.0:8000/'

#c.JupyterHub.bind_url = 'http://localhost:8000/dev' #### for dev path

#c.JupyterHub.hub_ip = 'jupyterhub'
#c.JupyterHub.hub_port = 8000

#c.JupyterHub.ip = "127.0.0.1" ###

#  Default: 'jupyterhub_config.py'
c.JupyterHub.config_file = '/workdir/jupyterhub/jupyterhub_config.py'

## File in which to store the cookie secret.
#  Default: 'jupyterhub_cookie_secret'
c.JupyterHub.cookie_secret_file = '/workdir/jupyterhub/jupyterhub_cookie_secret'

c.ConfigurableHTTPProxy.pid_file = '/workdir/jupyterhub/jupyterhub-proxy.pid'

c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'

#c.JupyterHub.spawner_class = 'podmancli'

##c.SudoSpawner.sudospawner_path = '/workdir/env/bin/sudospawner'

#c.JupyterHub.spawner_class = 'podmancli'

c.Spawner.default_url = '/tree/'

c.Spawner.notebook_dir=pathtofile

#c.Spawner.environment = {
 # "http_proxy": "http://your proxy",
 # "https_proxy": "https://your proxy",
 # "no_proxy": "127.0.0.1,localhost",
#}

####

# Connect containers to this Docker network
network_name = 'jupyter_network'
c.DockerSpawner.use_internal_ip = True
c.DockerSpawner.network_name = network_name

# Remove containers once they are stopped
c.DockerSpawner.remove = True

# For debugging arguments passed to spawned containers
c.DockerSpawner.debug = True

# User containers will access hub by container name on the Docker network
c.JupyterHub.hub_ip = "jupyterhub"
c.JupyterHub.hub_port = 8080

####


c.Spawner.cmd = ['/workdir/jupyterhub/env/bin/jupyterhub-singleuser']

#c.Spawner.cmd = 'jupterhub-singleuser'

notebook_dir = pathtofile
c.DockerSpawner.notebook_dir = notebook_dir


#c.DockerSpawner.volumes = { 'jupyterhub-user-{username}': notebook_dir }

#c.DockerSpawner.volumes = { 'jupyterhub-user-{username}': notebook_dir }



## The location of jupyterhub data files (e.g. /usr/local/share/jupyterhub)

c.JupyterHub.data_files_path = '/workdir/jupyterhub/env/share/jupyterhub'

## url for the database. e.g. `sqlite:///jupyterhub.sqlite`
#  Default: 'sqlite:///jupyterhub.sqlite'
c.JupyterHub.db_url = 'sqlite://///workdir/jupyterhub/jupyterhub.sqlite'

## log all database transactions. This has A LOT of output
#  Default: False
c.JupyterHub.debug_db = False

#  Default: '127.0.0.1'
#c.JupyterHub.hub_ip = '127.0.0.1'
#c.JupyterHub.hub_ip = '0.0.0.0'

#  Defaults to an empty set, in which case no user has admin access.
#  Default: set()
# c.Authenticator.admin_users = set()
c.Authenticator.admin_users = {'jupyterhub'}

## Set of usernames that are allowed to log in.
#  
#  Use this with supported authenticators to restrict which users can log in.
#  This is an additional list that further restricts users, beyond whatever
#  restrictions the authenticator has in place. Any user in this list is granted
#  the 'user' role on hub startup.
#  
#  If empty, does not perform any additional restriction.
c.Authenticator.allowed_users = {'jupyterhub'}

##


# we need the hub to listen on all ips when it is in a container
c.JupyterHub.hub_ip = '0.0.0.0' ####
# the hostname/ip that should be used to connect to the hub
# this is usually the hub container's name
#### c.JupyterHub.hub_connect_ip = 'localhost'


## Docker spawner
#c.JupyterHub.spawner_class='sudospawner.SudoSpawner'

#c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'
#c.DockerSpawner.image = os.environ['DOCKER_JUPYTER_CONTAINER']
#c.DockerSpawner.image = 'jupyter/base-notebook:latest'

#c.DockerSpawner.network_name = os.environ['DOCKER_NETWORK_NAME']
# See https://github.com/jupyterhub/dockerspawner/blob/master/examples/oauth/jupyterhub_config.py
#c.JupyterHub.hub_ip = os.environ['HUB_IP']

# user data persistence
# see https://github.com/jupyterhub/dockerspawner#data-persistence-and-dockerspawner
#notebook_dir = os.environ.get('DOCKER_NOTEBOOK_DIR')

# tell the user containers to connect to our docker network
#c.DockerSpawner.network_name = 'jupyterhub'
#c.DockerSpawner.notebook_dir = notebook_dir
#c.DockerSpawner.volumes = { 'jupyterhub-user-{username}': notebook_dir }

c.DockerSpawner.remove = True

# Other stuff
c.Spawner.cpu_limit = 1
c.Spawner.mem_limit = '10G'

c.SudoSpawner.mediator_log_level = "DEBUG"
c.JupyterHub.log_level = 10


#------------------------------------------------------------------------------
# PAMAuthenticator configuration
#------------------------------------------------------------------------------

# Authenticate local Linux/UNIX users with PAM

# The encoding to use for PAM
c.PAMAuthenticator.encoding = 'utf8'

# The PAM service to use for authentication.
#c.PAMAuthenticator.service = 'login'
#c.JupyterHub.authenticator_class = 'jupyterhub.auth.PAMAuthenticator'
#c.PAMAuthenticator.open_sessions = False

