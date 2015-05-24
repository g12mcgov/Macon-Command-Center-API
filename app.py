import socket
import binascii
import ConfigParser

# Local Includes
from database.db import RedisConnect
from log.loghandler import configLogger
from phillipshue.color import rgb_to_xy, hex_to_rgb

# Flask import  
from flask import Flask, abort
from flask.ext.jsonpify import jsonify

app = Flask(__name__)

@app.route("/", methods=['GET'])
def index():
	"""
	Returns the current IP address of (host) Raspberry Pi.
	"""
	ip_address = socket.gethostbyname(socket.gethostname())
	return jsonify({"IP": ip_address})

@app.route("/blinds/position", methods=['GET'])
def getBlindStatus():
	"""
	Returns a packet of the current blind positions.
	(side/backyard)
	"""
	blind_positions = {
	"side": db.retrieve("side-position") if db.retrieve("side-position") else None,
	"backyard": db.retrieve("backyard-position") if db.retrieve("backyard-position") else None
	}

	if None in blind_positions.values(): 
		abort(404)

	return jsonify(blind_positions)

@app.route("/blinds/backyard/<command>", methods=['GET'])
def backyardBlinds(command):
	"""
	Opens/closes the backyard blinds.
	"""
	command = command.lower()

	if command == 'open':
		db.insert("backyard-position", command)
		logger.info("Set 'backyard-position' to %s", command)
		return jsonify({"Status": "Ok"})
	elif command == 'close':
		db.insert("backyard-position", command)
		logger.info("Set 'backyard-position' to %s", command)
		return jsonify({"Status": "Ok"})
	else:
		logger.error(
			" Backyard Blinds: Invalid command (command=%s)", command
			)
		abort(404)

@app.route("/blinds/side/<command>", methods=['GET'])
def sideBlinds(command):
	"""
	Opens/closes the side blinds.
	"""
	command = command.lower()

	if command == 'open':
		db.insert("side-position", command)
		logger.info("Set 'side-position' to %s", command)
		return jsonify({"Status": "Ok"})
	elif command == 'close':
		db.insert("side-position", command)
		logger.info("Set 'side-position' to %s", command)
		return jsonify({"Status": "Ok"})
	else:
		logger.error(
			" Side Blinds: Invalid command (command=%s)", command
			)
		abort(404)

@app.route("/lights/state/<command>", methods=['GET'])
def changeLightState(command):
	"""
	Changes the state of the lights. (off/on)
	"""
	command = command.lower()

	if command == 'on':
		db.insert("state", command)
		logger.info("Set 'light state' to %s", command)
		return jsonify({"Status": "Ok"})
	elif command == 'off':
		db.insert("state", command)
		logger.info("Set 'light state' to %s", command)
		return jsonify({"Status": "Ok"})
	else:
		logger.error(
			" Invalid command (command=%s)", command
			)
		abort(404)

@app.route("/lights/state", methods=['GET'])
def getLightState():
	"""
	Returns the current state of the lights. (off/on)
	"""
	try:
		if not db.retrieve("state"):
			abort(404)	
		return jsonify({"state": db.retrieve("state")})
	except Exception as err:
		abort(404)

@app.route("/lights/currentcolor", methods=['GET'])
def getLightColor():
	"""
	Returns the current color of the lights.
	"""
	try:
		if not (db.retrieve("color-xy") or db.retrieve("color-hex")):
			abort(404)
		# Return both xy and hex color values	
		return jsonify({
			"color-xy": db.retrieve("color-xy"), 
			"color-hex": db.retrieve("color-hex")
			})
	except Exception as err:
		abort(404)

@app.route("/lights/<color>", methods=['GET'])
def changeLightColor(color):
	if not color.startswith("#"):
		logger.info(" Invalid color, must start with '#'")
		abort(404)
	else:
		hex_representation = binascii.unhexlify(color[1:])
		
		rgb = hex_to_rgb(color)
		xy = rgb_to_xy(rgb)
		
		# Log it
		colorpacket = '[ HEX=%s ], [ RGB=%s ], [ XY=%s ]' % (color, rgb, xy)
		logger.info("Set 'color' to %s", colorpacket)

		# # Insert into redis, but first check if already exists
		# if db.checkIfExists("color-xy") or db.checkIfExists("color-hex"):
		# 	abort(404)

		# Insert both xy and hex color
		db.insert("color-xy", xy)
		db.insert("color-hex", color)

		return jsonify({"Status": "Ok"})


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

	app.run(host='0.0.0.0')