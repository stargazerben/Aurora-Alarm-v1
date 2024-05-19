#!/usr/bin/python

import os
from xml.etree import ElementTree
from datetime import datetime

RED="red"                         # These 2 states trigger a photo
AMBER="amber"                     # These 2 states trigger a photo
LATE = (22, 23, 0, 1, 2, 3, 4, 5) # Hours of day deemed late
SHUTTER=20000000                  # Shuuter in microseconds if it is LATE (20s)

# For testing
# LATE = (22, 23, 0, 1, 2, 3, 4, 5, 10)
RED="green"
# SHUTTER=10000

count = 0
while True:
    os.system ("wget -q http://aurorawatch.lancs.ac.uk/api/0.1/status.xml")
    xml_file = open("status.xml", 'rb') 
    tree = ElementTree.parse(xml_file)
    xml_file.close()

    currentStateName = tree.find('current').find('state').get('name')
    state = tree.find('current').find('state').text
    updated = tree.find('updated').text
    os.remove ("status.xml")

    print("\n")
    print(currentStateName)
    print(state)
    print(updated)

    hour = datetime.now().hour
    is_late = (hour in LATE)

    # Tweak to fixed shutter speed if it is late
    shutter = ""
    if (is_late):
         shutter = "--shutter " + str (SHUTTER)

    if currentStateName == RED or currentStateName == AMBER:
        pix_file = "pix/pic_" + str (count) + ".jpg"
        command = "rpicam-jpeg -v 0 " + shutter + " -o " + pix_file
        print ("Taking picture as its " + currentStateName + " using : " + command)
        os.system (command)
        count = count + 1
        if currentStateName == RED:
           os.system ("ffplay /home/pi/Aurora/birdsong.mp3 -t 25 -autoexit") # -hide_banner -loglevel error")
    else:
        print ("Not taking a picture as its " + currentStateName + " at " + updated)

    # Sleep but if RED status shorten sleep
    sleep=300
    if currentStateName == RED:
        sleep=60

    print ("Sleeping for " + str(sleep) + " seconds")
    os.system ("sleep " + str(sleep))
