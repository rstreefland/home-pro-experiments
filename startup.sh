#!/bin/bash

# Ensure our main env shows up in ssh sessions
# we're passing on API host info
env | grep _ >> /etc/environment

# Start the ssh server
/usr/sbin/sshd -D
nohup python3 /root/home-pro-experiments/carbon-intensity/run.py &