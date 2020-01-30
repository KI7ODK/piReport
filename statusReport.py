#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created by Tyler Gardner, KI7ODK
Updated 23 September 2019

Raspberry Pi Status Reporting Script
"""

import os
import datetime
import board
import busio
import socket

import adafruit_ads1x15.ads1015 as ADS

from adafruit_ads1x15.analog_in import AnalogIn

#Gives a human-readable uptime string
#Function by Dave Smith https://thesmithfam.org
def getSysUptime():

     try:
         f = open( "/proc/uptime" )
         contents = f.read().split()
         f.close()
     except:
        return "Cannot open uptime file: /proc/uptime"
 
     total_seconds = float(contents[0])
 
     # Helper vars:
     MINUTE  = 60
     HOUR    = MINUTE * 60
     DAY     = HOUR * 24
 
     # Get the days, hours, etc:
     days    = int( total_seconds / DAY )
     hours   = int( ( total_seconds % DAY ) / HOUR )
     minutes = int( ( total_seconds % HOUR ) / MINUTE )
     seconds = int( total_seconds % MINUTE )
 
     # Build up the pretty string (like this: "N days, N hours, N minutes, N seconds")
     string = ""
     if days > 0:
         string += str(days) + " " + (days == 1 and "day" or "days" ) + ", "
     if len(string) > 0 or hours > 0:
         string += str(hours) + " " + (hours == 1 and "hour" or "hours" ) + ", "
     if len(string) > 0 or minutes > 0:
         string += str(minutes) + " " + (minutes == 1 and "minute" or "minutes" ) + ", "
     string += str(seconds) + " " + (seconds == 1 and "second" or "seconds" )
 
     return string;

#Setup TCP Socket Info
TCP_IP = '65.130.169.213'
TCP_PORT = 5005
BUFFER_SIZE = 1024

#Setup ADC
#try:
i2c = busio.I2C(board.SCL, board.SDA)
adc = ADS.ADS1015(i2c)
adc.gain = 1
chanVBat = AnalogIn(adc, ADS.P0)
chanVPi = AnalogIn(adc, ADS.P1)

#except:
	#print("ADC not connected")

#Get Pi Uptime
piUptime = getSysUptime()
#print(piUptime)

#Get System Time
piTime = datetime.datetime.now()

#Get Voltages
#try:
chanVoltage = chanVBat.voltage
scaleFactor = 3
batVoltage = chanVoltage*scaleFactor #Scale for voltage divider
piVoltage = chanVPi.voltage

#except:
#	batVoltage = "ADC Not Connected"
#	piVoltage = "ADC Not Connected"

#print(batVoltage)
#print(piVoltage)

#Create Message
message_str = "KI7ODK-10 Pi RMS Status;{};{};{} V;{} V".format(piTime, piUptime, batVoltage, piVoltage)
#print(message_str)
message = message_str.encode()

#Connect Socket and Send Message
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send(message)

#data = s.recv(BUFFER_SIZE)

s.close()
