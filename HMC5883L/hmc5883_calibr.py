#!/usr/bin/env python
# -*- coding: utf-8 -*-

from hmc5883 import *

compass = hmc5883l()
compass.callibration()
