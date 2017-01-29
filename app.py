import json
import socket
import random
import requests
import binascii
import ConfigParser
from threading import Thread

# Local Includes
from blinds.motor import Blinds
from database.db import RedisConnect
from projector.motor import Projector
from log.loghandler import configLogger
from phillipshue.color import rgb_to_xy, hex_to_rgb

# Flask import  
from flask import Flask, abort
from flask.ext.jsonpify import jsonify

# Phillips Hue
from phue import Bridge

app = Flask(__name__)

@app.route("/", methods=['GET'])
def index():
	"""
	Returns the current IP address of (host) Raspberry Pi.
	"""
	ip_address = socket.gethostbyname(socket.gethostname())
	return jsonify({"IP": ip_address})

@app.route("/blinds", methods=['GET'])
def getBlindStatus():
	"""
	Returns a packet of the current blind positions.
	"""
	blind_positions = db.retrieve("blinds-position") if db.retrieve("blinds-position") else None
	if None in blind_positions.values(): 
		abort(404)
	return jsonify(blind_positions)

@app.route("/blinds/<command>", methods=['GET'])
def blinds(command):
	"""
	Opens/closes the blinds.
	"""
	command = command.lower()

	if command == 'open':
		db.insert("blinds-position", command)
		blinds.forward()
		logger.info("Set 'blinds-position' to %s", command)
		return jsonify({"Status": "Ok"})
	elif command == 'close':
		db.insert("blinds-position", command)
		blinds.backward()
		logger.info("Set 'blinds-position' to %s", command)
		return jsonify({"Status": "Ok"})
	else:
		logger.error(
			" Blinds: Invalid command (command=%s)", command
			)
		abort(404)

@app.route("/lights/state/<command>", methods=['GET'])
def changeLightState(command):
	"""
	Changes the state of the lights. (off/on)
	"""
	command = command.lower()
	lights = bridge.get_light_objects()

	if command == 'on':
		# Loop through and turn all lights off
		for light in lights:
			light.on = True
		db.insert("state", command)
		logger.info("Set 'light state' to %s", command)
		return jsonify({"Status": "Ok"})
	elif command == 'off':
		for light in lights:
			light.on = False
		db.insert("state", command)
		logger.info("Set 'light state' to %s", command)
		return jsonify({
			"Status": "Ok"
			})
	else:
		logger.error(
			" Invalid command (command=%s)", command
			)
		abort(500)

@app.route("/lights/state", methods=['GET'])
def getLightState():
	"""
	Returns the current state of the lights. (off/on)
	"""
	try:
		# If a single light is off, mark as off 
		# (since we're not giving individual switches for each light)
		if False in [light.on for light in bridge.get_light_objects()]:
			return jsonify({
				"state": "off"
				})
		else:
			return jsonify({
				"state": "on"
				})
	except Exception as err:
		abort(404)

@app.route("/lights/currentcolor", methods=['GET'])
def getLightColor():
	"""
	Returns the current color of the lights.
	"""
	try:
		if not (db.retrieve("color-xy") or db.retrieve("color-hex")):
			abort(500)
		# Return both xy and hex color values	
		return jsonify({
			"color-xy": db.retrieve("color-xy"), 
			"color-hex": db.retrieve("color-hex")
			})
	except Exception as err:
		abort(500)

@app.route("/lights/<color>", methods=['GET'])
def changeLightColor(color):
	if not color.startswith("#"):
		logger.info(" Invalid color, must start with '#'")
		abort(500)
	else:
		hex_representation = binascii.unhexlify(color[1:])
		
		rgb = hex_to_rgb(color)
		xy = rgb_to_xy(rgb)
		
		# Log it
		colorpacket = '[ HEX=%s ], [ RGB=%s ], [ XY=%s ]' % (color, rgb, xy)
		logger.info("Set 'color' to %s", colorpacket)

		# Change Phillips Lights 
		lights = bridge.get_light_objects()
		for light in lights:
			light.on = True
			light.brightness = 254
			light.xy = xy

		# # Insert into redis, but first check if already exists
		# if db.checkIfExists("color-xy") or db.checkIfExists("color-hex"):
		# 	abort(404)

		# Insert both xy and hex color
		db.insert("color-xy", xy)
		db.insert("color-hex", color)

		return jsonify({"Status": "Ok"})

@app.route("/lights/theme/<theme>", methods=['GET'])
def changeLightTheme(theme):
	lights = bridge.get_light_objects()
	if theme == 'party':
		# myClassA()
		while True:
			for light in lights:
				light.brightness = 254
				light.xy = [random.random(), random.random()]
	elif theme == 'strobe':
		while True:
			for light in lights:
				light.on = True
				light.brightness = 254
				# White
				light.xy = [0.3227, 0.329]
				light.off = True
	elif theme == 'allon':
		for light in lights:
			light.on = True
			light.brightness = 254
			# Warm color
			light.xy = [0.5128, 0.4147]
		return jsonify({
			"status": "ok"
			})

@app.route("/movie/<command>", methods=['GET'])
def movieTime(command):
	"""
	Activates movie time.
	(lowers projector screen and turns off lights)
	"""
	command = command.lower()
	lights = bridge.get_light_objects()

	# Activate
	if command == 'start':
		# Lower projector screen
		projector_screen.hoist(projector_screen.projector_motor)
		# Insert into database, caching position
                db.insert("projector-position", command)
                logger.info("Lowered projector screen")
		# Turn off all lights
		for light in lights:
			light.on = False
		logger.info("Turned off all lights")
		return jsonify({
			"Status": "Ok"
			})
	# Deactivate
	elif command == 'stop':
		# Raise projector screen
		projector_screen.lower(projector_screen.projector_motor)
		# Insert into database, caching position 
                logger.info("Lowered projector screen")
		# Turn on all lights
		for light in lights:
			light.on = True
			light.brightness = 254
			light.xy = [0.5128, 0.4147]
		logger.info("Turned on all lights")
		return jsonify({
			"Status": "Ok"
			})
	else:
		logger.error(
			" Movie Time: Invalid command (command=%s)", command
			)
		abort(404)

if __name__ == "__main__":
	# Read in config parameters
	config = ConfigParser.RawConfigParser()
	config.readfp(open('config.cfg'))

	# Get params from file
	RASPBERRY_PI_IP_ADDRESS = config.get('macon_command_center', 'RASPBERRY_PI_IP_ADDRESS')
	REDIS_HOST = config.get('macon_command_center', 'REDIS_HOST')
	REDIS_PORT = config.get('macon_command_center', 'REDIS_PORT')
	REDIS_DB = config.get('macon_command_center', 'REDIS_DB')

	# Instantiate new RedisConnect object 
	db = RedisConnect(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

	# Config logger for endpoint logging
	logger = configLogger("Request")

	# Get Phillips Hue Connections
	bridge_ip = json.loads(
		requests.get('https://www.meethue.com/api/nupnp').content
		)
	bridge = Bridge(bridge_ip[0]['internalipaddress'])

	# Blinds 
	blinds = Blinds()

	# Projector
	projector_screen = Projector()

	app.run(host='0.0.0.0', debug=True)

