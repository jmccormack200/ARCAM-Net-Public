#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Batmannogui
# Generated: Thu Mar 10 19:02:06 2016
##################################################
import threading

import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from gmsk_radio import gmsk_radio  # grc-generated hier_block
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser


class batmanNoGui(gr.top_block):

    def __init__(self, ampl=0.7, args='', arq_timeout=.1*0 + 0.04, dest_addr=-1, iface='tun0', mtu=128, ogradio_addr=0, port="12345", rate=1e6, rx_antenna="TX/RX", rx_gain=65-20, rx_lo_offset=0, samps_per_sym=4, tx_gain=45, tx_lo_offset=0, max_arq_attempts=5 * 2, tx_freq=915e6, rx_freq=915e6):
        gr.top_block.__init__(self, "Batmannogui")

        self._lock = threading.RLock()

        ##################################################
        # Parameters
        ##################################################
        self.ampl = ampl
        self.args = args
        self.arq_timeout = arq_timeout
        self.dest_addr = dest_addr
        self.iface = iface
        self.mtu = mtu
        self.ogradio_addr = ogradio_addr
        self.port = port
        self.rate = rate
        self.rx_antenna = rx_antenna
        self.rx_gain = rx_gain
        self.rx_lo_offset = rx_lo_offset
        self.samps_per_sym = samps_per_sym
        self.tx_gain = tx_gain
        self.tx_lo_offset = tx_lo_offset
        self.max_arq_attempts = max_arq_attempts
        self.tx_freq = tx_freq
        self.rx_freq = rx_freq

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = rate

        ##################################################
        # Blocks
        ##################################################
        self.gmsk_radio_0 = gmsk_radio(
            rate=samp_rate,
            args=args,
            tx_gain=tx_gain,
            tx_freq=tx_freq,
            rx_ant=rx_antenna,
            rx_freq=rx_freq,
            rx_gain=rx_gain,
            ampl=ampl,
            rx_lo_offset=rx_lo_offset,
            tx_lo_offset=tx_lo_offset,
            samps_per_sym=samps_per_sym,
            access_code_threshold=0 + 12 + 4*0,
        )
        self.blocks_tuntap_pdu_0 = blocks.tuntap_pdu(iface, mtu*0 + 1532, False)

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.blocks_tuntap_pdu_0, 'pdus'), (self.gmsk_radio_0, 'msg_in'))    
        self.msg_connect((self.gmsk_radio_0, 'msg_out'), (self.blocks_tuntap_pdu_0, 'pdus'))    

    def get_ampl(self):
        return self.ampl

    def set_ampl(self, ampl):
        with self._lock:
            self.ampl = ampl
            self.gmsk_radio_0.set_ampl(self.ampl)

    def get_args(self):
        return self.args

    def set_args(self, args):
        with self._lock:
            self.args = args
            self.gmsk_radio_0.set_args(self.args)

    def get_arq_timeout(self):
        return self.arq_timeout

    def set_arq_timeout(self, arq_timeout):
        with self._lock:
            self.arq_timeout = arq_timeout

    def get_dest_addr(self):
        return self.dest_addr

    def set_dest_addr(self, dest_addr):
        with self._lock:
            self.dest_addr = dest_addr

    def get_iface(self):
        return self.iface

    def set_iface(self, iface):
        with self._lock:
            self.iface = iface

    def get_mtu(self):
        return self.mtu

    def set_mtu(self, mtu):
        with self._lock:
            self.mtu = mtu

    def get_ogradio_addr(self):
        return self.ogradio_addr

    def set_ogradio_addr(self, ogradio_addr):
        with self._lock:
            self.ogradio_addr = ogradio_addr

    def get_port(self):
        return self.port

    def set_port(self, port):
        with self._lock:
            self.port = port

    def get_rate(self):
        return self.rate

    def set_rate(self, rate):
        with self._lock:
            self.rate = rate
            self.set_samp_rate(self.rate)

    def get_rx_antenna(self):
        return self.rx_antenna

    def set_rx_antenna(self, rx_antenna):
        with self._lock:
            self.rx_antenna = rx_antenna
            self.gmsk_radio_0.set_rx_ant(self.rx_antenna)

    def get_rx_gain(self):
        return self.rx_gain

    def set_rx_gain(self, rx_gain):
        with self._lock:
            self.rx_gain = rx_gain
            self.gmsk_radio_0.set_rx_gain(self.rx_gain)

    def get_rx_lo_offset(self):
        return self.rx_lo_offset

    def set_rx_lo_offset(self, rx_lo_offset):
        with self._lock:
            self.rx_lo_offset = rx_lo_offset
            self.gmsk_radio_0.set_rx_lo_offset(self.rx_lo_offset)

    def get_samps_per_sym(self):
        return self.samps_per_sym

    def set_samps_per_sym(self, samps_per_sym):
        with self._lock:
            self.samps_per_sym = samps_per_sym
            self.gmsk_radio_0.set_samps_per_sym(self.samps_per_sym)

    def get_tx_gain(self):
        return self.tx_gain

    def set_tx_gain(self, tx_gain):
        with self._lock:
            self.tx_gain = tx_gain
            self.gmsk_radio_0.set_tx_gain(self.tx_gain)

    def get_tx_lo_offset(self):
        return self.tx_lo_offset

    def set_tx_lo_offset(self, tx_lo_offset):
        with self._lock:
            self.tx_lo_offset = tx_lo_offset
            self.gmsk_radio_0.set_tx_lo_offset(self.tx_lo_offset)

    def get_max_arq_attempts(self):
        return self.max_arq_attempts

    def set_max_arq_attempts(self, max_arq_attempts):
        with self._lock:
            self.max_arq_attempts = max_arq_attempts

    def get_tx_freq(self):
        return self.tx_freq

    def set_tx_freq(self, tx_freq):
        with self._lock:
            self.tx_freq = tx_freq
            self.gmsk_radio_0.set_tx_freq(self.tx_freq)

    def get_rx_freq(self):
        return self.rx_freq

    def set_rx_freq(self, rx_freq):
        with self._lock:
            self.rx_freq = rx_freq
            self.gmsk_radio_0.set_rx_freq(self.rx_freq)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        with self._lock:
            self.samp_rate = samp_rate
            self.gmsk_radio_0.set_rate(self.samp_rate)


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
    if options is None:
        options, _ = argument_parser().parse_args()

    tb = top_block_cls(ampl=options.ampl, args=options.args, arq_timeout=options.arq_timeout, dest_addr=options.dest_addr, iface=options.iface, mtu=options.mtu, ogradio_addr=options.ogradio_addr, port=options.port, rate=options.rate, rx_antenna=options.rx_antenna, rx_gain=options.rx_gain, rx_lo_offset=options.rx_lo_offset, samps_per_sym=options.samps_per_sym, tx_gain=options.tx_gain, tx_lo_offset=options.tx_lo_offset, max_arq_attempts=options.max_arq_attempts, tx_freq=options.tx_freq, rx_freq=options.rx_freq)
    tb.start()
    tb.wait()


if __name__ == '__main__':
    main()
