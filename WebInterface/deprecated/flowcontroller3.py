#!/usr/bin/env python2
##################################################
# ''GNU Radio Python Flow Graph
# Title: Nonbroadcastwithfreqandmac
# Generated: Mon Feb  1 16:46:29 2016
#
# This file works, but has NO flask functionality
#
##################################################
#from __future__ import print_function

from threading import Thread
from optparse import OptionParser
from gnuradio.eng_option import eng_option
from gnuradio import eng_notation

from broadcastFandMNoGui import broadcastFandMNoGui
import mac
import pmt
import wx
import sys

from frequencytable import FrequencyTable

import os
from time import sleep
import subprocess


# http://www.secdev.org/projects/scapy/
# Saving that link for later

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
        "", "--max-arq-attempts", dest="max_arq_attempts", type="intx", default=5 * 2,
        help="Set Max ARQ attempts [default=%default]")
    parser.add_option(
        "", "--mtu", dest="mtu", type="intx", default=128,
        help="Set MTU [default=%default]")
    parser.add_option(
        "", "--port", dest="port", type="string", default="12345",
        help="Set TCP port [default=%default]")
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
        "-l", "--radio-addr", dest="radio_addr", type="intx", default=63,
        help="Set Local address [default=%default]")
    parser.add_option(
        "", "--rx-freq", dest="rx_freq", type="eng_float", default=eng_notation.num_to_str(915e6),
        help="Set RX freq [default=%default]")
    parser.add_option(
        "", "--tx-freq", dest="tx_freq", type="eng_float", default=eng_notation.num_to_str(915e6),
        help="Set TX freq [default=%default]")
    parser.add_option(
        "-r", "--rate", dest="rate", type="eng_float", default=eng_notation.num_to_str(1e6),
        help="Set Sample rate [default=%default]")
    return parser


def main(top_block_cls=broadcastFandMNoGui, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()
    global tb
    tb = top_block_cls(ampl=options.ampl, args=options.args, arq_timeout=options.arq_timeout, dest_addr=options.dest_addr, iface=options.iface, max_arq_attempts=options.max_arq_attempts, mtu=options.mtu, port=options.port, rx_antenna=options.rx_antenna, rx_gain=options.rx_gain, rx_lo_offset=options.rx_lo_offset, samps_per_sym=options.samps_per_sym, tx_gain=options.tx_gain, tx_lo_offset=options.tx_lo_offset, radio_addr=options.radio_addr, rx_freq=options.rx_freq, tx_freq=options.tx_freq, rate=options.rate)
    tb.start()
    try:
        raw_input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()

if __name__ == '__main__':
    
    thread = Thread(target=main, args=())
    #thread.daemon = True
    thread.start()