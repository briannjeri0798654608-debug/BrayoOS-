#!/bin/bash
export DISPLAY=:1
export XDG_RUNTIME_DIR=/tmp/runtime-$$
mkdir -p $XDG_RUNTIME_DIR
unset SESSION_MANAGER
unset DBUS_SESSION_BUS_ADDRESS
openbox &
sleep 1
python ~/BrayoOS/core/boot.py
