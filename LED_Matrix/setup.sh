#!/bin/bash

cd ~
curl https://github.com/Obismadi99/KottiFlow/blob/main/LED_Matrix/Arrows.py > ~/rpi-rgb-led-matrix/bindings/python/samples/Arrows.py
curl https://github.com/Obismadi99/KottiFlow/blob/main/LED_Matrix/ecosystem.config.js > ~/ecosystem.config.js

sudo apt install npm
sudo npm install pm2@latest -g

sudo pm2 start ecosystem.config.js
sudo pm2 save
sudo pm2 startup