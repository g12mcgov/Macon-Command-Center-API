#!/usr/bin/python

#
# Author(s): Grant McGovern
# Date: Sat 23 May 2015 
#
# ~ Description:
#       - Defines a configLogger() method which allows a global
#		  logger (with specific names) to be used throughout the
#		  app.
#

import sys
import logging

## Setsup a logger for the entire application to use
def configLogger(name):
	logger = logging.basicConfig( 
    stream=sys.stdout, 
    level=logging.INFO, 
    format="%(asctime)s [ %(threadName)s ] [ %(levelname)s ] : %(message)s'", 
    datefmt='%Y-%m-%d %H:%M:%S' 
	) 

	logger = logging.getLogger(name)

	return logger