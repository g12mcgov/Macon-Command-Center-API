# Macon-Command-Center-API

A small Flask RESTful listener service for the [Macon Command Center](https://github.com/g12mcgov/Macon-Command-Center-API). This responds to Ajax requests and performs actions such as changing color of the Phillips Hue Lights, Opening/Closing Blinds, and returning current states (i.e. lights on/off, blinds open/closed).

It uses Redis as auxiliary support in the event the web-server goes down. The state of each item is backed up in Redis so in the event it all crashes, the current state is still persisted on the disk. 

This currently runs locally on a Raspberry Pi 2 and is written in Python to interact with RPI (GPIO) modules. 

Requirements:
=======

	Flask==0.10.1
	Jinja2==2.7.3
	MarkupSafe==0.23
	Werkzeug==0.10.4
	itsdangerous==0.24
	phue==0.8
	wsgiref==0.1.2
	redis==2.10.3

To install these just run:

```bash
$ sudo pip install -r requirements.txt
```

Running:
=======

To run it, simply execute:

```bash
$ python app.py
```
You'll then see the web-server start and the you can begin executing commands. Example log block:

	2015-05-23 23:46:46 [ MainThread ] [ INFO ] : Successfully established Redis connection.'
	2015-05-23 23:46:46 [ MainThread ] [ INFO ] :  * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)'
	2015-05-23 23:46:58 [ MainThread ] [ INFO ] : Set 'backyard-position' to close'
	2015-05-23 23:46:58 [ MainThread ] [ INFO ] : 192.168.1.4 - - [23/May/2015 23:46:58] "GET /blinds/backyard/close HTTP/1.1" 200 -'
	2015-05-23 23:47:10 [ MainThread ] [ INFO ] : Set 'backyard-position' to open'
	...
	...

Endpoints:
=======

The root endpoint (`/`) returns the IP Address of the host machine.

	/blinds/position 			# Returns current blind positions
	/blinds/side/:command 		# Opens/closes side blinds
	/blinds/backyard/:command 	# Opens/closes backyard blinds
	/lights/state/:command 		# Changes light state (on/off)
	/lights/state 				# Returns current light state (on/off)
	/lights/:color				# Sets new color
	/lights/color 				# Returns current color