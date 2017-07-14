#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2017 germanocapela gmail com.
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 
# 
# This block intends to be used with local_worker from gr-ofdm_tools
# 
# 

from plotter_base import *

class remote_client_qt(plotter_base):
    def __init__(self, label="", *args):
        plotter_base.__init__(self, blkname="remote_client_qt", label=label, *args)
        self.message_port_register_in(pmt.intern("pdus"));
        self.set_msg_handler(pmt.intern("pdus"), self.handler);

        # set up curves
        curve = Qwt.QwtPlotCurve("PSD");
        curve.attach(self);
        self.curves.append(curve);
        curve.setPen( Qt.QPen(Qt.Qt.green) );

        self.curve_data = [([],[]), ([],[])];

    def handler(self, msg_pmt):
        meta = pmt.to_python(pmt.car(msg_pmt))
        # Collect message, convert to Python format:
        msg = pmt.cdr(msg_pmt)
        # Convert to string:
        msg_str = "".join([chr(x) for x in pmt.u8vector_elements(msg)])

        fft_data = numpy.fromstring(msg_str, numpy.float32)

        # pass data
        self.curve_data[0] = (numpy.linspace(1,len(fft_data),len(fft_data)), fft_data);

        # trigger update
        self.emit(QtCore.SIGNAL("updatePlot(int)"), 0)
