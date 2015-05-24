#!/usr/bin/python

# Name: WIN 
# File: WIN/db.py
#
# Author(s): Grant McGovern & Gaurav Sheni
# Date: Wed 11 March 2015 
#
# URL: www.github.com/g12mcgov/WIN
#
# ~ Description:
#       - Provides a class for Redis usage throughout the app.
#
#

import sys
import redis

## Local Includes ##
from log.loghandler import configLogger


class RedisConnect:
	def __init__(self, host, port, db):
		self.HOST = host
		self.PORT = port
		self.DB = db

		# Setup logger for redis
		self.logger = configLogger("Redis")

		# Setup the Redis connection
		self.db = self.setup()

	def setup(self):
		""" Setups the RedisConnect class """
		try:
			database = redis.StrictRedis(host=self.HOST, port=self.PORT, db=self.DB)

			self.logger.info("Successfully established Redis connection.")

			return database

		except redis.exceptions.ConnectionError as err:
			raise err

	def checkIfExists(self, key):
		""" Checks if current query exists in DB """
			
		if self.db.get(key):
			return True
		else:
			return False

	def insert(self, key, value):
		""" Inserts into Redis, first checking if it already exists """
		self.db.set(key, value)
		return

	def retrieve(self, key):
		""" Retrieves a value in the redis db """
		try:
			return self.db.get(key)
		except redis.exceptions.DataError as err:
			raise err