#!/usr/bin/env python

'''
This file is part of gr-kx3.

gr-kx3 is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

gr-kx3 is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with gr-kx3.  If not, see <http://www.gnu.org/licenses/>.

Copyright 2012 Darren Long darren.long@mac.com
'''

from datetime import datetime
from gnuradio import audio
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import window
from gnuradio.eng_option import eng_option
from gnuradio.gr import firdes
from gnuradio.wxgui import fftsink2
from gnuradio.wxgui import forms
from gnuradio.wxgui import waterfallsink2
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import pexpect
import mutex
from threading import Thread, RLock
import time
import wx
from decimal import *
import traceback
import gc

gui_scale = 1
rig_poll_rate = 4

class grkx3(grc_wxgui.top_block_gui):

        def __init__(self):
                grc_wxgui.top_block_gui.__init__(self, title="gr-kx3")
                _icon_path = "/usr/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
                self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))
                ##################################################
                # Variables
                ##################################################
                self.rig_freq = rig_freq = float(pexpect.run("rigctl -m 2 f"))
                self.rigctl = pexpect.spawn("rigctl -m 2")
                self.rigctl.timeout = 2.5
                self.prefix = prefix = "~/grdata"
                self.sync_freq = sync_freq = 2
                self.samp_rate = samp_rate = 48000
                self.recfile = recfile = prefix + datetime.now().strftime("%Y.%m.%d.%H.%M.%S") + ".dat"
                self.freq = freq = rig_freq
                self.click_freq = click_freq = 0
                self.step_up = step_up = 1
                self.step_size = step_size = 6
                self.step_down = step_down = 1
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
                        dynamic_range=20,
                        ref_level=-40,
                        ref_scale=1.0,
                        sample_rate=samp_rate,
                        fft_size=2048,
                        fft_rate=30,
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
                        average=True,
                        avg_alpha=None,
                        title="FFT Plot",
                        peak_hold=True,
                        win=window.flattop,
                        size=(1190/gui_scale,600/gui_scale),
                )
                self.nb0.GetPage(1).Add(self.wxgui_fftsink2_0.win)
                self.gr_float_to_complex_0 = gr.float_to_complex(1)
                self._freq_text_box = forms.text_box(
                        parent=self.GetWin(),
                        value=self.freq,
                        callback=self.set_text_freq,
                        label="Frequency",
                        converter=forms.float_converter(),
                )
                self.GridAdd(self._freq_text_box, 1, 0, 1, 1)
                self._sync_freq_chooser = forms.drop_down(
                        parent=self.GetWin(),
                        value=self.sync_freq,
                        callback=self.set_sync_freq,
                        label="",
                        choices=[1,2,3],
                        labels=["Entry","Track","Track & Click"],
                )
                self.GridAdd(self._sync_freq_chooser, 1, 1, 1, 1)
                self._step_size_chooser = forms.drop_down(
                        parent=self.GetWin(),
                        value=self.step_size,
                        callback=self.set_step_size,
                        label="Step",
                        choices=[1, 2, 3,4,5,6,7],
                        labels=["Band","1MHz","100kHz","10kHz","1kHz","100Hz","10Hz"],
                )
                self.GridAdd(self._step_size_chooser, 1, 2, 1, 1)
                self._step_up_chooser = forms.button(
                        parent=self.GetWin(),
                        value=self.step_up,
                        callback=self.set_step_up,
                        label="",
                        choices=[1],
                        labels=["Step Up"],
                )
                self.GridAdd(self._step_up_chooser, 1, 3, 1, 1)
                self._step_down_chooser = forms.button(
                        parent=self.GetWin(),
                        value=self.step_down,
                        callback=self.set_step_down,
                        label="",
                        choices=[1],
                        labels=["Step Down"],
                )
                self.GridAdd(self._step_down_chooser, 1, 4, 1, 1)		
                
                self.audio_source_0 = audio.source(samp_rate, "pulse", True)
                
                ##################################################
                # Connections
                ##################################################
                self.connect((self.gr_float_to_complex_0, 0), (self.wxgui_waterfallsink2_0, 0))
                self.connect((self.audio_source_0, 1), (self.gr_float_to_complex_0, 0))
                self.connect((self.audio_source_0, 0), (self.gr_float_to_complex_0, 1))
                self.connect((self.gr_float_to_complex_0, 0), (self.wxgui_fftsink2_0, 0))
                self.lock = RLock()
                self.vfo_poll_skip = 0
                self.set_rig_vfo = False
                self.quit = False
                _poll_vfo_thread = Thread(target=self._poll_vfo_probe)
                _poll_vfo_thread.daemon = True
                _poll_vfo_thread.start()

        def quit(self):
            self.quit = True

        def skip_vfo_poll_CS(self):
            self.lock.acquire()
            if self.vfo_poll_skip >= 0:
                self.vfo_poll_skip = rig_poll_rate * 1
                #traceback.print_stack()
            self.lock.release()
            gc.collect()

        def should_skip_vfo_poll_CS(self):
            temp = self.vfo_poll_skip
            if temp != 0:
                if temp > 0:
                    self.vfo_poll_skip = temp - 1
                retval = True
            else:
                self.vfo_poll_skip = 0
                retval = False
            return retval

        def poll_vfo(self):
            retval = False
            self.poll_rigctl.sendline("f") 
            res = self.poll_rigctl.expect(["Frequency: ", pexpect.TIMEOUT])
            if res == 0:
                res = self.poll_rigctl.expect(["\r", pexpect.TIMEOUT])
                if res == 0:
                    rig_freq = self.poll_rigctl.before
                    self.set_rig_vfo = False
                    self._freq_text_box.set_value(float(rig_freq))
                    retval = True
            return retval    

        def _poll_vfo_probe(self):
            self.poll_rigctl = pexpect.spawn("rigctl -m 2")
            self.poll_rigctl.timeout = 1.5
            reset_rigctl = False
            while True:
                    if True == self.quit:
                        print "Warning: _poll_vfo_probe() quiting!"
                        break
                    self.lock.acquire()
                    try:
                        if self.should_skip_vfo_poll_CS() == False:
                            #msg = "_poll_vfo_probe() ... polling"
                            if not self.poll_vfo():
                                reset_rigctl = True
                        else:
                            #msg = "_poll_vfo_probe() ... skipping poll: " + str(self.vfo_poll_skip)
                            pass
                        #print msg
                    except AttributeError, e:
                        print "AttributeError in _poll_vfo_probe() ... rigctl error"
                        reset_rigctl = True
                    except ValueError, e:
                        print "ValueError in _poll_vfo_probe() ... rigctl error"
                        reset_rigctl = True
                    except Exception, e:
                        print "Exception in _poll_vfo_probe() ... unknown error"
                        reset_rigctl = True    
                    finally:
                        self.lock.release()
                    if True == reset_rigctl:
                        print "Warning: _poll_vfo_probe() resetting rigctl"
                        self.poll_rigctl.close()
                        self.poll_rigctl = pexpect.spawn("rigctl -m 2")
                        self.poll_rigctl.timeout = 1.5
                        reset_rigctl = False
                    time.sleep(1.0/(rig_poll_rate))
                    gc.collect()
                    
        def rig_respawn(self):
                self.rigctl.close()
                self.rigctl = pexpect.spawn("rigctl -m 2")
                self.rigctl.timeout = 2.5
        def get_rig_freq(self):
                return self.rig_freq

        def set_baseband_freq(self, rig_freq):
                self.rig_freq = rig_freq
                print"* set_baseband_freq(" + str(self.rig_freq) + ")"
                self.wxgui_waterfallsink2_0.set_baseband_freq(self.rig_freq)
                self.wxgui_fftsink2_0.set_baseband_freq(self.rig_freq)


        def get_prefix(self):
                return self.prefix

        def set_prefix(self, prefix):
                self.prefix = prefix
                self.set_recfile(self.prefix + datetime.now().strftime("%Y.%m.%d.%H.%M.%S") + ".dat")

        def get_step_size(self):
                return self.step_size

        def set_step_size(self, step_size):
                self.step_size = step_size
                self._step_size_chooser.set_value(self.step_size)

        def get_step_up(self):
                return self.step_up

        def set_step_up(self, step_up):
                self.skip_vfo_poll_CS()
                self.set_rig_vfo = True
                self.step_up = step_up
                self._step_up_chooser.set_value(self.step_up)
                # step up by the step size enum
                if(1 == self.step_size):
                    # step up one band
                    print "Step Up: Band - not implemented"
                elif(2 == self.step_size):
                    # step up 1MHz
                    self._freq_text_box.set_value(self.freq + 1000000.0)
                elif(3 == self.step_size):
                    # step up 100kHz
                    self._freq_text_box.set_value(self.freq + 100000.0)
                elif(4 == self.step_size):
                    # step up 10kHz
                    self._freq_text_box.set_value(self.freq + 10000.0)		    
                elif(5 == self.step_size):
                    # step up 1kHz
                    self._freq_text_box.set_value(self.freq + 1000.0)
                elif(6 == self.step_size):
                    # step up 100Hz
                    self._freq_text_box.set_value(self.freq + 100.0)
                elif(7 == self.step_size):
                    # step up 10Hz
                    self._freq_text_box.set_value(self.freq + 10.0)

                    
        def get_step_down(self):
                return self.step_down

        def set_step_down(self, step_down):
                self.skip_vfo_poll_CS()
                self.set_rig_vfo = True
                self.step_down = step_down
                self._step_down_chooser.set_value(self.step_down)
                # step down by the step size enum
                if(1 == self.step_size):
                    # step down one band
                    print "Step Down: Band - not implemented"
                elif(2 == self.step_size):
                    # step down 1MHz
                    self._freq_text_box.set_value(self.freq - 1000000.0)
                elif(3 == self.step_size):
                    # step down 100kHz
                    self._freq_text_box.set_value(self.freq - 100000.0)
                elif(4 == self.step_size):
                    # step down 10kHz
                    self._freq_text_box.set_value(self.freq - 10000.0)		    
                elif(5 == self.step_size):
                    # step down 1kHz
                    self._freq_text_box.set_value(self.freq - 1000.0)
                elif(6 == self.step_size):
                    # step down 100Hz
                    self._freq_text_box.set_value(self.freq - 100.0)
                elif(7 == self.step_size):
                    # step down 10Hz
                    self._freq_text_box.set_value(self.freq - 10.0)


        def get_samp_rate(self):
                return self.samp_rate

        def set_samp_rate(self, samp_rate):
                self.samp_rate = samp_rate
                self.wxgui_waterfallsink2_0.set_sample_rate(self.samp_rate)
                self.wxgui_fftsink2_0.set_sample_rate(self.samp_rate)

        def get_recfile(self):
                return self.recfile

        def set_recfile(self, recfile):
                self.recfile = recfile

        def get_freq(self):
                return self.freq

        def set_text_freq(self, freq):
            self.lock.acquire()
            if self.vfo_poll_skip > 0 and self.set_rig_vfo == False:
                print "* set_text_freq(" + str(self.freq) + ") ... ignoring"
            else:
                self.freq = freq
                print "* set_text_freq(" + str(self.freq) + ")"
                #traceback.print_stack()
                if 1 == self.sync_freq or self.set_rig_vfo == True:
                    #self.skip_vfo_poll_CS()
                    self.set_rig_vfo = False
                    self.set_rig_freq()
                self.set_baseband_freq(int(self.freq))
            self.lock.release()


        
        def set_rig_freq(self):
            print "* set_rig_freq(" + str(self.freq) + ")"
            self.rigctl.sendline("F " + str(self.freq))
            self.rigctl.expect("Rig command: ")
            #result = self.rigctl.before
            #print result
            
            

        def get_click_freq(self):
                return self.click_freq

        def set_click_freq(self, click_freq):
                if 3 == self.sync_freq:
                    self.skip_vfo_poll_CS()
                    self.click_freq = float(click_freq)
                    print "* set_click_freq(" + str(self.click_freq) + ")"
                    self.set_rig_vfo = True
                    self._freq_text_box.set_value( self.click_freq)
                
        def get_sync_freq(self):
                return self.sync_freq

        def set_sync_freq(self, sync_freq):
                self.sync_freq = sync_freq
                self.lock.acquire()
                if 1 == self.sync_freq: # direct entry
                    self.vfo_poll_skip = -1
                elif 1 < self.sync_freq: # 2 is vfo tracking, 3 track and click
                    self.vfo_poll_skip = rig_poll_rate * 1
                self.lock.release()



if __name__ == '__main__':
        parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
        (options, args) = parser.parse_args()
        tb = grkx3()
        try:
            tb.Run(True)
        except (KeyboardInterrupt, SystemExit):
            pass
        finally:
            exit_now = True;

