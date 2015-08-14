#!/usr/bin/env python
#
# Copyright 2014 Tim O'Shea
# Copyright 2015 Germano Capela 
# This file is part of GNU Radio
#
# GNU Radio is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# GNU Radio is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with GNU Radio; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
#
from plotter_base import *

def xcorr(a, b, length):
    e = numpy.fft.fft(a, length);
    f = numpy.fft.fft(b, length);
    g = f * numpy.conj(e);
    h = numpy.fft.fftshift(numpy.fft.ifft(g, length));
    return numpy.abs(h[len(h)/2:])

class fac_plot(plotter_base):
    def __init__(self, label="", obs_time=0, *args):
        plotter_base.__init__(self,blkname="fac_plot", *args)
        self.message_port_register_in(pmt.intern("cpdus"));
        self.message_port_register_in(pmt.intern("range"));
        self.set_msg_handler(pmt.intern("cpdus"), self.handler);
        self.set_msg_handler(pmt.intern("range"), self.range_received);

        self.block_length = 4096
        self.obs_time = obs_time
        self.tbase = numpy.linspace(0, self.obs_time/2.0, self.block_length/2)*1000

        # set up curve
        curve = Qwt.QwtPlotCurve("FAC");
        curve.attach(self);
        self.curves.append(curve);
        curve.setPen( Qt.QPen(Qt.Qt.red) );

        self.curve_data = [([],[]), ([],[])];

    def handler(self, msg):
        # get input
        meta = pmt.car(msg);
        x = pmt.to_python(pmt.cdr(msg))
        
        # pass data
        self.curve_data[0] = (self.tbase, xcorr(x, x, self.block_length));

        # trigger update
        self.emit(QtCore.SIGNAL("updatePlot(int)"), 0)

    def range_received(self, msg):
        (s,l) = pmt.to_python(msg)
        self.block_length = l
        self.tbase = numpy.linspace(0, self.obs_time/2.0, self.block_length/2)*1000

    def set_obs_time(self, obs_time):
        self.obs_time = obs_time