#!/bin/bash

# export env variables into /etc/environment to make them accessible for cron
printenv | grep -v "no_proxy" >> /etc/environment

cron -f
