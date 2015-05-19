#
#
# Author: Grant McGovern
#
#
# API to handle light changes.
# 
from phue import Bridge

class PhillipsHue():
	def __init__(self, ip):
		self.bridge = establishConnection(ip)

	def establishConnection(self, ip):
		try:
			bridge = Bridge(ip).connect()
			return bridge
		except PhueException as err:
			raise err



