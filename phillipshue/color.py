#
#
# Author: Grant McGovern
#
#
# An algorithm to convert RGB (0-255) values to X, Y for
# Phillips Hue lightbulbs.

import math

def hex_to_rgb(color):
	""" Converts a HEX color value to RGB Tuple """
	color = color.lstrip('#')
	length = len(color)
	return tuple(int(color[i:i + length/3], 16) for i in range(0, length, length/3))

# This is based on original code from http://stackoverflow.com/a/22649803
# and taken from https://gist.github.com/error454/6b94c46d1f7512ffe5ee
def EnhanceColor(normalized):
    if normalized > 0.04045:
        return math.pow( (normalized + 0.055) / (1.0 + 0.055), 2.4)
    else:
        return normalized / 12.92
 
def rgb_to_xy(rgb):
	""" Converts RGB tuple to X,Y pair for Phillips Hue API """
	r = rgb[0]
	g = rgb[1]
	b = rgb[2]

	rNorm = r / 255.0
	gNorm = g / 255.0
	bNorm = b / 255.0

	rFinal = EnhanceColor(rNorm)
	gFinal = EnhanceColor(gNorm)
	bFinal = EnhanceColor(bNorm)

	X = rFinal * 0.649926 + gFinal * 0.103455 + bFinal * 0.197109
	Y = rFinal * 0.234327 + gFinal * 0.743075 + bFinal * 0.022598
	Z = rFinal * 0.000000 + gFinal * 0.053077 + bFinal * 1.035763
 

	if X + Y + Z == 0:
		return (0, 0)
	else:
		xFinal = X / (X + Y + Z)
		yFinal = Y / (X + Y + Z)

		return (xFinal, yFinal)

