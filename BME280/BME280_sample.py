#!/usr/bin/env python
# -*- coding: utf-8 -*-

from BME280 import *

ps = BME280()

while True:
	ps_data = ps.get_data()
	print "Temperature:", ps_data['t'], "°C", "Pressure:", ps_data['p'], "Pa", "Altitude:", ps.get_altitude(ps_data['p']),"m", "Humidity:", ps_data['h'],"%"
	time.sleep(1)

