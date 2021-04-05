#!/bin/bash
source $VENV/bin/activate
echo "c.Authenticator.admin_users = {'$user'}" >> $VENV/etc/jupyterhub/jupyterhub_config.py
$VENV/bin/jupyterhub --config $VENV/etc/jupyterhub/jupyterhub_config.py