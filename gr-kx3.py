#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Kx3 Rx
# Generated: Sun Oct 28 15:31:01 2012
##################################################

# DML
gui_scale = 1
rig_poll_rate = 0.01

from datetime import datetime
from gnuradio import audio
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import window
from gnuradio.eng_option import eng_option
from gnuradio.gr import firdes
from gnuradio.wxgui import fftsink2
from gnuradio.wxgui import waterfallsink2
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import pexpect
import threading
import time
import wx

class grkx3(grc_wxgui.top_block_gui):

	def __init__(self):
		grc_wxgui.top_block_gui.__init__(self, title="Kx3 Rx")
		_icon_path = "/usr/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
		self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

		##################################################
		# Variables
		##################################################
		self.prefix = prefix = "/home/darren/grdata"
		self.poll_vfo = poll_vfo = 0
		self.samp_rate = samp_rate = 48000
		self.rig_freq = rig_freq = float(pexpect.run("rigctl -m 2 f"))
		self.recfile = recfile = prefix + datetime.now().strftime("%Y.%m.%d.%H.%M.%S") + ".dat"
		self.click_freq = click_freq = 0

		##################################################
		# Blocks
		##################################################
		self.nb0 = self.nb0 = wx.Notebook(self.GetWin(), style=wx.NB_TOP)
		self.nb0.AddPage(grc_wxgui.Panel(self.nb0), "Waterfall")
		self.nb0.AddPage(grc_wxgui.Panel(self.nb0), "FFT")
		self.GridAdd(self.nb0, 2, 0, 5, 8)
		self.wxgui_waterfallsink2_0 = waterfallsink2.waterfall_sink_c(
			self.nb0.GetPage(0).GetWin(),
			baseband_freq=rig_freq,
			dynamic_range=30,
			ref_level=-70,
			ref_scale=1.0,
			sample_rate=samp_rate,
			fft_size=2048,
			fft_rate=10,
			average=False,
			avg_alpha=None,
			title="Waterfall Plot",
			win=window.hamming,
			size=(1190/gui_scale,600/gui_scale),
		)
		self.nb0.GetPage(0).Add(self.wxgui_waterfallsink2_0.win)
		def wxgui_waterfallsink2_0_callback(x, y):
			self.set_click_freq(x)
		
		self.wxgui_waterfallsink2_0.set_callback(wxgui_waterfallsink2_0_callback)
		self.wxgui_fftsink2_0 = fftsink2.fft_sink_c(
			self.nb0.GetPage(1).GetWin(),
			baseband_freq=rig_freq,
			y_per_div=10,
			y_divs=10,
			ref_level=0,
			ref_scale=2.0,
			sample_rate=samp_rate,
			fft_size=2048,
			fft_rate=10,
			average=False,
			avg_alpha=None,
			title="FFT Plot",
			peak_hold=True,
			win=window.flattop,
			size=(1190/gui_scale,600/gui_scale),
		)
		self.nb0.GetPage(1).Add(self.wxgui_fftsink2_0.win)
		def _poll_vfo_probe():
		    prompt="Rig command: "
		    rigctl = pexpect.spawn("rigctl -m 2")
		    while True:
			    try: 
			        #pass
			        rigctl.sendline("f")
			        rigctl.expect("Frequency: ")
			        rigctl.expect("\r")
			        rig_freq = rigctl.before
			        #self.set_rig_freq(float(rig_freq))
			        break
			    except AttributeError, e:
			        print "AttributeError in _poll_vfo_probe() ... rigctl error"
			    except ValueError, e:
			        print "ValueError in _poll_vfo_probe() ... rigctl error"
				time.sleep(1.0/(rig_poll_rate))
		_poll_vfo_thread = threading.Thread(target=_poll_vfo_probe)
		_poll_vfo_thread.daemon = True
		_poll_vfo_thread.start()
		self.gr_float_to_complex_0 = gr.float_to_complex(1)
		self.audio_source_0 = audio.source(samp_rate, "", True)

		##################################################
		# Connections
		##################################################
		self.connect((self.gr_float_to_complex_0, 0), (self.wxgui_waterfallsink2_0, 0))
		self.connect((self.audio_source_0, 1), (self.gr_float_to_complex_0, 0))
		self.connect((self.audio_source_0, 0), (self.gr_float_to_complex_0, 1))
		self.connect((self.gr_float_to_complex_0, 0), (self.wxgui_fftsink2_0, 0))

	def get_prefix(self):
		return self.prefix

	def set_prefix(self, prefix):
		self.prefix = prefix
		self.set_recfile(self.prefix + datetime.now().strftime("%Y.%m.%d.%H.%M.%S") + ".dat")

	def get_poll_vfo(self):
		return self.poll_vfo

	def set_poll_vfo(self, poll_vfo):
		self.poll_vfo = poll_vfo
		self.set_rig_freq(self.poll_vfo)

	def get_samp_rate(self):
		return self.samp_rate

	def set_samp_rate(self, samp_rate):
		self.samp_rate = samp_rate
		self.wxgui_fftsink2_0.set_sample_rate(self.samp_rate)
		self.wxgui_waterfallsink2_0.set_sample_rate(self.samp_rate)

	def get_rig_freq(self):
		return self.rig_freq

	def set_rig_freq(self, rig_freq):
		self.rig_freq = rig_freq
		print"set_rig_freq(" + str(self.rig_freq) + ")"
		self.wxgui_waterfallsink2_0.set_baseband_freq(self.rig_freq)
		self.wxgui_fftsink2_0.set_baseband_freq(self.rig_freq)

	def get_recfile(self):
		return self.recfile

	def set_recfile(self, recfile):
		self.recfile = recfile

	def get_click_freq(self):
		return self.click_freq

	def set_click_freq(self, click_freq):
		self.click_freq = click_freq
		print "set_click_freq(" + str(click_freq) + ")"		
		result = pexpect.run("rigctl -m 2 F " + str(self.click_freq))
		print result
		self.set_rig_freq(click_freq)

if __name__ == '__main__':
	parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
	(options, args) = parser.parse_args()
	tb = grkx3()
	tb.Run(True)

