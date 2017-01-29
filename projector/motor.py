#!/usr/bin/env python

# -*- coding: utf-8 -*-
#
# @Author: grantmcgovern
# @Date:   2015-09-07 00:27:57
# @Email:   me@grantmcgovern.com
# @Web:    http://grantmcgovern.com
#
# @Last Modified by:   Grant McGovern
# @Last Modified time: 2016-02-25 23:12:56

from Adafruit_MotorHAT import (
	Adafruit_MotorHAT,
	Adafruit_DCMotor, 
	Adafruit_StepperMotor
	)

import time
import atexit

class Projector(object):
	def __init__(self):
		# create a default object, no changes to I2C address or frequency
		self.mh = Adafruit_MotorHAT()
		atexit.register(self.turnOffMotors)
		# 200 steps/rev, motor port #1
		self.projector_motor = self.mh.getStepper(200, 2)
		# 30 RPM
		self.projector_motor.setSpeed(50)

	# recommended for auto-disabling motors on shutdown!
	def turnOffMotors(self):
		self.mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
		self.mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
		self.mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
		self.mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)

	def lower(self, motor):
		motor.step(4500, Adafruit_MotorHAT.BACKWARD,  Adafruit_MotorHAT.DOUBLE)

	def hoist(self, motor):
		motor.step(4500, Adafruit_MotorHAT.FORWARD,  Adafruit_MotorHAT.DOUBLE)