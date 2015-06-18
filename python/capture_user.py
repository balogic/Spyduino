#! /usr/bin/env python

# -*- coding: utf-8 -*-

import sys
import serial
import pygame
import pygame.camera
from os import getenv
from pygame.locals import *
from datetime import datetime as dt


# Initializing the Camera device
pygame.camera.init()
cameras = pygame.camera.list_cameras()
print "List of cameras %s" % cameras
print "Using Webcam %s" % cameras[0]
cam = pygame.camera.Camera("/dev/video0", (640, 480))
home_dir = getenv('HOME')

'''
Adjust the value of this variable to set the distance
for the sensor to detect intruders

'''

RANGE = 300

# Managing the Camera device
def capture_image():
    
    '''
    Starts the camera, Captures the image, saves it & stops
    
    '''

    file_name = home_dir + '/image_captured/image_' + str(dt.now()) + '.jpg'
    cam.start()
    image = cam.get_image()
    pygame.image.save(image, file_name)
    


'''
Establishes a connection to Arduino board through serial interface

'''
arduino_board = serial.Serial(sys.argv[1], 9600)


'''
Enters an infite loop that runs until it receives Keyboard Interrupt

'''
while True:
    if arduino_board.inWaiting() > 0:
        data = arduino_board.readline().strip()

        try:
            '''
            The value received through serial interface would be
            string, in order to process futher, it is converted
            to numeric datatype.
            '''
            data = int(float(data))
            if data <= RANGE:
                capture_image()
                
                print data
                cam.stop()

        except BaseException, be:
            '''
            initially the board might send some strings that are not
            the numeric value, to handle such exception it is catched
            and ignored by printing an exception message.
            '''
            print be.message
