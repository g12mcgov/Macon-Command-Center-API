#!/bin/bash
#make-run.sh
#make sure a process is always running.

export DISPLAY=:0 #needed if you are running a simple gui app.

process_cam=start_camera
if ps ax | grep -v grep | grep $process_cam > /dev/null
then
    exit
else
    /home/pi/bin/start_camera > /dev/null &
fi

process_ngrok=ngrok
if ps ax | grep -v grep | grep $process_ngrok > /dev/null
then
    exit
else
    ~/./ngrok start macon-command-center-vid macon-command-center-api &
fi

process_api=python
if ps ax | grep -v grep | grep $process_api > /dev/null
then
    exit
else
   cd /home/pi/Developer/Macon-Command-Center-API
   python app.py
fi

exit