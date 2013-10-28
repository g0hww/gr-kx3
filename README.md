gr-kx3
======

A trivial pan-adapter for use with the Elecraft KX3, using gnuradio (see "Notes" below)
and hamlib, written in Python and released under the GPLv3. There are some screen-shots here: 
http://www.g0hww.net/2012/10/gnuradio-hamlib-and-kx3.html 
and more here: 
http://www.g0hww.net/2012/11/more-buttons-in-gr-kx3-more-bugs-too.html.

It uses pulseaudio for the soundcard I/Q input by default, so when gr-kx3 is running, run Pulse
Audio Volume Control and choose the correct soundcard for the stereo I/Q input from
the KX3. For me, the application appears on the Recording tab, as 

	ALSA plug-in [python-2.7]: ALSA Capture

The Frequency text input control will directly retune the radio when the
frequency control mode drop down list is set to "Entry". In that mode, the rig's VFO
is not polled.  When the frequency control mode drop down list is set to "Track" the VFO
frequency of the rig is polled. 
When set to "Track & Click", the rig VFO is tracked and clicking in the waterfall display
will retune the rig to the selected frequency. 

You can click in the waterfall (not in the spectrum plot) to re-tune the radio 
to that frequency.  You can select Step size increment from the drop down
list, and nudge the frequency up and down with the Step Up/Down buttons.
Support for stepping through bands is also planned but not yet implemented.

Regarding frequency offsets from PBT settings and IF offset configurations, all
bets are off for now, until the support for the FI command is added to the
KX3 (which has been promised by Wayne from Elecraft).

The code uses hamlib's rigctl (via pexpect) which then talks to rigctld over
TCP/IP, so you need to have rigctld running with a serial connection to the
radio, using a command like:

	rigctld -m 229 -r /dev/ttyUSB0 -s 38400

Notes
=====

Hamlib timeouts:
 
 Initially I found that I had to bodge hamlib itself in order to increase the timeouts for
 the KX3, which were exceeded whenever I switched bands on the radio. Newer versions of hamlib
 may make this unnecessary, and gr-kx3 is now more robust. There are
 some details of my original bodge here: 
 http://www.g0hww.net/2012/11/a-better-bodge-for-hamlib-and-kx3.html

Getting gnuradio:
 
 I tend to stay fairly up-to-date with my gnuradio versions, and gr-kx3 is typically updated
 to work with the latest versions of gnuradio. This may cause some incompatibilities with
 older gnuradio versions.  YMMV, but hey, you can always hack the python yourself :)
 
 Ubuntu Users can get probably get newish packages from the gqrx ppa, see here:
  https://launchpad.net/~gqrx/+archive/releases
 Otherwise, try following one of the methods listed here:
  http://gnuradio.org/redmine/projects/gnuradio/wiki/InstallingGR



Related Projects
================




Stefano, IZ0MJE has posted about projects using Funcube Dongles and USRPs to tap IF 
outputs from other Hamlib controlled transceivers, reusing code from gr-kx3.  See here:
http://www.tarapippo.net/gnuradio/ft950.html

