gr-kx3
======

A trivial gnuradio project for use with the Elecraft KX3, under the GPLv3. 

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

The code wraps up a call to rigctld, so you need to have that running, using a command like:

	rigctld -m 229 -r /dev/ttyUSB2 -s 38400
