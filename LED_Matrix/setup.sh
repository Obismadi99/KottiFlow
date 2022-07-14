#!/bin/bash

# Install RGB-Matrices drivers
echo "----------------------------------------------------------------------------"
echo "---------------------- Install RGB-Matrices drivers ------------------------"
echo "----------------------------------------------------------------------------"
cd ~
curl https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/rgb-matrix.sh > rgb-matrix.sh
sudo bash rgb-matrix.sh

# Install npm and pm2
echo "----------------------------------------------------------------------------"
echo "-------------------------- Install npm and PM2 -----------------------------"
echo "----------------------------------------------------------------------------"
echo -n "Do you want to install npm and PM2? [y/N] "
read
if [[ "$REPLY" =~ ^(yes|y|Y)$ ]]; then
	echo "Installing npm and PM2..."
    sudo apt install npm
    sudo npm install -g pm2@latest
fi

# Install numpy
echo "----------------------------------------------------------------------------"
echo "----------------------------- Install numpy --------------------------------"
echo "----------------------------------------------------------------------------"
echo -n "Do you want to install numpy? [y/N] "
read
if [[ "$REPLY" =~ ^(yes|y|Y)$ ]]; then
	echo "Installing numpy"
    pip3 install numpy
fi

# Download configuration and python files
echo "----------------------------------------------------------------------------"
echo "----------------- Download configuration and python files ------------------"
echo "----------------------------------------------------------------------------"
cd ~
curl https://raw.githubusercontent.com/Obismadi99/KottiFlow/main/LED_Matrix/Arrows.py > ~/rpi-rgb-led-matrix/bindings/python/samples/Arrows.py
curl https://raw.githubusercontent.com/Obismadi99/KottiFlow/main/LED_Matrix/ecosystem.config.js > ~/ecosystem.config.js

# Setup automatic start for Arrows.py
echo "----------------------------------------------------------------------------"
echo "------------------- Setup automatic start for Arrows.py --------------------"
echo "----------------------------------------------------------------------------"
sudo pm2 start ecosystem.config.js
sudo pm2 save
sudo pm2 startup