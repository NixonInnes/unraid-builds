from ubuntu:latest

ARG DEBIAN_FRONTEND=noninteractive

# Do updates
RUN apt-get update && apt-get upgrade -y
RUN ACCEPT_EULA=Y apt-get install -y python3-venv nodejs npm git

# Set default arguments for the default user
# which are overwritten by environment variables, if set
ENV user=admin

# Create a virtual environment in /opt/jupyterhub
ENV VENV /opt/jupyterhub
RUN python3 -m venv $VENV
ENV PATH "$VENV/bin:$PATH"

# Update python core packages
WORKDIR $VENV
RUN python -m pip install -U pip
RUN pip install setuptools wheel

# Install jupyter packages
RUN pip install jupyterhub jupyterlab ipywidgets jupyterhub-systemdspawner
RUN git clone https://github.com/jupyterhub/nativeauthenticator.git
RUN pip install -e nativeauthenticator/

# Install configurable http proxy
RUN npm install -g configurable-http-proxy

# Create the config file
RUN mkdir -p $VENV/etc/jupyterhub
WORKDIR $VENV/etc/jupyterhub
RUN $VENV/bin/jupyterhub --generate-config

# Create notebooks directory
RUN mkdir -p /data/notebooks
RUN chmod 777 /data/notebooks

# Append options to config
RUN echo "\
c.JupyterHub.hub_bind_url = 'http://localhost:8080'\n\
c.JupyterHub.spawner_class = 'systemdspawner.SystemdSpawner'\n\
c.SystemdSpawner.dynamic_users = True\n\
c.SystemdSpawner.user_workingdir = '/data/notebooks'\n\
c.JupyterHub.authenticator_class = 'nativeauthenticator.NativeAuthenticator'\n\
" >> jupyterhub_config.py

WORKDIR $VENV
COPY boot.sh /opt/

EXPOSE 8000
ENTRYPOINT ["/opt/boot.sh"]