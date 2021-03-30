from ubuntu:latest

ENV DEBIAN_FRONTEND=noninteractive

# Do updates
RUN apt-get update && apt-get upgrade -y
RUN ACCEPT_EULA=Y apt-get install -y python3-venv nodejs npm

# Set default arguments for the default user & password
# which are overwritten by environment variables, if set
ARG default_user=admin
ENV user=$default_user
ARG default_pwd=jupyter
ENV pwd=$default_pwd

# Create the default user
RUN useradd --create-home -s /bin/bash $user \
        && echo $user:$pwd | chpasswd

# Create a virtual environment in /opt/jupyterhub
ENV VENV /opt/jupyterhub
RUN python3 -m venv $VENV
ENV PATH "$VENV/bin:$PATH"

# Update python core packages
RUN python -m pip install -U pip
RUN pip install setuptools wheel

# Install jupyter packages
RUN pip install jupyterhub jupyterlab ipywidgets

# Install configurable http proxy
RUN npm install -g configurable-http-proxy

# Create the config file
RUN mkdir -p /opt/jupyterhub/etc/jupyterhub
WORKDIR /opt/jupyterhub/etc/jupyterhub
RUN $VENV/bin/jupyterhub --generate-config

# Append options to config
RUN echo "\
c.JupyterHub.hub_bind_url = 'http://localhost:8080'\n\
c.Spawner.default_url = '/lab'\n\
c.Authenticator.admin_users = {'$user'}\n\
" >> jupyterhub_config.py

EXPOSE 8000
CMD $VENV/bin/jupyterhub