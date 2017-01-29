#!/usr/bin/env python

# -*- coding: utf-8 -*-
#
# @Author: grantmcgovern
# @Date:   2015-09-07 00:27:57
# @Email:   me@grantmcgovern.com
# @Web:    http://grantmcgovern.com
#
# @Last Modified by:   Grant McGovern
# @Last Modified time: 2016-02-25 21:06:41

from Adafruit_MotorHAT import Adafruit_MotorHAT
from Adafruit_MotorHAT import Adafruit_DCMotor 
from Adafruit_MotorHAT import Adafruit_StepperMotor

import time
import atexit

class Blinds(object):
	def __init__(self):
		# create a default object, no changes to I2C address or frequency
		self.mh = Adafruit_MotorHAT(addr=0x60)
		# 200 steps/rev, motor port #2
		self.blinds = self.mh.getStepper(200, 2)
		# 30 RPM
		self.blinds.setSpeed(20)

	def backward(self):
		self.blinds.step(1000, Adafruit_MotorHAT.BACKWARD,  Adafruit_MotorHAT.SINGLE)

	def forward(self):
		self.blinds.step(1000, Adafruit_MotorHAT.FORWARD,  Adafruit_MotorHAT.SINGLE)

	def adjust_forward(self):
		self.blinds.step(5, Adafruit_MotorHAT.FORWARD,  Adafruit_MotorHAT.SINGLE)

	def adjust_backward(self):
		self.blinds.step(5, Adafruit_MotorHAT.BACKWARD,  Adafruit_MotorHAT.SINGLE)
