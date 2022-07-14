#!/bin/bash

# Download configuration and python files
cd ~
curl https://raw.githubusercontent.com/Obismadi99/KottiFlow/main/LED_Matrix/Arrows.py > ~/rpi-rgb-led-matrix/bindings/python/samples/Arrows.py
curl https://raw.githubusercontent.com/Obismadi99/KottiFlow/main/LED_Matrix/ecosystem.config.js > ~/ecosystem.config.js

# Install npm and pm2
sudo apt install npm
sudo npm install -g pm2@latest

# Install numpy
pip3 install numpy

# Setup automatic start for Arrowas
sudo pm2 start ecosystem.config.js
sudo pm2 save
sudo pm2 startup