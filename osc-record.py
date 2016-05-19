#!/usr/bin/env python
# -*- coding: utf-8 -*-

#mikechanged import liblo
from OSC import OSCServer
import sys
from datetime import datetime as dt
import datetime

# config for listening
listeningPort = 8001

print 'Number of arguments:', len(sys.argv), 'arguments.'
print 'Argument List:', str(sys.argv)



# now method
def now():
	return dt.today()

# start time
print '%s,INFO:osc-record started.\n' % now()

# create server, listening on given port
try:
    #mike changedserver = liblo.Server(listeningPort)
    server = OSCServer( ("localhost", listeningPort) )
except err:
	print "error starting server:"
    print str(err)
    sys.exit()

# callback functions 
def n_callback(path):
    print '%s,%s' % (now(), path)

def f_callback(path, args):
	print '%s,%s %f' % (now(), path, args[0])

def ff_callback(path, args):
	print '%s,%s %f %f' % (now(), path, args[0], args[1])

def fallback(path, args, types, src):
    print "got unknown message '%s' from '%s'" % (path, src.get_url())
    for a, t in zip(args, types):
        print "argument of type '%s': %s" % (t, a)

# register method taking an int and a float



#mikechanged
# server.add_method("/pedal", None, n_callback)
# server.add_method("/steerRight", None, n_callback)
# server.add_method("/steerLeft", None, n_callback)
# server.add_method("/steerReset", None, n_callback)
# server.add_method("/brake", None, n_callback)

# server.add_method("/speed", 'f', f_callback)
# server.add_method("/steerAngle", 'f', f_callback)
# server.add_method("/direction", 'f', f_callback)
# server.add_method("/location", 'ff', ff_callback)

# # register a fallback for unhandled messages
# server.add_method(None, None, fallback)


server.addMsgHandler("/pedal", None, n_callback)
server.addMsgHandler("/steerRight", None, n_callback)
server.addMsgHandler("/steerLeft", None, n_callback)
server.addMsgHandler("/steerReset", None, n_callback)
server.addMsgHandler("/brake", None, n_callback)

server.addMsgHandler("/speed", 'f', f_callback)
server.addMsgHandler("/steerAngle", 'f', f_callback)
server.addMsgHandler("/direction", 'f', f_callback)
server.addMsgHandler("/location", 'ff', ff_callback)

# register a fallback for unhandled messages
server.addMsgHandler(None, None, fallback)

# loop and dispatch messages every 100ms
while True:
    server.recv(100)

