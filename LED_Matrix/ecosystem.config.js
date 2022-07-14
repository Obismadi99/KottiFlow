module.exports = {
	apps : [{
	name :  "Arrows",
	script : "testArrows.py",
	cwd : "/home/pi/rpi-rgb-led-matrix/bindings/python/samples",
	args : "-t 0.01 --triangle-height-min=20 --triangle-width=32 --n-reshape-triangle=15 -c 3",
	interpreter : "/usr/bin/python",
	restart_delay : 1000
	}]
}
