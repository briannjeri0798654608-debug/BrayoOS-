#!/data/data/com.termux/files/usr/bin/bash

export DISPLAY=:0
export PULSE_SERVER=127.0.0.1

pulseaudio --start --exit-idle-time=-1
termux-x11 :0 &

sleep 3

dbus-daemon --session --fork
xfce4-session
