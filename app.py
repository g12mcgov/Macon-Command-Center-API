import socket
import binascii
from phillipshue.color import rgb_to_xy, hex_to_rgb

# Flask import  
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/", methods=['GET'])
def index():
	ip_address = socket.gethostbyname(socket.gethostname())
	return jsonify({"IP": ip_address})

@app.route("/blinds/position", methods=['GET'])
def getBlindStatus():
	return "Position: "

@app.route("/blinds/backyard/<command>", methods=['GET'])
def backyardBlinds(command):
	command = command.lower()

	if command == 'open':
		return "Open"
	elif command == 'close':
		return "Close"
	else:
		return "Invalid Command"

@app.route("/blinds/side/<command>", methods=['GET'])
def sideBlinds(command):
	command = command.lower()

	if command == 'open':
		return "Open"
	elif command == 'close':
		return "Close"
	else:
		return "Invalid Command"

@app.route("/lights/state/<command>", methods=['GET'])
def changeLightState(command):
	command = command.lower()

	if command == 'on':
		return "On"
	elif command == 'off':
		return "Off"
	else:
		return "Invalid Command"

@app.route("/lights/<color>", methods=['GET'])
def changeLightColor(color):
	if not color.startswith("#"):
		return "Invalid hex color value"
	else:
		hex_representation = binascii.unhexlify(color[1:])
		
		rgb = hex_to_rgb(color)
		xy = rgb_to_xy(rgb)
		
		return jsonify({"RGB": rgb, "XY": xy})


if __name__ == "__main__":
    app.run()