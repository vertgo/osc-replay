import argparse

import OSC
from OSC import OSCServer
from OSC import OSCClient
import time
import sys
from datetime import datetime as dt
import datetime
import threading
import sched

outPort = 10000

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--filename" , help="filename", type=str, required=True)
parser.add_argument("-o", "--outport", help="outgoing (passthrough) port number", type=int)


args = parser.parse_args()

print "loading file:", args.filename

if args.outport:
	outPort = args.outport

send_address = '127.0.0.1', outPort #self ip address
print "sending on port:", outPort



client = OSCClient()
client.connect( send_address )


#load up the file and read the lines
lines = [line.rstrip() for line in open(args.filename)]
print "numLines:", len(lines)
firstline = lines[0]
timestamps = [line.split(',')[0] for line in lines[2:]]

print "first timestamp:", timestamps[0]
messages   = [line.split(',')[1] for line in lines[2:]]

#message sending
def sendOSCMessage(idx):
	
	mess = messages[idx].split()
	omsg = OSC.OSCMessage( mess[0] )
	omsg.append(float(mess[1]))
	print "curmessage:", mess
	client.send( omsg)

# scheduler setup
s = sched.scheduler(time.time, time.sleep)
for idx in range(len(messages)):
	s.enter(float(timestamps[idx])/1000000.0, 1, sendOSCMessage, (idx,))


tStart = time.time()
s.run()
tEnd   = time.time()