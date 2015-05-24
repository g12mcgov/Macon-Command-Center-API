# Macon-Command-Center-API

A small Flask RESTful listener service for the Macon Command Center. Responds to Ajax requests and performs actions such as changing color of the Phillips Hue Lights and Opening/Closing Blinds.

This currently runs locally on a Raspberry Pi 2 and is written in Python to interact with RPI (GPIO) modules.

Running:
=======

```bash
$ python app.py
```

Endpoints:
=======

The root endpoint (`/`) returns the IP Address of the host machine.

	/blinds/position
	/blinds/side/:command
	/blinds/backyard/:command
	/lights/state/:command
	/lights/:color