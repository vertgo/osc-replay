osc-replay
======================
A simple OSC message recorder and replayer.
Depends on Python, pyOSC:
 - Python 2.7.3
 pip install pyOSC

Almost completely rewritten to use pyOSC from original osc-replay by kohei taniguchi. The original readme is still saved in this repo
there is almost no common code, but the ideas are similar. This runs on windows as liblo won't run on windows (even using ubuntu bash on windows with build 14342)



How to use
------
1. Run message receiver and record messages as 
	python pyOSCRecorder -f savedMessages.csv
	
usage: pyOSCRecorder.py [-h] [-p PORT] [-o OUTPORT] [-f FILENAME]
(the outport is currently not implemented, but should be used as a passthrough to another port)

optional arguments:
  -h, --help            show this help message and exit
  -p PORT, --port PORT  incoming port number
  -o OUTPORT, --outport OUTPORT
                        outgoing (passthrough) port number
  -f FILENAME, --filename FILENAME
                        filename
	
	To Terminate, kill the process with Ctrl+C

2. Run message sender and send messages with csv file.
	python pyOSCReplay


usage: pyOSCReplay.py [-h] -f FILENAME [-o OUTPORT]

optional arguments:
  -h, --help            show this help message and exit
  -f FILENAME, --filename FILENAME
                        filename
  -o OUTPORT, --outport OUTPORT
                        outgoing (passthrough) port number

	The process terminates when it reaches the end of csv.


