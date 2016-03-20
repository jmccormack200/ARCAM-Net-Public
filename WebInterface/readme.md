# Web Interface

This is the primary component of the SDR
Mesh Network. The backend is based in flask. A
web front end has been written to enable debugging and
interaction with the underlying control system. 

Flask acts as a wrapper and interface into GNU Radio.
We leverage SocketIO to create a means of interfacing
Flask to the front end, and to A.L.F.R.E.D. 

A.L.F.R.E.D. (further mentioned as alfred) is a 
component of the batman-adv ecosystem. It allows us
to share data across the mesh network in a distributed
way.

If you see something unclear, please talk to John, 
or if enough time has passed and John is off saving
the world in his flying Tesla Model S, email him at:
me@jdmccormack.com

## flowcontroller.py

This is the python file that sets up the flask server
and manages the SocketIO server. You run it just using
sudo python flowcontroller.py. You can then point
a browser to 127.0.0.1:5000 and see a helpful
web interface for interfacing to the data. 

This is a work in progress, soon it should also
set up and interface into Alfred using web sockets.

## frequencytable.py

This file is a simple program that is uses to limit
the frequencies that can be used
by the SDR. Essentially we are just using this
to prevent an infinite number of possible frequencies.

It currently works with a list of frequencies, but that
may change in the future. Open up the file to learn
more. 

## batmanNoGui.py

The GNU Radio block for establishing the network 

## program.py

This is a test file for working with alfred, and
will be changed to a more descriptive name soon.

## radiostats.html

This is the template for the web front end.

## static

These are all the static files used by the templates
in flask. This also contains raiseBatSignal.sh

## templates

This contains the templates themselves. As of now,
we have only one. It is unlikely we will be adding
more in the future. 
