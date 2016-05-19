import argparse

import OSC
from OSC import OSCServer
from OSC import OSCClient
import time
import sys
from datetime import datetime as dt
import datetime
import threading

inPort = 8000
outPort = 0
fileName = '{:%Y-%m-%d %H-%M-%S}'.format( datetime.datetime.now() ) + ".csv"

client = None

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--port", help="incoming port number", type=int)
parser.add_argument("-o", "--outport", help="outgoing (passthrough) port number", type=int)
parser.add_argument("-f", "--filename" , help="filename", type=str)

args = parser.parse_args()


firstTime = None


if args.port:
	inPort = args.port

print "incoming port:", inPort

if args.outport:
	outPort = args.outport

if (outPort > 0 ):
	print "passthroughPort:", outPort
	client = OSCClient()
	send_address = '127.0.0.1', outPort
	client.connect( send_address ) 




if args.filename:
	fileName = args.filename

print "fileName:", fileName


file = open(fileName, 'w')

def defaultCallback(path, tags, args, source):
	global firstTime
	curTime = datetime.datetime.now()
	if firstTime is None:
		firstTime = curTime
	timeDifference = (curTime - firstTime)
	#time difference in microseconds
	
	print "got message:", path, "args", args
	print >>file, '%i,%s %f' % ( timeDifference.microseconds + timeDifference.seconds * 1000000, path, args[0])

	msg = OSC.OSCMessage( path )
	msg.append( args )
	if ( client is not None ):
		client.send( msg )


server = OSCServer( ("localhost", inPort) )
server.addMsgHandler( "default", defaultCallback)
st = threading.Thread( target = server.serve_forever )
st.start()

try :
	while 1 :
		time.sleep(1)
except:
	print("\nClosing OSCServer.")
	server.close()
	file.close()
	st.join() ##!!!
	print("Done")