#!/bin/bash
DIR=$(dirname "$0")
sudo cp $DIR/nginx.conf /etc/nginx/nginx.conf
sudo systemctl restart nginx
