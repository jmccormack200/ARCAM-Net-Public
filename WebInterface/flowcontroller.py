#!/usr/bin/env python2
##################################################
# ''GNU Radio Python Flow Graph
# Title: Nonbroadcastwithfreqandmac
# Generated: Mon Feb  1 16:46:29 2016
#
# The name of this file may be misleading if
# threading is not used in the end. I just needed
# to change the title to ensure that it would
# not be overwritten when I went to build it again
# later. 
#
# This makes me realize I need to create a way
# to ensure that changes to the flow graph can
# be made without requiring massive code rewrites
# as we add features.
#
# TODO:
#   1) Sync Freq table with the changes from Alfred
#   2) Reduce to just have one frequency for now, not
#      one for RX and one for TX. 
#
#
##################################################
#from __future__ import print_function

async_mode = None

if async_mode is None:
    try:
        import eventlet
        async_mode = 'eventlet'
    except ImportError:
        pass

    if async_mode is None:
        try:
            from gevent import monkey
            async_mode = 'gevent'
        except ImportError:
            pass

    if async_mode is None:
        async_mode = 'threading'

    print('async_mode is ' + async_mode)

# monkey patching is necessary because this application uses a background
# thread
if async_mode == 'eventlet':
    import eventlet
    eventlet.monkey_patch()
elif async_mode == 'gevent':
    from gevent import monkey
    monkey.patch_all()

from threading import Thread
from optparse import OptionParser
from gnuradio.eng_option import eng_option
from gnuradio import eng_notation

from batmanNoGui import batmanNoGui
import mac
import pmt
import wx
import sys



from flask import Flask, render_template, request, jsonify,session
from flask_socketio import SocketIO, emit

from frequencytable import FrequencyTable

import os
from time import sleep, time
import subprocess

app = Flask(__name__)
#app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, host='0.0.0.0', async_mode=async_mode)
thread = None

@app.route('/')
def index():
    return render_template('radiostats.html', rxFreq=tb.get_rx_freq(), txFreq=tb.get_tx_freq(), txGain=tb.get_tx_gain(), rxGain=tb.get_rx_gain())


# http://www.secdev.org/projects/scapy/
# Saving that link for later

# TX Freq
@socketio.on('inc tx freq')
def inc_freq():
    newFreq = txfreqtable.increase_freq()
    os.system("echo " + "'" + str(newFreq) + "%" + str(time()) + "'" + " | sudo alfred -s 65")    
    sleep(7)
    tb.set_tx_freq(int(newFreq))
    tb.set_rx_freq(int(newFreq))
    emit('confirm tx freq', {'txfreq':newFreq}, broadcast=True)

@socketio.on('dec tx freq')
def dec_freq():
    newFreq = txfreqtable.decrease_freq()
    os.system("echo " + "'" + str(newFreq) + "%" + str(time()) + "'" + " | sudo alfred -s 65")
    sleep(7)
    tb.set_tx_freq(int(newFreq))
    tb.set_rx_freq(int(newFreq))
    emit('confirm tx freq', {'txfreq':newFreq}, broadcast=True)

@socketio.on('alfred set freq')
def set_freq(freq):
    print("PRINT")
    print(str(int(freq)))
    tb.set_tx_freq(int(freq))
    tb.set_rx_freq(int(freq))
    print(tb.get_tx_freq())
    emit('confirm tx freq', {'txfreq':tb.get_tx_freq()}, broadcast=True)	
 
# For this paper I think we should remove the separate tx/rx functionality

#RX Freq
@socketio.on('inc rx freq')
def inc_freq():
    tb.set_rx_freq(rxfreqtable.increase_freq())
    os.system("echo " + str(tb.get_rx_freq()) + " | sudo alfred -s 66")
    emit('confirm rx freq', {'rxfreq':tb.get_rx_freq()})

@socketio.on('dec rx freq')
def dec_freq():
    tb.set_rx_freq(rxfreqtable.decrease_freq())
    os.system("echo " + str(tb.get_rx_freq()) + " | sudo alfred -s 66")
    emit('confirm rx freq', {'rxfreq':tb.get_rx_freq()})

#TX Gain
@socketio.on('inc tx gain')
def inc_freq():
    tb.set_tx_gain(tb.get_tx_gain() + 1)
    emit('confirm tx gain', {'txgain':tb.get_tx_gain()})

@socketio.on('dec tx gain')
def dec_freq():
    tb.set_tx_gain(tb.get_tx_gain() - 1)
    emit('confirm tx gain', {'txgain':tb.get_tx_gain()})

#RX Gain
@socketio.on('inc rx gain')
def inc_freq():
    tb.set_rx_gain(tb.get_rx_gain() + 1)
    emit('confirm rx gain', {'rxgain':tb.get_rx_gain()})

@socketio.on('dec rx gain')
def dec_gain():
    tb.set_rx_gain(tb.get_rx_gain() - 1)
    emit('confirm rx gain', {'rxgain':tb.get_rx_gain()})

def argument_parser():
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    parser.add_option(
        "", "--ampl", dest="ampl", type="eng_float", default=eng_notation.num_to_str(0.7),
        help="Set TX BB amp [default=%default]")
    parser.add_option(
        "-a", "--args", dest="args", type="string", default='',
        help="Set USRP device args [default=%default]")
    parser.add_option(
        "-t", "--arq-timeout", dest="arq_timeout", type="eng_float", default=eng_notation.num_to_str(.1*0 + 0.04),
        help="Set ARQ timeout [default=%default]")
    parser.add_option(
        "-d", "--dest-addr", dest="dest_addr", type="intx", default=-1,
        help="Set Destination address [default=%default]")
    parser.add_option(
        "", "--iface", dest="iface", type="string", default='tun0',
        help="Set Interface name [default=%default]")
    parser.add_option(
        "", "--mtu", dest="mtu", type="intx", default=128,
        help="Set MTU [default=%default]")
    parser.add_option(
        "-l", "--ogradio-addr", dest="ogradio_addr", type="intx", default=0,
        help="Set Local address [default=%default]")
    parser.add_option(
        "", "--port", dest="port", type="string", default="12345",
        help="Set TCP port [default=%default]")
    parser.add_option(
        "-r", "--rate", dest="rate", type="eng_float", default=eng_notation.num_to_str(1e6),
        help="Set Sample rate [default=%default]")
    parser.add_option(
        "-A", "--rx-antenna", dest="rx_antenna", type="string", default="TX/RX",
        help="Set RX antenna [default=%default]")
    parser.add_option(
        "", "--rx-gain", dest="rx_gain", type="eng_float", default=eng_notation.num_to_str(65-20),
        help="Set RX gain [default=%default]")
    parser.add_option(
        "", "--rx-lo-offset", dest="rx_lo_offset", type="eng_float", default=eng_notation.num_to_str(0),
        help="Set RX LO offset [default=%default]")
    parser.add_option(
        "", "--samps-per-sym", dest="samps_per_sym", type="intx", default=4,
        help="Set Samples/symbol [default=%default]")
    parser.add_option(
        "", "--tx-gain", dest="tx_gain", type="eng_float", default=eng_notation.num_to_str(45),
        help="Set TX gain [default=%default]")
    parser.add_option(
        "", "--tx-lo-offset", dest="tx_lo_offset", type="eng_float", default=eng_notation.num_to_str(0),
        help="Set TX LO offset [default=%default]")
    parser.add_option(
        "", "--max-arq-attempts", dest="max_arq_attempts", type="intx", default=5 * 2,
        help="Set Max ARQ attempts [default=%default]")
    parser.add_option(
        "", "--tx-freq", dest="tx_freq", type="eng_float", default=eng_notation.num_to_str(915e6),
        help="Set TX freq [default=%default]")
    parser.add_option(
        "", "--rx-freq", dest="rx_freq", type="eng_float", default=eng_notation.num_to_str(915e6),
        help="Set RX freq [default=%default]")
    return parser

def main(top_block_cls=batmanNoGui, options=None):
    print("Initializing GNU Radio")
    macIP = input('Enter a number from 1 - 250 to be used for the mac and IP: ')

    if options is None:
        options, _ = argument_parser().parse_args()

    global tb

    tb = top_block_cls(ampl=options.ampl, args=options.args, arq_timeout=options.arq_timeout, dest_addr=options.dest_addr, iface=options.iface, mtu=options.mtu, ogradio_addr=options.ogradio_addr, port=options.port, rate=options.rate, rx_antenna=options.rx_antenna, rx_gain=options.rx_gain, rx_lo_offset=options.rx_lo_offset, samps_per_sym=options.samps_per_sym, tx_gain=options.tx_gain, tx_lo_offset=options.tx_lo_offset, max_arq_attempts=options.max_arq_attempts, tx_freq=options.tx_freq, rx_freq=options.rx_freq)
    tb.start()

    setupEverythingElse(macIP)
    try:
        raw_input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()

def setupEverythingElse(macIP):
    global txfreqtable
    txfreqtable = FrequencyTable()

    global rxfreqtable
    rxfreqtable = FrequencyTable()

    '''
    print("Setting IP Address")
    ip = '192.168.200.' + str(macIP)
    cmd = 'sudo ifconfig tun0 ' + ip
    os.system(cmd)
    print("Ip Address of tun0 is now " + ip)
    '''

    print("setting up bat0")
    os.system('sudo sh static/shell/raiseBatSignal.sh')
    ip = '192.168.200.' + str(macIP)
    cmd = 'sudo ifconfig bat0 ' + ip
    os.system(cmd)
    print("IP Address of bat0 is now " + ip)
    print("setup bat0")
    

    print("Setting up Alfred")
    sleep(1)
    print("...")
    sleep(1)
    print("...")
    sleep(1)
    print("...")
    #os.system('sudo alfred -i bat0 -m -c echo "Master Wayne says Hello"' &)
    args = ['sudo', 'alfred', '-i', 'bat0', '-m', 'master', '-c', 'sudo alfred -r 65 | python alfredCallBack.py']
    #args = ['sudo', 'alfred', '-i', 'bat0', '-m', 'master', '-c', 'espeak "Message Recieved"']
    #subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    subprocess.Popen(args)
    print("Starting rest of the server")


if __name__ == '__main__':
    print("Start")
    thread = Thread(target=main, args=())
    #thread.daemon = True
    try:
        thread.start()
    except(KeyboardInterrupt, SystemExit):
	tb.stop()
	thread.stop()
	sys.exit()
    socketio.run(app, host='0.0.0.0', debug=True, use_reloader=False)
