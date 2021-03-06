#!/usr/bin/env python2
##################################################
# GNU Radio Python Flow Graph
# Title: Such Samples, /home/ggc/rf_recordings/umts/umts6.4M.cfile Wow!
# Author: Tim O'Shea
# Generated: Sun Aug 16 12:35:32 2015
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from PyQt4 import Qt
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import numpy
import pyqt
import sys

from distutils.version import StrictVersion
class such_samples(gr.top_block, Qt.QWidget):

    def __init__(self, filename="/home/ggc/rf_recordings/umts/umts6.4M.cfile"):
        gr.top_block.__init__(self, "Such Samples, /home/ggc/rf_recordings/umts/umts6.4M.cfile Wow!")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Such Samples, /home/ggc/rf_recordings/umts/umts6.4M.cfile Wow!")
        try:
             self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
             pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "such_samples")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())


        ##################################################
        # Parameters
        ##################################################
        self.filename = filename

        ##################################################
        # Variables
        ##################################################
        self.obs_period = obs_period = 35e-3

        ##################################################
        # Blocks
        ##################################################
        self._obs_period_tool_bar = Qt.QToolBar(self)
        self._obs_period_tool_bar.addWidget(Qt.QLabel("Obs Period"+": "))
        self._obs_period_line_edit = Qt.QLineEdit(str(self.obs_period))
        self._obs_period_tool_bar.addWidget(self._obs_period_line_edit)
        self._obs_period_line_edit.returnPressed.connect(
        	lambda: self.set_obs_period(eng_notation.str_to_num(str(self._obs_period_line_edit.text().toAscii()))))
        self.top_layout.addWidget(self._obs_period_tool_bar)
        self.pyqt_range_input_0 = pyqt.range_input()
        self._pyqt_range_input_0_win = self.pyqt_range_input_0;
        self.top_layout.addWidget(self._pyqt_range_input_0_win)
        self.pyqt_file_message_souce_0 = pyqt.file_message_source(filename, "complex64")
        self.pyqt_cpsd_plot_0 = pyqt.cpsd_plot("Very Frequency")
        self._pyqt_cpsd_plot_0_win = self.pyqt_cpsd_plot_0;
        self.top_layout.addWidget(self._pyqt_cpsd_plot_0_win)
        self.fac_plot_0 = pyqt.fac_plot(label="Autocorrelation", obs_time=obs_period)
        self._fac_plot_0_win = self.fac_plot_0;
        self.top_layout.addWidget(self._fac_plot_0_win)
        self.blocks_message_debug_0 = blocks.message_debug()

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.pyqt_file_message_souce_0, 'pdus'), (self.fac_plot_0, 'cpdus'))    
        self.msg_connect((self.pyqt_file_message_souce_0, 'pdus'), (self.pyqt_cpsd_plot_0, 'cpdus'))    
        self.msg_connect((self.pyqt_file_message_souce_0, 'file_range'), (self.pyqt_range_input_0, 'file_range'))    
        self.msg_connect((self.pyqt_range_input_0, 'range'), (self.blocks_message_debug_0, 'print'))    
        self.msg_connect((self.pyqt_range_input_0, 'range'), (self.fac_plot_0, 'range'))    
        self.msg_connect((self.pyqt_range_input_0, 'range'), (self.pyqt_file_message_souce_0, 'range'))    

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "such_samples")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_filename(self):
        return self.filename

    def set_filename(self, filename):
        self.filename = filename

    def get_obs_period(self):
        return self.obs_period

    def set_obs_period(self, obs_period):
        self.obs_period = obs_period
        self.fac_plot_0.set_obs_time(self.obs_period)
        Qt.QMetaObject.invokeMethod(self._obs_period_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.obs_period)))


if __name__ == '__main__':
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    parser.add_option("", "--filename", dest="filename", type="string", default="/home/ggc/rf_recordings/umts/umts6.4M.cfile",
        help="Set filename [default=%default]")
    (options, args) = parser.parse_args()
    if(StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0")):
        Qt.QApplication.setGraphicsSystem(gr.prefs().get_string('qtgui','style','raster'))
    qapp = Qt.QApplication(sys.argv)
    tb = such_samples(filename=options.filename)
    tb.start()
    tb.show()
    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()
    tb = None #to clean up Qt widgets
