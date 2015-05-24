#!/bin/bash
$redis_check = "redis-cli PING"

if [ eval $redis_check = "PONG" ]
then
	echo "Redis Up"
else
	echo "Redis Down"
fi