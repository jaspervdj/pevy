#!/bin/bash

PEVY_DIR="$(pwd)"
PEVY_USER="$(whoami)"
ENV_DIR="$PEVY_DIR/env"

if [[ $PEVY_USER == root ]]; then
    echo "Don't run this as root! $0 will call sudo."
    exit 1
fi

echo "Installation directory: $PEVY_DIR"

if [[ ! -d env ]]; then
    virtualenv env
    source env/bin/activate
    python setup.py
fi

sudo tee /etc/systemd/system/pevy.service <<EOF
[Unit]
Description=pevy

[Service]
Type=simple
User=pi
WorkingDirectory=$PEVY_DIR
ExecStart=/bin/sh -c "$ENV_DIR/bin/pevy -c $PEVY_DIR/pevy.conf >>$PEVY_DIR/pevy.log 2>&1"

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl enable pevy
