from __future__ import print_function
import argparse

import OSC
from OSC import OSCServer
from OSC import OSCClient
import time
import sys
from datetime import datetime as dt
import datetime
import threading

#import sched

outPort = 10000

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--filename" , help="filename", type=str, required=True)
parser.add_argument("-o", "--outport", help="outgoing (passthrough) port number", type=int)
parser.add_argument("-v", "--verbose", help="verbose outputs (many traces)", action="store_true")
parser.add_argument("-l", "--loop", help="loops the playing at the end of the file", action="store_true")



args = parser.parse_args()

print( "loading file:", args.filename )

if args.outport:
	outPort = args.outport

send_address = '127.0.0.1', outPort #self ip address
print( "sending on port:", outPort )



client = OSCClient()
client.connect( send_address )


#load up the file and read the lines
lines = [line.rstrip() for line in open(args.filename)]
print( "numLines:", len(lines) )
firstline = lines[0]
timestamps = [ int(line.split(',')[0]) for line in lines[2:]]
numMSGs = len( timestamps )

print( "first timestamp:", timestamps[0] )
messages   = [line.split(',')[1] for line in lines[2:]]

#message sending
def sendOSCMessage(idx):
	global args
	mess = messages[idx].split()
	omsg = OSC.OSCMessage( mess[0] )
	omsg.append(float(mess[1]))
	if ( args.verbose ):
		print( "curmessage:", mess )
	client.send( omsg)


def checkIndex( nowUSeconds , idx):
	global args
	if ( args.verbose ):
		print( "checkIndex: index:", idx, "nowUseconds:", nowUSeconds, ",", timestamps[ idx] )
	if ( int( nowUSeconds ) < timestamps[ idx] ):
		# if ( args.verbose ):
		# 	print( "returning False" )
		return False
	else:
		sendOSCMessage(idx)
		# if ( args.verbose ):
		# 	print( "returning True" )
		return True

curIndex = 0

firstTime = datetime.datetime.now()
#try:
while True:
	curDelta = (datetime.datetime.now() - firstTime);
	microseconds =  curDelta.microseconds + curDelta.seconds *1000000
	
	print("us:", microseconds, end='\r')
	pastTime = checkIndex(microseconds, curIndex )
	while( pastTime ):
		curIndex += 1
		pastTime = checkIndex(microseconds, curIndex )
		if (curIndex >= numMSGs - 1):
			if ( args.loop ):
				print ( "looping...")
				curIndex = 0
				firstTime = datetime.datetime.now()
				
			else:
				exit()
		#don't wait, just keep going
#except:
#	print "Unexpected error:", sys.exc_info()[0]