gr-kx3
======

A trivial panadapter for use with the Elecraft KX3, using gnuradio and hamlib, 
released under the GPLv3. There are some screenshots here: 
http://www.g0hww.net/2012/10/gnuradio-hamlib-and-kx3.html 
and more here: 
http://www.g0hww.net/2012/11/more-buttons-in-gr-kx3-more-bugs-too.html.

It works.  Just about.  At the moment it doesn't track the VFO on the radio.  It
can, but there's a memory leak of about 1MB per second when it does, which is
very bad.

I've added a Frequency input control that will retune the radio.  If you press the 
Fetch button, it will fetch the frequency from the KX3 (as a work
around for the inability to poll the radio without causing the nasty
memory leak).

You can click in the waterfall (not in the spectrum plot) to re-tune the radio 
to that frequency.  You can select Step size increment from the drop down
list, and nudge the frequnecy up and down with the Step Up/Down buttons.
Support for stepping through bands is also planned but not yet implemented.

Regarding frequency offsets from PBT settings and IF offset configurations, all
bets are off for now, until the support for the FI command is added to the
KX3 (which has been promised by Wayne from Elecraft).

The code uses hamlib's rigctl (via pexpect) which then talks to rigctld over
TCP/IP, so you need to have rigctld running with a serial connection to the
radio, using a command like:

	rigctld -m 229 -r /dev/ttyUSB2 -s 38400

I found that I had to bodge hamlib itself in order to increase the timeouts for
the KX3, which were exceeded whenever I switched bands on the radio.  There are
some details here: 
http://www.g0hww.net/2012/11/a-better-bodge-for-hamlib-and-kx3.html
