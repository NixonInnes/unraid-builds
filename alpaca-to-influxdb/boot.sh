#!/bin/bash
CONFIG_FILE=/config/config.yaml
if [ ! -f "$CONFIG_FILE" ]; then
    echo "Copying default config to $CONFIG_FILE"
    cp $APPDIR/sample.yaml $CONFIG_FILE
fi

ln -s $CONFIG_FILE $APPDIR/config.yaml

python $APPDIR/main.py